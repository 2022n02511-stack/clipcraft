
import asyncio
import re

from dbus_next.aio import MessageBus
from dbus_next.service import ServiceInterface, method

from formatters.detector import detect_content
from formatters.cleaner import clean_text
from formatters.ai_formatter import AIFormatter
from storage.history import save, get_recent, clear


formatter = AIFormatter()


def is_already_formatted(text):
    has_heading = bool(re.search(r"(?m)^#{1,6}\s+\S", text))
    has_structure = bool(re.search(
        r"(?m)^\s*(?:[-*+]\s+|\d+\.\s+|\|.*\|)\S?",
        text
    ))
    return has_heading and has_structure


def process_text(text):
    if not text or not text.strip():
        return text

    content_type = detect_content(text)

    if content_type == "code":
        print("[ClipCraft] Code detected. Skipping Gemini.")
        return text

    if is_already_formatted(text):
        print("[ClipCraft] Already formatted. Skipping Gemini.")
        return text

    print(f"\n[ClipCraft] Detected type: {content_type}")

    cleaned_text = clean_text(text, content_type)
    return formatter.format_text(cleaned_text, content_type)


class ClipCraftInterface(ServiceInterface):

    def __init__(self):
        super().__init__("local.clipcraft.Clipboard")

    @method()
    def ReceiveText(self, text: "s") -> "s":
        print(f"\n[ClipCraft] Received {len(text)} characters.")

        try:
            result = process_text(text)

            if text.strip() and result:
                save(text, result)
                print("[ClipCraft] Saved to history.")

            print("\n[ClipCraft] Output:\n")
            print(result)

            return result or ""

        except Exception as error:
            print(f"\n[ClipCraft] Processing failed: {error}")
            return ""

    @method()
    def GetHistory(self) -> "a(ss)":
        try:
            return [list(row) for row in get_recent(10)]
        except Exception as error:
            print(f"[ClipCraft] History retrieval failed: {error}")
            return []

    @method()
    def ClearHistory(self) -> "b":
        try:
            clear()
            print("[ClipCraft] History cleared.")
            return True
        except Exception as error:
            print(f"[ClipCraft] History clearing failed: {error}")
            return False


async def main():
    bus = await MessageBus().connect()
    bus.export("/local/clipcraft", ClipCraftInterface())
    await bus.request_name("local.clipcraft")

    print("[ClipCraft] Clipboard formatter ready.")
    await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[ClipCraft] Stopped.")
