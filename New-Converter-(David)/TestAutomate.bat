@echo off
REM Set default arguments if not provided
set ARG1=%1
set ARG2=%2
set ARG3=%3

REM Navigate to the VufindautoAPI directory
cd ..\VufindautoAPI
echo Getting Data with CORE API ...

call mvn clean package

REM Check the Maven exit code
if %ERRORLEVEL% NEQ 0 (
    echo Maven build failed.
    exit /b %ERRORLEVEL%
)

call mvn exec:java -Dexec.args="%ARG1% %ARG2% %ARG3%"
REM Check the Java application exit code
if %ERRORLEVEL% NEQ 0 (
    echo Java application failed.
    exit /b %ERRORLEVEL%
)
cd ..
cd New-Converter-(David)
echo Converting JSON to Marc ...
call python convert.py

if %ERRORLEVEL% NEQ 0 (
    echo Py application failed.
    exit /b %ERRORLEVEL%
)
pause