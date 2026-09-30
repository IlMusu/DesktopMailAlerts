# Desktop Mail Notifier

A small Windows application that checks an email inbox for unread messages matching configured keywords and shows a desktop notification when a match is found. The application uses IMAP in read-only mode and never marks emails as read.

## How to Use

### 1. Configure the application

There is a configuration template file:

```text
config/configuration_template.json
```

Copy and rename it into:
```text
config/template.json
```

Then, fill this file with your configuration. <br>
Example:

```json
{
  "check_interval_minutes": 120,
  "mail_service": {
    "mail_address": "your@email.com",
    "password": "your-app-password",
    "imap_server": "imap.example.com",
    "imap_port": 993
  },
  "mail_checker": {
    "keywords": ["invoice", "important", "alert"],
    "search_in": ["subject", "sender", "body"],
    "notify_only_once": true
  },
  "notification": {
    "title": "New matching email",
    "description": "A matching unread email was found.",
    "position": "bottom-right",
    "position_margin": 20
  }
}
```

Fields marked **[OPTIONAL]** can be omitted and fall back to their default. Unknown or misspelled keys are rejected when the configuration is loaded.

- check_interval_minutes **[NUMBER]** **[OPTIONAL]** **[DEFAULT 60]**<br>
  Minimum time, in minutes, between two mailbox checks.

- mail_service **[REQUIRED]**
  - mail_address **[STRING]** **[REQUIRED]**<br>
    Address used to log in to the IMAP server.
  - password **[STRING]** **[REQUIRED]**<br>
    Password used to log in to the IMAP server. Many providers (Yahoo, Gmail, Outlook) do not accept the normal account password over IMAP: generate an app password in the account security settings and use that instead.
  - imap_server **[STRING]** **[REQUIRED]**<br>
    Host of the IMAP server, for example `imap.mail.yahoo.com`.
  - imap_port **[NUMBER]** **[REQUIRED]**<br>
    SSL port of the IMAP server, usually `993`.

- mail_checker **[REQUIRED]**
  - keywords **[LIST OF STRINGS]** **[OPTIONAL]** **[DEFAULT EMPTY]**<br>
    An email matches if any of these keywords appears in the searched fields. Matching is case-insensitive, so `Invoice` matches `invoice` and `INVOICE`.
  - search_in **[LIST OF STRINGS]** **[OPTIONAL]** **[DEFAULT ["subject", "sender", "body"]]**<br>
    Parts of the email that are searched for keywords. <br> Allowed values: `subject`, `sender`, `body`.
  - notify_only_once **[BOOLEAN]** **[OPTIONAL]** **[DEFAULT false]**<br>
    If `true`, each email is notified only once. If `false`, an unread matching email is notified again on every check.

- notification **[REQUIRED]**
  - title **[STRING]** **[OPTIONAL]** **[DEFAULT "MAIL DETECTED"]**<br>
    Title of the notification window.
  - description **[STRING]** **[OPTIONAL]** **[DEFAULT "CHECK YOUR MAILS!"]**<br>
    Message shown in the notification window.
  - position **[STRING]** **[OPTIONAL]** **[DEFAULT "center"]**<br>
    Position of the notification window on the screen. <br> Allowed values: `center`, `top-left`, `top-right`, `bottom-left`, `bottom-right`.
  - position_margin **[NUMBER]** **[OPTIONAL]** **[DEFAULT 0]**<br>
    Distance, in pixels, between the notification window and the screen edges. Ignored for `center`. The window is placed using the full screen size, so with a `bottom-*` position it may overlap the taskbar: increase this value if that happens.

### 2. Install

Before installing, make sure the complete project folder is in the location where you want to keep it permanently.

DO NOT REMOVE OR RENAME THE GENERATED FILES AFTER INSTALLATION.

The generated application and scheduled task use paths based on the original project location. Moving or renaming the folder afterwards will cause the application and/or scheduled task to stop working correctly. If you need to move the application to another location, run `uninstall.bat` first, move the project folder, and then run `install.bat` again.

Requirements: Python available in `PATH`.

Run:

```text
install.bat
```

The installer will:

- Remove any previous build.
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

The actual email-check interval is configured separately with `check_interval_minutes` in `configuration.json`.

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

## Testing

The program can be tested by running, from the project folder:

```text
python .\main.py --force-check
```

`--force-check` checks the mailbox immediately, ignoring `check_interval_minutes`, and shows the notification if a matching unread email is found. The dependencies in `requirements.txt` must be installed for this command to work. <br>
The simpler way to do this is to install the application with `install.bat`, open a console in the installation location, and then run:

```text
 `.venv\Scripts\python.exe .\main.py --force-check`.
```

**Warning:** with `notify_only_once` set to `true`, the emails notified during a test are recorded in `config/state.json` and will not be notified again by the scheduled task.

## Project Structure

```text
DesktopMailAlerts/
├── config/
│   ├── configuration_template.json
│   ├── configuration.json      (created by you)
│   └── state.json              (created at runtime)
├── assets/
│   └── notification.wav
├── src/
│   ├── configuration.py        Loads configuration.json into dataclasses (dacite)
│   ├── desktop_notifier.py     Notification window
│   ├── mail_service.py         IMAP access and keyword filtering
│   └── state.py                Persistent state
├── main.py
├── install.bat
├── uninstall.bat
├── requirements.txt
└── README.md
```

## Notes

The application stores previously notified email IDs and the next scheduled check time in:

```text
config/state.json
```

Delete this file to reset the notification history.
