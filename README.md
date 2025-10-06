# Leanote Exporter

通过 **网页版登录的 Cookie**，导出 Leanote 中的所有笔记。

本脚本将你的 Leanote 笔记按 notebook 分类导出为 Markdown 文件，并保留时间与元信息。

---

## ✨ 功能特性

* 🗂️ **按 notebook 建立文件夹**
  每个笔记本对应一个文件夹。

* 📝 **导出为 Markdown 文件**
  每条笔记导出为 `.md` 文件，格式如下：

  ```markdown
  # 标题

  @CreatedTime: 2023-05-15 09:32:12  
  @UpdatedTime: 2023-06-01 17:24:45  

  （笔记正文内容）
  ```

* 🕒 **保留时间戳**

  * 文件夹和文件名中写入创建日期（例如：`20230515_MyNote.md`）
  * 元信息中保留创建与更新时间

---

## ⚙️ 运行方式

1. **登录 Leanote 网页版**
   使用浏览器（建议 Chrome）登录你的 Leanote 帐号。

2. **获取 Cookie**

   * 打开 **开发者工具**（`F12` 或 `Ctrl+Shift+I` / macOS `Cmd+Option+I`）
   * 进入 **Application → Cookies → [https://leanote.com](https://leanote.com)**
   * 找到以下两个字段并复制：

     * `mongoMachineId`
     * `LEANOTE_SESSION`

3. **填写 Cookie**
   将这两个值填入 `export_leanote.py` 代码开头的 `cookies_dict` 部分。

4. **运行脚本**

   ```bash
   python export_leanote.py
   ```

   导出的笔记将保存到 `./Leanote_Export/` 目录中。

---

## 🧠 实现思路

* 使用 `requests` 模块模拟浏览器请求。
* 先访问 `https://leanote.com/notebook/getNotebooks` 获取所有笔记本名称与 ID。
* 对每个 notebook，调用 `https://leanote.com/note/listNotes/?notebookId=...` 获取笔记列表。
* 对每个笔记，调用 `https://leanote.com/note/getNoteContent?noteId=...` 获取正文内容。
* 将标题、创建时间、更新时间与内容写入 Markdown 文件中。

---

## 📂 输出结构示例

```
Leanote_Export/
├── reading/
│   ├── 20230515_MachineLearning.md
│   └── 20230621_BayesianStats.md
└── astronomy/
    ├── 20230703_ClusterDynamics.md
    └── 20230705_SimulationNotes.md
```

---

## 🪄 备注

* 如果运行时报 `JSONDecodeError`，通常是 **Cookie 过期** 或 **Session 无效**，请重新登录并更新 Cookie。
* 不需要 API key，只需登录后的浏览器 Cookie 即可访问。
* 建议使用 Python ≥ 3.8。

---

## 🧑‍💻 作者

编写与调试：@syrte & ChatGPT

项目基于个人 Leanote 数据导出需求。

如遇问题，可自行向 ChatGPT 咨询。
