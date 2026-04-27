# API 與路由設計文件 - 個人記帳簿

這份文件基於 PRD、系統架構與資料庫設計，規劃 Flask 的路由、URL 路徑、HTTP 方法及對應的 Jinja2 模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 / 儀表板 | GET | `/` | `index.html` | 顯示當月報表、圓餅圖與近期紀錄 |
| 歷史紀錄列表 | GET | `/records` | `records/index.html` | 顯示所有歷史紀錄，支援查詢與篩選 |
| 新增收支頁面 | GET | `/records/add` | `records/form.html` | 顯示新增收支的表單 |
| 建立收支 | POST | `/records/add` | — | 接收表單，存入 DB，重導向至列表或首頁 |
| 編輯收支頁面 | GET | `/records/<id>/edit` | `records/form.html` | 顯示編輯特定收支的表單 |
| 更新收支 | POST | `/records/<id>/edit` | — | 接收表單，更新 DB，重導向至列表 |
| 刪除收支 | POST | `/records/<id>/delete`| — | 刪除紀錄，重導向至列表 |
| 匯出 CSV | GET | `/records/export` | — | 根據條件產生 CSV 檔案供下載 |
| 帳戶列表 | GET | `/accounts` | `accounts/index.html` | 顯示所有帳戶與餘額 |
| 新增帳戶頁面 | GET | `/accounts/add` | `accounts/form.html` | 顯示新增帳戶表單 |
| 建立帳戶 | POST | `/accounts/add` | — | 接收表單，存入 DB，重導向至帳戶列表 |
| 編輯帳戶頁面 | GET | `/accounts/<id>/edit` | `accounts/form.html` | 顯示編輯帳戶表單 |
| 更新帳戶 | POST | `/accounts/<id>/edit` | — | 接收表單，更新 DB，重導向至帳戶列表 |
| 預算設定頁面 | GET | `/budgets` | `budgets/index.html` | 顯示與設定預算表單 |
| 儲存預算 | POST | `/budgets` | — | 接收表單，更新 DB，重導向至預算頁面 |

## 2. 每個路由的詳細說明

### 2.1 首頁與儀表板 (`app/routes/index.py`)
- **GET `/`**
  - **處理邏輯**：計算當月總收入、總支出，讀取預算進度，並拉取近期紀錄。
  - **輸出**：渲染 `index.html`，傳遞數據供前端 Chart.js 繪圖。

### 2.2 收支紀錄 (`app/routes/record.py`)
- **GET `/records`**
  - **輸入**：可選的 URL query 參數（如 `?month=2023-10` 或 `?category=食`）。
  - **處理邏輯**：呼叫 `Record.get_all()` (搭配篩選條件)。
  - **輸出**：渲染 `records/index.html`。
- **GET `/records/add`**
  - **處理邏輯**：取得所有帳戶列表供下拉選單選擇。
  - **輸出**：渲染 `records/form.html`。
- **POST `/records/add`**
  - **輸入**：表單欄位 `type`, `amount`, `category`, `date`, `description`, `account_id`。
  - **處理邏輯**：驗證資料後呼叫 `Record.create()`。
  - **輸出**：成功後重導向至 `/` 或 `/records`。若失敗則顯示錯誤。
- **GET `/records/<id>/edit`**
  - **處理邏輯**：用 `Record.get_by_id(id)` 取出資料供表單填入。
  - **輸出**：渲染 `records/form.html`。
- **POST `/records/<id>/edit`**
  - **輸入**：更新後的表單欄位。
  - **處理邏輯**：呼叫 `Record.update()`。
  - **輸出**：重導向至 `/records`。
- **POST `/records/<id>/delete`**
  - **處理邏輯**：呼叫 `Record.delete()`。
  - **輸出**：重導向至 `/records`。
- **GET `/records/export`**
  - **處理邏輯**：將篩選後的資料轉為 CSV 格式。
  - **輸出**：回傳 CSV 檔案的 HTTP Response。

### 2.3 帳戶管理 (`app/routes/account.py`)
- **GET `/accounts`**
  - **處理邏輯**：呼叫 `Account.get_all()`，計算目前各帳戶餘額。
  - **輸出**：渲染 `accounts/index.html`。
- **GET `/accounts/add`** / **POST `/accounts/add`**
  - **處理邏輯**：顯示表單或呼叫 `Account.create()`。
- **GET `/accounts/<id>/edit`** / **POST `/accounts/<id>/edit`**
  - **處理邏輯**：顯示表單或呼叫 `Account.update()`。

### 2.4 預算管理 (`app/routes/budget.py`)
- **GET `/budgets`**
  - **處理邏輯**：取得目前所有的預算設定。
  - **輸出**：渲染 `budgets/index.html`。
- **POST `/budgets`**
  - **輸入**：`year_month`, `amount`。
  - **處理邏輯**：若該月已有預算則更新，否則建立 `Budget.create()` 或 `Budget.update()`。
  - **輸出**：重導向回 `/budgets`。

## 3. Jinja2 模板清單

所有頁面均繼承自 `base.html`，以保持共同的導覽列與外觀。

- `templates/base.html`: 共用佈局 (包含 Navbar、CSS/JS 引入)。
- `templates/index.html`: 首頁與儀表板 (報表顯示)。
- `templates/records/index.html`: 收支列表頁。
- `templates/records/form.html`: 新增與編輯收支共用的表單頁。
- `templates/accounts/index.html`: 帳戶列表頁。
- `templates/accounts/form.html`: 新增與編輯帳戶共用的表單頁。
- `templates/budgets/index.html`: 預算設定頁面。

## 4. 路由骨架程式碼
請參考 `app/routes/` 目錄下的 Python 檔案。
