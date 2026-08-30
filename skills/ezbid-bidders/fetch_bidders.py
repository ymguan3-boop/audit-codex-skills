#!/usr/bin/env python3
"""
ezbid.tw 投標廠商資料抓取腳本
從台灣政府採購與標案情報站抓取各標案的投標廠商列表

使用方式：
    python fetch_bidders.py              # 抓取所有標案
    python fetch_bidders.py --limit 10    # 僅抓取前10筆
    python fetch_bidders.py --test        # 測試模式（僅抓取1筆）

資料來源：
    ezbid.tw（台灣政府採購與標案情報站）
    資料來源為政府電子採購網（PCC），每日更新三次
"""

import os
import sys
import json
import time
import sqlite3
import argparse
from pathlib import Path
from datetime import datetime

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("請先安裝 playwright: pip install playwright && playwright install chromium")
    sys.exit(1)

# 設定路徑
SCRIPT_DIR = Path(__file__).parent
DEFAULT_DB_PATH = SCRIPT_DIR / '政府採購決標資訊研析系統.db'
LOG_DIR = SCRIPT_DIR / 'logs'

def log(message, log_file=None):
    """記錄訊息"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f'[{timestamp}] {message}'
    print(line)
    if log_file:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(line + '\n')

def get_tenders_from_db(db_path, limit=None):
    """從資料庫取得標案清單"""
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # 取得所有標案
    query = '''
        SELECT DISTINCT "標案案號", "機關代碼", "機關名稱", "標案名稱" 
        FROM "1080101-1141231宜蘭縣"
    '''
    if limit:
        query += f' LIMIT {limit}'
    
    cursor.execute(query)
    tenders = cursor.fetchall()
    conn.close()
    
    return tenders

def fetch_tender_bidders(page, agency_code, tender_id):
    """從 ezbid.tw 抓取標案的投標廠商列表"""
    url = f'https://ezbid.tw/detail/{agency_code}/{tender_id}'
    
    try:
        page.goto(url, wait_until='networkidle', timeout=30000)
        time.sleep(2)
        
        # 向下捲動以載入完整內容
        page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(2)
        
        # 解析投標廠商列表
        bidders = page.evaluate('''() => {
            const bidders = [];
            const bodyText = document.body.innerText || '';
            
            // 尋找投標廠商列表區塊
            const match = bodyText.match(/投標廠商列表\\s*\\(共\\s*(\\d+)\\s*家\\)([\\s\\S]*?)(?:詳細資料|延伸探索|$)/);
            if (match) {
                const vendorSection = match[2];
                const lines = vendorSection.split('\\n');
                
                for (const line of lines) {
                    const trimmed = line.trim();
                    
                    // 跳過空行和標題
                    if (!trimmed || trimmed.startsWith('廠商名稱')) {
                        continue;
                    }
                    
                    // 使用 Tab 分隔解析
                    const parts = trimmed.split('\\t');
                    if (parts.length >= 2) {
                        const vendorName = parts[0].trim();
                        
                        // 跳過空廠商名稱
                        if (!vendorName) {
                            continue;
                        }
                        
                        // 從所有欄位中尋找狀態和金額
                        let status = '';
                        let bidAmount = null;
                        let priceDiff = null;
                        
                        for (let i = 1; i < parts.length; i++) {
                            const part = parts[i].trim();
                            if (part === 'WINNER' || part === '未得標') {
                                status = part;
                            } else if (part.startsWith('$')) {
                                const amountText = part.replace(/[$,]/g, '');
                                if (amountText && amountText !== '--') {
                                    bidAmount = parseFloat(amountText);
                                }
                            } else if (part && part !== '--' && !part.startsWith('.detail')) {
                                // 如果不是狀態也不是金額，可能是價差
                                priceDiff = part;
                            }
                        }
                        
                        // 如果找不到狀態，預設為未得標
                        if (!status) {
                            status = '未得標';
                        }
                        
                        bidders.push({
                            vendorName: vendorName,
                            status: status,
                            bidAmount: bidAmount,
                            priceDiff: priceDiff
                        });
                    }
                }
            }
            
            return bidders;
        }''')
        
        return bidders
        
    except Exception as e:
        return []

def save_bidders(db_path, tender_id, agency_code, agency_name, tender_name, bidders):
    """儲存投標廠商資料到資料庫"""
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # 確保資料表存在
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS 投標廠商 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            標案案號 TEXT NOT NULL,
            機關代碼 TEXT,
            機關名稱 TEXT,
            標案名稱 TEXT,
            廠商名稱 TEXT NOT NULL,
            是否得標 TEXT,
            投標金額 REAL,
            價差 TEXT,
            更新時間 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(標案案號, 廠商名稱)
        )
    ''')
    
    saved_count = 0
    for bidder in bidders:
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO 投標廠商 
                (標案案號, 機關代碼, 機關名稱, 標案名稱, 廠商名稱, 是否得標, 投標金額, 價差)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                tender_id,
                agency_code,
                agency_name,
                tender_name,
                bidder['vendorName'],
                '是' if bidder['status'] == 'WINNER' else '否',
                bidder.get('bidAmount'),
                bidder.get('priceDiff')
            ))
            saved_count += 1
        except Exception as e:
            pass
    
    conn.commit()
    conn.close()
    
    return saved_count

def main():
    parser = argparse.ArgumentParser(description='ezbid.tw 投標廠商資料抓取')
    parser.add_argument('--db', type=str, default=None, help='資料庫路徑（預設: 腳本同層目錄）')
    parser.add_argument('--limit', type=int, default=None, help='限制抓取筆數')
    parser.add_argument('--test', action='store_true', help='測試模式（僅抓取1筆）')
    args = parser.parse_args()
    
    # 設定資料庫路徑
    db_path = Path(args.db) if args.db else DEFAULT_DB_PATH
    if not db_path.exists():
        print(f"資料庫不存在: {db_path}")
        sys.exit(1)
    
    # 設定 log 檔案
    LOG_DIR.mkdir(exist_ok=True)
    log_file = LOG_DIR / f'fetch_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    
    # 測試模式
    limit = 1 if args.test else args.limit
    
    log('開始抓取 ezbid.tw 投標廠商資料...', log_file)
    log(f'資料庫: {db_path}', log_file)
    
    # 取得標案清單
    tenders = get_tenders_from_db(db_path, limit)
    log(f'共 {len(tenders)} 個標案', log_file)
    
    success_count = 0
    fail_count = 0
    total_bidders = 0
    
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        
        for i, (tender_id, agency_code, agency_name, tender_name) in enumerate(tenders):
            log(f'[{i+1}/{len(tenders)}] {tender_id} - {tender_name[:30]}', log_file)
            
            # 抓取投標廠商
            bidders = fetch_tender_bidders(page, agency_code, tender_id)
            
            if bidders:
                saved = save_bidders(db_path, tender_id, agency_code, agency_name, tender_name, bidders)
                log(f'  找到 {len(bidders)} 家廠商，儲存 {saved} 筆', log_file)
                success_count += 1
                total_bidders += len(bidders)
            else:
                log(f'  未找到投標廠商資訊', log_file)
                fail_count += 1
            
            # 避免過度請求
            time.sleep(1)
        
        browser.close()
    
    log(f'完成！成功: {success_count}, 失敗: {fail_count}, 共 {total_bidders} 家廠商', log_file)
    print(f'\n詳細記錄請查看: {log_file}')

if __name__ == '__main__':
    main()
