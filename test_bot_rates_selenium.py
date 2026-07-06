import pandas as pd
import json
import sys
import io
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

URL = "https://rate.bot.com.tw/xrt?Lang=zh-TW"

def test_fetch_rates_selenium():
    print("====== 1. 初始化真實瀏覽器 (無頭模式) ======")
    chrome_options = Options()
    # 啟用無頭模式（不跳出瀏覽器視窗，在背景執行）
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    # 偽裝真實瀏覽器特徵
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        
        print("\n====== 2. 瀏覽器正在載入網頁並通過驗證 ======")
        driver.get(URL)
        
        # 靜置 5 秒鐘，讓網頁完成 JavaScript 驗證挑戰與資料載入
        print("等待 5 秒讓網頁挑戰載入...")
        time.sleep(5)
        
        # 取得通過驗證後的完整網頁原始碼
        page_source = driver.page_source
        driver.quit()
        
        print("\n====== 3. 開始解析 HTML 表格 ======")
        html_data = io.StringIO(page_source)
        dfs = pd.read_html(html_data, flavor='lxml')
        currency = dfs[0]
        print(f"成功找到表格！原始資料筆數: {len(currency)} 筆")
        
        print("\n====== 4. 欄位篩選與資料清洗 ======")
        currency_fix = currency.iloc[:, [0, 3, 4]].copy()
        currency_fix.columns = ['幣別', '即期買入', '即期賣出']
        currency_fix['幣別'] = currency_fix['幣別'].str.extract(r'\((\w+)\)')
        
        currency_final = currency_fix[
            (currency_fix['即期買入'] != '-') & (currency_fix['即期賣出'] != '-')
        ].reset_index(drop=True)
        
        daily_rates_data = currency_final.set_index('幣別').T.to_dict()
        return daily_rates_data

    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    result = test_fetch_rates_selenium()
    
    if result:
        print("\n✅ 【測試成功】突破防火牆挑戰！")
        print(json.dumps(result, indent=4, ensure_ascii=False))
    else:
        print("\n❌ 【測試失敗】即便使用模擬瀏覽器也無法穿透驗證。")