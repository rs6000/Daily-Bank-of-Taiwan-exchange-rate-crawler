import pandas as pd
import json
from datetime import datetime, UTC # <-- 新增導入 UTC
import sys
import os
import pytz # 用於處理時區轉換

# --- 設定 ---
URL = "https://rate.bot.com.tw/xrt?Lang=zh-TW"
OUTPUT_FILE = "data/rates.json"
SOURCE_NAME = "Bank of Taiwan (BOT)"
BASE_CURRENCY = "TWD" # 數據以新台幣為基礎

def fetch_and_process_rates():
    """
    從台灣銀行網頁爬取匯率並處理成結構化數據。
    """
    print(f"Fetching data from {SOURCE_NAME}...")
    
    try:
        # 讀取網頁：pd.read_html 會返回網頁中所有表格的 DataFrame 列表
        dfs = pd.read_html(URL, encoding='utf-8')
        currency = dfs[0]
    except Exception as e:
        print(f"Error fetching or parsing HTML: {e}", file=sys.stderr)
        return None

    # 1. 擷取需要的欄位 (幣別/即期買入/即期賣出)
    # 修正警告：使用 .copy() 確保 currency_fix 是一個獨立的 DataFrame 副本
    currency_fix = currency.iloc[:, [0, 1, 2]].copy() 
    currency_fix.columns = [u'幣別', u'即期買入', u'即期賣出']

    # 2. 清除幣別欄重複字元，提取括號內的幣別代碼
    # 由於上面使用了 .copy()，這裡的賦值操作不會再觸發 SettingWithCopyWarning
    currency_fix[u'幣別'] = currency_fix[u'幣別'].str.extract(r'\((\w+)\)')

    # 3. 過濾掉有空值或無效值 ('-') 的紀錄
    currency_final = currency_fix[
        (currency_fix[u'即期買入'] != '-') & (currency_fix[u'即期賣出'] != '-')
    ].reset_index(drop=True)
    
    # --- 轉換為 JSON 結構 ---
    
    # 設置爬取時間 - 轉換成台北時區 (Asia/Taipei, GMT+8)
    
    # 修正棄用警告：使用 datetime.now(UTC) 取得時區感知 (timezone-aware) 的 UTC 時間
    utc_now = datetime.now(UTC) 
    taipei_tz = pytz.timezone('Asia/Taipei')
    taipei_now = utc_now.astimezone(taipei_tz)
    
    # 格式化為 ISO 8601 字符串 (包含 +08:00 資訊)
    current_time_taipei = taipei_now.isoformat()
    
    # 將 DataFrame 轉換為適合 API 的字典列表
    rates_list = currency_final.to_dict(orient='records')
    
    # 建立最終的 JSON 物件
    final_data = {
        "base_currency": BASE_CURRENCY,
        "date_fetched_taipei": current_time_taipei, 
        "source": SOURCE_NAME,
        "rates": rates_list
    }
    
    return final_data

def save_to_json(data):
    """
    將資料儲存為 JSON 檔案。
    """
    try:
        # 確保 data 資料夾存在
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            # 確保寫入檔案時，中文不會被編碼成 \uXXXX
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"Successfully saved data to {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"Error saving file: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    rate_data = fetch_and_process_rates()
    
    if rate_data and rate_data['rates']:
        print("\n--- JSON Data Output Preview (中文顯示) ---")
        
        # 輸出到終端機時，也要指定 ensure_ascii=False 才能正確顯示中文
        json_preview = json.dumps(
            rate_data, 
            indent=4, 
            ensure_ascii=False 
        )
        
        # 為了避免輸出過長，只印出開頭 500 個字符
        print(json_preview[:500] + "\n...") 
        
        save_to_json(rate_data)
    else:
        # 如果爬取失敗，以錯誤狀態碼 (1) 退出，讓 GitHub Action 報告失敗
        print("Failed to fetch or process rate data. Exiting.", file=sys.stderr)
        sys.exit(1)