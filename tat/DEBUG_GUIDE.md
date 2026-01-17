# BankResearch Debug Guide

## Latest Changes - v0.6.0

### ✅ Keybind Changes (Thay Đổi Phím Tắt)
**Vấn đề:** F8 xung đột với phím chức năng của game.

**Giải pháp:**
- Changed from **F8** to **NumPad8** for research/debug
- Added **NumPad7** for Bank sorting

**Keybinds:**
```python
@keybind("NumPadSeven")   # NumPad7 - Sort Bank
def do_bank_sort(_) -> None:
    ...

@keybind("NumPadEight")   # NumPad8 - Dump Structure  
def do_research(_) -> None:
    ...
```

### ✅ Added Sort Functionality (Thêm Chức Năng Sort)
Thêm chức năng sort Bank với 5 phương thức:
1. **Boividevngu** (mặc định)
2. By Rarity
3. By Type
4. By Name
5. By Level

**Menu Options:**
- SpinnerOption to select sort method
- Button to trigger sort
- Keybind NumPad7 for quick sort

### ✅ Improved Debug Logging
- ERROR và WARNING **luôn** được ghi vào file, ngay cả khi debug mode tắt
- Thêm logging chi tiết cho sort operations
- Full traceback cho mọi exception

```python
# Now logs errors even when debug is off
if DEBUG_ENABLED or level in ["ERROR", "WARNING"]:
    write_to_file()
```

---

## Previous Fixes (v0.5.x)

## Issue Fixed

### Error
```
AttributeError: type object 'KeybindType' has no attribute 'PRESSED'
File "F:\SteamLibrary\steamapps\common\Borderlands 3\sdk_mods\BankSort\__init__.py", line 323
@keybind("F8", KeybindType.PRESSED)
```

### Root Cause
The code was incorrectly using `KeybindType.PRESSED` as a parameter. In the `mods_base` SDK:
- `KeybindType` is a **class**, not an enum
- The keybind decorator doesn't accept a `KeybindType` parameter
- The decorator has an optional `event_filter` parameter that accepts `EInputEvent` enum values

### Fix Applied
Changed from:
```python
from mods_base.keybinds import keybind, KeybindType

@keybind("F8", KeybindType.PRESSED)
def do_research(_) -> None:
```

To:
```python
from mods_base.keybinds import keybind

@keybind("F8")
def do_research(_) -> None:
```

The keybind decorator uses `EInputEvent.IE_Pressed` as the default event filter, so no additional parameter is needed.

## Debug Mechanism Added

### Features (Similar to MagnetLoot Mod)

1. **Toggle Debug Mode**: Enable/disable debug logging through the mod options menu
2. **Timestamped Logs**: All debug messages include millisecond-precision timestamps
3. **Log Levels**: Support for INFO, DEBUG, WARNING, and ERROR levels
4. **Dual Output**: Logs printed to console AND saved to `debug.log` file
5. **Selective Logging**: Only WARNING and ERROR messages show when debug is disabled

### How to Use

#### Enable Debug Mode
1. Open the in-game mod menu
2. Navigate to "Bank Research" mod
3. Toggle "🐛 Enable Debug Mode" to ON

#### Debug Output Locations
- **Console**: Real-time debug messages in the game console
- **File**: `debug.log` in the mod directory (same location as the mod)

#### Debug Log Format
```
[HH:MM:SS.mmm] [BankResearch] [LEVEL] Message
```

Example:
```
[12:34:56.789] [BankResearch] [INFO] Starting dump_player_controller
[12:34:56.790] [BankResearch] [DEBUG] Attempting to get PlayerController
[12:34:56.791] [BankResearch] [DEBUG] Found 245 attributes
```

### Debug Points Added

The debug mechanism logs important events throughout the code:

1. **Initialization**: When mod loads
2. **Keybind Press**: When F8 is pressed
3. **PlayerController Operations**: When getting PC and checking attributes
4. **Object Search**: When searching for Bank/Inventory objects
5. **File Operations**: When saving dumps to files
6. **Errors**: All errors and exceptions with full tracebacks

### Debug vs Normal Mode

**Normal Mode** (Debug OFF):
- Only ERROR and WARNING messages shown
- Minimal console output
- No debug.log file created
- Better performance

**Debug Mode** (Debug ON):
- All INFO and DEBUG messages shown
- Detailed operation logging
- All logs saved to debug.log file
- Useful for troubleshooting

## Version Changes

- **v0.5.0**: Original version with KeybindType error
- **v0.5.1**: Fixed KeybindType error + added debug mechanism

## Testing Recommendations

1. Load the mod and verify no errors appear
2. Press F8 or use the mod menu button to test dump functionality
3. Enable debug mode and press F8 again to see detailed logs
4. Check the `debug.log` file in the mod directory
5. Disable debug mode and verify logs are minimal

## Additional Notes

- The debug mechanism is inspired by magnetloot mod's logging approach
- Debug logging has minimal performance impact when disabled
- The debug.log file will grow over time; delete it periodically if needed
- All timestamps use 24-hour format with millisecond precision
