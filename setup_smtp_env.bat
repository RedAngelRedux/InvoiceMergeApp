@echo off
:: SMTP Environment Setup for InvoiceMergeAndMail
:: This script sets the required environment variables for email functionality

echo Setting up SMTP environment variables...

:: SMTP server address (e.g., smtp.office365.com)
setx SMTP_HOST smtp.ionos.com

:: SMTP port (e.g., 587 for TLS)
setx SMTP_PORT 465

@REM :: SMTP username (usually the sender's email)
@REM setx SMTP_USER rcocchia@topprioritycouriers.com

@REM :: SMTP password (leave blank for user to fill in later)
@REM echo.
@REM echo IMPORTANT: You must manually set SMTP_PASSWORD when ready.
@REM echo You can do this by running:
@REM echo     setx SMTP_PASSWORD your_password_here
@REM echo.

:: Sender email address
:: setx SMTP_FROM user@example.com

echo.
echo SMTP Server environment variables have been set.
:: echo You may need to restart your command prompt for changes to take effect.
pause

echo Setting up IMAP environment variables...
setx IMAP_ARCHIVE_FOLDER InvoiceArchive
echo.
echo IMAP environment variables have been set.
echo You may need to restart your command prompt for changes to take effect.
pause
