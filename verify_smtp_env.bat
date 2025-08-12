@echo off
:: Verify SMTP Environment Variables
:: Checks if required variables are set and displays their values

setlocal

echo Checking SMTP environment variables...
echo.

:: List of required variables
@REM set VARS=SMTP_HOST SMTP_PORT SMTP_USER SMTP_PASS
set VARS=SMTP_HOST SMTP_PORT IMAP_HOST IMAP_PORT

for %%V in (%VARS%) do (
    call :CheckVar %%V
)

echo.
echo Verification complete.
pause
exit /b

:CheckVar
set VAR_NAME=%1
call set VAR_VALUE=%%%VAR_NAME%%%

if defined VAR_VALUE (
    if "%VAR_NAME%"=="SMTP_PASSWORD" (
        if "%VAR_VALUE%"=="" (
            echo [%VAR_NAME%] is set but currently blank. Please update it with your password.
        ) else (
            echo [%VAR_NAME%] is set.
        )
    ) else (
        echo [%VAR_NAME%] = %VAR_VALUE%
    )
) else (
    echo [%VAR_NAME%] is NOT set. Please run setup_smtp_env.bat to configure it.
)
goto :eof