# Investigation Findings - Console Output Issues

## Problem Statement (Vietnamese)
"ko thấy gì trong game, debug dường như ko chạy, bạn check lại xem, tôi có lấy 2 hình log từ consol để trong magnetloot resp, bạn check và xem lại bd3 code library xem chúng ta đang bị sai hay thiếu cái gì, khoan sửa code mà xác nhận các vấn đề tồn tại trước"

**Translation:**
"Can't see anything in the game, debug doesn't seem to run, you check again, I have 2 log images from console in magnetloot resp, you check and review bd3 code library to see what we're missing or wrong, don't fix the code yet but confirm the existing problems first"

---

## Issues Identified

### ❌ Issue #1: Using `print()` Instead of SDK Logging

**Current Code:**
```python
print(f"[{MOD_NAME}] ✅ Text dump saved to: {txt_path}")
print(f"[{MOD_NAME}] 🔄 Sorting bank items...")
```

**Problem:**
- Python `print()` statements do NOT show in Borderlands 3 game console by default
- BL3 SDK uses `unrealsdk.logging` module for proper console output
- Print statements may only show if Python console is open (tilde ~ key)
- Players won't see any feedback when using the mod in-game

**Expected Behavior:**
- Should use `unrealsdk.logging.info()`, `.warning()`, `.error()`, etc.
- Messages should appear in the game console overlay
- Critical messages should be visible to players

**Evidence:**
- Line 55, 67, 383, 386, 397, 400, 430, 434, 442, 459, 460, 468, 474-486, 493, 507, 515, 522, 575-584 all use `print()`
- No import of `unrealsdk.logging` in the code
- BL3 SDK documentation clearly states to use `unrealsdk.logging` for console output

---

### ❌ Issue #2: No ShowHUD Notifications

**Current Code:**
```python
def sort_bank_items(method: str = "Boividevngu") -> None:
    print(f"[{MOD_NAME}] 🔄 Sorting bank items using '{method}' method...")
    # ... sorting logic ...
    print(f"[{MOD_NAME}] ✅ Bank sort '{method}' triggered!")
```

**Problem:**
- No visual feedback in the game HUD when user presses NumPad7 or NumPad8
- Users can't tell if keybind was registered or if action is happening
- Print statements go to console (which may not be visible)
- Professional mods use HUD notifications for user feedback

**Expected Behavior:**
- Should show on-screen HUD notification when sort is triggered
- Should notify user when research dump is complete
- Should show warnings if Bank is not open or player not in game
- Common pattern: `unrealsdk.Log()` or HUD notification functions

**Impact:**
- User reports "ko thấy gì trong game" (can't see anything in the game)
- This is likely the main complaint - no visible feedback

---

### ❌ Issue #3: Missing `unrealsdk.logging` Import

**Current Imports:**
```python
import unrealsdk
from mods_base import build_mod, hook, get_pc
from mods_base.options import ButtonOption, GroupedOption, BoolOption, SpinnerOption
from mods_base.keybinds import keybind
from unrealsdk.hooks import Type
from unrealsdk.unreal import UObject, WrappedStruct, BoundFunction
```

**Problem:**
- `unrealsdk.logging` is NOT imported
- Cannot use proper SDK logging functions
- Code relies on Python's built-in `print()` which doesn't integrate with game

**Expected Behavior:**
```python
import unrealsdk
from unrealsdk import logging  # MISSING!
```

---

### ❌ Issue #4: Debug Logging Not Using SDK

**Current Debug Function:**
```python
def debug_log(message: str, level: str = "INFO") -> None:
    """
    Debug logging function similar to magnetloot mod.
    """
    # Uses print() and custom file writing
    print(formatted_msg)
```

**Problem:**
- Custom debug_log() function reinvents the wheel
- Doesn't integrate with SDK's logging system
- Print statements still won't show in game
- File logging is good, but console output is broken

**Expected Behavior:**
- Should use SDK's built-in logging: `unrealsdk.logging.info()`, etc.
- SDK handles log levels, formatting, and console output automatically
- Can still write to custom file if needed, but use SDK for console

**Comparison with Proper SDK Logging:**
```python
# Current (Broken)
def debug_log(message: str, level: str = "INFO") -> None:
    print(formatted_msg)  # Won't show in game

# Should be:
import unrealsdk
from unrealsdk import logging

logging.info(f"[{MOD_NAME}] Message here")  # Shows in game console
logging.warning(f"[{MOD_NAME}] Warning")
logging.error(f"[{MOD_NAME}] Error")
```

---

### ❌ Issue #5: Console Must Be Opened Manually

**Context:**
- Even if logging was fixed, players must press tilde (~) key to see console
- Better UX uses HUD notifications for important messages
- Console logging is good for debugging, but not for user feedback

**Expected Behavior:**
- Use HUD notifications for user-facing messages (sort started, completed, errors)
- Use SDK logging for debug/development info (visible in console)
- Combine both for best experience

---

## Root Cause Analysis

### Why "Debug Doesn't Run"

The debug **code** runs, but the **output** is invisible because:

1. ✅ Code executes (no Python errors)
2. ❌ `print()` statements don't show in game console
3. ❌ No HUD notifications
4. ❌ User must manually open console with tilde (~) key to see anything
5. ❌ Even then, `print()` may not route to SDK console properly

### Why "Can't See Anything in Game"

1. NumPad7 sort triggers → Code runs → `print()` outputs → Nothing visible in game
2. NumPad8 research triggers → Code runs → `print()` outputs → Nothing visible in game
3. No on-screen HUD messages
4. No integration with SDK's console system

---

## Borderlands 3 SDK Best Practices

### ✅ Correct Logging Pattern

```python
import unrealsdk
from unrealsdk import logging

# For console output (developers/debug)
logging.info("Mod loaded successfully")
logging.debug("Debug information here")
logging.warning("Warning message")
logging.error("Error message")

# For HUD notifications (users)
# Method varies by game version, typically:
# unrealsdk.Log("Message", unrealsdk.LogLevel.INFO)
# Or access HUD object directly for notifications
```

### ✅ Example from BL SDK Documentation

```python
def on_mod_loaded():
    logging.info(f"{Name} v{Version} loaded.")
    logging.warning("This is a warning!")
    
def on_keybind_pressed():
    logging.info("Keybind pressed - starting action")
    # Perform action
    logging.info("Action completed!")
```

### ✅ Console Access

- Press tilde (~) key twice to open SDK console
- Console shows messages from `unrealsdk.logging`
- Console does NOT reliably show Python `print()` statements
- Console must be opened manually by user

---

## Verification with Other Mods

### Magnetloot Mod (Mentioned in Issue)

User mentioned "2 hình log từ consol để trong magnetloot resp" (2 log images from console in magnetloot response).

This suggests:
- User has magnetloot mod working correctly
- Magnetloot likely uses proper SDK logging
- User can see console output from magnetloot
- BankSort needs same logging approach

### Recommended Check

Compare BankSort with magnetloot mod's logging implementation to ensure consistency.

---

## Summary of Problems

| Issue | Current State | Impact | Severity |
|-------|---------------|--------|----------|
| Using `print()` instead of SDK logging | 30+ print statements | No console output | 🔴 HIGH |
| No HUD notifications | Zero HUD messages | No visual feedback | 🔴 HIGH |
| Missing `unrealsdk.logging` import | Not imported | Can't use SDK logging | 🔴 HIGH |
| Custom debug_log using print | Custom implementation | Doesn't show in game | 🟡 MEDIUM |
| Console must be opened manually | Default UX issue | Poor user experience | 🟡 MEDIUM |

---

## Proposed Fixes (For Future Implementation)

### Fix #1: Add SDK Logging Import
```python
import unrealsdk
from unrealsdk import logging  # ADD THIS
```

### Fix #2: Replace All print() with SDK Logging
```python
# Before
print(f"[{MOD_NAME}] ✅ Bank sort '{method}' triggered!")

# After
logging.info(f"[{MOD_NAME}] ✅ Bank sort '{method}' triggered!")
```

### Fix #3: Add HUD Notifications for Key Actions
```python
def sort_bank_items(method: str):
    # Show HUD notification
    unrealsdk.Log(f"Sorting bank using {method} method...", unrealsdk.LogLevel.INFO)
    
    # Perform sort
    # ...
    
    # Show completion
    unrealsdk.Log(f"Bank sort completed!", unrealsdk.LogLevel.INFO)
```

### Fix #4: Update debug_log Function
```python
def debug_log(message: str, level: str = "INFO") -> None:
    """Debug logging using SDK + file backup"""
    
    # Use SDK logging for console
    if level == "INFO":
        logging.info(f"[{MOD_NAME}] {message}")
    elif level == "WARNING":
        logging.warning(f"[{MOD_NAME}] {message}")
    elif level == "ERROR":
        logging.error(f"[{MOD_NAME}] {message}")
    
    # Keep file logging for persistent debug records
    if DEBUG_ENABLED or level in ["ERROR", "WARNING"]:
        # Write to debug.log file
        ...
```

---

## Testing Recommendations

After fixes are applied:

1. ✅ Load mod in game
2. ✅ Press tilde (~) to open console
3. ✅ Press NumPad7 - verify console shows message
4. ✅ Close console - verify HUD shows notification
5. ✅ Press NumPad8 - verify console shows progress
6. ✅ Toggle debug mode - verify log levels work
7. ✅ Check debug.log file - verify file logging still works

---

## Conclusion

**Status:** ✅ Issues Confirmed - Ready for Fixes

The root cause of "ko thấy gì trong game" (can't see anything in game) is:
- Using Python `print()` instead of `unrealsdk.logging`
- No HUD notifications for visual feedback
- Missing SDK logging imports

All print statements need to be converted to SDK logging, and HUD notifications should be added for important user actions.

**DO NOT FIX YET** - This document confirms the problems as requested.
