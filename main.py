from core.clipboard import ClipboardMonitor


def on_copy(text):
    print(f"\n[ClipCraft] Detected {len(text)} characters.")


if __name__ == "__main__":
    monitor = ClipboardMonitor(on_copy)

    try:
        monitor.start()
    except KeyboardInterrupt:
        monitor.stop()
        print("\nClipCraft stopped.")