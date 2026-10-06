# labreport-skill

[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**一个"填实验报告"的 skill：自带脚本、不用安装、不依赖任何命令行工具。**

把三份材料交给会看图的 agent（Claude / DSH / Codex / Cursor 都行），它就能产出一份合规的实验报告：

| 输入 | 作用 |
|---|---|
| ① 未填写的实验报告 `.docx` | **章节提纲的唯一来源**（表内"实验报告应包括以下内容：…"） |
| ② 课堂报告书（手写页照片／整理表） | **数据来源** ＋ **文末附件的原件** |
| ③ 教材／讲义的实验内容设计 | 正文依据（设计方案、原理、步骤） |

产出：**一份 docx** —— 章节按模板提纲、数据来自课堂报告书并逐项校验、
课堂报告书的表格**整表嵌入**第五节（保留合并关系、表名写在表格上一行）、
公式全部是 **Word 原生公式**、课堂报告书原件作为**附件放在报告框内的最后**。

## 怎么用

把本目录作为 skill 装进你的 agent（Claude/DSH 放 `skills/labreport-skill/`；
Codex/Cursor 把 `SKILL.md` 内容粘到它认的指令文件里），然后直接说：

> 用这个 skill 把实验报告写好：模板是 `报告模板.docx`，课堂报告书在 `照片/` 里，教材在 `教材/` 里。

agent 会按 `SKILL.md` 的流程走：`doctor → inspect_docx → check_data → extract_tables → fill_report → add_attachment → audit_report`。

## 自带脚本（不需要安装）

```bash
python scripts/doctor.py                 # 环境体检
python scripts/inspect_docx.py 模板.docx  # 表格物理网格、合并单元格、嵌套表、公式
python scripts/check_data.py data.json   # 单位归一化 / 平均值自洽 / 离群 / 公式重算比对
python scripts/extract_tables.py 课堂报告书.docx -o tables.json
python scripts/fill_report.py 模板.docx --map map.json --data data.json --apply -o 成品.docx --fit-rows "2:5,2:6"
python scripts/add_attachment.py 成品.docx 页1.jpg 页2.jpg --into "2,6,1" --apply
python scripts/audit_report.py 成品.docx --source 模板.docx --data data.json --require-attachment
```

只要求 **Python 3.9+** 和 `python-docx`（缺了脚本会提示）。
**没有 `labreport` 命令、没有 pip 安装、没有 PDF 转换**（要 PDF 自己用 Word/WPS 另存）。

## 为什么是"自带脚本的 skill"而不是 CLI

- **好分发**：别人拿到目录就能用，不需要装包、不需要配 PATH；
- **agent 友好**：`SKILL.md` 写清"何时调用哪个脚本"，确定性的事交给脚本（合并单元格换算、OMML 生成、数值校验），需要理解的事交给模型（看照片、判断放哪里、与你确认）；
- **可覆盖**：实验特异性放在 `references/cards/`，换实验只加一张卡。

## 目录

```
labreport-skill/
├─ SKILL.md              agent 读的唯一入口（三份输入 / 七节 / 表格嵌入 / 附件 / 自检）
├─ scripts/              9 个入口脚本（都只是转发，不含实现）
├─ lib/labreport/        实现：物理网格、OMML、数据校验、自检、附件
└─ references/
   ├─ data-format.md     data.json / map.json 全部字段与规则
   └─ cards/             实验知识卡（内置扭摆法）
```

## 已验证

用真实材料（未填写的实验报告 + 手写课堂报告书两页 + 教材扫描页）跑通：

```
extract_tables  → 4 张表（含合并关系与表名）
check_data      → 9 个目标量与课堂报告书一致，平均值自洽，0 error
fill_report     → 七节正文 + 16 条原生公式 + 4 张嵌入表
add_attachment  → 附件在报告框内（1 行标签 + 每页一张满图）
audit_report    → 数据回读 24/24 · 章节 7/7 · 附件在文末 · error 0 / warn 0
```

## 许可

MIT，见 [LICENSE](LICENSE)。
