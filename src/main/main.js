// src/main/main.js
const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');

const isDev = !app.isPackaged;

// Ports
const NEXT_SERVER_PORT = 3000;
const NEXT_SERVER_URL = `http://localhost:${NEXT_SERVER_PORT}`;
const PYTHON_BACKEND_PORT = 7000;
const PYTHON_BACKEND_URL = `http://127.0.0.1:${PYTHON_BACKEND_PORT}`;

let pythonProcess = null;
let mainWindow;

/**
 * Determines the correct path to the Python executable and server script
 * based on whether we are in Development or Production (Packaged).
 */
function getPythonPaths() {
  const rootDir = path.resolve(__dirname, '../../'); // Go up from src/main to root

  // In dev, we use the local venv python. Update this if your path differs!
  // It's safer to rely on 'python' in PATH or a specific env var if possible.
  // Using a relative path lookup for robustness if "python" command isn't global.
  let pythonExecutable = 'python'; // Default to global python

  // Try to find local venv if exists (Common convention)
  const localVenvPath = path.join(rootDir, '.venv', 'Scripts', 'python.exe');
  if (fs.existsSync(localVenvPath)) {
    pythonExecutable = localVenvPath;
  }

  // Script path: src/python/api/server.py
  const scriptPath = path.join(rootDir, 'src', 'python', 'api', 'server.py');

  return { pythonExecutable, scriptPath, rootDir };
}

function startPythonBackend() {
  console.log('Electron: Starting Python backend...');

  const { pythonExecutable, scriptPath, rootDir } = getPythonPaths();
  console.log(`Electron: Python Executable: ${pythonExecutable}`);
  console.log(`Electron: Server Script: ${scriptPath}`);

  if (!fs.existsSync(scriptPath)) {
    console.error(`Electron Error: Python script not found at ${scriptPath}`);
    return;
  }

  // Arguments for uvicorn
  // We run the server.py directly or via module
  // Since we structured it to be importable, we can run the file directly
  const args = [
    scriptPath
  ];

  const spawnOptions = {
    cwd: rootDir, // Set CWD to project root so imports work
    stdio: ['ignore', 'pipe', 'pipe'], // Capture stdout/stderr
    env: {
      ...process.env,
      PYTHONIOENCODING: 'utf-8',
      PYTHONPATH: rootDir // Ensure src module is importable
    }
  };

  if (process.platform === 'win32') {
    // Windows specific optimizations
    // spawnOptions.windowsHide = true; // Use with care during debugging
  }

  pythonProcess = spawn(pythonExecutable, args, spawnOptions);

  pythonProcess.stdout.on('data', (data) => {
    console.log(`[Python]: ${data.toString()}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`[Python Err]: ${data.toString()}`);
  });

  pythonProcess.on('error', (err) => {
    console.error('Electron: Failed to start Python process:', err);
  });

  pythonProcess.on('exit', (code, signal) => {
    console.log(`Electron: Python backend exited with code ${code} and signal ${signal}`);
    pythonProcess = null;
  });

  console.log(`Electron: Python backend started on port ${PYTHON_BACKEND_PORT}`);
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    autoHideMenuBar: true,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    },
  });

  const startUrl = isDev
    ? NEXT_SERVER_URL
    : `file://${path.join(__dirname, '../renderer/out/index.html')}`; // Updated for new renderer location

  console.log(`Electron: Loading URL: ${startUrl}`);
  mainWindow.loadURL(startUrl);

  if (isDev) {
    mainWindow.webContents.openDevTools();
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(() => {
  startPythonBackend();
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('will-quit', () => {
  if (pythonProcess) {
    console.log('Electron: Killing Python backend...');
    pythonProcess.kill();
    // On Windows, sometimes kill() isn't enough for tree termination, 
    // but for a single script it usually works.
    pythonProcess = null;
  }
});
