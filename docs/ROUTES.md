# 路由設計文件 (ROUTES)

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 | GET | `/` | `templates/index.html` | 顯示網站入口、系統介紹與功能導覽 |
| 會員註冊頁面 | GET | `/auth/register` | `templates/auth/register.html` | 顯示註冊表單 |
| 處理會員註冊 | POST | `/auth/register` | — | 接收表單、加密密碼存入 DB，註冊成功後重導向 |
| 會員登入頁面 | GET | `/auth/login` | `templates/auth/login.html` | 顯示登入表單 |
| 處理會員登入 | POST | `/auth/login` | — | 驗證帳號密碼，成功後寫入 Session、重導向至首頁 |
| 會員登出 | GET | `/auth/logout` | — | 清除 Session 並重導向至首頁 |
| 會員歷史紀錄 | GET | `/profile/history` | `templates/profile/history.html` | 顯示會員過去所有的抽籤與測算紀錄 |
| 求籤與擲筊頁面 | GET | `/fortune/draw` | `templates/fortune/draw.html` | 顯示求籤動畫與擲筊介面 |
| 產生抽籤結果 | POST | `/fortune/draw` | — | 伺服器端隨機抽籤、儲存 `Record` 進 DB、重導向至結果頁面 |
| 籤詩結果與分享 | GET | `/fortune/result/<record_id>` | `templates/fortune/result.html` | 根據紀錄 ID 顯示籤詩結果、解籤並且提供分享按鈕 |
| 捐獻香油錢頁面 | GET | `/donate` | `templates/donate/index.html` | 顯示捐款方案、付款資訊與表單 |
| 處理捐獻與回傳 | POST | `/donate/success` | `templates/donate/success.html` | 接收付款表單或第三方金流回傳，顯示感謝神明畫面 |
| 捐獻完成(直接瀏覽)| GET | `/donate/success` | `templates/donate/success.html` | 直接瀏覽感謝頁面 |

## 2. 每個路由的詳細說明

### 首頁 (`/main/`)
- URL: `/` (GET)
- 處理邏輯: 處理首頁請求，判斷是否已登入來決定顯示登入狀態。
- 輸出: 渲染 `templates/index.html`。

### 會員模組 (`/auth/`)
- URL: `/auth/register` (GET)
  - 處理邏輯: 顯示註冊表單。
  - 輸出: 渲染 `templates/auth/register.html`。
- URL: `/auth/register` (POST)
  - 輸入: `username`, `password`, `confirm_password`。
  - 處理邏輯: 驗證欄位是否為空、兩次密碼是否一致、檢查帳號是否重複。呼叫 `User.create` 建立帳號。
  - 輸出: 成功重導向至 `/auth/login`，失敗導回 `register` 顯示錯誤。
- URL: `/auth/login` (GET)
  - 處理邏輯: 顯示登入表單。
  - 輸出: 渲染 `templates/auth/login.html`。
- URL: `/auth/login` (POST)
  - 輸入: `username`, `password`。
  - 處理邏輯: 呼叫 `User.get_by_username`，比對 bcrypt 密碼。驗證成功建立 session。
  - 輸出: 成功重導向至 `/`，失敗重導向至 `/auth/login`。
- URL: `/auth/logout` (GET)
  - 處理邏輯: 清除 session 中的 user 資訊。
  - 輸出: 重導向至 `/`。
- URL: `/profile/history` (GET)
  - 處理邏輯: 驗證登入狀態。呼叫 `Record.get_by_user_id` 取得所有歷史紀錄。
  - 輸出: 將資料傳給 `templates/profile/history.html` 渲染。

### 抽籤測算模組 (`/fortune/`)
- URL: `/fortune/draw` (GET)
  - 處理邏輯: 必須登入（否則導向登入頁面）。準備求籤頁面環境。
  - 輸出: 渲染 `templates/fortune/draw.html`。
- URL: `/fortune/draw` (POST)
  - 輸入: 使用者提交求籤動作 (表單 POST)。
  - 處理邏輯: 呼叫 `Lot.get_random` 重後端取得一張籤，接著呼叫 `Record.create(user_id, lot_id)`。
  - 輸出: 重導向至 `/fortune/result/<record_id>`。
- URL: `/fortune/result/<record_id>` (GET)
  - 輸入: URL PATH 變數 `record_id`。
  - 處理邏輯: 呼叫 `Record.get_by_id(record_id)`，如果找不到回傳 404，如果找到了則檢查權限（公開分享或僅限本人，取決於隱私設定，本 MVP 允許公開存取以便社群分享）。
  - 輸出: 渲染 `templates/fortune/result.html`。

### 香油錢模組 (`/donate/`)
- URL: `/donate` (GET)
  - 處理邏輯: 顯示捐贈表單與付款指示。
  - 輸出: 渲染 `templates/donate/index.html`。
- URL: `/donate/success` (GET, POST)
  - 輸入: (POST) 付款相關資訊表單欄位。
  - 處理邏輯: 紀錄已成功收到香油錢（本專案暫以展示感謝頁為主）。
  - 輸出: 渲染 `templates/donate/success.html`。

## 3. Jinja2 模板清單

所有的模板將繼承自基礎樣板 `layout.html` 以保持風格統一。

1. `templates/layout.html` (Base template, 包含 Header, Footer)
2. `templates/index.html` (首頁)
3. `templates/auth/register.html` (註冊表單)
4. `templates/auth/login.html` (登入表單)
5. `templates/profile/history.html` (歷史紀錄列表頁面)
6. `templates/fortune/draw.html` (求籤流程、動畫頁面)
7. `templates/fortune/result.html` (抽籤結果、解籤說明與分享頁面)
8. `templates/donate/index.html` (香油錢首頁)
9. `templates/donate/success.html` (捐獻感謝頁面)

## 4. 路由骨架程式碼
開發人員將根據此文件，實作位於 `app/routes/` 裡的這些檔案與 Flask Blueprint 功能：
- `__init__.py`
- `main.py`
- `auth.py`
- `fortune.py`
- `donate.py`
