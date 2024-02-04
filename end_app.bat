@echo off 
FOR /F "tokens=5" %a in ('netstat -aon | find "0.0.0.0:3000" | find "LISTENING"') do ( 
SET pid=%a 
) 
IF "%pid%"=="" ( 
    echo FastAPI app is not running 
) ELSE ( 
    echo Stopping FastAPI app (PID: %pid%) 
    taskkill /F /PID %pid% /T 
) 
