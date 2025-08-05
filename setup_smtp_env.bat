@echo off
:: SMTP Environment Setup for InvoiceMergeAndMail
:: This script sets the required environment variables for email functionality

echo Setting up SMTP environment variables...

:: SMTP server address (e.g., smtp.office365.com)
setx SMTP_HOST smtp.1and1.com

:: SMTP port (e.g., 587 for TLS)
setx SMTP_PORT 465

:: SMTP username (usually the sender's email)
setx SMTP_USER rcocchia@topprioritycouriers.com

:: SMTP password (leave blank for user to fill in later)
echo.
echo IMPORTANT: You must manually set SMTP_PASSWORD when ready.
echo You can do this by running:
echo     setx SMTP_PASSWORD your_password_here
echo.

:: Sender email address
:: setx SMTP_FROM user@example.com

echo.
echo SMTP environment variables have been set (except password).
echo You may need to restart your command prompt for changes to take effect.
pause