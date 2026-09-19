import os
import json
from dataclasses import dataclass, field

@dataclass
class State:
    notified_uids: list[str] = field(default_factory=list)
    next_check_timestamp: float = 0
    next_check_date: str = ""

class StateManager:
    def __init__(self, file: str, max_uids: int = 1000):
        self.file = file
        self.max_uids = max_uids
        self.state = self.load()

    def load(self) -> State:
        if not os.path.exists(self.file):
            return State()
        try:
            with open(self.file, "r", encoding="utf-8") as f:
                return State(**json.load(f))
        except (json.JSONDecodeError, TypeError, OSError):
            return State()

    def save(self):
        self.state.notified_uids = self.state.notified_uids[-self.max_uids:]
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(self.state.__dict__, f, indent=4)