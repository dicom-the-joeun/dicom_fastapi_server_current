@REM!/bin/bash 
@REM start_app_prod.bat 
cd "$(dirname ".\create_bat_fastapi.bat")" 
call .\env\Scripts\activate 
start /B python -m uvicorn app.main:app --reload --host=192.168.30.103 --port=3000 --log-config=app/conf/log_config_prod.ini