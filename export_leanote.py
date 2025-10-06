import requests
import os
from datetime import datetime
import re
import time  # 用于更新时间戳

# ------------------------
# 使用浏览器 cURL 的完整 cookie（放在最前面）
# ------------------------
cookies_dict = {
    "LEANOTE_FLASH": "",
    "mongoMachineId": "xxx",
    "LEANOTE_SESSION": "xxx"
}

session = requests.Session()
session.cookies.update(cookies_dict)

# 浏览器 UA 等 headers
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
    "Connection": "keep-alive",
    "DNT": "1",
})

# ------------------------
# 配置
# ------------------------
BASE_DIR = "./Leanote_Export"

# 处理文件名非法字符
def sanitize_filename(name):
    return re.sub(r'[\\/:"*?<>|]+', "_", name)

# ISO 时间字符串转 YYYY-MM-DD HH:MM:SS
def format_time(iso_time_str):
    dt = datetime.fromisoformat(iso_time_str.replace('Z', '+00:00'))
    return dt.strftime('%Y-%m-%d %H:%M:%S')

# 写入单条笔记到 Markdown 并更新文件时间戳
def write_note_to_file(folder_path, note_content, note_summary):
    note_title = note_content.get("Title") or note_summary.get("Title") or "Untitled"
    created_str = format_time(note_content['CreatedTime'])
    updated_str = format_time(note_content['UpdatedTime'])
    created_date = created_str.split(" ")[0].replace("-", "")
    file_name = f"{created_date}_{sanitize_filename(note_title)}.md"
    file_path = os.path.join(folder_path, file_name)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# {note_title}\n\n")
        f.write(f"@CreatedTime: {created_str}\n")
        f.write(f"@UpdatedTime: {updated_str}\n\n")
        f.write(note_content.get('Content', ''))
    print(f"Saved note: {file_path}")

    # 更新文件系统时间戳（使用 UpdatedTime）
    try:
        dt = datetime.fromisoformat(note_content['UpdatedTime'].replace('Z', '+00:00'))
        timestamp = dt.timestamp()
        os.utime(file_path, (timestamp, timestamp))
        print(f"Updated file timestamp: {file_path}")
    except Exception as e:
        print(f"Failed to update timestamp for {file_path}: {e}")

# ------------------------
# 获取 notebooks
# ------------------------
notebooks_url = "https://leanote.com/notebook/getNotebooks"
resp = session.get(notebooks_url)

try:
    notebooks = resp.json()
except Exception:
    print("获取 notebooks 失败，可能是 cookie 已过期或登录失效")
    print(resp.text[:500])
    exit(1)

# ------------------------
# 遍历 notebooks 获取 notes
# ------------------------
for nb in notebooks:
    notebook_title = sanitize_filename(nb['Title'])
    notebook_folder = os.path.join(BASE_DIR, notebook_title)
    os.makedirs(notebook_folder, exist_ok=True)

    notebook_id = nb['NotebookId']

    notes_list_url = f"https://leanote.com/note/listNotes/?notebookId={notebook_id}"
    notes_list = session.get(notes_list_url).json()

    for note_summary in notes_list:
        note_id = note_summary['NoteId']
        note_content_url = f"https://leanote.com/note/getNoteContent?noteId={note_id}"
        note_content = session.get(note_content_url).json()
        write_note_to_file(notebook_folder, note_content, note_summary)

print("All notes exported successfully.")
