# BankSort - Borderlands 3 Bank Research & Sorting Mod

![Version](https://img.shields.io/badge/version-0.7.1-blue)
![BL3](https://img.shields.io/badge/Borderlands_3-Compatible-green)
![Python](https://img.shields.io/badge/python-3.x-blue)

A Borderlands 3 mod for researching and sorting bank inventory, with comprehensive data scanning inspired by [apocalyptech/bl3data](https://github.com/apocalyptech/bl3data).

> 📝 **Latest Update**: Enhanced item data extraction with diagnostic mode and Vietnamese language support. See [FIX_ITEM_EXTRACTION_VI.md](FIX_ITEM_EXTRACTION_VI.md) for details.

## 🎯 Features

### Current (v0.7.1)
- ✅ **Item Information Extraction** - Automatically extract item properties
- ✅ **Sorting Logic Implementation** - Sort by rarity, type, name, level
- ✅ **Enhanced Bank Structure Scanning** - Comprehensive object introspection
- ✅ **Categorized Data Analysis** - Inventory, Bank, Items, Balance, Serial data
- ✅ **Multiple Output Formats** - Text, JSON, and focused summaries
- ✅ **Debug Logging System** - Detailed operation tracking
- ✅ **Sort Method Selection** - UI for choosing sort algorithm
- ✅ **Easy-to-Use Keybinds** - NumPad7 for sort, NumPad8 for research

### Coming Soon
- 🔄 **Physical Item Reordering** - Apply sorted order to actual bank (requires API discovery)
- 🎯 **Item Filtering** - Filter by rarity, type, level
- ⚖️ **Balance Data Analysis** - Deep item stat inspection

## 🚀 Quick Start

### Installation
1. Install [Oak Mod Manager](https://github.com/bl-sdk/oak-mod-manager) or SDK
2. Place `__init__.py` in your BL3 mods folder
3. Launch Borderlands 3

### Basic Usage
1. Open console with tilde (~) key (press twice)
2. Open your bank in-game
3. Press **NumPad8** to scan bank structure
4. Check output files in mod folder:
   - `mod_data_summary.txt` - Quick overview ⭐ Start here!
   - `bank_structure_dump.txt` - Full detailed dump
   - `bank_structure_dump.json` - Structured data

### Sort Bank
1. Press **NumPad7** OR
2. Use mod menu → "Sort Bank Now"
3. View sorted results in console

> ⚠️ **Note**: Sorting logic is implemented and shows results in console. Physical reordering in game requires additional API discovery through scanning.

## 📖 Documentation

### For Users
- **[Quick Start (v0.7.0)](QUICK_START_V070.md)** - Get started quickly
- **[README (Vietnamese)](README_VI.md)** - Hướng dẫn tiếng Việt
- **[Quick Start (v0.6)](QUICK_START.md)** - Previous version guide

### For Developers
- **[BL3Data Enhancements](BL3DATA_ENHANCEMENTS.md)** - Technical details on bl3data-inspired features
- **[Implementation Summary](IMPLEMENTATION_SUMMARY_V070.md)** - What was implemented and why
- **[Debug Guide](DEBUG_GUIDE.md)** - Debugging and troubleshooting

## 🔍 What's New in v0.7.0?

### Enhanced Scanning (bl3data-inspired)
Drawing from [apocalyptech/bl3data](https://github.com/apocalyptech/bl3data)'s proven data extraction techniques:

- **19+ Classes Scanned** (vs 7 previously)
- **Categorized Findings** - Automatic sorting into relevant categories
- **Serial Number Data** - Item identification and tracking
- **Optimized Performance** - Single-pass categorization
- **Better Output** - New summary file for quick reference

### Why bl3data?
bl3data is the gold standard for Borderlands 3 data extraction and modding. By applying its techniques to runtime object introspection, we get:
- Comprehensive API discovery
- Structured, analyzable data
- Foundation for actual implementation

See [BL3DATA_ENHANCEMENTS.md](BL3DATA_ENHANCEMENTS.md) for details.

## 🎮 Keybinds

| Key | Function | Description |
|-----|----------|-------------|
| **NumPad7** | Sort Bank | Trigger sort with selected method |
| **NumPad8** | Research | Dump bank structure to files |

## ⚙️ Mod Options

Access via in-game mod menu → "Bank Research":

- **🐛 Enable Debug Mode** - Detailed logging on/off
- **🔄 Sort Method** - Choose: Boividevngu, Rarity, Type, Name, Level
- **🔄 Sort Bank Now** - Button to trigger sort
- **🔍 Dump Bank Structure** - Button to run research

## 📁 Output Files

Generated in mod directory:

| File | Purpose | When |
|------|---------|------|
| `mod_data_summary.txt` | Quick categorized overview | NumPad8 |
| `bank_structure_dump.txt` | Full human-readable dump | NumPad8 |
| `bank_structure_dump.json` | Machine-readable data | NumPad8 |
| `debug.log` | Debug messages | Always (errors) or when debug mode on |

## 🛠️ Development Status

### Phase 1: Research & Discovery ✅ (Current)
- ✅ Enhanced scanning with bl3data techniques
- ✅ Comprehensive data categorization
- ✅ Multiple output formats
- ✅ Optimized performance

### Phase 2: Testing 🔄 (Next)
- In-game testing with various bank configurations
- API method discovery and validation
- Performance analysis

### Phase 3: Implementation 📋 (Future)
- Actual sorting logic
- Item manipulation
- Additional features

### Phase 4: Polish 📋 (Future)
- Error handling
- UI improvements
- Performance optimization

## 🔗 Related Projects

- **[bl3data](https://github.com/apocalyptech/bl3data)** - Inspiration for our scanning approach
- **[Oak Mod Manager](https://github.com/bl-sdk/oak-mod-manager)** - Required for running mods
- **[bl3-cli-saveedit](https://github.com/apocalyptech/bl3-cli-saveedit)** - Save editing tool

## 🤝 Contributing

Feedback and contributions welcome! Particularly:
- In-game testing results
- API discovery findings
- Documentation improvements

## 📝 Version History

- **v0.7.1** (2024-01) - Sorting logic implementation
  - Item information extraction
  - Sorting algorithms for all methods
  - Console output of sorted results
  - Ready for physical reordering API discovery

- **v0.7.0** (2024-01) - Enhanced scanning with bl3data techniques
  - 19+ classes scanned
  - Categorized data analysis
  - New summary output
  - Performance optimization

- **v0.6.2** (2023) - Keybind improvements and debug enhancements
  - NumPad keybinds
  - Enhanced debug logging
  - Sort method selection

- **v0.5.x** - Initial research version
  - Basic bank structure dumping
  - Debug mechanism

## 📄 License

See repository license file.

## 🙏 Credits

- **apocalyptech** - For bl3data toolkit that inspired v0.7.0 enhancements
- **BL3 Modding Community** - For documentation and support
- **Oak SDK Team** - For the modding framework

---

**Current Version**: 0.7.1  
**Status**: ✅ Sorting logic complete, physical reordering requires API discovery  
**Compatibility**: Borderlands 3 with Oak Mod Manager

For questions or issues, please open a GitHub issue.
