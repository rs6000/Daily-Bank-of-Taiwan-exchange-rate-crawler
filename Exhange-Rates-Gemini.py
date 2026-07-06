import pandas as pd
import json
from datetime import datetime, UTC
import sys
import os
import pytz
import io
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# --- 設定 ---
URL = "https://rate.bot.com.tw/xrt?Lang=zh-TW"
# 將輸出檔案名稱改為 history.json 更能體現其內容
OUTPUT_FILE = "data/history.json" 
SOURCE_NAME = "Bank of Taiwan (BOT)"
BASE_CURRENCY = "TWD"

def fetch_and_process_rates():
    """
    從台灣銀行網頁爬取匯率並處理成結構化數據。（相容 GitHub Actions 與本地端）
    """
    print(f"Fetching data from {SOURCE_NAME} using Selenium...")
    
    # --- 設定防崩潰與 GitHub Actions 相容的瀏覽器參數 ---
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")          # 強制無頭模式（背景執行）
    chrome_options.add_argument("--no-sandbox")             # Linux 環境防權限崩潰
    chrome_options.add_argument("--disable-dev-shm-usage") # 防止記憶體不足崩潰
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    try:
        # 啟動瀏覽器並載入網頁
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(URL)
        
        # 等待 5 秒鐘讓網頁繞過 Challenge Validation 挑戰並完整載入
        time.sleep(5)
        
        # 取得通過驗證後的 HTML
        page_source = driver.page_source
        driver.quit()

        # 將 HTML 字串交給 Pandas 解析（使用 io.StringIO 符合新版規範）
        html_data = io.StringIO(page_source)
        dfs = pd.read_html(html_data, encoding='utf-8', flavor='lxml')
        currency = dfs[0]
    except Exception as e:
        print(f"Error fetching or parsing HTML via Selenium: {e}", file=sys.stderr)
        return None

    # --- 資料清洗與轉換（保持你原本的邏輯與結構） ---
    # 修正切片：0是幣別、3是即期買入、4是即期賣出
    currency_fix = currency.iloc[:, [0, 3, 4]].copy()
    currency_fix.columns = [u'幣別', u'即期買入', u'即期賣出']
    currency_fix[u'幣別'] = currency_fix[u'幣別'].str.extract(r'\((\w+)\)')
    currency_final = currency_fix[
        (currency_fix[u'即期買入'] != '-') & (currency_fix[u'即期賣出'] != '-')
    ].reset_index(drop=True)
    
    # 結構變為: {'USD': {'即期買入': '32.22', '即期賣出': '32.32'}, ...}
    daily_rates_data = currency_final.set_index(u'幣別').T.to_dict()
    
    return daily_rates_data


def save_to_history(new_daily_data):
    """
    讀取舊的歷史數據，新增當日資料，然後存回檔案。
    """
    # 設置爬取時間 - 轉換成台北時區
    utc_now = datetime.now(UTC) 
    taipei_tz = pytz.timezone('Asia/Taipei')
    taipei_now = utc_now.astimezone(taipei_tz)
    
    # 取得當天的日期鍵 (例如: '2025-10-09')
    date_key = taipei_now.strftime('%Y-%m-%d')
    # 取得完整的時間字串 (用於 last_updated_taipei)
    time_string = taipei_now.isoformat()
    
    # 1. 嘗試讀取現有的歷史檔案
    history_data = {}
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
        except json.JSONDecodeError:
            print("Warning: Existing history file is corrupted. Starting a new history.", file=sys.stderr)
        except FileNotFoundError:
            pass # 檔案不存在，history_data 保持為 {}
    
    # 2. 初始化頂層結構
    if 'history' not in history_data:
        history_data['base_currency'] = BASE_CURRENCY
        history_data['source'] = SOURCE_NAME
        history_data['last_updated_taipei'] = time_string 
        history_data['history'] = {} 
    

    # 3. 插入新的每日數據
    if new_daily_data:
        history_data['last_updated_taipei'] = time_string 
        history_data['history'][date_key] = new_daily_data
        
        
    try:
        # 4. 寫回檔案
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, ensure_ascii=False, indent=4)
        
        print(f"Successfully saved historical data to {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"Error saving file: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    daily_rates = fetch_and_process_rates()
    
    if daily_rates:
        print("\n--- JSON Data Output Preview (中文顯示) ---")
        json_preview = json.dumps(daily_rates, indent=4, ensure_ascii=False)
        print(json_preview[:500] + "\n...") 
        
        # 呼叫儲存函數
        save_to_history(daily_rates)
    else:
        print("Failed to fetch or process rate data. Exiting.", file=sys.stderr)
        sys.exit(1)