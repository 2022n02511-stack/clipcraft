
import subprocess
import time
from typing import Callable


class ClipboardMonitor:
    def __init__(self, callback: Callable[[str], None], interval=0.5):
        self.callback = callback
        self.interval = interval
        self.last_text = None
        self.running = False

    def read_clipboard(self):
        try:
            result = subprocess.run(
                ["wl-paste", "--no-newline"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=2
            )

            if result.returncode != 0:
                return None

            return result.stdout

        except (subprocess.TimeoutExpired, FileNotFoundError):
            return None

    def start(self):
        self.running = True

        # Ignore whatever was already in the clipboard at startup.
        self.last_text = self.read_clipboard()

        print("ClipCraft is monitoring your clipboard...")

        while self.running:
            current_text = self.read_clipboard()

            if current_text is not None and current_text != self.last_text:
                self.last_text = current_text

                if current_text.strip():
                    self.callback(current_text)

            time.sleep(self.interval)

    def stop(self):
        self.running = False
