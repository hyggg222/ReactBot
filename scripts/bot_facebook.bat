@echo OFF
REM --- THAY DOI CAC THONG SO DUOI DAY ---
set PROJECT_PATH="D:\project\bot_tt_facebook"
set NPM_SCRIPT="serve-all"
set BROWSER_URL="http://localhost:3000"

REM --- Bat dau chay ---
echo Khoi dong server...
cd /d %PROJECT_PATH%

REM Chay lenh NPM trong mot cua so terminal moi
start "MyDevServer" cmd /k "npm run %NPM_SCRIPT%"

REM Doi 10 giay de server khoi dong xong
echo Dang cho server khoi dong, vui long doi...d
timeout /t 10

REM Mo trinh duyet
echo Mo trang web...
start %BROWSER_URL%

exit