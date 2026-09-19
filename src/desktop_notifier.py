import os
import winsound
from winotify import Notification

class DesktopNotifier:
    def __init__(self, message_title: str, message_description: str, sound_file: str):
        self.message_title = message_title
        self.message_description = message_description
        self.sound_file = sound_file

    def play_notification_sound(self):
        if not os.path.exists(self.sound_file):
            print( f"Sound file not found: {self.sound_file}")
            return
        
        try:
            winsound.PlaySound(self.sound_file, winsound.SND_FILENAME)
        except Exception as e:
            print(f"Could not play sound: {e}")


    def show_notification(self, ):
        toast = Notification(
                app_id="Desktop mail notifier",
                title=self.message_title,
                msg=self.message_description
            )
        toast.show()

        self.play_notification_sound()