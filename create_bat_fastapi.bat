:: 기본 세팅
call .\env\Scripts\activate
pip install -r requirements.txt

:: end_app.bat 스크립트 생성
@echo off
echo @echo off > end_app.bat
echo FOR /F "tokens=5" %%a in ('netstat -aon ^| find "0.0.0.0:3000" ^| find "LISTENING"') do ( >> end_app.bat
echo SET pid=%%a >> end_app.bat
echo ) >> end_app.bat
echo IF "%%pid%%"=="" ( >> end_app.bat
echo     echo FastAPI app is not running >> end_app.bat
echo ) ELSE ( >> end_app.bat
echo     echo Stopping FastAPI app (PID: %%pid%%) >> end_app.bat
echo     taskkill /F /PID %%pid%% /T >> end_app.bat
echo ) >> end_app.bat


FOR /F "tokens=5" %%P IN ('netstat -a -n -o ^| findstr :8000 ^| findstr LISTENING') DO Taskkill /F /PID %%P

:: start_app_debug.bat 스크립트 생성
echo cd "$(dirname "%~0")" > start_app_debug.bat
echo call .\env\Scripts\activate >> start_app_debug.bat
echo python -m uvicorn app.main:app --reload --host=192.168.30.103 --port=3000 >> start_app_debug.bat

:: start_app_prod.bat 스크립트 생성
echo @REM!/bin/bash > start_app_prod.bat
echo @REM start_app_prod.bat >> start_app_prod.bat
echo cd "$(dirname "%~0")" >> start_app_prod.bat
echo call .\env\Scripts\activate >> start_app_prod.bat
echo start /B python -m uvicorn app.main:app --reload --host=192.168.30.103 --port=3000 --log-config=app/conf/log_config_prod.ini >> start_app_prod.bat

echo Scripts created successfully!
