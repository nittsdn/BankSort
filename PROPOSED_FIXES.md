# Proposed Fixes - Console Output Issues

## Overview

This document shows exactly how to fix the console output and HUD notification issues identified in INVESTIGATION_FINDINGS.md.

**DO NOT IMPLEMENT YET - AWAITING USER CONFIRMATION**

---

## Fix #1: Add SDK Logging Import

### Current Code (Line 9-18):
```python
import unrealsdk
from mods_base import build_mod, hook, get_pc
from mods_base.options import ButtonOption, GroupedOption, BoolOption, SpinnerOption
from mods_base.keybinds import keybind
from unrealsdk.hooks import Type
from unrealsdk.unreal import UObject, WrappedStruct, BoundFunction
from typing import Any
import os
import json
from datetime import datetime
```

### Proposed Fix:
```python
import unrealsdk
from unrealsdk import logging  # ADD THIS LINE
from mods_base import build_mod, hook, get_pc
from mods_base.options import ButtonOption, GroupedOption, BoolOption, SpinnerOption
from mods_base.keybinds import keybind
from unrealsdk.hooks import Type
from unrealsdk.unreal import UObject, WrappedStruct, BoundFunction
from typing import Any
import os
import json
from datetime import datetime
```

**Change:** Add `from unrealsdk import logging` after line 9

---

## Fix #2: Update debug_log Function

### Current Code (Line 35-67):
```python
def debug_log(message: str, level: str = "INFO") -> None:
    """
    Debug logging function similar to magnetloot mod.
    Logs to console and optionally to file when debug mode is enabled.
    
    Args:
        message: The message to log
        level: Log level (INFO, DEBUG, WARNING, ERROR)
    """
    global DEBUG_ENABLED
    
    # Early return for non-critical messages when debug is off (performance optimization)
    if not DEBUG_ENABLED and level not in ["ERROR", "WARNING"]:
        return
    
    timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    formatted_msg = f"[{timestamp}] [{MOD_NAME}] [{level}] {message}"
    
    # Always print errors and warnings, and all messages when debug is enabled
    if level in ["ERROR", "WARNING"] or DEBUG_ENABLED:
        print(formatted_msg)  # ❌ PROBLEM: Uses print()
    
    # Log to file if debug enabled or if it's an error/warning
    if DEBUG_ENABLED or level in ["ERROR", "WARNING"]:
        try:
            mod_dir = get_mod_directory()
            # Ensure directory exists
            os.makedirs(mod_dir, exist_ok=True)
            log_file = os.path.join(mod_dir, "debug.log")
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(formatted_msg + '\n')
        except Exception as e:
            print(f"[{MOD_NAME}] Failed to write to debug log: {e}")  # ❌ PROBLEM
```

### Proposed Fix:
```python
def debug_log(message: str, level: str = "INFO") -> None:
    """
    Debug logging function using SDK logging for console output.
    Also logs to file when debug mode is enabled.
    
    Args:
        message: The message to log
        level: Log level (INFO, DEBUG, WARNING, ERROR)
    """
    global DEBUG_ENABLED
    
    # Early return for non-critical messages when debug is off (performance optimization)
    if not DEBUG_ENABLED and level not in ["ERROR", "WARNING"]:
        return
    
    timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    formatted_msg = f"[{timestamp}] [{MOD_NAME}] [{level}] {message}"
    
    # ✅ FIX: Use SDK logging for console output (visible in game)
    if level in ["ERROR", "WARNING"] or DEBUG_ENABLED:
        if level == "ERROR":
            logging.error(formatted_msg)
        elif level == "WARNING":
            logging.warning(formatted_msg)
        elif level == "DEBUG":
            logging.debug(formatted_msg)
        else:  # INFO
            logging.info(formatted_msg)
    
    # Log to file if debug enabled or if it's an error/warning
    if DEBUG_ENABLED or level in ["ERROR", "WARNING"]:
        try:
            mod_dir = get_mod_directory()
            # Ensure directory exists
            os.makedirs(mod_dir, exist_ok=True)
            log_file = os.path.join(mod_dir, "debug.log")
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(formatted_msg + '\n')
        except Exception as e:
            logging.error(f"[{MOD_NAME}] Failed to write to debug log: {e}")  # ✅ FIX
```

**Changes:**
- Replace `print(formatted_msg)` with appropriate `logging.X()` calls
- Use `logging.error()`, `logging.warning()`, `logging.debug()`, `logging.info()`
- Update exception handler to use `logging.error()`

---

## Fix #3: Update save_dump_to_file Function

### Current Code (Line 372-401):
```python
def save_dump_to_file(result: dict) -> None:
    """Save dump results to files"""
    debug_log("Saving dump to files", "INFO")
    
    mod_dir = get_mod_directory()
    
    # Save text file
    txt_path = os.path.join(mod_dir, OUTPUT_FILE)
    try:
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(result["all_text"]))
        print(f"[{MOD_NAME}] ✅ Text dump saved to: {txt_path}")  # ❌
        debug_log(f"Text dump saved to: {txt_path}", "INFO")
    except Exception as e:
        print(f"[{MOD_NAME}] ❌ Error saving text file: {e}")  # ❌
        debug_log(f"Error saving text file: {e}", "ERROR")
    
    # Save JSON file
    json_path = os.path.join(mod_dir, JSON_FILE)
    try:
        # Remove all_text from JSON (too large)
        json_result = {k: v for k, v in result.items() if k != 'all_text'}
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_result, f, indent=2, default=str)
        print(f"[{MOD_NAME}] ✅ JSON dump saved to: {json_path}")  # ❌
        debug_log(f"JSON dump saved to: {json_path}", "INFO")
    except Exception as e:
        print(f"[{MOD_NAME}] ❌ Error saving JSON file: {e}")  # ❌
        debug_log(f"Error saving JSON file: {e}", "ERROR")
```

### Proposed Fix:
```python
def save_dump_to_file(result: dict) -> None:
    """Save dump results to files"""
    debug_log("Saving dump to files", "INFO")
    
    mod_dir = get_mod_directory()
    
    # Save text file
    txt_path = os.path.join(mod_dir, OUTPUT_FILE)
    try:
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(result["all_text"]))
        logging.info(f"[{MOD_NAME}] ✅ Text dump saved to: {txt_path}")  # ✅ FIX
        debug_log(f"Text dump saved to: {txt_path}", "INFO")
    except Exception as e:
        logging.error(f"[{MOD_NAME}] ❌ Error saving text file: {e}")  # ✅ FIX
        debug_log(f"Error saving text file: {e}", "ERROR")
    
    # Save JSON file
    json_path = os.path.join(mod_dir, JSON_FILE)
    try:
        # Remove all_text from JSON (too large)
        json_result = {k: v for k, v in result.items() if k != 'all_text'}
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_result, f, indent=2, default=str)
        logging.info(f"[{MOD_NAME}] ✅ JSON dump saved to: {json_path}")  # ✅ FIX
        debug_log(f"JSON dump saved to: {json_path}", "INFO")
    except Exception as e:
        logging.error(f"[{MOD_NAME}] ❌ Error saving JSON file: {e}")  # ✅ FIX
        debug_log(f"Error saving JSON file: {e}", "ERROR")
```

**Changes:** Replace all 6 `print()` calls with `logging.info()` or `logging.error()`

---

## Fix #4: Update sort_bank_items Function

### Current Code (Line 417-468):
```python
def sort_bank_items(method: str = "Boividevngu") -> None:
    """
    Sort items in the bank based on the selected method.
    
    Args:
        method: Sort method name (Boividevngu, By Rarity, By Type, By Name, By Level)
    """
    debug_log(f"sort_bank_items called with method: {method}", "INFO")
    
    try:
        pc = get_pc()
        if not pc:
            debug_log("PlayerController not found - cannot sort bank", "WARNING")
            print(f"[{MOD_NAME}] ⚠️ Please load into game first!")  # ❌
            return
        
        debug_log(f"PlayerController found, attempting to sort bank using '{method}' method", "DEBUG")
        print(f"[{MOD_NAME}] 🔄 Sorting bank items using '{method}' method...")  # ❌
        
        # Try to find bank inventory objects
        bank_objects = unrealsdk.find_all("OakInventory")
        debug_log(f"Found {len(bank_objects)} OakInventory objects", "DEBUG")
        
        if not bank_objects:
            debug_log("No bank inventory objects found", "WARNING")
            print(f"[{MOD_NAME}] ⚠️ No bank inventory found. Open bank first!")  # ❌
            return
        
        # Log the sorting operation
        debug_log(f"Starting sort operation with {len(bank_objects)} bank objects", "INFO")
        
        # TODO: Implement actual sorting logic based on Bank API research
        # ... (placeholder comment) ...
        
        # Placeholder for actual sorting logic
        print(f"[{MOD_NAME}] ✅ Bank sort '{method}' triggered!")  # ❌
        print(f"[{MOD_NAME}] ℹ️ Note: Full sorting implementation requires game API research")  # ❌
        debug_log(f"Bank sort '{method}' completed (placeholder)", "INFO")
        
    except Exception as e:
        import traceback
        error_msg = f"Error sorting bank: {e}"
        debug_log(error_msg, "ERROR")
        debug_log(f"Traceback: {traceback.format_exc()}", "ERROR")
        print(f"[{MOD_NAME}] ❌ {error_msg}")  # ❌
```

### Proposed Fix:
```python
def sort_bank_items(method: str = "Boividevngu") -> None:
    """
    Sort items in the bank based on the selected method.
    
    Args:
        method: Sort method name (Boividevngu, By Rarity, By Type, By Name, By Level)
    """
    debug_log(f"sort_bank_items called with method: {method}", "INFO")
    
    try:
        pc = get_pc()
        if not pc:
            debug_log("PlayerController not found - cannot sort bank", "WARNING")
            logging.warning(f"[{MOD_NAME}] ⚠️ Please load into game first!")  # ✅ FIX
            # ✅ ADD: HUD notification for user feedback
            unrealsdk.Log("Please load into game first!", unrealsdk.LogLevel.WARNING)
            return
        
        debug_log(f"PlayerController found, attempting to sort bank using '{method}' method", "DEBUG")
        logging.info(f"[{MOD_NAME}] 🔄 Sorting bank items using '{method}' method...")  # ✅ FIX
        # ✅ ADD: HUD notification
        unrealsdk.Log(f"Sorting bank using {method} method...", unrealsdk.LogLevel.INFO)
        
        # Try to find bank inventory objects
        bank_objects = unrealsdk.find_all("OakInventory")
        debug_log(f"Found {len(bank_objects)} OakInventory objects", "DEBUG")
        
        if not bank_objects:
            debug_log("No bank inventory objects found", "WARNING")
            logging.warning(f"[{MOD_NAME}] ⚠️ No bank inventory found. Open bank first!")  # ✅ FIX
            # ✅ ADD: HUD notification
            unrealsdk.Log("No bank inventory found. Open bank first!", unrealsdk.LogLevel.WARNING)
            return
        
        # Log the sorting operation
        debug_log(f"Starting sort operation with {len(bank_objects)} bank objects", "INFO")
        
        # TODO: Implement actual sorting logic based on Bank API research
        # ... (placeholder comment) ...
        
        # Placeholder for actual sorting logic
        logging.info(f"[{MOD_NAME}] ✅ Bank sort '{method}' triggered!")  # ✅ FIX
        logging.info(f"[{MOD_NAME}] ℹ️ Note: Full sorting implementation requires game API research")  # ✅ FIX
        # ✅ ADD: HUD notification
        unrealsdk.Log(f"Bank sort '{method}' triggered!", unrealsdk.LogLevel.INFO)
        debug_log(f"Bank sort '{method}' completed (placeholder)", "INFO")
        
    except Exception as e:
        import traceback
        error_msg = f"Error sorting bank: {e}"
        debug_log(error_msg, "ERROR")
        debug_log(f"Traceback: {traceback.format_exc()}", "ERROR")
        logging.error(f"[{MOD_NAME}] ❌ {error_msg}")  # ✅ FIX
        # ✅ ADD: HUD notification
        unrealsdk.Log(f"Error: {error_msg}", unrealsdk.LogLevel.ERROR)
```

**Changes:**
- Replace 6 `print()` calls with `logging.info()`, `logging.warning()`, `logging.error()`
- Add 4 `unrealsdk.Log()` calls for HUD notifications (visible in game!)

---

## Fix #5: Update do_research Function

### Current Code (Line 470-487):
```python
@keybind("NumPadEight")
def do_research(_) -> None:
    """Keybind: NumPad8 to dump Bank structure"""
    debug_log("NumPad8 pressed - starting Bank structure research", "INFO")
    print(f"[{MOD_NAME}] 🔍 Starting Bank structure research...")  # ❌
    print(f"[{MOD_NAME}] Please wait...")  # ❌
    
    result = dump_player_controller()
    save_dump_to_file(result)
    
    if result["success"]:
        print(f"[{MOD_NAME}] ✅ Research complete!")  # ❌
        print(f"[{MOD_NAME}] 📄 Check files in: {get_mod_directory()}")  # ❌
        print(f"[{MOD_NAME}] Files: {OUTPUT_FILE}, {JSON_FILE}")  # ❌
        debug_log("Research completed successfully", "INFO")
    else:
        print(f"[{MOD_NAME}] ❌ Research failed: {result.get('error', 'Unknown error')}")  # ❌
        debug_log(f"Research failed: {result.get('error', 'Unknown error')}", "ERROR")
```

### Proposed Fix:
```python
@keybind("NumPadEight")
def do_research(_) -> None:
    """Keybind: NumPad8 to dump Bank structure"""
    debug_log("NumPad8 pressed - starting Bank structure research", "INFO")
    logging.info(f"[{MOD_NAME}] 🔍 Starting Bank structure research...")  # ✅ FIX
    logging.info(f"[{MOD_NAME}] Please wait...")  # ✅ FIX
    # ✅ ADD: HUD notification
    unrealsdk.Log("Starting Bank structure research...", unrealsdk.LogLevel.INFO)
    
    result = dump_player_controller()
    save_dump_to_file(result)
    
    if result["success"]:
        logging.info(f"[{MOD_NAME}] ✅ Research complete!")  # ✅ FIX
        logging.info(f"[{MOD_NAME}] 📄 Check files in: {get_mod_directory()}")  # ✅ FIX
        logging.info(f"[{MOD_NAME}] Files: {OUTPUT_FILE}, {JSON_FILE}")  # ✅ FIX
        # ✅ ADD: HUD notification
        unrealsdk.Log("Research complete! Check mod folder for files.", unrealsdk.LogLevel.INFO)
        debug_log("Research completed successfully", "INFO")
    else:
        logging.error(f"[{MOD_NAME}] ❌ Research failed: {result.get('error', 'Unknown error')}")  # ✅ FIX
        # ✅ ADD: HUD notification
        unrealsdk.Log(f"Research failed: {result.get('error', 'Unknown error')}", unrealsdk.LogLevel.ERROR)
        debug_log(f"Research failed: {result.get('error', 'Unknown error')}", "ERROR")
```

**Changes:**
- Replace 6 `print()` calls with `logging.info()` or `logging.error()`
- Add 3 HUD notifications for user feedback

---

## Fix #6: Update do_bank_sort Function

### Current Code (Line 489-494):
```python
@keybind("NumPadSeven")
def do_bank_sort(_) -> None:
    """Keybind: NumPad7 to sort Bank"""
    debug_log(f"NumPad7 pressed - triggering bank sort with method: {CURRENT_SORT_METHOD}", "INFO")
    print(f"[{MOD_NAME}] 🔄 Sorting bank...")  # ❌
    sort_bank_items(CURRENT_SORT_METHOD)
```

### Proposed Fix:
```python
@keybind("NumPadSeven")
def do_bank_sort(_) -> None:
    """Keybind: NumPad7 to sort Bank"""
    debug_log(f"NumPad7 pressed - triggering bank sort with method: {CURRENT_SORT_METHOD}", "INFO")
    logging.info(f"[{MOD_NAME}] 🔄 Sorting bank...")  # ✅ FIX
    sort_bank_items(CURRENT_SORT_METHOD)
```

**Changes:** Replace 1 `print()` with `logging.info()`

---

## Fix #7: Update on_debug_toggle Function

### Current Code (Line 501-515):
```python
def on_debug_toggle(option: BoolOption, new_value: bool) -> None:
    """Toggle debug mode on/off"""
    global DEBUG_ENABLED
    DEBUG_ENABLED = new_value
    
    if DEBUG_ENABLED:
        print(f"[{MOD_NAME}] 🐛 Debug mode ENABLED")  # ❌
        debug_log("Debug mode enabled by user", "INFO")
        debug_log("=" * 60, "INFO")
        debug_log("Debug logging is now active!", "INFO")
        debug_log("All debug messages will be printed to console and saved to debug.log", "INFO")
        debug_log("=" * 60, "INFO")
    else:
        debug_log("Debug mode disabled by user", "INFO")
        print(f"[{MOD_NAME}] 🐛 Debug mode DISABLED")  # ❌
```

### Proposed Fix:
```python
def on_debug_toggle(option: BoolOption, new_value: bool) -> None:
    """Toggle debug mode on/off"""
    global DEBUG_ENABLED
    DEBUG_ENABLED = new_value
    
    if DEBUG_ENABLED:
        logging.info(f"[{MOD_NAME}] 🐛 Debug mode ENABLED")  # ✅ FIX
        # ✅ ADD: HUD notification
        unrealsdk.Log("Debug mode ENABLED", unrealsdk.LogLevel.INFO)
        debug_log("Debug mode enabled by user", "INFO")
        debug_log("=" * 60, "INFO")
        debug_log("Debug logging is now active!", "INFO")
        debug_log("All debug messages will be printed to console and saved to debug.log", "INFO")
        debug_log("=" * 60, "INFO")
    else:
        debug_log("Debug mode disabled by user", "INFO")
        logging.info(f"[{MOD_NAME}] 🐛 Debug mode DISABLED")  # ✅ FIX
        # ✅ ADD: HUD notification
        unrealsdk.Log("Debug mode DISABLED", unrealsdk.LogLevel.INFO)
```

**Changes:**
- Replace 2 `print()` calls with `logging.info()`
- Add 2 HUD notifications

---

## Fix #8: Update on_sort_method_change Function

### Current Code (Line 517-522):
```python
def on_sort_method_change(option: SpinnerOption, new_value: str) -> None:
    """Handle sort method change"""
    global CURRENT_SORT_METHOD
    CURRENT_SORT_METHOD = new_value
    debug_log(f"Sort method changed to: {new_value}", "INFO")
    print(f"[{MOD_NAME}] 🔄 Sort method set to: {new_value}")  # ❌
```

### Proposed Fix:
```python
def on_sort_method_change(option: SpinnerOption, new_value: str) -> None:
    """Handle sort method change"""
    global CURRENT_SORT_METHOD
    CURRENT_SORT_METHOD = new_value
    debug_log(f"Sort method changed to: {new_value}", "INFO")
    logging.info(f"[{MOD_NAME}] 🔄 Sort method set to: {new_value}")  # ✅ FIX
    # ✅ ADD: HUD notification
    unrealsdk.Log(f"Sort method: {new_value}", unrealsdk.LogLevel.INFO)
```

**Changes:**
- Replace 1 `print()` with `logging.info()`
- Add 1 HUD notification

---

## Fix #9: Update Initialization Messages

### Current Code (Line 575-584):
```python
print("="*80)  # ❌
print(f"[{MOD_NAME}] v{__version__} Loaded!")  # ❌
print(f"[{MOD_NAME}] Keybinds:")  # ❌
print(f"[{MOD_NAME}]   NumPad7 - Sort Bank (current method: {CURRENT_SORT_METHOD})")  # ❌
print(f"[{MOD_NAME}]   NumPad8 - Dump Bank Structure")  # ❌
print(f"[{MOD_NAME}] 🐛 Debug mode: {'ENABLED' if DEBUG_ENABLED else 'DISABLED'} (toggle in options)")  # ❌
print(f"[{MOD_NAME}] 📁 Available sort methods: {', '.join(SORT_METHODS.keys())}")  # ❌
print(f"[{MOD_NAME}] Output files: {OUTPUT_FILE}, {JSON_FILE}, debug.log")  # ❌
print(f"[{MOD_NAME}] Location: {get_mod_directory()}")  # ❌
print("="*80)  # ❌

debug_log(f"{MOD_NAME} v{__version__} initialized", "INFO")
```

### Proposed Fix:
```python
logging.info("="*80)  # ✅ FIX
logging.info(f"[{MOD_NAME}] v{__version__} Loaded!")  # ✅ FIX
logging.info(f"[{MOD_NAME}] Keybinds:")  # ✅ FIX
logging.info(f"[{MOD_NAME}]   NumPad7 - Sort Bank (current method: {CURRENT_SORT_METHOD})")  # ✅ FIX
logging.info(f"[{MOD_NAME}]   NumPad8 - Dump Bank Structure")  # ✅ FIX
logging.info(f"[{MOD_NAME}] 🐛 Debug mode: {'ENABLED' if DEBUG_ENABLED else 'DISABLED'} (toggle in options)")  # ✅ FIX
logging.info(f"[{MOD_NAME}] 📁 Available sort methods: {', '.join(SORT_METHODS.keys())}")  # ✅ FIX
logging.info(f"[{MOD_NAME}] Output files: {OUTPUT_FILE}, {JSON_FILE}, debug.log")  # ✅ FIX
logging.info(f"[{MOD_NAME}] Location: {get_mod_directory()}")  # ✅ FIX
logging.info("="*80)  # ✅ FIX

# ✅ ADD: HUD notification when mod loads
unrealsdk.Log(f"{MOD_NAME} v{__version__} loaded!", unrealsdk.LogLevel.INFO)

debug_log(f"{MOD_NAME} v{__version__} initialized", "INFO")
```

**Changes:**
- Replace 10 `print()` calls with `logging.info()`
- Add 1 HUD notification for mod load

---

## Summary of Changes

### Statistics:
- **Total print() statements to replace:** 30+
- **Total logging.X() calls to add:** 30+
- **Total HUD notifications to add:** 11
- **Total imports to add:** 1

### Impact:
- ✅ Console output will be visible in game (when console is open)
- ✅ HUD notifications provide immediate visual feedback
- ✅ Users will see when keybinds are pressed
- ✅ Errors and warnings will be visible
- ✅ Debug mode will work as expected
- ✅ Fixes "ko thấy gì trong game" (can't see anything in game)

### Files to Modify:
- `__init__.py` - All changes in this file

### Testing Checklist:
- [ ] Mod loads without errors
- [ ] Press `~` key to open console - verify messages appear
- [ ] Press NumPad7 - verify console shows message AND HUD shows notification
- [ ] Press NumPad8 - verify console shows progress AND HUD shows notification
- [ ] Toggle debug mode - verify HUD notification appears
- [ ] Change sort method - verify HUD notification appears
- [ ] Check debug.log file - verify file logging still works
- [ ] Test with console closed - verify HUD notifications still visible

---

## Alternative: Simpler Approach (If unrealsdk.Log Doesn't Work)

If `unrealsdk.Log()` is not available or doesn't work for HUD notifications, we can still improve visibility by:

1. Using `logging.info()` for all console output (Fix #1-9)
2. Adding ShowHUD notifications using game-specific functions (requires research)
3. At minimum, console output will work when console is open

The most important fix is replacing `print()` with `logging.X()` - this alone will make debug output visible.

---

## Implementation Order:

1. **First:** Add import (Fix #1)
2. **Second:** Update debug_log function (Fix #2)
3. **Third:** Update all other functions (Fix #3-9)
4. **Fourth:** Test in game
5. **Fifth:** Adjust HUD notifications based on testing

---

**STATUS: READY TO IMPLEMENT - AWAITING USER APPROVAL**
