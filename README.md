# sink-switch for Windows

A powerful command-line and hotkey-driven utility to quickly switch between your audio playback devices on Windows.

This script allows you to create a curated list of your favorite audio devices and cycle through them with a simple command or a global hotkey, complete with toast notifications.

## Features

- **Device Management:**
  - **List:** See all available audio devices with their readable names and command-line IDs.
  - **Visual Config:** A graphical interface (GUI) to easily check/uncheck devices to include in your cycle.
  - **Initialize:** Automatically generates a configuration file.
- **User-Controlled Cycling:**
  - **Smart Cycling:** Switch in a simple, predictable round-robin order (A -> B -> C -> A).
  - **State Memory:** Remembers the last cycled device, even if you manually switch devices in between.
- **Direct Access:** Instantly switch to any audio device by its ID.
- **Visual Feedback:** Displays a native Windows toast notification (with icon) on every successful switch.
- **Global Hotkeys:** Comes with an optional AutoHotkey script to bind cycling to `Alt + Mute` (or any custom key).
- **Automated Installer:** Includes a setup script to handle dependencies and startup shortcuts.

## Dependencies

1.  **PowerShell:** Included with all modern versions of Windows.
2.  **SoundVolumeView.exe:** Automatically downloaded by the installer.
3.  **BurntToast PowerShell Module:** Automatically installed by the installer.
4.  **AutoHotkey (Optional):** Required only for global hotkeys.

## Installation & Setup

1.  **Run the Installer:**
    Open a PowerShell terminal in the project directory and run the installer. This script will download `SoundVolumeView`, install the notification module, initialize your config, and create a startup shortcut for hotkeys.
    ```powershell
    .\install.ps1
    ```

2.  **Configure Devices:**
    To choose which devices are included in your toggle cycle, run the UI command:
    ```powershell
    .\sink-switch.ps1 ui
    ```
    A window will appear allowing you to check or uncheck devices.

## Usage (Command Line)

All commands can be run from a PowerShell terminal.

- **`list` (alias: `ls`)**: Lists all available audio devices and their IDs.
- **`ui` (alias: `gui`)**: Opens the graphical configuration window.
- **`cycle` (alias: `cy`)**: Switches to the next device in your enabled list.
- **`set <DeviceID>` (alias: `s`)**: Sets a specific audio device as the default and updates the cycle position.
- **`current` (alias: `c`)**: Shows the current default playback and recording devices.
- **`init`**: Re-initializes the configuration file (WARNING: Overwrites existing config).

## Usage (Global Hotkeys)

If you ran the installer, the hotkey script should start automatically with Windows.

- **Default Hotkey:** Press `Alt + Mute` (`!Volume_Mute`) to cycle devices.
- **Customize:** Edit `keybindings.ahk` to change the key combination.
- **Manual Start:** Double-click `keybindings.ahk` to start it manually (look for the green "H" icon in the tray).

## Future Development

The current PowerShell version is a fully functional prototype. The next phase of development is a complete rewrite in **Go** to provide:
- A single, standalone `.exe` with zero dependencies.
- Native performance using Windows Core Audio APIs.
- Built-in global hotkey support (removing the need for AutoHotkey).
