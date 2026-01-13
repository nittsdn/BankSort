# Logging Fix Summary - BankSort Mod

## Vấn Đề (Problem)
"vẫn ko thấy mod chạy, bạn check log nếu ko thấy gì thì lấy log của magnetloot xem sao"

**Translation:** "Still don't see the mod running, check the log if you don't see anything then get the magnetloot log to see"

## Nguyên Nhân (Root Cause)
Mod sử dụng Python `print()` thay vì SDK logging của Borderlands 3. Điều này khiến:
- Messages không hiển thị trong game console
- User không thấy phản hồi khi nhấn NumPad7 hoặc NumPad8
- Mod chạy nhưng "vô hình" (invisible)

**English:** Mod was using Python `print()` instead of Borderlands 3 SDK logging. This caused messages to not show in the game console, making the mod appear "invisible" even though it was running.

---

## Các Thay Đổi (Changes Made)

### ✅ 1. Thêm SDK Logging Import
```python
import unrealsdk
from unrealsdk import logging  # ← ADDED THIS
```

### ✅ 2. Cập Nhật Hàm debug_log()
Thay đổi từ `print()` sang SDK logging:

```python
# TRƯỚC (Before):
print(formatted_msg)

# SAU (After):
if level == "ERROR":
    logging.error(formatted_msg)
elif level == "WARNING":
    logging.warning(formatted_msg)
elif level == "DEBUG":
    logging.dev_warning(formatted_msg)
else:  # INFO
    logging.info(formatted_msg)
```

### ✅ 3. Thay Thế Tất Cả print() Statements
Đã thay thế 30+ câu lệnh `print()` với SDK logging:

| Function | Before | After |
|----------|--------|-------|
| `save_dump_to_file()` | `print(...)` | `logging.info(...)` / `logging.error(...)` |
| `sort_bank_items()` | `print(...)` | `logging.info(...)` / `logging.warning(...)` / `logging.error(...)` |
| `do_research()` | `print(...)` | `logging.info(...)` / `logging.error(...)` |
| `do_bank_sort()` | `print(...)` | `logging.info(...)` |
| `on_debug_toggle()` | `print(...)` | `logging.info(...)` |
| `on_sort_method_change()` | `print(...)` | `logging.info(...)` |
| Initialization | `print(...)` | `logging.info(...)` |

---

## Cách Kiểm Tra (How to Verify)

### Bước 1: Load Mod
1. Chạy Borderlands 3
2. Load vào game (vào character)
3. Mod sẽ tự động load

### Bước 2: Mở Console
Nhấn phím **tilde (~)** hai lần để mở console

### Bước 3: Kiểm Tra Messages
Bạn sẽ thấy messages khi mod load:
```
[BankResearch] v0.6.0 Loaded!
[BankResearch] Keybinds:
[BankResearch]   NumPad7 - Sort Bank (current method: Boividevngu)
[BankResearch]   NumPad8 - Dump Bank Structure
...
```

### Bước 4: Test Keybinds
1. **NumPad7** - Sort Bank:
   - Mở Bank trong game
   - Nhấn NumPad7
   - Console sẽ hiện: "🔄 Sorting bank items using 'Boividevngu' method..."
   
2. **NumPad8** - Dump Structure:
   - Nhấn NumPad8
   - Console sẽ hiện: "🔍 Starting Bank structure research..."

### Bước 5: Kiểm Tra Debug Mode
1. Mở mod menu
2. Toggle "Enable Debug Mode" ON
3. Console sẽ hiện: "🐛 Debug mode ENABLED"
4. Thực hiện các hành động sẽ thấy nhiều log hơn

---

## Expected Console Output

### Khi Load Mod:
```
================================================================================
[BankResearch] v0.6.0 Loaded!
[BankResearch] Keybinds:
[BankResearch]   NumPad7 - Sort Bank (current method: Boividevngu)
[BankResearch]   NumPad8 - Dump Bank Structure
[BankResearch] 🐛 Debug mode: DISABLED (toggle in options)
[BankResearch] 📁 Available sort methods: Boividevngu, By Rarity, By Type, By Name, By Level
[BankResearch] Output files: bank_structure_dump.txt, bank_structure_dump.json, debug.log
[BankResearch] Location: [mod directory path]
================================================================================
```

### Khi Nhấn NumPad7 (Sort):
```
[BankResearch] 🔄 Sorting bank...
[BankResearch] 🔄 Sorting bank items using 'Boividevngu' method...
[BankResearch] ✅ Bank sort 'Boividevngu' triggered!
[BankResearch] ℹ️ Note: Full sorting implementation requires game API research
```

### Khi Nhấn NumPad8 (Research):
```
[BankResearch] 🔍 Starting Bank structure research...
[BankResearch] Please wait...
[BankResearch] ✅ Text dump saved to: [path]
[BankResearch] ✅ JSON dump saved to: [path]
[BankResearch] ✅ Research complete!
[BankResearch] 📄 Check files in: [path]
[BankResearch] Files: bank_structure_dump.txt, bank_structure_dump.json
```

### Khi Bật Debug Mode:
```
[BankResearch] 🐛 Debug mode ENABLED
[HH:MM:SS.mmm] [BankResearch] [INFO] Debug mode enabled by user
[HH:MM:SS.mmm] [BankResearch] [INFO] ============================================================
[HH:MM:SS.mmm] [BankResearch] [INFO] Debug logging is now active!
[HH:MM:SS.mmm] [BankResearch] [INFO] All debug messages will be printed to console and saved to debug.log
[HH:MM:SS.mmm] [BankResearch] [INFO] ============================================================
```

---

## Troubleshooting

### ❓ Vẫn không thấy messages?
1. ✅ Kiểm tra xem mod có load không (check mod menu)
2. ✅ Đảm bảo đã mở console bằng phím tilde (~)
3. ✅ Thử toggle debug mode ON để thấy nhiều log hơn
4. ✅ Check file `debug.log` trong thư mục mod

### ❓ Console không mở được?
- Phím tilde (~) thường là phím bên trái số 1 trên keyboard
- Nhấn 2 lần để mở SDK console
- Nếu không được, check keybind settings trong game

### ❓ Mod không load?
- Check có error message trong console không
- Kiểm tra file `__init__.py` có trong folder đúng không
- Đảm bảo mods_base SDK >= 1.0

---

## Technical Details

### SDK Logging Levels
Mod bây giờ sử dụng:
- `logging.info()` - Thông tin chung
- `logging.warning()` - Cảnh báo
- `logging.error()` - Lỗi
- `logging.dev_warning()` - Debug messages (khi debug mode bật)

### File Logging
Debug log file vẫn hoạt động bình thường:
- File: `debug.log` trong thư mục mod
- Ghi: ERROR và WARNING (luôn), INFO và DEBUG (khi debug mode bật)
- Format: `[HH:MM:SS.mmm] [BankResearch] [LEVEL] Message`

---

## Comparison: Before vs After

### Before (Using print()):
```python
print(f"[{MOD_NAME}] ✅ Bank sort '{method}' triggered!")
# ❌ Không hiện trong game console
# ❌ User không thấy gì
```

### After (Using SDK logging):
```python
logging.info(f"[{MOD_NAME}] ✅ Bank sort '{method}' triggered!")
# ✅ Hiện trong game console
# ✅ User thấy feedback rõ ràng
```

---

## Next Steps

Nếu bạn vẫn gặp vấn đề sau khi apply fix này:

1. **Bật debug mode** và test lại
2. **Share console output** hoặc file `debug.log`
3. **Chụp screenshot** console khi nhấn keybinds
4. **Check magnetloot logs** để so sánh format

---

## Version History
- **v0.6.0**: Original version with print() statements
- **v0.6.1**: Fixed - All print() replaced with SDK logging ← Current

---

**Tóm lại:** Mod bây giờ sử dụng SDK logging đúng cách, messages sẽ hiển thị trong game console khi bạn mở bằng phím tilde (~). Không còn "vô hình" nữa! 🎉
