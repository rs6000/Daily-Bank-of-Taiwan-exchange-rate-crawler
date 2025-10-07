# 🤖 臺灣銀行每日匯率爬蟲與 API

**專案名稱：Daily-Bank-of-Taiwan-exchange-rate-crawler**

---

## 🚀 專案簡介

本專案是一個使用 **Python 和 GitHub Actions** 建立的全自動化每日排程爬蟲。

它從**臺灣銀行（Bank of Taiwan, BOT）**的官方網站爬取即時外匯牌告匯率，並將數據格式化為 JSON 檔案。透過 GitHub Pages，您可以將此 JSON 檔案作為一個**免費、公開的 API 接口**供任何應用程式使用。

---

## 💡 快速開始：API 接口 (GitHub Pages)  
一旦您在專案中啟用了 GitHub Pages，您的 API 接口將會是以下格式。

**請將以下 URL 中的 `rs6000` 替換為您的 GitHub 用戶名！**

```bat
https://rs6000.github.io/Daily-Bank-of-Taiwan-exchange-rate-crawler/data/rates.json
```

## 📑 數據格式 (JSON Structure)
API 返回的 JSON 數據結構簡潔明瞭，包含基礎資訊和所有即期匯率。
```json
{
    "base_currency": "TWD",
    "date_fetched_taipei": "2025-10-06T09:10:45.123456+08:00",
    "source": "Bank of Taiwan (BOT)",
    "rates": [
        {
            "幣別": "USD",
            "即期買入": "32.22",
            "即期賣出": "32.32"
        },
        {
            "幣別": "EUR",
            "即期買入": "34.65",
            "即期賣出": "35.05"
        },
        // ... 其他所有幣別數據
    ]
}
```

### 欄位說明
| 欄位名稱 | 說明 |
| :--- | :--- |
| `base_currency` | 基礎幣別，固定為 TWD (新臺幣)。 |
| `date_fetched_taipei` | 數據爬取時間，以 **臺北時區 (GMT+8)** ISO 8601 格式顯示。 |
| `source` | 數據來源：臺灣銀行。 |
| `rates` | 匯率列表，包含所有幣別。 |
| `幣別` | 外幣代碼 (例如 USD, JPY, EUR)。 |
| `即期買入` | 臺灣銀行買入外幣的價格（對客戶來說是賣出價）。 |
| `即期賣出` | **臺灣銀行賣出外幣的價格（對客戶來說是買入價）。** |

## ⚙️ 設置與部署教學
本專案的自動化核心是 GitHub Actions，您只需要配置一次，它就會每日自動運行。 

### 1️⃣ 部署專案檔案
請確保您的儲存庫包含以下檔案（或資料夾）：
| 檔案/資料夾 | 說明 |
| :--- | :--- |
| `Exhange-Rates-Gemini.py` | 爬蟲主程式碼。 |
| `.github/workflows/schedule.yml` | GitHub Actions 排程配置檔。 |
| `data/` | 用於存放生成的 `rates.json` 檔案。 |

### 2️⃣ 啟用 GitHub Pages
這是讓您的 JSON 檔案公開變成 API 的關鍵步驟：

進入您的 GitHub 儲存庫的 Settings。

點擊左側的 Pages。

在 Source 或 Branch 選項中，選擇您的主分支（通常是 main 或 master），並將 / (root) 資料夾設定為發佈來源。

點擊 Save。

### 3️⃣ 檢查 GitHub Actions
進入您的儲存庫的 Actions 頁籤。# 💰 臺灣銀行每日即時匯率爬蟲與 API  
**專案名稱：Daily-Bank-of-Taiwan-exchange-rate-crawler**

---

## 🚀 專案簡介
本專案是一個使用 **Python + GitHub Actions** 建立的全自動化每日排程爬蟲。  

它會從 **臺灣銀行（Bank of Taiwan, BOT）** 官方網站擷取即時外匯牌告匯率，  
並將資料格式化成標準化的 JSON 檔案。  

透過 **GitHub Pages**，即可將此 JSON 轉為 **免費、穩定、公開的 API 接口**，  
可供任何前端、後端、或 App 即時取得最新匯率資料。

---

## 🌐 公開 API 接口
啟用 GitHub Pages 後，API 將自動可用。

> ⚠️ 請將以下範例中的「`rs6000`」替換為您的 GitHub 帳號名稱。

```bash
https://rs6000.github.io/Daily-Bank-of-Taiwan-exchange-rate-crawler/data/rates.json
```

---

## 📊 數據格式 (JSON Structure)

API 會返回一個清晰的 JSON 結構，包含匯率時間、來源與各幣別即期匯率。

```json
{
    "base_currency": "TWD",
    "date_fetched_taipei": "2025-10-06T09:10:45.123456+08:00",
    "source": "Bank of Taiwan (BOT)",
    "rates": [
        {
            "幣別": "USD",
            "即期買入": "32.22",
            "即期賣出": "32.32"
        },
        {
            "幣別": "EUR",
            "即期買入": "34.65",
            "即期賣出": "35.05"
        }
        // ... 其他幣別
    ]
}
```

### 🧩 欄位說明
| 欄位名稱 | 說明 |
|:---|:---|
| `base_currency` | 基礎幣別（固定為 **TWD** 新臺幣）。 |
| `date_fetched_taipei` | 爬取時間（**台北時區 GMT+8**，ISO 8601 格式）。 |
| `source` | 資料來源（臺灣銀行 BOT）。 |
| `rates` | 匯率列表（含各幣別的買入/賣出價）。 |
| `幣別` | 外幣代碼（例如 USD、JPY、EUR）。 |
| `即期買入` | 臺灣銀行買入外幣價格（即客戶賣出價）。 |
| `即期賣出` | 臺灣銀行賣出外幣價格（即客戶買入價）。 |

---

## ⚙️ 自動化部署教學

### 1️⃣ 專案結構
請確保您的儲存庫包含以下內容：

| 檔案/資料夾 | 說明 |
|:---|:---|
| `Exchange-Rates-Gemini.py` | 主要爬蟲程式（自動抓取臺銀匯率）。 |
| `.github/workflows/schedule.yml` | GitHub Actions 排程設定。 |
| `data/` | 儲存輸出的 `rates.json`。 |

---

### 2️⃣ 啟用 GitHub Pages
讓 JSON 成為公開 API 的步驟：

1. 前往 GitHub → **Settings → Pages**
2. 在 **Source / Branch** 選項中選擇主要分支（`main` 或 `master`）
3. 指定資料夾為 `/ (root)`
4. 點擊 **Save**

啟用後數分鐘，您的 API 即可線上使用 🎉

---

### 3️⃣ 啟用 GitHub Actions 自動排程
1. 前往 GitHub → **Actions**
2. 找到工作流程 **「Daily Exchange Rate Crawler (BOT - TPE Time)」**
3. 點擊 **Run workflow** 可立即手動執行一次
4. 成功後，Actions Bot 會自動提交更新後的 `data/rates.json`

之後將會每日自動執行一次（依 `schedule.yml` 設定的時間）。

---

## 🧠 小提醒
- JSON 會每日更新一次，時間基於台北時區。
- 若要手動更新，可直接重新執行 GitHub Actions。
- 若您 fork 專案，請先檢查 **workflow 權限** 及 **GitHub Pages 設定** 是否開啟。

---

## ❤️ 備註

在左側選擇 Daily Exchange Rate Crawler (BOT - TPE Time) 工作流。

您可以點擊右上角的 Run workflow 按鈕，手動觸發一次運行以進行首次測試。

成功運行後，GitHub Actions Bot 將會自動提交最新的 data/rates.json 檔案到您的儲存庫，並透過 GitHub Pages 公開。

---
📦 Made with ❤️ by ChatGPT & Gemini
📜 MIT License © 2025


