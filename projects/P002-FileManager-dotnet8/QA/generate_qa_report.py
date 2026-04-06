#!/usr/bin/env python3
"""
P002-FileManager-dotnet8 - 合併 QA 報告產生器
將龍哥 + Sub-agent 的測試結果與截圖合併成一份 Word 報告
"""
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os
from datetime import datetime

BASE_DIR = "/home/devpro/Claude-Workspace/projects/P002-FileManager-dotnet8/QA"
SCREENSHOT_DIR = os.path.join(BASE_DIR, "QA_Screenshots_Combined")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# 收集所有截圖
playwright_dir = os.path.join(BASE_DIR, "screenshots/playwright")
final_dir = os.path.join(BASE_DIR, "screenshots/final")

all_screenshots = {}
for d in [playwright_dir, final_dir]:
    if os.path.exists(d):
        for f in os.listdir(d):
            if f.endswith(".png"):
                all_screenshots[f] = os.path.join(d, f)

# 測試案例定義
TEST_CASES = [
    # ===== 登入系統 =====
    {
        "category": "登入系統",
        "id": "TC-001",
        "name": "登入頁面",
        "api": None,
        "api_result": None,
        "screenshot": "TC-001_login_page.png",
        "status": "PASS",
        "notes": "登入頁面正常顯示"
    },
    {
        "category": "登入系統",
        "id": "TC-003",
        "name": "錯誤密碼提示",
        "api": None,
        "api_result": None,
        "screenshot": "TC-003_wrong_password.png",
        "status": "PASS",
        "notes": "錯誤密碼顯示正確提示"
    },
    {
        "category": "登入系統",
        "id": "TC-004",
        "name": "Admin 儀表板",
        "api": None,
        "api_result": None,
        "screenshot": "TC-004_admin_dashboard.png",
        "status": "PASS",
        "notes": "Admin 登入後顯示儀表板"
    },
    {
        "category": "登入系統",
        "id": "TC-005",
        "name": "Admin 可見所有網域",
        "api": None,
        "api_result": None,
        "screenshot": "TC-005_admin_all_domains.png",
        "status": "PASS",
        "notes": "Admin 可瀏覽所有網域資料"
    },
    {
        "category": "登入系統",
        "id": "TC-109",
        "name": "一般使用者登入",
        "api": None,
        "api_result": None,
        "screenshot": "TC-109_user_dashboard.png",
        "status": "PASS",
        "notes": "一般使用者登入成功"
    },
    {
        "category": "登入系統",
        "id": "TC-110",
        "name": "一般使用者只看自己網域",
        "api": None,
        "api_result": None,
        "screenshot": "TC-110_user_domain_only.png",
        "status": "PASS",
        "notes": "一般使用者權限隔離正常"
    },
    {
        "category": "登入系統",
        "id": "TC-111",
        "name": "不允許的網域被拒絕",
        "api": None,
        "api_result": None,
        "screenshot": "TC-111_disallowed_domain.png",
        "status": "PASS",
        "notes": "網域存取控制正常"
    },
    {
        "category": "登入系統",
        "id": "TC-108",
        "name": "登出功能",
        "api": None,
        "api_result": None,
        "screenshot": "TC-108_logged_out.png",
        "status": "PASS",
        "notes": "登出功能正常"
    },
    # ===== 檔案管理 FM =====
    {
        "category": "FM-001",
        "id": "FM001",
        "name": "首頁 / 資料夾瀏覽",
        "api": "GET /api/files?path=/home/devpro/data",
        "api_result": "200 OK",
        "screenshot": "FM001_filelist_fullpage.png",
        "alt_screenshot": "TC001_homepage.png",
        "status": "PASS",
        "notes": "首頁正常顯示檔案列表與側邊欄"
    },
    {
        "category": "FM-002",
        "id": "FM002",
        "name": "新增資料夾",
        "api": "POST /api/folders",
        "api_result": "200 OK - Folder created",
        "screenshot": "FM002_new_folder_dialog.png",
        "alt_screenshot": "TC004_new_folder_dialog.png",
        "status": "PASS",
        "notes": "新增資料夾對話框正常彈出，API 成功建立"
    },
    {
        "category": "FM-003",
        "id": "FM003",
        "name": "重新命名",
        "api": "PATCH /api/files/rename",
        "api_result": "200 OK - File renamed successfully",
        "screenshot": "TC-103_rename_dialog.png",
        "status": "PASS",
        "notes": "重新命名對話框正常，API 成功執行"
    },
    {
        "category": "FM-004",
        "id": "FM004",
        "name": "移動檔案 / 資料夾",
        "api": "PATCH /api/files/move",
        "api_result": "200 OK - movedCount: 1",
        "screenshot": "TC-104_move_dialog.png",
        "status": "PASS",
        "notes": "移動對話框正常，API 成功移動檔案"
    },
    {
        "category": "FM-005",
        "id": "FM005",
        "name": "刪除檔案 / 資料夾",
        "api": "DELETE /api/files",
        "api_result": "200 OK",
        "screenshot": "TC-105_delete_dialog.png",
        "status": "PASS",
        "notes": "刪除確認對話框正常"
    },
    {
        "category": "FM-006",
        "id": "FM006",
        "name": "單一檔案上傳",
        "api": "POST /api/upload",
        "api_result": "200 OK - totalUploaded: 1",
        "screenshot": "TC-106_upload_dialog.png",
        "status": "PASS",
        "notes": "上傳對話框正常，API 成功上傳檔案"
    },
    {
        "category": "FM-007",
        "id": "FM007",
        "name": "多重上傳",
        "api": "POST /api/upload (多檔)",
        "api_result": "200 OK - totalUploaded: 2",
        "screenshot": None,
        "status": "PASS",
        "notes": "API 支援多重檔案上傳，UI 复用上傳對話框"
    },
    {
        "category": "FM-008",
        "id": "FM008",
        "name": "拖拉上傳",
        "api": "POST /api/upload",
        "api_result": "N/A (UI 元件層級互動)",
        "screenshot": None,
        "status": "N/A",
        "notes": "Blazor 元件支援，需手動測試"
    },
    {
        "category": "FM-009",
        "id": "FM009",
        "name": "檔案下載",
        "api": "GET /api/files/download/{path}",
        "api_result": "200 OK - Content downloaded",
        "screenshot": None,
        "status": "PASS",
        "notes": "API 成功下載檔案，瀏覽器直接下載"
    },
    {
        "category": "FM-010",
        "id": "FM010",
        "name": "多重下載",
        "api": "POST /api/files/download",
        "api_result": "200 OK - ZIP bundle",
        "screenshot": None,
        "status": "PASS",
        "notes": "API 返回 ZIP 壓縮包"
    },
    {
        "category": "FM-011",
        "id": "FM011",
        "name": "搜尋 / 篩選",
        "api": "POST /api/files/search",
        "api_result": "200 OK - Found 8 items",
        "screenshot": "TC-107_search_results.png",
        "alt_screenshot": "TC005_search.png",
        "status": "PASS",
        "notes": "搜尋對話框與結果正常顯示"
    },
    # ===== 設定與 Debug =====
    {
        "category": "設定",
        "id": "TC-006",
        "name": "設定頁面",
        "api": "GET /api/settings",
        "api_result": "200 OK",
        "screenshot": "TC006_settings.png",
        "status": "PASS",
        "notes": "設定頁面正常顯示所有設定值"
    },
    {
        "category": "Debug",
        "id": "TC-007",
        "name": "Debug Header 驗證",
        "api": "All endpoints",
        "api_result": "X-Trace-ID, X-Request-Duration-Ms, X-Server-Time present",
        "screenshot": "TC007_debug_header.png",
        "status": "PASS",
        "notes": "所有 API 回應皆包含 Debug Header"
    },
]

def set_cell_bg(cell, hex_color):
    """設定儲存格背景顏色"""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)

def add_screenshot(doc, img_path, width=Inches(6)):
    """加入截圖（保持比例）"""
    if os.path.exists(img_path):
        doc.add_picture(img_path, width=width)
        last_para = doc.paragraphs[-1]
        last_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        return True
    return False

def create_report():
    doc = Document()

    # ===== 封面 =====
    doc.add_heading("P002-FileManager-dotnet8", 0)
    doc.add_heading("QA 完整測試報告", level=1)
    doc.add_paragraph(f"測試日期：2026-04-06")
    doc.add_paragraph(f"測試人員：龍哥 🐉 + QA Sub-agent")
    doc.add_paragraph(f"報告產生：{datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # ===== 摘要 =====
    total = len(TEST_CASES)
    passed = sum(1 for tc in TEST_CASES if tc["status"] == "PASS")
    n_a = sum(1 for tc in TEST_CASES if tc["status"] == "N/A")
    with_screenshot = sum(1 for tc in TEST_CASES if tc.get("screenshot") or tc.get("alt_screenshot"))

    doc.add_heading("測試摘要", level=1)
    summary_table = doc.add_table(rows=5, cols=2)
    summary_table.style = "Table Grid"
    summary_data = [
        ("總測試案例數", str(total)),
        ("通過 (PASS)", str(passed)),
        ("不適用 (N/A)", str(n_a)),
        ("有截圖", str(with_screenshot)),
        ("截圖覆蓋率", f"{with_screenshot}/{total} ({with_screenshot*100//total}%)"),
    ]
    for i, (label, value) in enumerate(summary_data):
        row = summary_table.rows[i]
        row.cells[0].text = label
        row.cells[1].text = value
        set_cell_bg(row.cells[0], "E8E8E8")

    # ===== 安全性測試 =====
    doc.add_heading("安全性測試", level=1)
    sec_table = doc.add_table(rows=3, cols=3)
    sec_table.style = "Table Grid"
    sec_headers = ["測試項目", "API", "結果"]
    for i, h in enumerate(sec_headers):
        sec_table.rows[0].cells[i].text = h
        set_cell_bg(sec_table.rows[0].cells[i], "4F81BD")
        sec_table.rows[0].cells[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(255,255,255)
    sec_data = [
        ("路徑遍歷防護 (../)", "所有 API", "✅ 阻擋"),
        ("脫離 rootFolder", "所有 API", "✅ 阻擋"),
    ]
    for i, (test, api, result) in enumerate(sec_data, 1):
        sec_table.rows[i].cells[0].text = test
        sec_table.rows[i].cells[1].text = api
        sec_table.rows[i].cells[2].text = result

    # ===== 詳細測試案例 =====
    doc.add_heading("詳細測試案例", level=1)

    current_category = None
    for tc in TEST_CASES:
        if tc["category"] != current_category:
            doc.add_heading(f"— {tc['category']} —", level=2)
            current_category = tc["category"]

        # 案例標題
        status_emoji = "✅" if tc["status"] == "PASS" else ("⚠️" if tc["status"] == "N/A" else "❌")
        p = doc.add_paragraph()
        run = p.add_run(f"{tc['id']}: {tc['name']} {status_emoji}")
        run.bold = True
        run.font.size = Pt(12)

        # 資料表
        tbl = doc.add_table(rows=5, cols=2)
        tbl.style = "Table Grid"
        rows_data = [
            ("狀態", tc["status"]),
            ("API", tc["api"] or "N/A"),
            ("API 回應", tc["api_result"] or "N/A"),
            ("說明", tc["notes"]),
            ("截圖", tc.get("screenshot") or tc.get("alt_screenshot") or "無"),
        ]
        for i, (label, value) in enumerate(rows_data):
            tbl.rows[i].cells[0].text = label
            tbl.rows[i].cells[1].text = value
            set_cell_bg(tbl.rows[i].cells[0], "F2F2F2")

        # 截圖
        screenshot_file = tc.get("screenshot") or tc.get("alt_screenshot")
        if screenshot_file and screenshot_file in all_screenshots:
            doc.add_paragraph()
            added = add_screenshot(doc, all_screenshots[screenshot_file], width=Inches(5.5))
            if added:
                cap = doc.add_paragraph(f"▲ {screenshot_file}")
                cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                cap.runs[0].font.size = Pt(9)
                cap.runs[0].font.color.rgb = RGBColor(128,128,128)
        else:
            doc.add_paragraph(f"⚠️ 截圖：無（{screenshot_file or '未指定'}）").runs[0].font.color.rgb = RGBColor(180,180,180)

        doc.add_paragraph()  # 空行

    # ===== 截圖目錄 =====
    doc.add_heading("截圖檔案清單", level=1)
    screenshot_table = doc.add_table(rows=len(all_screenshots)+1, cols=3)
    screenshot_table.style = "Table Grid"
    screenshot_table.rows[0].cells[0].text = "檔案名"
    screenshot_table.rows[0].cells[1].text = "大小"
    screenshot_table.rows[0].cells[2].text = "路徑"
    for cell in screenshot_table.rows[0].cells:
        set_cell_bg(cell, "4F81BD")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255,255,255)

    for i, (fname, fpath) in enumerate(sorted(all_screenshots.items()), 1):
        size = os.path.getsize(fpath)
        size_str = f"{size/1024:.0f} KB" if size > 1024 else f"{size} B"
        screenshot_table.rows[i].cells[0].text = fname
        screenshot_table.rows[i].cells[1].text = size_str
        screenshot_table.rows[i].cells[2].text = fpath

    # ===== 儲存 =====
    output_path = os.path.join(BASE_DIR, "QA_Report_Combined_20260406.docx")
    doc.save(output_path)
    print(f"✅ 報告已產生：{output_path}")
    print(f"   截圖數量：{len(all_screenshots)}")
    return output_path

if __name__ == "__main__":
    create_report()
