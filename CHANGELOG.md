# Changelog

All notable changes to Mine Squad Pi will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.1] - 2026-01-18
### Added
- RGB keyboard support for Raspberry Pi 500+
- New `KeyboardRGB` class to manage keyboard lighting effects
- Control key illumination during gameplay (white for movement, cyan for actions)
- Visual feedback effects:
  - Hue cycling effect on mine explosion
  - Red effect on enemy/hazard damage
  - Green flash when placing a beacon
  - Multicolor effect when a hotspot is picked up
- Control keys preview in Settings menu when changing control scheme
- Automatic save/restore of user's original keyboard RGB configuration
- Increased turn delay for joystick (225ms vs 125ms for keyboard) to prevent accidental mine steps

### Fixed
- Joystick detection now filters fake devices (requires at least 2 analog axes)

## [1.0] - 2026-01-01
### Added
- Initial release

