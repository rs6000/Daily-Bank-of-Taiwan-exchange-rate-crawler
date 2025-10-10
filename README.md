# 🤖 臺灣銀行每日即時匯率爬蟲與 API

**專案名稱：Daily-Bank-of-Taiwan-exchange-rate-crawler**

---

## 🚀 專案簡介

本專案使用 **Python** 與 **GitHub Actions** 建立全自動化每日爬蟲，
每日自動從 **臺灣銀行（Bank of Taiwan, BOT）** 官方網站擷取即時匯率，
並將結果格式化為 JSON (`rates.json`)，公開於 GitHub Pages，
可作為免費、即時的外匯 API。

---

## 💡 API 使用方式

啟用 GitHub Pages 後，即可透過下列 URL 取得匯率資料：

> ⚠️ 將下列範例中的 `rs6000` 替換為您的 GitHub 帳號。

```
https://rs6000.github.io/Daily-Bank-of-Taiwan-exchange-rate-crawler/data/rates.json
```

---

## 📑 JSON 數據格式 2025-10-10 更改

```json
{
    "base_currency": "TWD",
    "source": "Bank of Taiwan (BOT)",
    "last_updated_taipei": "2025-10-10T09:10:45.123456+08:00",
    "history": {
        "2025-10-08": {
            "USD": {
                "即期買入": "32.22",
                "即期賣出": "32.32"
            },
            "JPY": {
                "即期買入": "0.2051",
                "即期賣出": "0.2101"
            }
        },
        "2025-10-09": {
            "USD": {
                "即期買入": "32.25",
                "即期賣出": "32.35"
            },
            "JPY": {
                "即期買入": "0.2060",
                "即期賣出": "0.2110"
            }
            // ... (該日所有其他幣別)
        },
        "2025-10-10": {
            // ... (最新一天的匯率數據)
        },
    }
}
```



### 欄位說明
| 欄位名稱 | 說明 |
| :--- | :--- |
| `base_currency` | 基礎幣別（固定為新臺幣 TWD） |
| `source` | 資料來源（臺灣銀行） |
| `last_updated_taipei` | **檔案最近更新時間**（Action Bot 執行時間，臺北時區 GMT+8） |
| `history` | 核心數據：以**日期**為鍵（Key）的歷史匯率記錄字典 |
| 日期鍵 (`"YYYY-MM-DD"`) | `history` 下的子鍵，包含該日所有幣別的匯率數據 |
| 幣別鍵 (`"USD"`) | 日期鍵下的子鍵，包含該幣別的即期買入和賣出價格 |
| `即期買入` | 臺灣銀行買入外幣價（對客戶為賣出價） |
| `即期賣出` | 臺灣銀行賣出外幣價（對客戶為買入價） |
#### 這個結構讓您能夠輕鬆地透過日期和幣別進行查詢：
```script
// 範例：前端如何獲取 10/09 的日圓即期賣出價
const rate = data.history['2025-10-09']['JPY']['即期賣出'];
```

---

## ⚙️ 部署與設定

### 1️⃣ 專案結構

| 檔案 / 資料夾 | 說明 |
| :--- | :--- |
| `Exchange-Rates-Gemini.py` | 爬蟲主程式 |
| `.github/workflows/schedule.yml` | GitHub Actions 排程設定 |
| `data/` | 存放 `rates.json` 的資料夾 |

---

### 2️⃣ 啟用 GitHub Pages

1. 進入 **Settings → Pages**
2. 在 **Source / Branch** 選擇主分支（main 或 master）
3. 發佈目錄選擇 `/ (root)`
4. 點擊 **Save**

---

### 3️⃣ 啟用每日自動更新 (GitHub Actions)

1. 前往 **Actions** 分頁  
2. 找到 **Daily Exchange Rate Crawler (BOT - TPE Time)**  
3. 點擊 **Run workflow** 以手動測試  
4. 成功後會每日自動更新 `data/rates.json`

---
📦 Made with ❤️ by ChatGPT & Gemini
📜 MIT License © 2025


