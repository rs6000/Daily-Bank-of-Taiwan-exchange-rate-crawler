import pandas as pd
import json
from datetime import datetime, UTC
import sys
import os
import pytz

# --- 設定 ---
URL = "https://rate.bot.com.tw/xrt?Lang=zh-TW"
# 將輸出檔案名稱改為 history.json 更能體現其內容
OUTPUT_FILE = "data/history.json" 
SOURCE_NAME = "Bank of Taiwan (BOT)"
BASE_CURRENCY = "TWD"

def fetch_and_process_rates():
    """
    從台灣銀行網頁爬取匯率並處理成結構化數據。
    """
    print(f"Fetching data from {SOURCE_NAME}...")
    
    # ... (HTML 爬取和 DataFrame 處理邏輯保持不變)
    try:
        dfs = pd.read_html(URL, encoding='utf-8')
        currency = dfs[0]
    except Exception as e:
        print(f"Error fetching or parsing HTML: {e}", file=sys.stderr)
        return None

    currency_fix = currency.iloc[:, [0, 1, 2]].copy()
    currency_fix.columns = [u'幣別', u'即期買入', u'即期賣出']
    currency_fix[u'幣別'] = currency_fix[u'幣別'].str.extract(r'\((\w+)\)')
    currency_final = currency_fix[
        (currency_fix[u'即期買入'] != '-') & (currency_fix[u'即期賣出'] != '-')
    ].reset_index(drop=True)
    
    # --- 關鍵修改點 1: 轉換為新的結構 ---
    
    # 將 DataFrame 設置 '幣別' 為索引，並轉換為字典
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
        # *** 修正：將所有頂層鍵依序初始化 ***
        history_data['base_currency'] = BASE_CURRENCY
        history_data['source'] = SOURCE_NAME
        history_data['last_updated_taipei'] = time_string # 確保它在 history 之前
        history_data['history'] = {} 
   

    # 3. 插入新的每日數據
    if new_daily_data:
        # 更新 last_updated_taipei 的值，而不是重新插入
        history_data['last_updated_taipei'] = time_string 
        history_data['history'][date_key] = new_daily_data
        
        
    try:
        # 4. 寫回檔案
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            # 確保寫入檔案時，中文不會被編碼成 \uXXXX
            json.dump(history_data, f, ensure_ascii=False, indent=4)
        
        print(f"Successfully saved historical data to {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"Error saving file: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    daily_rates = fetch_and_process_rates()
    
    if daily_rates:
        print("\n--- JSON Data Output Preview (中文顯示) ---")
        
        # 為了預覽，我們只顯示當日抓取到的數據
        json_preview = json.dumps(
            daily_rates, 
            indent=4, 
            ensure_ascii=False 
        )
        
        # 為了避免輸出過長，只印出開頭 500 個字符
        print(json_preview[:500] + "\n...") 
        
        # 呼叫新的儲存函數
        save_to_history(daily_rates)
    else:
        # 如果爬取失敗，以錯誤狀態碼 (1) 退出
        print("Failed to fetch or process rate data. Exiting.", file=sys.stderr)
        sys.exit(1)