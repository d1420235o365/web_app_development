# 微型圖書館 (Mini Library) 流程圖文件

## 1. 使用者流程圖 (User Flow)

描述使用者進入系統後，如何進行書籍搜尋、借閱、歸還以及管理操作。

```mermaid
flowchart TD
    Start([使用者進入網站]) --> Home[首頁 - 書籍搜尋與列表]
    Home --> Search{是否搜尋書籍?}
    Search -->|是| SearchResult[顯示過濾後的書籍]
    Search -->|否| AllBooks[顯示所有館藏]
    
    SearchResult & AllBooks --> Detail[查看書籍詳情]
    
    Detail --> AuthCheck{已登入?}
    AuthCheck -->|否| Login[登入頁面]
    Login --> AuthCheck
    
    AuthCheck -->|是| RoleCheck{使用者角色?}
    
    RoleCheck -->|借閱者| BorrowAction[點擊借閱]
    BorrowAction --> BorrowStatus{書籍是否在庫?}
    BorrowStatus -->|是| BorrowSuccess[完成借閱紀錄]
    BorrowStatus -->|否| BorrowFail[提示已被借出]
    
    RoleCheck -->|管理員| AdminAction{執行管理操作?}
    AdminAction -->|新增書籍| AddBook[填寫書籍資訊]
    AdminAction -->|編輯/刪除| EditBook[更新書籍狀態]
    AdminAction -->|追蹤逾期| OverdueList[查看逾期清單]
    
    BorrowSuccess --> Profile[個人中心 - 查看借閱紀錄]
    Profile --> ReturnAction[點擊歸還]
    ReturnAction --> ReturnSuccess[更新書籍為在庫]
```

---

## 2. 系統序列圖 (Sequence Diagram)

以「借書流程」為例，描述資料如何在各元件之間流動。

```mermaid
sequenceDiagram
    actor User as 借閱者
    participant Browser as 瀏覽器 (View)
    participant Flask as Flask Routes (Controller)
    participant Model as SQLAlchemy Models
    participant DB as SQLite Database

    User->>Browser: 點擊「確認借閱」
    Browser->>Flask: POST /books/borrow/<id>
    
    rect rgb(240, 240, 240)
        Note over Flask, DB: 借閱邏輯檢核
        Flask->>Model: 查詢書籍狀態 (id)
        Model->>DB: SELECT status FROM books WHERE id=...
        DB-->>Model: 返回狀態 (Available)
        
        Flask->>Model: 建立借閱紀錄
        Model->>DB: INSERT INTO borrow_records (user_id, book_id, borrow_date)
        
        Flask->>Model: 更新書籍狀態
        Model->>DB: UPDATE books SET status='Borrowed' WHERE id=...
        DB-->>Model: 寫入成功
    end
    
    Model-->>Flask: 回傳處理結果
    Flask-->>Browser: 重導向至個人紀錄頁 (Redirect /profile)
    Browser-->>User: 顯示「借閱成功」訊息
```

---

## 3. 功能清單對照表

以下是系統各功能對應的 URL 路徑與 HTTP 方法規劃：

| 功能名稱 | URL 路徑 | HTTP 方法 | 說明 |
| :--- | :--- | :--- | :--- |
| **首頁/書籍搜尋** | `/` | `GET` | 顯示書籍列表與搜尋介面 |
| **書籍詳情** | `/book/<int:id>` | `GET` | 查看特定書籍的詳細資訊 |
| **登入** | `/login` | `GET`, `POST` | 使用者與管理員登入 |
| **登出** | `/logout` | `GET` | 登出當前帳號 |
| **執行借書** | `/book/borrow/<int:id>` | `POST` | 建立借閱紀錄並更新書籍狀態 |
| **執行還書** | `/book/return/<int:id>` | `POST` | 更新借閱紀錄並將書籍標記為在庫 |
| **個人中心** | `/profile` | `GET` | 查看個人借閱歷史與當前借閱 |
| **管理後台** | `/admin/dashboard` | `GET` | 管理員概覽（含逾期統計） |
| **新增書籍** | `/admin/book/add` | `GET`, `POST` | 管理員手動新增圖書 |
| **編輯書籍** | `/admin/book/edit/<int:id>`| `GET`, `POST` | 修改書籍基本資訊 |
| **刪除書籍** | `/admin/book/delete/<int:id>`| `POST` | 從館藏中移除書籍 |
| **逾期清單** | `/admin/overdue` | `GET` | 篩選出所有已逾期的借閱紀錄 |

---

**後續步驟建議：**
流程設計已完成，您可以輸入 `/db-design` 來設計具體的資料庫 Table Schema。
