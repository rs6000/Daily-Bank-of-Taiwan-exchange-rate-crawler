import pandas as pd
import json
from datetime import datetime, UTC
import sys
import os
import pytz
import logging 

# --- 設定 ---
URL = "https://rate.bot.com.tw/xrt?Lang=zh-TW"
OUTPUT_FILE = "data/history.json" 
LOG_FILE = "data/app.log" 
SOURCE_NAME = "Bank of Taiwan (BOT)"
BASE_CURRENCY = "TWD"

# --- 日誌配置 ---
# 確保 data 資料夾存在 (log 和 json 都會放在這裡)
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True) 

# 配置日誌格式：時間, 日誌級別, 訊息 (同時輸出到檔案和控制台)
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'), 
        logging.StreamHandler(sys.stdout) 
    ]
)
logger = logging.getLogger(__name__)

def fetch_and_process_rates():
    """從台灣銀行網頁爬取匯率並處理成結構化數據。"""
    logger.info(f"--- 開始執行爬蟲：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
    logger.info(f"Fetching data from {SOURCE_NAME}...")
    
    try:
        dfs = pd.read_html(URL, encoding='utf-8')
        currency = dfs[0]
        logger.info("Successfully fetched HTML content.")
    except Exception as e:
        logger.error(f"Error fetching or parsing HTML: {e}")
        return None

    try:
        currency_fix = currency.iloc[:, [0, 1, 2]].copy()
        currency_fix.columns = [u'幣別', u'即期買入', u'即期賣出']
        currency_fix[u'幣別'] = currency_fix[u'幣別'].str.extract(r'\((\w+)\)')
        currency_final = currency_fix[
            (currency_fix[u'即期買入'] != '-') & (currency_fix[u'即期賣出'] != '-')
        ].reset_index(drop=True)
        
        # 轉換為以幣別為鍵的字典結構
        daily_rates_data = currency_final.set_index(u'幣別').T.to_dict()
        logger.info(f"Data processed. Found {len(daily_rates_data)} valid currency rates.")
        
        return daily_rates_data
    
    except Exception as e:
        logger.error(f"Error during data processing: {e}")
        return None


def save_to_history(new_daily_data):
    """讀取舊的歷史數據，新增當日資料，然後存回檔案。"""
    # 設置時間
    utc_now = datetime.now(UTC) 
    taipei_tz = pytz.timezone('Asia/Taipei')
    taipei_now = utc_now.astimezone(taipei_tz)
    
    date_key = taipei_now.strftime('%Y-%m-%d')
    time_string = taipei_now.isoformat()
    
    # 1. 嘗試讀取現有的歷史檔案
    history_data = {}
    logger.info(f"Attempting to read existing file: {OUTPUT_FILE}")
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
            logger.info("Existing history file loaded successfully.")
        except json.JSONDecodeError:
            logger.warning("Existing history file is corrupted (JSONDecodeError). Starting a new history.")
        except FileNotFoundError:
            pass 
    
    # 2. 初始化頂層結構
    if 'history' not in history_data:
        history_data['base_currency'] = BASE_CURRENCY
        history_data['source'] = SOURCE_NAME
        history_data['history'] = {}
        logger.info("Initialized new history structure.")

    # 3. 插入新的每日數據
    if new_daily_data:
        history_data['history'][date_key] = new_daily_data
        history_data['last_updated_taipei'] = time_string
        logger.info(f"Inserted new rates for date: {date_key}. Total dates in history: {len(history_data['history'])}.")
        
    try:
        # 4. 寫回檔案
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, ensure_ascii=False, indent=4)
        
        logger.info(f"Successfully wrote data to {OUTPUT_FILE}")
        
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    daily_rates = fetch_and_process_rates()
    
    if daily_rates:
        # 輸出預覽到 Actions log
        print("\n--- JSON Data Output Preview (中文顯示) ---")
        json_preview = json.dumps(
            daily_rates, 
            indent=4, 
            ensure_ascii=False 
        )
        print(json_preview[:500] + "\n...") 
        
        save_to_history(daily_rates)
        logger.info(f"--- 程式執行結束。結果已儲存於 {OUTPUT_FILE} 及 {LOG_FILE} ---")
    else:
        logger.error("Failed to fetch or process rate data. Exiting with error code 1.")
        sys.exit(1)
        
    # 關鍵：強制關閉日誌系統，確保 app.log 寫入完成
    logging.shutdown()