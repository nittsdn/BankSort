"""
BankResearch - Phase 0. 5: Bank Structure Discovery
Dumps Bank and Inventory structures to understand the API
"""

if True:
    assert __import__("mods_base").__version_info__ >= (1, 0), "Please update the SDK"

import unrealsdk
from mods_base import build_mod, hook, get_pc
from mods_base.options import ButtonOption, GroupedOption
from mods_base.keybinds import keybind, KeybindType
from unrealsdk.hooks import Type
from unrealsdk.unreal import UObject, WrappedStruct, BoundFunction
from typing import Any
import os
import json
from datetime import datetime

__version__: str = "0.5.0"
__version_info__: tuple[int, ... ] = (0, 5, 0)

# ==================== CONSTANTS ====================

MOD_NAME = "BankResearch"
OUTPUT_FILE = "bank_structure_dump.txt"
JSON_FILE = "bank_structure_dump.json"

# ==================== UTILITY FUNCTIONS ====================

def get_mod_directory() -> str:
    """Get the mod directory path"""
    return os. path.dirname(os.path.abspath(__file__))

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
        return f"<Error getting repr:  {e}>"

def safe_type(obj: Any) -> str:
    """Safely get type of object"""
    try: 
        return str(type(obj))
    except Exception as e:
        return f"<Error getting type: {e}>"

# ==================== DUMP FUNCTIONS ====================

def dump_object_recursive(obj: Any, name: str, depth: int = 0, max_depth: int = 3) -> list:
    """Recursively dump object structure"""
    lines = []
    indent = "  " * depth
    
    if depth > max_depth:
        lines. append(f"{indent}[Max depth reached]")
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
                lines.append(f"{indent}  - {attr}: <Error:  {e}>")
    except Exception as e:
        lines. append(f"{indent}Error getting attributes: {e}")
    
    return lines

def dump_player_controller() -> dict:
    """Dump PlayerController structure focusing on Bank/Inventory"""
    
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
        pc = get_pc()
        
        if not pc: 
            lines.append("❌ ERROR: PlayerController not found!")
            lines.append("This usually means you're not in-game yet.")
            result["error"] = "PlayerController not found"
            result["all_text"] = lines
            return result
        
        result["pc_found"] = True
        lines.append("✅ PlayerController found!")
        lines.append(f"Type: {safe_type(pc)}")
        lines.append(f"Value: {safe_str(pc)}")
        lines.append("")
        
        # Get all attributes
        lines.append("="*80)
        lines.append("ALL PLAYERCONTROLLER ATTRIBUTES")
        lines.append("="*80)
        
        pc_attrs = dir(pc)
        result["pc_attributes"] = pc_attrs
        
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
        lines.append("="*80)
        lines.append("🎯 BANK-RELATED ATTRIBUTES (Deep Dive)")
        lines.append("="*80)
        lines.append("")
        
        bank_keywords = ['bank', 'storage', 'vault']
        for attr in pc_attrs:
            if any(kw in attr.lower() for kw in bank_keywords):
                lines.append(f"Found Bank-related: {attr}")
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
                    lines. append(f"  Error accessing {attr}: {e}")
                lines.append("")
        
        # Focus on Inventory-related attributes
        lines.append("="*80)
        lines.append("📦 INVENTORY-RELATED ATTRIBUTES (Deep Dive)")
        lines.append("="*80)
        lines.append("")
        
        inventory_keywords = ['inventory', 'item', 'equipment']
        for attr in pc_attrs: 
            if any(kw in attr.lower() for kw in inventory_keywords):
                lines. append(f"Found Inventory-related: {attr}")
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
                lines.append("")
        
        # Check Pawn's inventory
        lines.append("="*80)
        lines.append("🧍 PAWN INVENTORY CHECK")
        lines.append("="*80)
        lines.append("")
        
        if hasattr(pc, 'Pawn') and pc.Pawn:
            pawn = pc.Pawn
            lines.append(f"✅ Pawn found: {safe_str(pawn)}")
            lines.append(f"Pawn type: {safe_type(pawn)}")
            lines.append("")
            
            pawn_attrs = dir(pawn)
            for attr in pawn_attrs:
                if any(kw in attr.lower() for kw in ['inventory', 'item', 'equipment', 'bank']):
                    lines.append(f"Pawn. {attr}:")
                    try:
                        value = getattr(pawn, attr, None)
                        dump_lines = dump_object_recursive(value, f"Pawn.{attr}", depth=0, max_depth=3)
                        lines.extend(dump_lines)
                    except Exception as e:
                        lines.append(f"  Error:  {e}")
                    lines. append("")
        else:
            lines.append("❌ No Pawn found")
        
        # Try to find Bank objects using unrealsdk. find_all
        lines.append("="*80)
        lines.append("🔍 SEARCHING FOR BANK OBJECTS WITH find_all()")
        lines.append("="*80)
        lines.append("")
        
        search_classes = [
            "BankInventory",
            "OakInventory", 
            "OakBank",
            "InventoryComponent",
            "BankComponent",
            "OakInventoryItemPickup",
            "OakStorageComponent"
        ]
        
        for class_name in search_classes: 
            try:
                lines.append(f"Searching for:  {class_name}")
                objects = unrealsdk.find_all(class_name)
                
                if objects:
                    lines.append(f"  ✅ Found {len(objects)} objects!")
                    for i, obj in enumerate(objects[: 3]):  # Only show first 3
                        lines.append(f"  Object {i+1}:")
                        lines.append(f"    Type: {safe_type(obj)}")
                        lines.append(f"    Str: {safe_str(obj)[: 200]}")
                        
                        # Dump its structure
                        dump_lines = dump_object_recursive(obj, f"{class_name}[{i}]", depth=0, max_depth=2)
                        lines.extend(dump_lines)
                else:
                    lines.append(f"  ❌ No objects found")
            except Exception as e:
                lines.append(f"  ⚠️ Error searching:  {e}")
            lines.append("")
        
        result["success"] = True
        
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
    
    result["all_text"] = lines
    return result

def save_dump_to_file(result: dict) -> None:
    """Save dump results to files"""
    
    mod_dir = get_mod_directory()
    
    # Save text file
    txt_path = os.path.join(mod_dir, OUTPUT_FILE)
    try:
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(result["all_text"]))
        print(f"[{MOD_NAME}] ✅ Text dump saved to:  {txt_path}")
    except Exception as e:
        print(f"[{MOD_NAME}] ❌ Error saving text file: {e}")
    
    # Save JSON file
    json_path = os.path.join(mod_dir, JSON_FILE)
    try:
        # Remove all_text from JSON (too large)
        json_result = {k: v for k, v in result.items() if k != 'all_text'}
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_result, f, indent=2, default=str)
        print(f"[{MOD_NAME}] ✅ JSON dump saved to: {json_path}")
    except Exception as e:
        print(f"[{MOD_NAME}] ❌ Error saving JSON file: {e}")

# ==================== KEYBIND & BUTTON ====================

@keybind("F8", KeybindType. PRESSED)
def do_research(_) -> None:
    """Keybind:  F8 to dump Bank structure"""
    print(f"[{MOD_NAME}] 🔍 Starting Bank structure research...")
    print(f"[{MOD_NAME}] Please wait...")
    
    result = dump_player_controller()
    save_dump_to_file(result)
    
    if result["success"]:
        print(f"[{MOD_NAME}] ✅ Research complete!")
        print(f"[{MOD_NAME}] 📄 Check files in: {get_mod_directory()}")
        print(f"[{MOD_NAME}] Files:  {OUTPUT_FILE}, {JSON_FILE}")
    else:
        print(f"[{MOD_NAME}] ❌ Research failed:  {result. get('error', 'Unknown error')}")

def on_research_button(_:  ButtonOption) -> None:
    """Button callback for manual research"""
    do_research(None)

# ==================== OPTIONS ====================

research_button = ButtonOption(
    "🔍 Dump Bank Structure",
    on_press=on_research_button
)

main_group = GroupedOption(
    "Bank Research",
    children=[
        research_button,
    ]
)

# ==================== INITIALIZATION ====================

build_mod(
    options=[main_group],
)

print("="*80)
print(f"[{MOD_NAME}] v{__version__} Loaded!")
print(f"[{MOD_NAME}] Press F8 or use mod menu to dump Bank structure")
print(f"[{MOD_NAME}] Output files: {OUTPUT_FILE}, {JSON_FILE}")
print(f"[{MOD_NAME}] Location: {get_mod_directory()}")
print("="*80)