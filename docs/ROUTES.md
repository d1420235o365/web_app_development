# 微型圖書館 (Mini Library) 路由設計文件

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁/書籍搜尋** | GET | `/` | `index.html` | 顯示書籍列表與搜尋介面 |
| **書籍詳情** | GET | `/book/<id>` | `book_detail.html` | 顯示單一書籍詳細資訊與借閱按鈕 |
| **登入頁面** | GET | `/login` | `login.html` | 顯示登入表單 |
| **執行登入** | POST | `/login` | — | 驗證身分，建立 Session |
| **執行登出** | GET | `/logout` | — | 清除 Session，重導向至首頁 |
| **註冊頁面** | GET | `/register` | `register.html` | 顯示註冊表單 |
| **執行註冊** | POST | `/register` | — | 建立新使用者，重導向至登入 |
| **個人中心** | GET | `/profile` | `profile.html` | 顯示個人借閱紀錄與歸還按鈕 |
| **執行借書** | POST | `/book/borrow/<id>` | — | 檢查在庫狀態，建立紀錄，更新書籍 |
| **執行還書** | POST | `/book/return/<id>` | — | 更新借閱紀錄，將書籍改為在庫 |
| **管理員後台** | GET | `/admin/dashboard` | `admin/dashboard.html` | 顯示管理統計與功能入口 |
| **新增書籍頁面** | GET | `/admin/book/add` | `admin/book_form.html` | 顯示新增書籍表單 |
| **執行新增書籍** | POST | `/admin/book/add` | — | 將新書存入資料庫 |
| **編輯書籍頁面** | GET | `/admin/book/edit/<id>`| `admin/book_form.html` | 顯示編輯書籍表單 (帶入舊資料) |
| **執行編輯書籍** | POST | `/admin/book/edit/<id>`| — | 更新資料庫中的書籍資訊 |
| **執行刪除書籍** | POST | `/admin/book/delete/<id>`| — | 從資料庫移除書籍紀錄 |
| **逾期清單** | GET | `/admin/overdue` | `admin/overdue.html` | 篩選並顯示所有逾期未還的紀錄 |

---

## 2. 每個路由詳細說明

### 2.1 書籍相關 (Main & Borrow)
- **`/book/borrow/<id>` (POST)**
  - **輸入**: URL 中的 `id` (書籍 ID)，Session 中的 `user_id`。
  - **處理**: 檢查 `Book.status == 'Available'`，若是則呼叫 `BorrowRecord.create()` 並 `Book.update(status='Borrowed')`。
  - **輸出**: 重導向至 `/profile`。
  - **錯誤處理**: 若書籍已借出，回傳錯誤訊息並留在詳情頁。

### 2.2 身分驗證 (Auth)
- **`/login` (POST)**
  - **輸入**: 表單中的 `username`, `password`。
  - **處理**: 查詢 `User` 並比對 `password_hash`。成功則將 `user_id` 與 `role` 存入 `session`。
  - **輸出**: 重導向至 `/` 或 `/admin/dashboard` (依角色)。
  - **錯誤處理**: 帳密錯誤時，重導向回登入頁並顯示閃退訊息 (Flash Message)。

### 2.3 管理功能 (Admin)
- **權限保護**: 所有 `/admin` 開頭的路由需檢查 `session['role'] == 'admin'`，否則重導向至登入或報錯 403。

---

## 3. Jinja2 模板清單

所有模板均繼承自 `base.html`：
- `base.html`: 包含導航欄 (Nav)、標題與基礎樣式引用。
- `index.html`: 書籍卡片列表、搜尋列。
- `book_detail.html`: 書籍資訊、借閱按鈕。
- `login.html`, `register.html`: 登入與註冊表單。
- `profile.html`: 使用者的借閱紀錄表格 (含還書按鈕)。
- `admin/dashboard.html`: 管理員主介面、數據概覽。
- `admin/book_form.html`: 新增與編輯書籍共用的表單模板。
- `admin/overdue.html`: 逾期紀錄篩選清單。

---

## 4. 路由骨架程式碼規劃
檔案將依模組拆分為：
- `app/routes/main.py`: 公開頁面。
- `app/routes/auth.py`: 登入註冊。
- `app/routes/borrow.py`: 借還書邏輯。
- `app/routes/admin.py`: 管理功能。
