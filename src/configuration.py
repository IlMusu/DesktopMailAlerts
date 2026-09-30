import json
from dataclasses import dataclass
from dacite import Config, from_dict
from src.desktop_notifier import DesktopNotifierConfiguration
from src.mail_service import MailCheckerConfiguration, MailServiceConfiguration

@dataclass
class Configuration:
    mail_service: MailServiceConfiguration
    mail_checker: MailCheckerConfiguration
    notification: DesktopNotifierConfiguration
    check_interval_minutes: float= 60

class ConfigurationManager:
    def __init__(self, file: str):
        self.file = file
        self.configuration = self.load()

    def load(self) -> Configuration:
        with open(self.file, "r", encoding="utf-8") as f:
            data = json.load(f)
        # strict: reject unknown keys, so typos are reported instead of silently ignored.
        return from_dict(Configuration, data, config=Config(strict=True))