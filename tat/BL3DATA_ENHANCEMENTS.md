# BL3Data-Inspired Enhancements - v0.7.0

## Overview

Version 0.7.0 enhances BankSort with comprehensive data scanning techniques inspired by the [apocalyptech/bl3data](https://github.com/apocalyptech/bl3data) repository, which is a well-established toolkit for Borderlands 3 modding and data extraction.

## What is bl3data?

The bl3data repository provides utilities for:
- Extracting and processing game data from Borderlands 3
- Deep inspection of game objects and structures
- Understanding item serialization and inventory systems
- Supporting mod development with comprehensive data analysis

## Enhancements Applied

### 1. Expanded Class Scanning

**Previous approach:**
- Scanned only 7 basic bank/inventory class names
- Limited to obvious inventory-related classes

**New approach (bl3data-inspired):**
- Expanded to 11 bank/inventory class names
- Added 9 additional mod-related classes for comprehensive scanning
- Includes balance, serialization, and item pool classes

```python
# New classes added for comprehensive scanning
MOD_RELATED_CLASSES = [
    "OakPlayerController",
    "OakCharacter_Player", 
    "OakPlayerPawn",
    "InventoryBalanceStateComponent",
    "InventorySerialNumberDatabase",
    "ItemPoolData",
    "InventoryGenericPartData",
    "WeaponBalanceStateComponent",
    "InventoryData"
]
```

### 2. Categorized Data Scanning

Implemented `scan_for_mod_data()` function that categorizes findings into:
- **Inventory-related**: Attributes dealing with inventory slots and items
- **Bank-related**: Storage, vault, and bank-specific data
- **Item-related**: Weapons, gear, and equipment information
- **Balance-related**: Item stats, parts, and balance data (crucial for understanding items)
- **Serial-related**: Item identification and serialization data

This categorization makes it easier to identify which attributes are most relevant for mod development.

### 3. Inventory Serial Number Scanning

Added dedicated scanning for serial number data, inspired by bl3data's `inv_serial_crypt.py`:
- Searches for serial, GUID, and ID-related attributes
- Important for understanding item structure
- Essential for future item manipulation features

### 4. Enhanced Output Files

**New file: `mod_data_summary.txt`**
- Focused summary of mod-relevant data
- Categorized findings for quick reference
- Easier to parse than full dumps
- Follows bl3data's approach of creating focused, readable outputs

### 5. Comprehensive JSON Data

Enhanced JSON output now includes:
- `mod_scan_findings`: Categorized data from all scanned classes
- `serial_data_findings`: Serial number and ID-related data
- Structured for programmatic analysis (like bl3data's data processing scripts)

## How to Use the Enhancements

### Step 1: Run Enhanced Research
1. Load Borderlands 3 with the mod
2. Open the Bank (if testing bank-specific features)
3. Press **NumPad8** to run enhanced research

### Step 2: Review Output Files

**Quick Overview:**
```
mod_data_summary.txt - Start here! Contains categorized summary
```

**Detailed Analysis:**
```
bank_structure_dump.txt - Human-readable full dump
bank_structure_dump.json - Machine-readable structured data
```

**Debugging:**
```
debug.log - Detailed operation logs (when debug mode enabled)
```

### Step 3: Analyze Findings

Look for:
- **Methods with "Get" or "Set"** in inventory/bank categories → Potential ways to read/modify items
- **Balance-related attributes** → Understanding item stats and properties
- **Serial-related data** → Item identification for sorting/filtering
- **Item pools and spawns** → Understanding where items come from

## Comparison with bl3data Approach

| Aspect | bl3data | BankSort v0.7.0 |
|--------|---------|-----------------|
| **Data Source** | PAK file extraction | Live game object introspection |
| **Scope** | All game data | Runtime objects and attributes |
| **Format** | Multiple specialized scripts | Single integrated mod |
| **Use Case** | Offline data analysis | In-game debugging and development |
| **Output** | Extracted game files | JSON + Text dumps |

## Benefits for Mod Development

### 1. Understanding Item Structure
The categorized scanning helps identify:
- How items are stored in the bank
- What attributes control item properties
- How to access item lists

### 2. Finding Useful APIs
By scanning multiple related classes, you can discover:
- Methods to get/set inventory items
- Balance components that affect item stats
- Serial number data for item identification

### 3. Debugging Made Easier
The summary file provides quick answers to:
- "Which class has bank-related methods?"
- "Where can I find item serial numbers?"
- "What balance data is available?"

### 4. Future Feature Development
This groundwork enables:
- Actual sorting implementation (finding methods to reorder items)
- Item filtering (using serial and balance data)
- Custom item manipulation (understanding the full structure)

## Next Steps for Implementation

Based on bl3data's methodology, here's how to proceed with actual sorting:

### Phase 1: Identify Item Access Methods ✓ (Current)
- ✓ Comprehensive class scanning
- ✓ Categorized attribute findings
- ✓ Serial number data identification

### Phase 2: Test Item Access (Next)
1. Review `mod_data_summary.txt` for promising methods
2. Test calling Get methods on inventory/bank objects
3. Verify we can retrieve item lists
4. Document working methods

### Phase 3: Implement Sorting
1. Extract item list from bank
2. Sort based on selected method (rarity, type, etc.)
3. Use Set methods to reorder items
4. Test in-game

### Phase 4: Polish and Test
1. Add error handling
2. Test with various bank sizes
3. Validate all sort methods
4. Performance optimization

## References

- **bl3data repository**: https://github.com/apocalyptech/bl3data
- **bl3data README**: Explains data extraction philosophy
- **inv_serial_crypt.py**: Inspired our serial number scanning
- **objectPropertyGenerator.py**: Similar object introspection approach

## Technical Notes

### Why This Approach Works

Like bl3data's utilities, our enhanced scanning:
1. **Doesn't assume structure**: Discovers what's actually available
2. **Categorizes findings**: Makes patterns easier to spot
3. **Provides multiple views**: Summary + detailed dumps
4. **Documents automatically**: Each scan generates fresh documentation

### Compatibility

- Works with any Borderlands 3 version (discovers available classes dynamically)
- Safe to run repeatedly (read-only operations)
- No game modifications (pure introspection)

## Version History

- **v0.7.0** (Current): bl3data-inspired comprehensive scanning
  - Added MOD_RELATED_CLASSES scanning
  - Implemented categorized data scanning
  - Added serial number data scanning
  - Created mod_data_summary.txt output
  - Enhanced JSON with structured findings

- **v0.6.2** (Previous): Basic bank structure dumping
  - Simple class scanning
  - Basic attribute listing
  - Text and JSON output

## Credits

- **apocalyptech**: For the excellent bl3data toolkit that inspired these enhancements
- **BL3 Modding Community**: For documentation and support
- Original BankSort mod developers

## Conclusion

By applying bl3data's proven data extraction and analysis techniques to live game object introspection, BankSort v0.7.0 provides a powerful foundation for understanding and eventually manipulating Borderlands 3's inventory and bank systems.

The enhanced scanning will reveal the actual APIs available at runtime, making it possible to implement real sorting functionality based on discovered methods rather than assumptions.

---

**Happy Modding! 🎮**
