#!/usr/bin/env python3
"""
PCIC 標案資料匯出腳本
自動導航至「標案自選欄位表」，設定條件後匯出 Excel。

使用方式：
    python run_export.py                          # 預設模式
    python run_export.py --yilan                  # 宜蘭縣全額度匯出（含所屬機關、預算0起）
    python run_export.py --export-dir DIR         # 指定匯出目錄

依賴：
    pip install playwright
    playwright install chromium
"""
import sys, os, time, argparse
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = 'https://pcic.pcc.gov.tw/pwc-web/service/bidAta001'


def set_yilan_full_export(page, log):
    """設定宜蘭縣全額度匯出條件：列印層級=含所屬機關、預算=0起"""
    log('  [宜蘭模式] 設定列印層級=含所屬機關')
    try:
        page.evaluate('''() => {
            // 找「列印層級」的 radio button，選「含所屬機關」
            const radios = document.querySelectorAll('input[type="radio"]');
            for (const r of radios) {
                const label = r.closest('label') || document.querySelector(`label[for="${r.id}"]`);
                const text = label ? label.textContent : r.value;
                if (text.includes('含所屬機關') || r.value.includes('含所屬')) {
                    r.click();
                    r.dispatchEvent(new Event('change', {bubbles: true}));
                    return '已選含所屬機關';
                }
            }
            return '未找到含所屬機關';
        }''')
        log('  [宜蘭模式] 列印層級已設定')
    except Exception as e:
        log(f'  [宜蘭模式] 列印層級設定失敗: {str(e)[:50]}')

    log('  [宜蘭模式] 設定預算=0起')
    try:
        page.evaluate('''() => {
            const sels = document.querySelectorAll('select');
            for (let i = 0; i < sels.length; i++) {
                const opts = Array.from(sels[i].options);
                const hasBudget = opts.some(o => o.text.includes('萬') || o.text.includes('億'));
                if (hasBudget) {
                    let minOpt = opts[0];
                    for (const o of opts) {
                        if (!isNaN(parseInt(o.value)) && parseInt(o.value) < parseInt(minOpt.value)) minOpt = o;
                    }
                    sels[i].value = minOpt.value;
                    sels[i].dispatchEvent(new Event('change', {bubbles: true}));
                    return `設定select[${i}] 為 ${minOpt.text}`;
                }
            }
            return '未找到';
        }''')
        log('  [宜蘭模式] 預算已設定為最小值')
    except Exception as e:
        log(f'  [宜蘭模式] 預算設定失敗: {str(e)[:50]}')

    log('  [宜蘭模式] 設定機關=宜蘭縣政府')
    try:
        page.evaluate('''() => {
            const sels = document.querySelectorAll('select');
            for (const s of sels) {
                const opts = Array.from(s.options);
                const yilan = opts.find(o => o.text.includes('宜蘭縣'));
                if (yilan) {
                    s.value = yilan.value;
                    s.dispatchEvent(new Event('change', {bubbles: true}));
                    return `機關設為: ${yilan.text}`;
                }
            }
            return '未找到宜蘭縣';
        }''')
        log('  [宜蘭模式] 機關已設定為宜蘭縣政府')
    except Exception as e:
        log(f'  [宜蘭模式] 機關設定失敗: {str(e)[:50]}')


def main():
    parser = argparse.ArgumentParser(description='PCIC 標案資料匯出')
    parser.add_argument('--export-dir', type=str, default=None,
                        help='匯出目錄（預設: 腳本同層 exports/）')
    parser.add_argument('--yilan', action='store_true',
                        help='宜蘭縣全額度匯出模式（含所屬機關、預算0起）')
    args = parser.parse_args()

    BASE = Path(__file__).parent.parent
    EXPORT_DIR = Path(args.export_dir) if args.export_dir else BASE / 'exports'
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    STATUS = BASE / '_status.txt'
    CMD = BASE / '_cmd.txt'

    def log(msg):
        ts = time.strftime('%H:%M:%S')
        line = f'[{ts}] {msg}'
        print(line, flush=True)
        with open(BASE / '_run.log', 'a', encoding='utf-8') as f:
            f.write(line + '\n')

    def ss(page, name):
        p = str(EXPORT_DIR / f'{name}.png')
        page.screenshot(path=p)
        log(f'  截圖: {name}.png')

    STATUS.write_text('STARTING', encoding='utf-8')
    log('啟動瀏覽器...')

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(URL, wait_until='domcontentloaded', timeout=60000)
        time.sleep(5)
        ss(page, '00_login')
        STATUS.write_text('WAITING_LOGIN', encoding='utf-8')
        log('瀏覽器已開啟，請在該視窗登入')
        log('等待 CONTINUE 指令...')

        # 等待使用者登入（透過 _cmd.txt 檔案通訊）
        for i in range(600):
            if CMD.exists():
                cmd = CMD.read_text(encoding='utf-8').strip()
                if cmd == 'CONTINUE':
                    CMD.write_text('', encoding='utf-8')
                    log('收到 CONTINUE')
                    break
            if i % 12 == 0:
                log(f'  等待中 ({i}/600)')
            time.sleep(5)
        else:
            log('逾時')
            STATUS.write_text('TIMEOUT', encoding='utf-8')
            browser.close()
            sys.exit(1)

        ss(page, '01_after_login')

        # 步驟1: 展開「標案管理」子選單
        log('步驟1: 展開「標案管理」子選單')
        for tag in ['a', 'span', 'div', 'li', 'button']:
            try:
                el = page.locator(f'{tag}:visible:has-text("標案管理")').first
                if el.count() and el.is_visible():
                    el.click(); time.sleep(3)
                    log(f'  已點擊 {tag}:has-text("標案管理")')
                    break
            except: pass
        ss(page, '02_menu_expanded')

        # 步驟2: 點「報表查詢」
        log('步驟2: 點「報表查詢」')
        for tag in ['a', 'span', 'div', 'button', 'li']:
            try:
                el = page.locator(f'{tag}:visible:has-text("報表查詢")').first
                if el.count() and el.is_visible():
                    el.click(); time.sleep(5)
                    log(f'  已點擊 {tag}:has-text("報表查詢")')
                    break
            except: pass
        ss(page, '03_report')

        # 步驟3: 點「標案自選欄位表」
        log('步驟3: 點「標案自選欄位表」')
        for tag in ['a', 'span', 'div', 'button', 'td', 'li']:
            try:
                el = page.locator(f'{tag}:visible:has-text("標案自選欄位表")').first
                if el.count() and el.is_visible():
                    el.click(); time.sleep(5)
                    log(f'  已點擊 {tag}:has-text("標案自選欄位表")')
                    break
            except: pass
        ss(page, '04_selfields')

        # 步驟4: 設定篩選條件
        if args.yilan:
            log('步驟4: [宜蘭模式] 設定全額度匯出條件')
            set_yilan_full_export(page, log)
        else:
            log('步驟4: 設定預算為最小值')
            all_selects = page.evaluate('''() => {
                const sels = document.querySelectorAll('select');
                return Array.from(sels).map((s, i) => ({
                    idx: i,
                    id: s.id || '',
                    name: s.name || '',
                    visible: s.offsetParent !== null,
                    allOpts: Array.from(s.options).slice(0,5).map(o => o.text + '=' + o.value)
                }));
            }''')
            log(f'  所有select: {all_selects}')
            budget_set = False
            for s in all_selects:
                if not s['visible']:
                    continue
                sid = (s['id'] + s['name']).lower()
                opts_text = ' '.join(s['allOpts']).lower()
                if any(k in sid for k in ['budget', 'amount', '預算', '發包']) or \
                   any(k in opts_text for k in ['萬', '億']):
                    log(f'  找到預算select idx={s["idx"]} id={s["id"]} opts={s["allOpts"]}')
                    try:
                        page.evaluate(f'''() => {{
                            const sel = document.querySelectorAll('select')[{s['idx']}];
                            const opts = Array.from(sel.options);
                            let minOpt = opts[0];
                            for (const o of opts) {{
                                if (!isNaN(parseInt(o.value)) && parseInt(o.value) < parseInt(minOpt.value)) minOpt = o;
                            }}
                            sel.value = minOpt.value;
                            sel.dispatchEvent(new Event('change', {{bubbles: true}}));
                        }}''')
                        log(f'  已設定預算為最小值')
                        budget_set = True
                        break
                    except Exception as e:
                        log(f'  設定失敗: {str(e)[:50]}')
            if not budget_set:
                log('  未找到預算select，嘗試用含「萬/億」option 的 select')
                try:
                    page.evaluate('''() => {
                        const sels = document.querySelectorAll('select');
                        for (let i = 0; i < sels.length; i++) {
                            const opts = Array.from(sels[i].options);
                            const hasBudget = opts.some(o => o.text.includes('萬') || o.text.includes('億'));
                            if (hasBudget) {
                                let minOpt = opts[0];
                                for (const o of opts) {
                                    if (!isNaN(parseInt(o.value)) && parseInt(o.value) < parseInt(minOpt.value)) minOpt = o;
                                }
                                sels[i].value = minOpt.value;
                                sels[i].dispatchEvent(new Event('change', {bubbles: true}));
                                return `設定select[${i}] 為 ${minOpt.text}`;
                            }
                        }
                        return '未找到';
                    }''')
                    log(f'  index方式: 已嘗試')
                except Exception as e:
                    log(f'  index方式失敗: {str(e)[:50]}')
        ss(page, '05_filled')

        # 步驟5: 執行查詢
        log('步驟5: 執行查詢')
        for txt in ['執行查詢', '查詢']:
            btn = page.locator(f'button:visible:has-text("{txt}")').first
            if btn.count() and btn.is_visible():
                btn.click(); time.sleep(10)
                log(f'  已點擊 {txt}'); break
        ss(page, '06_result')

        # 步驟6: 匯出 Excel
        log('步驟6: 匯出')
        export_btn = page.locator('button:visible:has-text("匯出"), a:visible:has-text("匯出")').first
        if export_btn.count() and export_btn.is_visible():
            log(f'  找到匯出按鈕: {export_btn.inner_text()[:30]}')
            export_btn.click()
            time.sleep(2)
            ss(page, '06_dropdown_open')
            dropdown_items = page.locator('li a:visible, ul.dropdown-menu a:visible, .dropdown-menu a:visible').all()
            log(f'  下拉選項數: {len(dropdown_items)}')
            for item in dropdown_items:
                try:
                    txt = item.inner_text().strip()[:30]
                    log(f'    選項: {txt}')
                except: pass
            found = False
            for item in dropdown_items:
                try:
                    txt = item.inner_text().strip().lower()
                    if any(k in txt for k in ['excel', 'xlsx', 'xls', 'csv']):
                        log(f'  點擊: {txt}')
                        with page.expect_download(timeout=120000) as dl:
                            item.click()
                        d = dl.value
                        p = str(EXPORT_DIR / f'export_{time.strftime("%Y%m%d_%H%M%S")}.xlsx')
                        d.save_as(p)
                        log(f'  下載成功: {p}')
                        found = True
                        break
                except Exception as e:
                    log(f'  下載問題: {str(e)[:80]}')
            if not found:
                log('  未找到EXCEL選項，嘗試直接點匯出')
                try:
                    with page.expect_download(timeout=120000) as dl:
                        export_btn.click()
                    d = dl.value
                    p = str(EXPORT_DIR / f'export_{time.strftime("%Y%m%d_%H%M%S")}.xlsx')
                    d.save_as(p)
                    log(f'  下載成功: {p}')
                except Exception as e:
                    log(f'  下載失敗: {str(e)[:80]}')
        else:
            log('  無匯出按鈕')
        ss(page, '07_after_export')
        STATUS.write_text('ALL_DONE', encoding='utf-8')
        log('完成!')
        time.sleep(10)
        browser.close()


if __name__ == '__main__':
    main()
