# 流程圖文件 — 食譜收藏系統

> 版本：v1.1　　最後更新：2026-05-07　　對應 PRD：v1.1

本文件基於 PRD 與系統架構設計，使用 Mermaid 語法繪製使用者操作流程圖及系統資料處理序列圖。

---

## 1. 使用者流程圖（User Flow）

### 1.1 一般使用者主流程

從使用者進入網站開始，涵蓋所有主要功能的完整操作路徑。

```mermaid
flowchart LR
    Start([使用者開啟網頁]) --> Home[首頁\n熱門食譜列表]
    Home --> Action{選擇操作}

    Action -->|註冊 / 登入| Auth[身分驗證頁面]
    Auth -->|登入成功| Home

    Action -->|瀏覽食譜| Browse[食譜列表頁\n關鍵字 + 分類篩選]
    Browse -->|點擊食譜| Detail[食譜詳情頁\n含營養標示]

    Action -->|食材組合搜尋| IngSearch[食材搜尋頁\n輸入多種食材標籤]
    IngSearch -->|送出| IngResult[搜尋結果頁\n完全符合 + 部分符合]
    IngResult -->|點擊食譜| Detail

    Action -->|健身者評估| FitFilter[健身食譜篩選\n增肌 / 減脂 / 維持]
    FitFilter -->|點擊食譜| Detail

    Action -->|孕婦專區| PregnancyFilter[孕婦食譜篩選\n孕期階段選擇]
    PregnancyFilter -->|點擊食譜| Detail

    Detail -->|點擊收藏| CheckLogin{是否已登入？}
    CheckLogin -->|否| Auth
    CheckLogin -->|是| Saved[加入我的收藏 ✓]

    Action -->|新增食譜| CheckLogin2{是否已登入？}
    CheckLogin2 -->|否| Auth
    CheckLogin2 -->|是| AddForm[新增食譜表單\n名稱、食材、步驟、圖片]
    AddForm -->|送出成功| Detail

    Action -->|我的收藏| CheckLogin3{是否已登入？}
    CheckLogin3 -->|否| Auth
    CheckLogin3 -->|是| Favorites[我的收藏清單]
    Favorites -->|點擊食譜| Detail
```

---

### 1.2 管理員操作流程

```mermaid
flowchart LR
    AdminStart([管理員開啟網頁]) --> AdminLogin[管理員登入頁]
    AdminLogin -->|驗證成功| Dashboard[後台管理控制台\n總覽數據]

    Dashboard --> AdminAction{選擇管理操作}

    AdminAction -->|管理食譜| RecipeList[食譜列表\n含審核狀態]
    RecipeList -->|核准| Approve[食譜設為公開 ✓]
    RecipeList -->|退回| Reject[食譜設為退回 ✗]
    RecipeList -->|下架| Delete[強制刪除食譜]
    RecipeList -->|編輯| EditForm[編輯食譜表單]
    EditForm -->|儲存| RecipeList

    AdminAction -->|管理使用者| UserList[使用者列表]
    UserList -->|停用帳號| DisableUser[帳號停用 ✓]
    UserList -->|設為管理員| SetAdmin[提升權限]
```

---

## 2. 系統序列圖（Sequence Diagram）

### 2.1 使用者新增食譜流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask Route
    participant Model as Recipe Model
    participant DB as SQLite

    User->>Browser: 填寫新增食譜表單（名稱、食材、步驟）並送出
    Browser->>Route: POST /recipe/add

    Route->>Route: 驗證 session（是否已登入）

    alt 未登入
        Route-->>Browser: 302 重導向至 /auth/login
    else 已登入
        Route->>Route: 驗證表單必填欄位
        alt 表單驗證失敗
            Route-->>Browser: 400 回傳錯誤提示，保留填寫內容
        else 驗證通過
            Route->>Model: create_recipe(data)
            Model->>DB: INSERT INTO recipes (title, desc, ...)
            DB-->>Model: 回傳新 recipe_id
            Model->>DB: INSERT INTO recipe_ingredients (recipe_id, ingredient_id)
            DB-->>Model: 成功
            Model-->>Route: recipe_id
            Route-->>Browser: 302 重導向至 /recipe/<id>
            Browser->>User: 顯示新增成功的食譜詳情頁
        end
    end
```

---

### 2.2 食材組合搜尋食譜流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask Route
    participant Model as Recipe Model
    participant DB as SQLite

    User->>Browser: 輸入食材標籤（如：雞蛋、豆腐、蔥）並送出
    Browser->>Route: GET /recipe/search/ingredients?items=雞蛋,豆腐,蔥

    Route->>Model: search_by_ingredients([雞蛋, 豆腐, 蔥])
    Model->>DB: SELECT recipe_id, COUNT(*) matched\nFROM recipe_ingredients\nWHERE ingredient IN (...)\nGROUP BY recipe_id\nORDER BY matched DESC
    DB-->>Model: 回傳食譜清單（含符合數量）
    Model->>Model: 區分「完全符合」與「部分符合」
    Model-->>Route: {full_match: [...], partial_match: [...]}
    Route-->>Browser: 渲染搜尋結果頁（Jinja2）
    Browser->>User: 顯示符合食材的食譜列表
```

---

### 2.3 使用者登入驗證流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask Route（auth.py）
    participant Model as User Model
    participant DB as SQLite

    User->>Browser: 輸入帳號與密碼，點擊登入
    Browser->>Route: POST /auth/login

    Route->>Model: find_user_by_email(email)
    Model->>DB: SELECT * FROM users WHERE email = ?
    DB-->>Model: 回傳使用者資料（含雜湊密碼）

    alt 使用者不存在
        Route-->>Browser: 顯示「帳號不存在」錯誤
    else 使用者存在
        Model->>Model: check_password_hash(stored_hash, input_pw)
        alt 密碼錯誤
            Route-->>Browser: 顯示「密碼錯誤」提示
        else 密碼正確
            Route->>Route: session['user_id'] = user.id\nsession['role'] = user.role
            Route-->>Browser: 302 重導向至首頁
            Browser->>User: 顯示登入成功狀態
        end
    end
```

---

### 2.4 管理員審核食譜流程

```mermaid
sequenceDiagram
    actor Admin as 管理員
    participant Browser as 瀏覽器
    participant Route as Flask Route（admin.py）
    participant Model as Recipe Model
    participant DB as SQLite

    Admin->>Browser: 點擊「核准」或「下架」按鈕
    Browser->>Route: POST /admin/recipe/<id>/approve\n或 POST /admin/recipe/<id>/delete

    Route->>Route: 驗證 session['role'] == 'admin'

    alt 非管理員
        Route-->>Browser: 403 無權限頁面
    else 管理員身份確認
        Route->>Model: update_recipe_status(id, status)
        Model->>DB: UPDATE recipes SET status = ? WHERE id = ?
        DB-->>Model: 成功
        Model-->>Route: 完成
        Route-->>Browser: 302 重導向回管理食譜列表
        Browser->>Admin: 顯示操作成功提示
    end
```

---

## 3. 功能清單對照表

| 功能描述 | URL 路徑 | HTTP 方法 | 對應 Blueprint | 說明 |
|----------|----------|-----------|----------------|------|
| 首頁（熱門食譜） | `/` | GET | recipe | 呈現首頁與推薦食譜 |
| 食譜列表 + 關鍵字搜尋 | `/recipe/` | GET | recipe | 支援 `?q=` 關鍵字與分類篩選 |
| 食材組合搜尋 | `/recipe/search/ingredients` | GET | recipe | 多食材標籤輸入，回傳符合清單 |
| 健身食譜篩選 | `/recipe/fitness` | GET | recipe | 依 `?goal=` 篩選增肌/減脂/維持 |
| 孕婦食譜篩選 | `/recipe/pregnancy` | GET | recipe | 依孕期階段篩選安全食譜 |
| 食譜詳情頁 | `/recipe/<int:id>` | GET | recipe | 顯示食譜內容與完整營養標示 |
| 新增食譜（表單） | `/recipe/add` | GET | recipe | 顯示新增表單（需登入） |
| 處理新增食譜 | `/recipe/add` | POST | recipe | 驗證並寫入 DB，含食材關聯 |
| 編輯食譜（表單） | `/recipe/<int:id>/edit` | GET | recipe | 顯示編輯表單（限本人或管理員） |
| 處理編輯食譜 | `/recipe/<int:id>/edit` | POST | recipe | 更新 DB 資料 |
| 刪除食譜 | `/recipe/<int:id>/delete` | POST | recipe | 刪除食譜（限本人或管理員） |
| 收藏/取消收藏 | `/recipe/<int:id>/favorite` | POST | recipe | 操作 favorites 關聯資料 |
| 我的收藏清單 | `/user/favorites` | GET | user | 顯示已收藏食譜清單（需登入） |
| 使用者個人頁面 | `/user/profile` | GET | user | 顯示個人資訊與已發布食譜 |
| 註冊頁面 | `/auth/register` | GET | auth | 顯示註冊表單 |
| 處理註冊 | `/auth/register` | POST | auth | 驗證欄位、雜湊密碼、建立帳號 |
| 登入頁面 | `/auth/login` | GET | auth | 顯示登入表單 |
| 處理登入 | `/auth/login` | POST | auth | 驗證密碼、建立 Session |
| 登出 | `/auth/logout` | GET | auth | 清除 Session，重導向首頁 |
| 後台控制台 | `/admin/` | GET | admin | 數據總覽（需管理員權限） |
| 後台食譜管理 | `/admin/recipes` | GET | admin | 所有食譜列表與審核狀態 |
| 核准食譜 | `/admin/recipe/<int:id>/approve` | POST | admin | 設定食譜狀態為公開 |
| 下架/刪除食譜 | `/admin/recipe/<int:id>/delete` | POST | admin | 強制刪除違規食譜 |
| 後台使用者管理 | `/admin/users` | GET | admin | 所有使用者列表 |
| 停用使用者帳號 | `/admin/user/<int:id>/disable` | POST | admin | 停用指定帳號 |
