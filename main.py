import os
import sys
import time
from datetime import datetime
from src.configuration import ConfigurationManager
from src.desktop_notifier import DesktopNotifier
from src.mail_service import MailChecker, MailService
from src.state import StateManager

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(sys.executable)))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
CONFIG_FILE = os.path.join(BASE_DIR, "config/configuration.json")
STATE_FILE = os.path.join(BASE_DIR, "config/state.json")


def _should_execute(state_manager: StateManager) -> bool:
    return time.time() >= state_manager.state.next_check_timestamp


def _check_emails(mail_checker: MailChecker, notifier: DesktopNotifier, state_manager: StateManager) -> None:
    print("Checking emails...")

    mails = mail_checker.retrieve_mails_passing_filter()
    for mail in mails:
        notified_set = set(state_manager.state.notified_uids)
        notified_set.add(mail.uid)
        state_manager.state.notified_uids = list(notified_set)

    if len(mails) > 0:
        print("At least one mail to notify has been found!")
        notifier.show_notification()
    else:
        print("No mails to notify have been found")


def _update_state(wait_in_seconds: int, state_manager: StateManager,) -> None:
    state = state_manager.state
    state.next_check_timestamp = time.time() + wait_in_seconds
    state.next_check_date = datetime.fromtimestamp(state.next_check_timestamp).isoformat()
    state_manager.save()


def main(argv: list[str]):
    config_manager = ConfigurationManager(CONFIG_FILE)
    config = config_manager.configuration
    state_manager = StateManager(STATE_FILE, 1000)
    state = state_manager.state

    force_check = "--force-check" in argv

    print("======================================")
    print("Desktop Mail Notifier")
    print("======================================")

    print(f"Keywords: {', '.join(config.mail_checker.keywords)}" )
    print()

    if not force_check and not _should_execute(state_manager):
        print("Skipping current execution!")
        return

    mail_service = MailService(config.mail_service)
    mail_checker = MailChecker(config.mail_checker, mail_service, state.notified_uids)
    notifier = DesktopNotifier(config.notification)

    wait_in_seconds = config.check_interval_minutes * 60
    _check_emails(mail_checker, notifier, state_manager)
    _update_state(wait_in_seconds, state_manager)

    print("Done!")

if __name__ == "__main__":
    main(sys.argv)