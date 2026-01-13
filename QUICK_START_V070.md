# Quick Start Guide - v0.7.0 Enhanced Scanning

## What's New in v0.7.0? 🎉

BankSort now includes comprehensive scanning inspired by [apocalyptech/bl3data](https://github.com/apocalyptech/bl3data)!

### New Features:
- ✅ Scans 20+ game classes (vs 7 previously)
- ✅ Categorizes findings (inventory, bank, items, balance, serial data)
- ✅ Creates focused summary file for quick reference
- ✅ Enhanced JSON output with structured data

## How to Use (3 Easy Steps)

### Step 1: Run the Scan
1. Load Borderlands 3
2. (Optional) Open the Bank 
3. Press **NumPad8** OR use mod menu → "Dump Bank Structure"

### Step 2: Check the Summary File
Open: `mod_data_summary.txt` in your mod folder

This file shows you:
- Which classes were found
- How many inventory/bank/item attributes each has
- Quick overview of what's available

### Step 3: Deep Dive (If Needed)
For detailed analysis, check:
- `bank_structure_dump.txt` - Full human-readable dump
- `bank_structure_dump.json` - Machine-readable structured data
- `debug.log` - Debug info (if debug mode enabled)

## What to Look For

### For Implementing Sorting:
Look for methods like:
```
GetInventoryList()
SetInventoryOrder()
GetItemArray()
ReorderItems()
```

### For Understanding Items:
Look for attributes like:
```
BalanceData
ItemSerial
WeaponType
Rarity
Level
```

### For Bank Access:
Look for:
```
BankStorage
VaultItems
StorageComponent
```

## Example Output

```
MOD-RELATED CLASSES FOUND:
OakPlayerController:
  Inventory attributes: 5
  Bank attributes: 2
  Item attributes: 8
  Balance attributes: 3
  Serial attributes: 1
  Total methods: 45
  Total properties: 23
```

## Comparison with Previous Version

| Feature | v0.6.2 | v0.7.0 |
|---------|--------|--------|
| Classes scanned | 7 | 20+ |
| Categorization | ❌ | ✅ |
| Summary file | ❌ | ✅ |
| Serial data scan | ❌ | ✅ |
| bl3data techniques | ❌ | ✅ |

## Tips

### 💡 Tip 1: Start with the Summary
Don't overwhelm yourself with the full dump. Start with `mod_data_summary.txt` to get oriented.

### 💡 Tip 2: Enable Debug Mode
Before running the scan, enable debug mode in mod options for detailed logs.

### 💡 Tip 3: Run at Different Times
Try scanning:
- At main menu (to see base objects)
- With bank open (to see active bank objects)
- With inventory open (to see inventory objects)

### 💡 Tip 4: Search the Output
The text dumps are searchable! Use Ctrl+F to find:
- "Get" methods (for reading data)
- "Set" methods (for modifying data)
- Specific keywords like "rarity", "level", etc.

## Understanding the Categories

### 🎒 Inventory-Related
Attributes/methods dealing with player inventory system. Look here for general inventory access.

### 🏦 Bank-Related
Specific to bank storage. This is where you'll find bank-specific APIs.

### 🎯 Item-Related
Individual items (weapons, gear, etc.). Understanding this helps with item manipulation.

### ⚖️ Balance-Related
Item stats, parts, and balance data. Critical for understanding item properties.

### 🔢 Serial-Related
Item IDs and serial numbers. Useful for item identification and tracking.

## Troubleshooting

### No Output Files?
- Check mod directory permissions
- Enable debug mode and check debug.log
- Make sure you pressed NumPad8 (not the number row)

### Found 0 Objects?
This is sometimes normal! Try:
- Opening the bank before scanning
- Scanning at different game states
- Checking if you're in-game (not main menu)

### Too Much Information?
- Start with `mod_data_summary.txt` only
- Ignore classes with 0 attributes
- Focus on classes with inventory/bank attributes

## Next Steps

After reviewing the scan results:
1. Identify promising classes (ones with many inventory/bank attributes)
2. Note methods that look useful (especially Get/Set methods)
3. Plan to test calling those methods
4. Eventually implement actual sorting based on discovered APIs

## Need Help?

- Check `BL3DATA_ENHANCEMENTS.md` for technical details
- Check `README_VI.md` for Vietnamese documentation
- Enable debug mode and share debug.log when reporting issues

---

**Version:** 0.7.0  
**Based on:** [apocalyptech/bl3data](https://github.com/apocalyptech/bl3data) techniques  
**Status:** ✅ Ready to test in-game
