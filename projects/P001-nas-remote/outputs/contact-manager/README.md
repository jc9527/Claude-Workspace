# 聯絡人管理系統

一個使用 Python Flask 打造的聯絡人管理系統，支援 CRUD 操作與關鍵字搜尋。

## 快速開始

```bash
pip install -r requirements.txt
python app.py
```

服務啟動後，開啟瀏覽器前往 http://127.0.0.1:5000

## API 端點

| 方法 | 路徑 | 說明 |
|------|------|------|
| GET | /contacts | 取得所有聯絡人 |
| GET | /contacts/<id> | 取得單一聯絡人 |
| POST | /contacts | 新增聯絡人 |
| PUT | /contacts/<id> | 更新聯絡人 |
| DELETE | /contacts/<id> | 刪除聯絡人 |
| GET | /contacts/search?q=<keyword> | 搜尋聯絡人 |

## 資料模型

```json
{
  "id": "uuid-xxx",
  "name": "王小明",
  "phone": "0912-345-678",
  "email": "wang@example.com",
  "company": "ABC 公司",
  "notes": "業務窗口",
  "created_at": "2026-04-05T10:00:00Z",
  "updated_at": "2026-04-05T10:00:00Z"
}
```
