# Facebook Automation Bot

A hybrid Electron + Next.js + Python application for automating Facebook interactions.

## 🏗 Project Structure

This project follows a modular Monorepo-style structure:

```
ReactBot/
├── src/
│   ├── main/               # Electron Main Process
│   ├── renderer/           # Next.js Frontend (UI)
│   └── python/             # Python Backend
│       ├── api/            # FastAPI Gateway
│       ├── core/           # Automation Logic (Selenium)
│       └── utils/          # Configuration & Helpers
├── resources/              # Static resources (profiles, etc.)
└── output/                 # Runtime generated files (screenshots)
```

## 🚀 Getting Started

### Prerequisites

*   **Node.js**: v18+
*   **Python**: v3.10+
*   **Google Chrome**: Installed

### Installation

1.  **Install Node.js Dependencies**:
    ```bash
    npm install
    ```

2.  **Install Python Dependencies**:
    It is recommended to create a virtual environment first.
    ```bash
    # Create venv
    python -m venv .venv
    
    # Activate venv (Windows)
    .venv\Scripts\activate

    # Install requirements
    pip install -r src/python/requirements.txt
    ```

### Running the App

*   **Development Mode** (Run Frontend + Backend concurrently):
    ```bash
    npm run serve-all
    ```
    *   This starts Next.js on `localhost:3000` and the Python API on `localhost:7000`.

*   **Start Electron Shell** (Requires dev servers running):
    ```bash
    npm start
    ```

## 🛠 Configuration

Configuration is handled in `src/python/utils/config.py`.
It automatically detects paths, but you can override settings using environment variables or a `.env` file.

## 🛡 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
