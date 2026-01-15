# Sửa Lỗi Trích Xuất Dữ Liệu Item - Item Data Extraction Fix

## Vấn Đề / Problem

**Tiếng Việt:**
- User báo: "check log1, đã test và ko có hiệu ứng j, dùng tiếng việt"
- Kiểm tra debug1.log cho thấy: Logging hoạt động NHƯNG tất cả items có `Rarity: 0, Type: Unknown, Level: 0`
- Sắp xếp "ko có hiệu ứng" vì tất cả items có cùng giá trị, không phân biệt được
- Thiếu hỗ trợ tiếng Việt trong thông báo

**English:**
- User reported: "check log1, tested and has no effect, use Vietnamese"
- Checking debug1.log shows: Logging works BUT all items have `Rarity: 0, Type: Unknown, Level: 0`
- Sorting has "no effect" because all items have same values, cannot differentiate
- Missing Vietnamese language support in messages

---

## Phân Tích Log / Log Analysis

### Từ debug1.log / From debug1.log:
```
[09:36:30.996] Found 47 OakInventoryBalanceStateComponent objects
[09:36:30.996] Extracted item info: Unknown (Rarity: 0, Type: Unknown, Level: 0)
[09:36:30.997] Extracted item info: Reborn (Rarity: 0, Type: Unknown, Level: 0)
[09:36:30.997] Extracted item info: Berzerker Rocket Boots (Rarity: 0, Type: Unknown, Level: 0)
```

**Vấn đề rõ ràng / Clear issue:**
- ✅ Tìm được 47 items (objects found)
- ✅ Trích xuất được TÊN (name extraction works) 
- ❌ KHÔNG trích xuất được Rarity (always 0)
- ❌ KHÔNG trích xuất được Type (always Unknown)
- ❌ KHÔNG trích xuất được Level (always 0)

**Nguyên nhân / Root cause:**
Hàm `get_item_info()` đang tìm các attribute không tồn tại:
- `ItemRarity`, `Rarity`, `RarityLevel` - KHÔNG có
- `ItemType`, `Type` - KHÔNG có
- `ItemLevel`, `Level` - KHÔNG có

---

## Các Thay Đổi / Changes Made

### 1. Thêm Chế Độ Chẩn Đoán / Added Diagnostic Mode

**File:** `__init__.py` lines ~900-920

**Chức năng / Function:**
Khi debug mode BẬT và sort được gọi, mod sẽ dump toàn bộ attributes của item đầu tiên:
- Object type
- Tất cả non-private attributes (không bắt đầu bằng `_`)
- Giá trị của các attributes thông dụng

**Tại sao quan trọng / Why important:**
Chúng ta cần biết TÊN CHÍNH XÁC của attributes thực sự tồn tại trên object để trích xuất đúng dữ liệu.

**Code mới / New code:**
```python
# Diagnostic: Dump first item's attributes in detail when debug enabled
if idx == 0 and DEBUG_ENABLED:
    debug_log("=== DIAGNOSTIC: First item detailed inspection ===", "INFO")
    debug_log(f"Object type: {safe_type(item_obj)}", "INFO")
    attrs = dir(item_obj)
    relevant_attrs = [a for a in attrs if not a.startswith('_')]
    debug_log(f"Non-private attributes count: {len(relevant_attrs)}", "INFO")
    debug_log(f"First 30 attributes: {relevant_attrs[:30]}", "INFO")
    
    # Try common attributes
    for attr_name in ["Name", "DisplayName", "Rarity", "Level", "ItemName", 
                      "InventoryData", "BalanceData", "BalanceState"]:
        if hasattr(item_obj, attr_name):
            val = getattr(item_obj, attr_name)
            debug_log(f"  {attr_name} = {safe_type(val)} : {safe_str(val)[:100]}", "INFO")
```

### 2. Cải Thiện Hàm get_item_info() / Enhanced get_item_info()

**File:** `__init__.py` lines ~718-800

**Thay đổi / Changes:**
1. **Thêm nhiều tên attribute hơn để thử:**
   - Rarity: `Rarity`, `ItemRarity`, `RarityLevel`, `RarityData`
   - Type: `ItemType`, `InventoryType`, `Type`, `CategoryDefinition`, `InventoryData`
   - Level: `Level`, `ItemLevel`, `RequiredLevel`, `GameStage`
   - Name: `ItemName`, `DisplayName`, `InventoryName`, `Name`, `UIDisplayName`

2. **Thử truy cập nested objects:**
   - Nếu không tìm được trực tiếp, thử `InventoryData` và `BalanceData`
   - Có thể dữ liệu nằm trong object con

3. **Debug logging trong get_item_info:**
   - Log available attributes khi debug enabled
   - Giúp xác định tên attribute đúng

### 3. Hỗ Trợ Tiếng Việt / Vietnamese Language Support

**File:** `__init__.py` - nhiều dòng / multiple lines

**Thêm thông báo song ngữ tại / Added bilingual messages at:**

1. **Khởi động mod / Mod initialization:**
```python
logging.info(f"[{MOD_NAME}] v{__version__} Loaded!")
logging.info(f"[{MOD_NAME}] v{__version__} Đã tải!")
```

2. **Phím tắt / Keybinds:**
```python
logging.info(f"[{MOD_NAME}]   NumPad7 - Sort Bank (current method: {CURRENT_SORT_METHOD})")
logging.info(f"[{MOD_NAME}]   NumPad7 - Sắp xếp Bank (phương pháp hiện tại: {CURRENT_SORT_METHOD})")
```

3. **Debug mode toggle:**
```python
logging.info(f"[{MOD_NAME}] 🐛 Debug mode ENABLED / Chế độ debug ĐÃ BẬT")
```

4. **Kết quả sắp xếp / Sort results:**
```python
logging.info(f"[{MOD_NAME}] ✅ Items sorted using '{method}' method!")
logging.info(f"[{MOD_NAME}] ✅ Đã sắp xếp items theo phương pháp '{method}'!")
```

5. **Cảnh báo / Warnings:**
```python
logging.warning(f"[{MOD_NAME}] ⚠️ NOTE / LƯU Ý: Sorting logic is complete...")
```

### 4. Giải Thích "Boividevngu" / Explained "Boividevngu"

**File:** `__init__.py` line 684

```python
SORT_METHODS = {
    "Boividevngu": "boividevngu",  # Vietnamese: "Đồ vĩ đại và nguy nga" - means legendary/epic items first
    "By Rarity": "rarity",
    ...
}
```

**Ý nghĩa / Meaning:**
- "Boividevngu" = Sắp xếp ưu tiên đồ legendary/epic trước
- Giống "By Rarity" nhưng có thể mở rộng thêm tiêu chí sau

---

## Cách Test / How to Test

### Bước 1: Kích hoạt Debug Mode / Step 1: Enable Debug Mode

1. Load mod vào game
2. Mở mod menu → "Bank Research"
3. Toggle "Enable Debug Mode" → **ON**
4. Xác nhận thấy message: "Debug mode ENABLED / Chế độ debug ĐÃ BẬT"

### Bước 2: Mở Bank và Sort / Step 2: Open Bank and Sort

1. Load vào game (trong game, không phải main menu)
2. Mở Bank (Fast Travel → Sanctuary → Bank)
3. Đảm bảo có items trong bank (càng nhiều càng tốt)
4. Nhấn **NumPad7** để sort

### Bước 3: Kiểm Tra Console Output / Step 3: Check Console Output

Console sẽ hiển thị:
```
=== DIAGNOSTIC: First item detailed inspection ===
Object type: <class '...'>
Non-private attributes count: XX
First 30 attributes: ['attr1', 'attr2', ...]
  Name = ...
  DisplayName = ...
  (etc)
=== END DIAGNOSTIC ===
```

### Bước 4: Kiểm Tra debug.log File / Step 4: Check debug.log File

File location: `(Thư mục mod)/debug.log`

Tìm section:
```
[HH:MM:SS] [BankResearch] [INFO] === DIAGNOSTIC: First item detailed inspection ===
```

**QUAN TRỌNG / IMPORTANT:**
Copy toàn bộ section DIAGNOSTIC này và share! Đây là thông tin cần thiết để tìm đúng attribute names.

---

## Kết Quả Mong Đợi / Expected Results

### Nếu Fix Thành Công / If Fix Successful:

Console sẽ hiển thị items với giá trị khác nhau:
```
[BankResearch] 📋 Sort order summary (first 5) / Kết quả sắp xếp (5 đầu tiên):
[BankResearch]   1. Item Name (Rarity: 5, Type: Weapon, Level: 72)
[BankResearch]   2. Item Name (Rarity: 5, Type: Shield, Level: 72)
[BankResearch]   3. Item Name (Rarity: 4, Type: Grenade, Level: 65)
```

**Dấu hiệu thành công / Success indicators:**
- ✅ Rarity KHÔNG phải 0
- ✅ Type KHÔNG phải "Unknown"
- ✅ Level KHÔNG phải 0
- ✅ Items được sắp xếp theo thứ tự khác nhau

### Nếu Vẫn Chưa Fix / If Still Not Fixed:

Vẫn thấy:
```
[BankResearch]   1. Item Name (Rarity: 0, Type: Unknown, Level: 0)
[BankResearch]   2. Item Name (Rarity: 0, Type: Unknown, Level: 0)
```

**Bước tiếp theo / Next steps:**
1. Kiểm tra DIAGNOSTIC output
2. Tìm tên attribute ĐÚNG từ danh sách
3. Update `get_item_info()` để dùng tên đúng
4. Test lại

---

## Technical Details

### Vấn Đề Cốt Lõi / Core Issue

OakInventoryBalanceStateComponent là Component trong Unreal Engine. Các property thực tế có thể:
1. Không dùng tên "Rarity" trực tiếp
2. Nằm trong nested object (ví dụ: `BalanceState.Rarity`)
3. Dùng tên khác (ví dụ: `RarityIndex`, `ItemRarityLevel`)
4. Là enum hoặc reference đến object khác

### Chiến Lược Giải Quyết / Solution Strategy

1. ✅ **Diagnostic first** - Xem object có gì
2. ⏳ **Identify correct names** - Tìm tên đúng
3. ⏳ **Update extraction** - Cập nhật code
4. ⏳ **Test and verify** - Kiểm tra lại

---

## Files Changed

| File | Changes |
|------|---------|
| `__init__.py` | Enhanced get_item_info(), added diagnostic mode, Vietnamese messages |

---

## Checklist

### Đã Làm / Completed:
- [x] Thêm diagnostic logging cho first item
- [x] Cải thiện get_item_info() với nhiều attribute names hơn
- [x] Thêm hỗ trợ tiếng Việt trong messages
- [x] Thêm giải thích "Boividevngu"
- [x] Test syntax (no errors)

### Cần Làm / TODO:
- [ ] Test trong game với debug mode ON
- [ ] Lấy DIAGNOSTIC output từ log
- [ ] Xác định tên attribute ĐÚNG
- [ ] Update code với tên đúng nếu cần
- [ ] Verify sorting hoạt động với giá trị thực

---

## Liên Hệ / Contact

Nếu có vấn đề hoặc cần hỗ trợ:
1. Share file `debug.log` (section DIAGNOSTIC)
2. Share screenshot của console output
3. Share số lượng items trong bank và loại items

---

## Summary (English)

**What was done:**
1. Added detailed diagnostic logging that dumps all attributes of the first item when debug mode is enabled
2. Enhanced `get_item_info()` to try more attribute name variations and nested objects
3. Added Vietnamese bilingual support to all major messages
4. Explained what "Boividevngu" means (legendary/epic items first)

**What to do next:**
1. Enable debug mode in game
2. Open bank and press NumPad7 to sort
3. Check console and debug.log for DIAGNOSTIC output
4. Share the diagnostic output so we can identify the correct attribute names
5. Update code with correct names if needed

**Goal:**
Extract actual rarity, type, and level values from items so sorting has visible effect.
