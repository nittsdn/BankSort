# BankResearch Mod - Hướng Dẫn Sử Dụng (Tiếng Việt)

## 📖 Giới Thiệu

BankResearch là mod cho Borderlands 3 giúp bạn:
- ✅ Sắp xếp items trong Bank theo nhiều cách khác nhau
- ✅ Research/debug Bank structure để phát triển tính năng mới
- ✅ Debug logging chi tiết để tìm lỗi

**Version hiện tại:** v0.6.0

---

## 🎮 Cách Sử Dụng

### Phím Tắt (Keybinds)

| Phím | Chức Năng | Mô Tả |
|------|-----------|-------|
| **NumPad7** | Sort Bank | Sắp xếp items trong Bank theo method đã chọn |
| **NumPad8** | Dump Structure | Dump Bank structure ra file (để research) |

⚠️ **Lưu ý:** Không dùng phím F1-F12 vì game đã sử dụng!

### Menu Options

Mở mod menu trong game và tìm "Bank Research", bạn sẽ thấy:

1. **🐛 Enable Debug Mode**
   - Bật/tắt debug logging
   - Khi bật: ghi tất cả log ra console và file
   - Khi tắt: chỉ ghi ERROR và WARNING

2. **🔄 Sort Method** (Spinner)
   - Chọn phương thức sắp xếp
   - Options:
     - **Boividevngu** ⭐ (mặc định)
     - By Rarity (theo độ hiếm)
     - By Type (theo loại vũ khí/item)
     - By Name (theo tên A-Z)
     - By Level (theo level)

3. **🔄 Sort Bank Now** (Button)
   - Click để sort Bank ngay
   - Giống như nhấn NumPad7

4. **🔍 Dump Bank Structure** (Button)
   - Click để dump Bank structure
   - Giống như nhấn NumPad8

---

## 📝 Hướng Dẫn Chi Tiết

### Cách Sort Bank

**Bước 1:** Chọn phương thức sort
- Mở mod menu → "Bank Research"
- Chọn "Sort Method" 
- Pick "Boividevngu" (hoặc method khác)

**Bước 2:** Mở Bank trong game

**Bước 3:** Sort!
- **Cách 1:** Nhấn **NumPad7**
- **Cách 2:** Dùng button "Sort Bank Now" trong menu

**Kết quả:**
- Console sẽ hiện message
- Items sẽ được sắp xếp (nếu đã implement đủ API)

### Cách Bật Debug Mode

1. Mở mod menu
2. Tìm "Bank Research"
3. Toggle "Enable Debug Mode" thành **ON**
4. Từ giờ mọi thao tác sẽ được log chi tiết

**Debug log sẽ lưu ở:**
- Console: real-time output
- File: `debug.log` trong thư mục mod

### Cách Research Bank API

Nếu bạn muốn phát triển thêm features:

1. Load vào game
2. Nhấn **NumPad8** (hoặc dùng button)
3. Check output files:
   - `bank_structure_dump.txt` - human readable
   - `bank_structure_dump.json` - machine readable
4. Đọc files để hiểu Bank API

---

## 🔧 Troubleshooting

### Mod không load
- ✅ Đảm bảo file tên là `__init__.py` (KHÔNG phải `banksort___init__.py`)
- ✅ Check console có error message không
- ✅ Đảm bảo SDK đã update (cần mods_base >= 1.0)

### Keybind không hoạt động
- ✅ Đảm bảo bạn đang nhấn NumPad7/8 (không phải số trên keyboard)
- ✅ Check xem game có map các phím này không
- ✅ Bật debug mode để xem log

### Sort không hoạt động
- ✅ Mở Bank trước khi sort
- ✅ Bật debug mode để xem log chi tiết
- ✅ Check file debug.log xem có error không

### Debug log không ghi
- ✅ Check quyền ghi file trong thư mục mod
- ✅ ERROR và WARNING luôn được ghi (không cần bật debug mode)
- ✅ INFO và DEBUG chỉ ghi khi debug mode bật

---

## 📂 Files Được Tạo Ra

Mod sẽ tạo các files sau trong thư mục mod:

| File | Mô Tả | Khi Nào Tạo |
|------|-------|-------------|
| `debug.log` | Debug logging | Khi có WARNING/ERROR hoặc debug mode bật |
| `bank_structure_dump.txt` | Bank structure (text) | Khi nhấn NumPad8 |
| `bank_structure_dump.json` | Bank structure (JSON) | Khi nhấn NumPad8 |

---

## 🎯 Các Phương Thức Sort

### 1. Boividevngu ⭐ (Mặc định)
- Phương thức sort đặc biệt
- Được yêu cầu trong issue

### 2. By Rarity
- Sort theo độ hiếm của item
- Thứ tự: Legendary → Epic → Rare → Uncommon → Common

### 3. By Type
- Sort theo loại item
- Ví dụ: Assault Rifle, Shotgun, Pistol, Shield, v.v.

### 4. By Name
- Sort theo tên A-Z
- Alphabetical order

### 5. By Level
- Sort theo level requirement của item
- Từ thấp đến cao

---

## ⚠️ Lưu Ý Quan Trọng

### Sort Function - Current Status

**✅ Đã hoàn thành:**
- UI/Menu với SpinnerOption
- Keybinds (NumPad7)
- Button trong menu
- Debug logging chi tiết
- Error handling

**⚙️ Đang placeholder:**
- Logic sort thực tế cần research thêm về Bank API
- Hiện tại khi sort, mod sẽ:
  - Tìm Bank objects
  - Log thông tin
  - Hiện message
  - NHƯNG chưa sort items thực sự

**📝 Để implement sort đầy đủ cần:**
1. Research Bank API bằng NumPad8
2. Tìm methods để get/set items
3. Implement sort logic
4. Test in-game

---

## 🐛 Debug Log Format

```
[HH:MM:SS.mmm] [BankResearch] [LEVEL] Message
```

**Ví dụ:**
```
[14:23:45.123] [BankResearch] [INFO] NumPad7 pressed - triggering bank sort
[14:23:45.125] [BankResearch] [DEBUG] PlayerController found
[14:23:45.130] [BankResearch] [DEBUG] Found 45 OakInventory objects
[14:23:45.135] [BankResearch] [INFO] Bank sort 'Boividevngu' completed
```

**Log Levels:**
- **INFO**: Thông tin chung
- **DEBUG**: Chi tiết debug (chỉ khi debug mode bật)
- **WARNING**: Cảnh báo (luôn ghi)
- **ERROR**: Lỗi với full traceback (luôn ghi)

---

## 📞 Hỗ Trợ

Nếu gặp vấn đề:

1. **Bật debug mode** trong mod menu
2. **Reproduce lỗi** (làm lại bước gây lỗi)
3. **Check console** xem có error message
4. **Check file `debug.log`** trong thư mục mod
5. **Share log** khi báo lỗi

**Thông tin hữu ích khi báo lỗi:**
- Version mod (hiện tại: v0.6.0)
- Console output
- File debug.log
- Bước reproduce lỗi

---

## 📜 Version History

- **v0.6.0** (Latest):
  - ✅ Đổi keybind sang NumPad7/8
  - ✅ Thêm sort function với "Boividevngu"
  - ✅ Cải thiện debug logging
  - ✅ Thêm menu options đầy đủ

- **v0.5.2**:
  - Fixed BoolOption parameter error
  - Improved debug log file creation

- **v0.5.1**:
  - Fixed KeybindType error
  - Added debug mechanism

- **v0.5.0**:
  - Initial research version

---

## 🚀 Tính Năng Tương Lai

Dự định phát triển:
- [ ] Implement sort logic hoàn chỉnh cho tất cả methods
- [ ] Auto-sort khi mở Bank (option)
- [ ] Custom sort rules
- [ ] Sort inventory (ngoài Bank)
- [ ] Export/Import Bank layouts

---

**Chúc bạn chơi game vui vẻ! 🎮**
