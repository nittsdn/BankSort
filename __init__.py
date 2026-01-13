"""
BankResearch - Phase 0.7: Enhanced Bank Structure Discovery
Dumps Bank and Inventory structures to understand the API

Version 0.7.0: Enhanced with comprehensive scanning inspired by apocalyptech/bl3data
- Added MOD_RELATED_CLASSES scanning for comprehensive data extraction
- Enhanced object introspection with categorized findings
- Added inventory serial number data scanning
- Improved mod data summary output for easier analysis
"""

if True:
    assert __import__("mods_base").__version_info__ >= (1, 0), "Please update the SDK"

import unrealsdk
from unrealsdk import logging
from mods_base import build_mod, hook, get_pc
from mods_base.options import ButtonOption, GroupedOption, BoolOption, SpinnerOption
from mods_base.keybinds import keybind
from unrealsdk.hooks import Type
from unrealsdk.unreal import UObject, WrappedStruct, BoundFunction
from typing import Any
import os
import json
from datetime import datetime

__version__: str = "0.7.0"
# Parse version info from version string to keep them in sync
__version_info__: tuple[int, ...] = tuple(int(x) for x in __version__.split('.'))

# ==================== CONSTANTS ====================

MOD_NAME = "BankResearch"
OUTPUT_FILE = "bank_structure_dump.txt"
JSON_FILE = "bank_structure_dump.json"
SUMMARY_FILE = "mod_data_summary.txt"

# Possible class names for bank/inventory objects in Borderlands 3
# The actual class name may vary by game version, so we try multiple options
# Expanded based on bl3data research patterns
# Note: OakInventoryItemPickup is removed - it's for ground item pickups, not bank
BANK_CLASS_NAMES = [
    "BankInventory",
    "OakInventory", 
    "OakBank",
    "InventoryComponent",
    "BankComponent",
    "OakStorageComponent",
    "OakInventoryBalanceStateComponent",
    "OakInventoryCustomizationPartInfo",
    "InventoryBalanceData"
]

# Additional class names for comprehensive mod data scanning
# Based on bl3data's approach to data extraction
# Note: Some classes may overlap with BANK_CLASS_NAMES - this is intentional
# to ensure comprehensive scanning in different contexts
MOD_RELATED_CLASSES = [
    "OakPlayerController",
    "OakCharacter_Player",
    "OakPlayerPawn",
    "InventoryBalanceStateComponent",  # Overlaps with BANK_CLASS_NAMES - intentional
    "InventorySerialNumberDatabase",
    "ItemPoolData",
    "InventoryGenericPartData",
    "WeaponBalanceStateComponent",
    "InventoryData"  # Overlaps with BANK_CLASS_NAMES - intentional
]

# ==================== DEBUG SETTINGS ====================

DEBUG_ENABLED = False  # Will be controlled by options

# ==================== UTILITY FUNCTIONS ====================

def debug_log(message: str, level: str = "INFO") -> None:
    """
    Debug logging function using SDK logging for console output.
    Uses logging.info() for INFO, logging.warning() for WARNING,
    logging.error() for ERROR, and logging.dev_warning() for DEBUG.
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
    
    # Use SDK logging for console output (visible in game)
    if level in ["ERROR", "WARNING"] or DEBUG_ENABLED:
        if level == "ERROR":
            logging.error(formatted_msg)
        elif level == "WARNING":
            logging.warning(formatted_msg)
        elif level == "DEBUG":
            logging.dev_warning(formatted_msg)
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
            logging.error(f"[{MOD_NAME}] Failed to write to debug log: {e}")

def get_mod_directory() -> str:
    """Get the mod directory path"""
    return os.path.dirname(os.path.abspath(__file__))

def safe_str(obj: Any) -> str:
    """Safely convert object to string"""
    try:
        return str(obj)
    except Exception as e:
        return f"<Error converting to string: {e}>"

def safe_repr(obj: Any) -> str:
    """Safely get repr of object"""
    try: 
        return repr(obj)
    except Exception as e:
        return f"<Error getting repr: {e}>"

def safe_type(obj: Any) -> str:
    """Safely get type of object"""
    try: 
        return str(type(obj))
    except Exception as e:
        return f"<Error getting type: {e}>"

def scan_for_mod_data(obj: Any, name: str) -> dict:
    """
    Scan an object for mod-relevant data.
    Inspired by bl3data's comprehensive data extraction approach.
    
    Args:
        obj: The object to scan
        name: Name/identifier for the object
        
    Returns:
        Dictionary with categorized findings
    """
    findings = {
        "name": name,
        "type": safe_type(obj),
        "inventory_related": [],
        "bank_related": [],
        "item_related": [],
        "balance_related": [],
        "serial_related": [],
        "methods": [],
        "properties": []
    }
    
    # Define category keywords mapping (optimized single-pass categorization)
    category_keywords = {
        "inventory_related": ['inventory', 'invslot', 'invitem'],
        "bank_related": ['bank', 'storage', 'vault', 'stash'],
        "item_related": ['item', 'weapon', 'gear', 'equipment'],
        "balance_related": ['balance', 'part', 'generic'],
        "serial_related": ['serial', 'guid', 'id', 'uuid']
    }
    
    try:
        attrs = dir(obj)
        
        for attr in attrs:
            # Skip private attributes
            if attr.startswith('_'):
                continue
                
            try:
                value = getattr(obj, attr, None)
                is_callable = callable(value)
                value_type = safe_type(value)
                attr_lower = attr.lower()
                
                # Single-pass categorization using the mapping
                for category, keywords in category_keywords.items():
                    if any(kw in attr_lower for kw in keywords):
                        findings[category].append({
                            "name": attr,
                            "type": value_type,
                            "callable": is_callable
                        })
                
                # Collect all methods and properties
                if is_callable:
                    findings["methods"].append(attr)
                else:
                    findings["properties"].append(attr)
                    
            except Exception as e:
                debug_log(f"Error scanning attribute {attr}: {e}", "DEBUG")
                
    except Exception as e:
        debug_log(f"Error scanning object {name}: {e}", "ERROR")
    
    return findings

# ==================== DUMP FUNCTIONS ====================

def dump_object_recursive(obj: Any, name: str, depth: int = 0, max_depth: int = 3) -> list:
    """Recursively dump object structure"""
    debug_log(f"dump_object_recursive called: name={name}, depth={depth}, max_depth={max_depth}", "DEBUG")
    
    lines = []
    indent = "  " * depth
    
    if depth > max_depth:
        lines.append(f"{indent}[Max depth reached]")
        debug_log(f"Max depth reached for {name}", "DEBUG")
        return lines
    
    # Basic info
    lines.append(f"{indent}{'='*60}")
    lines.append(f"{indent}Name: {name}")
    lines.append(f"{indent}Type: {safe_type(obj)}")
    lines.append(f"{indent}Value: {safe_str(obj)}")
    lines.append(f"{indent}{'='*60}")
    
    # Try to get attributes
    try: 
        attrs = dir(obj)
        lines.append(f"{indent}Attributes ({len(attrs)}):")
        
        for attr in attrs:
            # Skip private/magic attributes for now
            if attr.startswith('_'):
                continue
                
            try:
                value = getattr(obj, attr, '<No Value>')
                value_type = safe_type(value)
                value_str = safe_str(value)[:100]  # Truncate long strings
                
                lines.append(f"{indent}  - {attr}:  {value_type} = {value_str}")
                
                # If it's related to inventory/bank, dig deeper
                if any(keyword in attr.lower() for keyword in ['inventory', 'bank', 'item', 'equipment']):
                    lines.append(f"{indent}    ↳ [IMPORTANT] Digging deeper...")
                    if depth < max_depth and not callable(value):
                        sub_lines = dump_object_recursive(value, attr, depth + 1, max_depth)
                        lines.extend(sub_lines)
                        
            except Exception as e: 
                lines.append(f"{indent}  - {attr}: <Error: {e}>")
    except Exception as e:
        lines.append(f"{indent}Error getting attributes: {e}")
    
    return lines

def dump_player_controller() -> dict:
    """Dump PlayerController structure focusing on Bank/Inventory"""
    debug_log("Starting dump_player_controller", "INFO")
    
    result = {
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "success": False,
        "error":  None,
        "pc_found": False,
        "pc_attributes": [],
        "bank_related": {},
        "inventory_related": {},
        "all_text": []
    }
    
    lines = []
    lines.append("="*80)
    lines.append(f"BANK RESEARCH - Structure Dump")
    lines.append(f"Timestamp: {result['timestamp']}")
    lines.append("="*80)
    lines.append("")
    
    try:
        # Get PlayerController
        debug_log("Attempting to get PlayerController", "DEBUG")
        pc = get_pc()
        
        if not pc: 
            lines.append("❌ ERROR: PlayerController not found!")
            lines.append("This usually means you're not in-game yet.")
            result["error"] = "PlayerController not found"
            result["all_text"] = lines
            debug_log("PlayerController not found", "WARNING")
            return result
        
        debug_log(f"PlayerController found: {safe_type(pc)}", "INFO")
        result["pc_found"] = True
        lines.append("✅ PlayerController found!")
        lines.append(f"Type: {safe_type(pc)}")
        lines.append(f"Value: {safe_str(pc)}")
        lines.append("")
        
        # Get all attributes
        debug_log("Getting PlayerController attributes", "DEBUG")
        lines.append("="*80)
        lines.append("ALL PLAYERCONTROLLER ATTRIBUTES")
        lines.append("="*80)
        
        pc_attrs = dir(pc)
        result["pc_attributes"] = pc_attrs
        debug_log(f"Found {len(pc_attrs)} attributes", "DEBUG")
        
        for attr in pc_attrs:
            try:
                value = getattr(pc, attr, None)
                attr_type = safe_type(value)
                is_callable = callable(value)
                
                # Mark important ones
                importance = ""
                if any(kw in attr.lower() for kw in ['bank', 'inventory', 'item', 'equipment', 'storage']):
                    importance = " ⭐ IMPORTANT"
                
                lines.append(f"  {attr}: {attr_type} {'(callable)' if is_callable else ''}{importance}")
                
            except Exception as e:
                lines.append(f"  {attr}: <Error: {e}>")
        
        lines.append("")
        
        # Focus on Bank-related attributes
        debug_log("Searching for Bank-related attributes", "DEBUG")
        lines.append("="*80)
        lines.append("🎯 BANK-RELATED ATTRIBUTES (Deep Dive)")
        lines.append("="*80)
        lines.append("")
        
        bank_keywords = ['bank', 'storage', 'vault']
        bank_found_count = 0
        for attr in pc_attrs:
            if any(kw in attr.lower() for kw in bank_keywords):
                bank_found_count += 1
                lines.append(f"Found Bank-related: {attr}")
                debug_log(f"Processing bank attribute: {attr}", "DEBUG")
                try:
                    value = getattr(pc, attr, None)
                    if value is not None and not callable(value):
                        dump_lines = dump_object_recursive(value, attr, depth=0, max_depth=4)
                        lines.extend(dump_lines)
                        result["bank_related"][attr] = safe_str(value)
                    else:
                        lines.append(f"  Type: {safe_type(value)}")
                        lines.append(f"  Callable: {callable(value)}")
                except Exception as e:
                    lines.append(f"  Error accessing {attr}: {e}")
                    debug_log(f"Error accessing {attr}: {e}", "ERROR")
                lines.append("")
        
        debug_log(f"Found {bank_found_count} bank-related attributes", "INFO")
        
        # Focus on Inventory-related attributes
        debug_log("Searching for Inventory-related attributes", "DEBUG")
        lines.append("="*80)
        lines.append("📦 INVENTORY-RELATED ATTRIBUTES (Deep Dive)")
        lines.append("="*80)
        lines.append("")
        
        inventory_keywords = ['inventory', 'item', 'equipment']
        inventory_found_count = 0
        for attr in pc_attrs: 
            if any(kw in attr.lower() for kw in inventory_keywords):
                inventory_found_count += 1
                lines.append(f"Found Inventory-related: {attr}")
                debug_log(f"Processing inventory attribute: {attr}", "DEBUG")
                try:
                    value = getattr(pc, attr, None)
                    if value is not None and not callable(value):
                        dump_lines = dump_object_recursive(value, attr, depth=0, max_depth=4)
                        lines.extend(dump_lines)
                        result["inventory_related"][attr] = safe_str(value)
                    else:
                        lines.append(f"  Type: {safe_type(value)}")
                        lines.append(f"  Callable: {callable(value)}")
                except Exception as e: 
                    lines.append(f"  Error accessing {attr}: {e}")
                    debug_log(f"Error accessing {attr}: {e}", "ERROR")
                lines.append("")
        
        debug_log(f"Found {inventory_found_count} inventory-related attributes", "INFO")
        
        # Scan for mod-related classes (bl3data approach)
        debug_log("Scanning for mod-related classes", "INFO")
        lines.append("="*80)
        lines.append("🔍 MOD-RELATED CLASS SCANNING (bl3data approach)")
        lines.append("="*80)
        lines.append("")
        lines.append("Scanning for classes that may contain useful mod data...")
        lines.append("")
        
        mod_data_findings = {}
        for class_name in MOD_RELATED_CLASSES:
            try:
                lines.append(f"Scanning: {class_name}")
                debug_log(f"Scanning class: {class_name}", "DEBUG")
                objects = unrealsdk.find_all(class_name)
                
                if objects:
                    lines.append(f"  ✅ Found {len(objects)} {class_name} objects")
                    debug_log(f"Found {len(objects)} {class_name} objects", "INFO")
                    
                    # Scan first object for mod-related data
                    if len(objects) > 0:
                        obj = objects[0]
                        findings = scan_for_mod_data(obj, class_name)
                        mod_data_findings[class_name] = findings
                        
                        # Report findings
                        if findings["inventory_related"]:
                            lines.append(f"    📦 Inventory attrs: {len(findings['inventory_related'])}")
                            for item in findings["inventory_related"][:3]:  # Show first 3
                                lines.append(f"      - {item['name']} ({item['type']})")
                        
                        if findings["bank_related"]:
                            lines.append(f"    🏦 Bank attrs: {len(findings['bank_related'])}")
                            for item in findings["bank_related"][:3]:
                                lines.append(f"      - {item['name']} ({item['type']})")
                        
                        if findings["item_related"]:
                            lines.append(f"    🎯 Item attrs: {len(findings['item_related'])}")
                            for item in findings["item_related"][:3]:
                                lines.append(f"      - {item['name']} ({item['type']})")
                        
                        if findings["balance_related"]:
                            lines.append(f"    ⚖️ Balance attrs: {len(findings['balance_related'])}")
                            for item in findings["balance_related"][:3]:
                                lines.append(f"      - {item['name']} ({item['type']})")
                        
                        if findings["serial_related"]:
                            lines.append(f"    🔢 Serial attrs: {len(findings['serial_related'])}")
                            for item in findings["serial_related"][:3]:
                                lines.append(f"      - {item['name']} ({item['type']})")
                        
                        lines.append(f"    📋 Total methods: {len(findings['methods'])}")
                        lines.append(f"    📋 Total properties: {len(findings['properties'])}")
                else:
                    lines.append(f"  ❌ No objects found")
                    debug_log(f"No {class_name} objects found", "DEBUG")
            except Exception as e:
                lines.append(f"  ⚠️ Error scanning: {e}")
                debug_log(f"Error scanning {class_name}: {e}", "DEBUG")
            lines.append("")
        
        # Store mod scan results
        result["mod_scan_findings"] = mod_data_findings
        
        # Check Pawn's inventory
        debug_log("Checking Pawn inventory", "DEBUG")
        lines.append("="*80)
        lines.append("🧍 PAWN INVENTORY CHECK")
        lines.append("="*80)
        lines.append("")
        
        if hasattr(pc, 'Pawn') and pc.Pawn:
            pawn = pc.Pawn
            lines.append(f"✅ Pawn found: {safe_str(pawn)}")
            lines.append(f"Pawn type: {safe_type(pawn)}")
            lines.append("")
            debug_log(f"Pawn found: {safe_type(pawn)}", "DEBUG")
            
            pawn_attrs = dir(pawn)
            pawn_found_count = 0
            for attr in pawn_attrs:
                if any(kw in attr.lower() for kw in ['inventory', 'item', 'equipment', 'bank']):
                    pawn_found_count += 1
                    lines.append(f"Pawn.{attr}:")
                    debug_log(f"Processing pawn attribute: {attr}", "DEBUG")
                    try:
                        value = getattr(pawn, attr, None)
                        dump_lines = dump_object_recursive(value, f"Pawn.{attr}", depth=0, max_depth=3)
                        lines.extend(dump_lines)
                    except Exception as e:
                        lines.append(f"  Error: {e}")
                        debug_log(f"Error accessing Pawn.{attr}: {e}", "ERROR")
                    lines.append("")
            debug_log(f"Found {pawn_found_count} pawn attributes", "DEBUG")
        else:
            lines.append("❌ No Pawn found")
            debug_log("No Pawn found", "WARNING")
        
        # Try to find Bank objects using unrealsdk. find_all
        debug_log("Searching for Bank objects with find_all()", "DEBUG")
        lines.append("="*80)
        lines.append("🔍 SEARCHING FOR BANK OBJECTS WITH find_all()")
        lines.append("="*80)
        lines.append("")
        
        for class_name in BANK_CLASS_NAMES: 
            try:
                lines.append(f"Searching for: {class_name}")
                debug_log(f"Searching for class: {class_name}", "DEBUG")
                objects = unrealsdk.find_all(class_name)
                
                if objects:
                    lines.append(f"  ✅ Found {len(objects)} objects!")
                    debug_log(f"Found {len(objects)} {class_name} objects", "INFO")
                    for i, obj in enumerate(objects[:3]):  # Only show first 3
                        lines.append(f"  Object {i+1}:")
                        lines.append(f"    Type: {safe_type(obj)}")
                        lines.append(f"    Str: {safe_str(obj)[:200]}")
                        
                        # Dump its structure
                        dump_lines = dump_object_recursive(obj, f"{class_name}[{i}]", depth=0, max_depth=2)
                        lines.extend(dump_lines)
                else:
                    lines.append(f"  ❌ No objects found")
                    debug_log(f"No {class_name} objects found", "DEBUG")
            except Exception as e:
                lines.append(f"  ⚠️ Error searching: {e}")
                debug_log(f"Error searching {class_name}: {e}", "ERROR")
            lines.append("")
        
        # Additional scan: Look for inventory serial data (bl3data approach)
        debug_log("Scanning for inventory serial data", "INFO")
        lines.append("="*80)
        lines.append("🔢 INVENTORY SERIAL NUMBER DATA SCAN")
        lines.append("="*80)
        lines.append("")
        lines.append("Looking for item serial number and identification data...")
        lines.append("(Useful for understanding item structure and manipulation)")
        lines.append("")
        
        serial_keywords = ['serial', 'guid', 'itemid', 'inventoryid']
        serial_findings = {}
        
        # Scan PlayerController for serial-related attributes
        for attr in pc_attrs:
            attr_lower = attr.lower()
            if any(kw in attr_lower for kw in serial_keywords):
                try:
                    value = getattr(pc, attr, None)
                    serial_findings[attr] = {
                        "type": safe_type(value),
                        "callable": callable(value),
                        "value_preview": safe_str(value)[:100]
                    }
                    lines.append(f"PC.{attr}:")
                    lines.append(f"  Type: {safe_type(value)}")
                    lines.append(f"  Callable: {callable(value)}")
                    if not callable(value):
                        lines.append(f"  Preview: {safe_str(value)[:100]}")
                except Exception as e:
                    lines.append(f"  Error: {e}")
                lines.append("")
        
        result["serial_data_findings"] = serial_findings
        
        if not serial_findings:
            lines.append("❌ No serial-related attributes found in PlayerController")
            lines.append("This is normal - serial data might be in item objects themselves")
        
        lines.append("")
        
        result["success"] = True
        debug_log("dump_player_controller completed successfully", "INFO")
        
    except Exception as e:
        import traceback
        lines.append("")
        lines.append("="*80)
        lines.append("❌ CRITICAL ERROR")
        lines.append("="*80)
        lines.append(f"Error: {e}")
        lines.append("")
        lines.append("Traceback:")
        lines.append(traceback.format_exc())
        result["error"] = str(e)
        debug_log(f"Critical error in dump_player_controller: {e}", "ERROR")
        debug_log(f"Traceback: {traceback.format_exc()}", "ERROR")
    
    result["all_text"] = lines
    return result

def save_dump_to_file(result: dict) -> None:
    """Save dump results to files"""
    debug_log("Saving dump to files", "INFO")
    
    mod_dir = get_mod_directory()
    
    # Save text file
    txt_path = os.path.join(mod_dir, OUTPUT_FILE)
    try:
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(result["all_text"]))
        logging.info(f"[{MOD_NAME}] ✅ Text dump saved to: {txt_path}")
        debug_log(f"Text dump saved to: {txt_path}", "INFO")
    except Exception as e:
        logging.error(f"[{MOD_NAME}] ❌ Error saving text file: {e}")
        debug_log(f"Error saving text file: {e}", "ERROR")
    
    # Save JSON file with enhanced mod data
    json_path = os.path.join(mod_dir, JSON_FILE)
    try:
        # Remove all_text from JSON (too large) but keep new scan data
        json_result = {
            k: v for k, v in result.items() 
            if k != 'all_text'
        }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_result, f, indent=2, default=str)
        logging.info(f"[{MOD_NAME}] ✅ JSON dump saved to: {json_path}")
        debug_log(f"JSON dump saved to: {json_path}", "INFO")
    except Exception as e:
        logging.error(f"[{MOD_NAME}] ❌ Error saving JSON file: {e}")
        debug_log(f"Error saving JSON file: {e}", "ERROR")
    
    # Save mod scan summary (new - inspired by bl3data's focused data extraction)
    summary_path = os.path.join(mod_dir, "mod_data_summary.txt")
    try:
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("MOD DATA SCAN SUMMARY\n")
            f.write("Comprehensive scan inspired by bl3data extraction techniques\n")
            f.write("="*80 + "\n\n")
            
            # Write mod scan findings
            if "mod_scan_findings" in result:
                f.write("MOD-RELATED CLASSES FOUND:\n")
                f.write("-"*80 + "\n")
                for class_name, findings in result["mod_scan_findings"].items():
                    f.write(f"\n{class_name}:\n")
                    f.write(f"  Type: {findings['type']}\n")
                    if findings["inventory_related"]:
                        f.write(f"  Inventory attributes: {len(findings['inventory_related'])}\n")
                    if findings["bank_related"]:
                        f.write(f"  Bank attributes: {len(findings['bank_related'])}\n")
                    if findings["item_related"]:
                        f.write(f"  Item attributes: {len(findings['item_related'])}\n")
                    if findings["balance_related"]:
                        f.write(f"  Balance attributes: {len(findings['balance_related'])}\n")
                    if findings["serial_related"]:
                        f.write(f"  Serial attributes: {len(findings['serial_related'])}\n")
                    f.write(f"  Total methods: {len(findings['methods'])}\n")
                    f.write(f"  Total properties: {len(findings['properties'])}\n")
                f.write("\n")
            
            # Write serial data findings
            if "serial_data_findings" in result and result["serial_data_findings"]:
                f.write("\nSERIAL NUMBER DATA FOUND:\n")
                f.write("-"*80 + "\n")
                for attr, data in result["serial_data_findings"].items():
                    f.write(f"\n{attr}:\n")
                    f.write(f"  Type: {data['type']}\n")
                    f.write(f"  Callable: {data['callable']}\n")
                    if not data['callable']:
                        f.write(f"  Preview: {data['value_preview']}\n")
                f.write("\n")
            
            f.write("\n" + "="*80 + "\n")
            f.write("For full details, see bank_structure_dump.txt and bank_structure_dump.json\n")
            f.write("="*80 + "\n")
        
        logging.info(f"[{MOD_NAME}] ✅ Mod data summary saved to: {summary_path}")
        debug_log(f"Mod data summary saved to: {summary_path}", "INFO")
    except Exception as e:
        logging.error(f"[{MOD_NAME}] ❌ Error saving mod summary: {e}")
        debug_log(f"Error saving mod summary: {e}", "ERROR")

# ==================== KEYBIND & BUTTON ====================

# ==================== BANK SORT FUNCTIONS ====================

SORT_METHODS = {
    "Boividevngu": "boividevngu",
    "By Rarity": "rarity",
    "By Type": "type",
    "By Name": "name",
    "By Level": "level"
}

CURRENT_SORT_METHOD = "Boividevngu"  # Default sort method

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
            logging.warning(f"[{MOD_NAME}] ⚠️ Please load into game first!")
            return
        
        debug_log(f"PlayerController found, attempting to sort bank using '{method}' method", "DEBUG")
        logging.info(f"[{MOD_NAME}] 🔄 Sorting bank items using '{method}' method...")
        
        # Try to find bank inventory objects - try multiple possible class names
        bank_objects = []
        found_class_name = None
        
        for class_name in BANK_CLASS_NAMES:
            try:
                debug_log(f"Trying to find class: {class_name}", "DEBUG")
                objects = unrealsdk.find_all(class_name)
                if objects:
                    bank_objects = objects
                    found_class_name = class_name
                    debug_log(f"Found {len(objects)} {class_name} objects", "INFO")
                    logging.info(f"[{MOD_NAME}] ✅ Found {len(objects)} {class_name} objects")
                    break  # Exit the for loop once we find valid objects
            except ValueError as ve:
                debug_log(f"Class {class_name} not found: {ve}", "DEBUG")
                continue
            except Exception as e:
                debug_log(f"Error searching for {class_name}: {e}", "DEBUG")
                continue
        
        if not bank_objects:
            debug_log("No bank inventory objects found with any class name", "WARNING")
            logging.warning(f"[{MOD_NAME}] ⚠️ No bank inventory found!")
            logging.warning(f"[{MOD_NAME}] ")
            logging.warning(f"[{MOD_NAME}] This mod is still in RESEARCH phase.")
            logging.warning(f"[{MOD_NAME}] Sorting is NOT yet implemented.")
            logging.warning(f"[{MOD_NAME}] ")
            logging.warning(f"[{MOD_NAME}] To help implement sorting:")
            logging.warning(f"[{MOD_NAME}]   1. Make sure you're in-game")
            logging.warning(f"[{MOD_NAME}]   2. Open the bank")
            logging.warning(f"[{MOD_NAME}]   3. Press NumPad8 to research bank structure")
            logging.warning(f"[{MOD_NAME}]   4. Check the generated files: bank_structure_dump.txt")
            logging.warning(f"[{MOD_NAME}]   5. Share the files to help identify the correct bank API")
            return
        
        # Log the sorting operation
        debug_log(f"Found {len(bank_objects)} {found_class_name} objects for sorting", "INFO")
        
        # TODO: Implement actual sorting logic based on Bank API research
        # Steps needed:
        # 1. Run NumPad8 to dump Bank structure and understand the API
        # 2. Find methods to get items list from bank_objects
        # 3. Implement sorting algorithms for each method (Boividevngu, Rarity, Type, Name, Level)
        # 4. Find methods to reorder/update items in the bank
        # 5. Test each sort method in-game
        # Reference: See bank_structure_dump.txt and bank_structure_dump.json for API details
        
        # WARNING: Sorting is NOT implemented yet - this is just research/placeholder
        logging.warning(f"[{MOD_NAME}] ⚠️ IMPORTANT: Bank sorting is NOT yet implemented!")
        logging.warning(f"[{MOD_NAME}] This mod is still in RESEARCH phase.")
        logging.warning(f"[{MOD_NAME}] ")
        logging.warning(f"[{MOD_NAME}] Found {len(bank_objects)} '{found_class_name}' objects")
        logging.warning(f"[{MOD_NAME}] but we need to verify if this is the correct class.")
        logging.warning(f"[{MOD_NAME}] ")
        logging.warning(f"[{MOD_NAME}] Next steps:")
        logging.warning(f"[{MOD_NAME}]   1. Press NumPad8 to research bank structure")
        logging.warning(f"[{MOD_NAME}]   2. Check bank_structure_dump.txt and .json files")
        logging.warning(f"[{MOD_NAME}]   3. Find the correct API to access and sort bank items")
        debug_log(f"Bank sort '{method}' attempted but not implemented (placeholder)", "INFO")
        
    except Exception as e:
        import traceback
        error_msg = f"Error sorting bank: {e}"
        debug_log(error_msg, "ERROR")
        debug_log(f"Traceback: {traceback.format_exc()}", "ERROR")
        logging.error(f"[{MOD_NAME}] ❌ {error_msg}")

@keybind("NumPadEight")
def do_research(_) -> None:
    """Keybind: NumPad8 to dump Bank structure"""
    debug_log("NumPad8 pressed - starting Bank structure research", "INFO")
    logging.info(f"[{MOD_NAME}] 🔍 Starting Bank structure research...")
    logging.info(f"[{MOD_NAME}] ℹ️ This will help identify which game classes exist for bank sorting")
    logging.info(f"[{MOD_NAME}] Please wait...")
    
    result = dump_player_controller()
    save_dump_to_file(result)
    
    if result["success"]:
        logging.info(f"[{MOD_NAME}] ✅ Research complete!")
        logging.info(f"[{MOD_NAME}] 📄 Check files in: {get_mod_directory()}")
        logging.info(f"[{MOD_NAME}] Files: {OUTPUT_FILE}, {JSON_FILE}, {SUMMARY_FILE}")
        debug_log("Research completed successfully", "INFO")
    else:
        logging.error(f"[{MOD_NAME}] ❌ Research failed: {result.get('error', 'Unknown error')}")
        debug_log(f"Research failed: {result.get('error', 'Unknown error')}", "ERROR")

@keybind("NumPadSeven")
def do_bank_sort(_) -> None:
    """Keybind: NumPad7 to sort Bank"""
    debug_log(f"NumPad7 pressed - triggering bank sort with method: {CURRENT_SORT_METHOD}", "INFO")
    logging.info(f"[{MOD_NAME}] 🔄 Attempting to sort bank with method: {CURRENT_SORT_METHOD}")
    sort_bank_items(CURRENT_SORT_METHOD)

def on_research_button(_: ButtonOption) -> None:
    """Button callback for manual research"""
    debug_log("Research button pressed", "INFO")
    do_research(None)

def on_debug_toggle(option: BoolOption, new_value: bool) -> None:
    """Toggle debug mode on/off"""
    global DEBUG_ENABLED
    DEBUG_ENABLED = new_value
    
    if DEBUG_ENABLED:
        logging.info(f"[{MOD_NAME}] 🐛 Debug mode ENABLED")
        debug_log("Debug mode enabled by user", "INFO")
        debug_log("=" * 60, "INFO")
        debug_log("Debug logging is now active!", "INFO")
        debug_log("All debug messages will be printed to console and saved to debug.log", "INFO")
        debug_log("=" * 60, "INFO")
    else:
        debug_log("Debug mode disabled by user", "INFO")
        logging.info(f"[{MOD_NAME}] 🐛 Debug mode DISABLED")

def on_sort_method_change(option: SpinnerOption, new_value: str) -> None:
    """Handle sort method change"""
    global CURRENT_SORT_METHOD
    CURRENT_SORT_METHOD = new_value
    debug_log(f"Sort method changed to: {new_value}", "INFO")
    logging.info(f"[{MOD_NAME}] 🔄 Sort method set to: {new_value}")

def on_sort_button(_: ButtonOption) -> None:
    """Button callback for sorting bank"""
    debug_log(f"Sort button pressed, using method: {CURRENT_SORT_METHOD}", "INFO")
    sort_bank_items(CURRENT_SORT_METHOD)

# ==================== OPTIONS ====================

debug_option = BoolOption(
    "🐛 Enable Debug Mode",
    value=False,
    description="Enable detailed debug logging (similar to magnetloot mod). "
                "Logs will be printed to console and saved to debug.log file.",
    on_change=on_debug_toggle
)

sort_method_option = SpinnerOption(
    "🔄 Sort Method",
    value="Boividevngu",
    choices=list(SORT_METHODS.keys()),
    description="Select the method to sort bank items. Press NumPad7 or use the button below to sort.",
    on_change=on_sort_method_change
)

sort_button = ButtonOption(
    "🔄 Sort Bank Now",
    description="Sort bank items using the selected method (or press NumPad7)",
    on_press=on_sort_button
)

research_button = ButtonOption(
    "🔍 Dump Bank Structure",
    description="Press to dump Bank/Inventory structure to files (or press NumPad8)",
    on_press=on_research_button
)

main_group = GroupedOption(
    "Bank Research",
    children=[
        debug_option,
        sort_method_option,
        sort_button,
        research_button,
    ]
)

# ==================== INITIALIZATION ====================

build_mod(
    options=[main_group],
)

logging.info("="*80)
logging.info(f"[{MOD_NAME}] v{__version__} Loaded!")
logging.info(f"[{MOD_NAME}] ℹ️ Press tilde (~) key twice to open console and see messages")
logging.info(f"[{MOD_NAME}] Keybinds:")
logging.info(f"[{MOD_NAME}]   NumPad7 - Sort Bank (current method: {CURRENT_SORT_METHOD})")
logging.info(f"[{MOD_NAME}]   NumPad8 - Dump Bank Structure")
logging.info(f"[{MOD_NAME}] 🐛 Debug mode: {'ENABLED' if DEBUG_ENABLED else 'DISABLED'} (toggle in options)")
logging.info(f"[{MOD_NAME}] 📁 Available sort methods: {', '.join(SORT_METHODS.keys())}")
logging.info(f"[{MOD_NAME}] Output files: {OUTPUT_FILE}, {JSON_FILE}, {SUMMARY_FILE}, debug.log")
logging.info(f"[{MOD_NAME}] Location: {get_mod_directory()}")
logging.info("="*80)

debug_log(f"{MOD_NAME} v{__version__} initialized", "INFO")