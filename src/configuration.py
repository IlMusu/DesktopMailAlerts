import json
from dataclasses import dataclass

@dataclass
class Configuration:
    email_address: str
    password: str
    imap_server: str
    imap_port: int
    check_interval_minutes: float
    keywords: list[str]
    search_in: list[str]
    notification_audio_file: str
    message_title: str
    message_description: str


class ConfigurationManager:
    def __init__(self, file: str):
        self.file = file
        self.configuration = self.load()

    def load(self) -> Configuration:
        with open(self.file, "r", encoding="utf-8") as f:
            return Configuration(**json.load(f))