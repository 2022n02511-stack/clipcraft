# ClipCraft

**An intelligent clipboard assistant for your desktop.**

ClipCraft is a desktop clipboard management and text-formatting tool designed to make copied text more useful. It monitors clipboard activity, optionally processes text using AI, and maintains a searchable history of copied content.

The goal is to build a cross-platform application with a shared core and lightweight operating-system-specific integrations.

## Current Features

- **Clipboard monitoring:** Detects newly copied text.
- **Live preview:** Displays the current clipboard contents in the GNOME top-bar popup.
- **Automatic formatting:** Optionally processes copied text using an AI-powered backend.
- **Formatting toggle:** Enable or disable automatic formatting at any time.
- **Clipboard history:** Saves copied text whether automatic formatting is enabled or disabled.
- **History restoration:** Select a previous entry to restore it to the clipboard.
- **Undo formatting:** Restore the original text after automatic formatting.
- **Persistent storage:** Uses SQLite to preserve clipboard history across sessions.

## How It Works

ClipCraft currently follows a modular architecture:

```text
                 CLIPBOARD
                     |
                     v
            GNOME Shell Extension
                     |
             Clipboard Monitoring
                     |
                     v
                D-Bus IPC
                     |
                     v
              Python Backend
                     |
          +----------+----------+
          |                     |
          v                     v
    AI Formatting          History Manager
          |                     |
          v                     v
    Formatted Text           SQLite
          |                     |
          +----------+----------+
                     |
                     v
              Clipboard UI
```

The GNOME extension handles desktop integration, while the Python backend handles processing and persistent history.

## Technology Stack

| Component | Technology |
|---|---|
| Desktop integration | GNOME Shell Extensions |
| Extension language | JavaScript (GJS) |
| Backend | Python |
| Inter-process communication | D-Bus |
| Database | SQLite |
| Clipboard utilities | Wayland clipboard tools |
| AI integration | Google Gemini API |

## Project Structure

```text
clipcraft/
│
├── core/
│   └── dbus_server.py
│
├── storage/
│   └── history.py
│
├── schemas/
│   └── org.gnome.shell.extensions.clipcraft.gschema.xml
│
├── extension/
│   └── [GNOME integration]
│
├── .env
├── requirements.txt
└── README.md
```

*Note: The installed GNOME extension currently lives separately in the user's GNOME extensions directory. The repository structure will be consolidated as development progresses.*

## Development Environment

Current development environment:

- Fedora Linux
- GNOME 49
- Wayland
- Python 3.14
- Node.js for JavaScript syntax checking
- VS Code

### Running the Backend

From the project directory:

```bash
python3 -m core.dbus_server
```

The backend can also run as a systemd user service:

```bash
systemctl --user start clipcraft.service
```

Check its status:

```bash
systemctl --user status clipcraft.service
```

### Checking the GNOME Extension

```bash
node --check ~/.local/share/gnome-shell/extensions/clipcraft@local/extension.js
```

Reload the extension:

```bash
gnome-extensions disable clipcraft@local
gnome-extensions enable clipcraft@local
```

On Wayland, a fresh GNOME login may be necessary to fully reload modified extension code.

## Configuration

ClipCraft uses environment variables for sensitive configuration.

Create a `.env` file for local development and provide your own AI API key.

**Never commit API keys or other secrets to version control.**

## Roadmap

### Phase 1: Core Clipboard Experience
- [x] Clipboard monitoring
- [x] Live clipboard preview
- [x] Automatic formatting toggle
- [x] Persistent SQLite history
- [x] History restoration
- [x] Undo formatting
- [ ] Preview copy button
- [ ] Improve history interface
- [ ] Improve error handling

### Phase 2: Formatting Engine
- [ ] Support multiple formatting operations
- [ ] Custom formatting instructions
- [ ] Manual formatting commands
- [ ] GUI-based formatting controls
- [ ] Formatting presets
- [ ] Better API configuration

### Phase 3: Cross-Platform Support
- [ ] Windows integration
- [ ] macOS integration
- [ ] Shared platform-independent core
- [ ] Platform-specific clipboard adapters
- [ ] Unified configuration and storage

### Phase 4: Extensibility
- [ ] Custom commands
- [ ] User-defined workflows
- [ ] Multiple AI providers
- [ ] Bring-your-own API key support
- [ ] Plugin architecture

### Phase 5: Public Release
- [ ] Installation and onboarding
- [ ] Documentation
- [ ] Security and privacy review
- [ ] Packaging and distribution
- [ ] Automated testing

## Design Philosophy

ClipCraft aims to be:

- **Lightweight:** Stay out of the way until needed.
- **Modular:** Keep desktop integrations separate from core functionality.
- **Extensible:** Allow new commands, providers, and workflows.
- **Private:** Give users control over their clipboard data and API credentials.
- **Cross-platform:** Maintain one shared core with platform-specific integrations.

## Project Status

**Early development.**

The current prototype runs on Fedora with GNOME and supports clipboard monitoring, AI formatting, live preview, and persistent clipboard history.

The architecture and user interface are still evolving.

## License

To be determined.
