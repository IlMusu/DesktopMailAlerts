# Desktop Mail Notifier

A small Windows application that checks an email inbox for unread messages matching configured keywords and shows a desktop notification when a match is found. The application uses IMAP and does not mark emails as read.

## How to Use

### 1. Configure the application

Open:

```text
config/configuration.json
```

and configure your email account and notification settings.

Example:

```json
{
  "email_address": "your@email.com",
  "password": "your-password",
  "imap_server": "imap.example.com",
  "imap_port": 993,
  "check_interval_minutes": 120,
  "keywords": ["invoice", "important", "alert"],
  "search_in": ["subject", "sender", "body"],
  "notification_audio_file": "assets/notification.wav",
  "message_title": "New matching email",
  "message_description": "A matching unread email was found."
}
```

### 2. Install

Before installing, make sure the complete project folder is in the location where you want to keep it permanently.

DO NOT REMOVE OR RENAME THE GENERATED FILES AFTER INSTALLATION.

The generated application and scheduled task use paths based on the original project location. Moving or renaming the folder afterwards will cause the application and/or scheduled task to stop working correctly. If you need to move the application to another location, run uninstall.bat first, move the project folder, and then run install.bat again.

Run:

```text
install.bat
```

The installer will:

- Create a Python virtual environment.
- Install the required dependencies.
- Build the application.
- Create a Windows Task Scheduler task.
- Start the application once.

After installation, the application runs automatically through Windows Task Scheduler.

### 3. Scheduling

The Task Scheduler interval is configured in `install.bat`:

```bat
set "CHECK_INTERVAL_MINUTES=30"
```

This controls how often Windows starts the application.

The actual email-check interval is configured separately in `configuration.json`.

For example:

```text
Task Scheduler:       every 30 minutes
Email check:          every 2 hours
```

The application starts every 30 minutes but only checks the mailbox when the configured email-check interval has elapsed.

### 4. Uninstall

Run:

```text
uninstall.bat
```

This stops the application, removes the scheduled task, and deletes the generated build files.

Your `config` and `assets` folders are preserved.

## Project Structure

```text
DesktopMailAlerts/
├── config/
│   ├── configuration.json
│   └── state.json
├── assets/
│   └── notification.wav
├── src/
│   ├── configuration.py
│   ├── desktop_notifier.py
│   ├── mail_service.py
│   └── state.py
├── main.py
├── install.bat
├── uninstall.bat
├── requirements.txt
└── README.md
```

## Notes

The application stores previously notified email IDs and scheduling information in:

```text
config/state.json
```
