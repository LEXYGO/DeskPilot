# DeskPilot

DeskPilot is a small desktop application for controlling height-adjustable desks through a compatible desk module.

## Features

The app runs as a tray application on Linux and connects via WebSocket to a compatible desk module. It displays the current desk height, controls presets, and saves user settings locally.

## Features

- Tray icon
- Current desk height display
- Support for up to 9 presets

## Officialy supported / planed Desk Modules:

The following desk modules are planned or already compatible:

- **FlexiSmart** by @LEXYGO for LoctecMotion and Flexispot desks (repository not public yet, but I am working on it :D)

### Supported module requirements

Official desk modules must support the following command interface and behavior over WebSocket on port 81:

- `i` : Request device info in the format `<max_height> <min_height> <presetcount> <current_height_in_mm>`
- `s` : Stop up/down movement
- `d` : Move **down** until stopped
- `u` : Move **up** until stopped
- `goto<requested_height>` : Move to the requested height (exact height not required; a close value is sufficient)
- `1` : Move to preset 1 if it exists on the desk
- `2` : Move to preset 2 if it exists on the desk
- `3` : Move to preset 3 if it exists on the desk
- `4` : Move to preset 4 if it exists on the desk
- `5` : Move to preset 5 if it exists on the desk
- `6` : Move to preset 6 if it exists on the desk
- `7` : Move to preset 7 if it exists on the desk
- `8` : Move to preset 8 if it exists on the desk
- `9` : Move to preset 9 if it exists on the desk

Additionally, the desk must send its current height in millimeters every time the height changes.

## Download & Installation

You can download the pre-compiled binaries for Windows and Linux from the [Releases](https://github.com/LEXYGO/DeskPilot/releases) page.

### 🪟 Windows
1. Download the `DeskPilot_Vx.x.x_x86-64_setup.exe`.
2. Run the installer and follow the instructions.
3. The App can be set to launch on system startup.

### 🐧 Linux (AppImage)
1. Download the `DeskPilot_Vx.x.x_x86-64.AppImage`.
2. Make it executable via your file manager or run the following terminal command:
   ```bash
   chmod +x DeskPilot_Vx.x.x_x86-64.AppImage
   ```
3. Double-click the file to run the app.

## Usage

- The tray icon starts automatically.
- Use the dashboard to set the desk module IP address and preset names.
- The app connects using `ws://<ip>:<port>`. The Port is 81 by default.
- Once connected, preset commands are available from the tray menu.

## Configuration

The app stores settings in a configuration file under the user data directory:

- `max_height`
- `min_height`
- `preset_count`
- `ip`
- `port`
- `p1` through `p9`

## Contributing & Support

If you encounter any bugs or have feature requests, please open an issue on the [GitHub Issue Tracker](https://github.com/DEIN/LEXYGO/DeskPilot/issues).

## License

MIT

This project uses the following open source libraries:
- [PySide6](https://wiki.qt.io/Qt_for_Python) by The Qt Company, licensed under LGPL v3
- [platformdirs](https://github.com/platformdirs/platformdirs) by the platformdirs contributors, licensed under MIT

Thanks to Gabriel Grant from [Pictogrammers.com](https://pictogrammers.com/contributor/gabrielgrant/) for the desk icon.