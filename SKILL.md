---
name: labreport-skill
description: 大学实验报告填写与自检工作流。用户提供「未填写的实验报告 .docx」「课堂报告书（手写页照片或整理表）」「教材/讲义的实验内容设计」，要求"把数据填进报告""按模板写好报告""检查报告填全没有"时使用。章节以未填写报告的提纲为准，公式必须是 Word 原生公式，课堂报告书原件作为附件附在报告最后。所有操作都通过本 skill 自带的 scripts/ 脚本完成，不需要安装任何东西。
---

# 实验报告填写 skill

**这个 skill 自带脚本，不需要安装任何包，也不存在 `labreport` 命令。**
所有硬活都用 `python scripts/xxx.py …` 调用；你（agent）负责需要理解的部分：看照片识别手写数字、判断内容写在哪里、与用户确认。

脚本位置：本 skill 目录下的 `scripts/`（`<SKILL_DIR>/scripts/`）。
运行环境只要求 **Python 3.9+**，依赖 `python-docx`（缺失时脚本会提示怎么装）。

## 0. 三份输入（缺一不可）

| # | 材料 | 作用 | 形态 |
|---|---|---|---|
| ① | **实验报告（未填写）** | **章节提纲的唯一来源**（表内写着"实验报告应包括以下内容：…"）＋ 封面/表头 | `.docx` |
| ② | **课堂报告书** | **数据来源**（原始记录表格）＋ **文末附件的原件** | 手写页照片（1～2 页），或另有一份整理成表格的 `.docx` |
| ③ | **实验内容设计** | 正文依据（教材/讲义里的"设计方案、目标任务、原理、步骤"） | 教材扫描页或 PDF |

**先分类再动手**：逐张看图片，判断哪些是课堂报告书、哪些是教材、哪些无关，把"文件名 → 类别 → 一句话内容"列给用户确认后再继续。

## 1. 铁律（顺序不能变）

1. 先 `python scripts/doctor.py`；缺核心依赖就停下告诉用户，不要绕过。
2. **看照片识别手写数字是你的活**；但**不要自己拼 OMML 公式、不要手写 docx**——那是脚本的活。
3. 数据先落成 `data.json`，跑 `python scripts/check_data.py`；**有 error 就回看照片复核，禁止猜**。
4. `fill_report.py` 默认**只出计划不写文件**：把计划给用户确认后再加 `--apply`。
5. 交付前必须 `python scripts/audit_report.py … --require-attachment` 通过（退出码 0）。
6. 公式必须是 **Word 原生公式**：`audit_report.py` 会查"空公式"和"LaTeX 残留"。

## 2. 正文：严格按未填写报告的提纲

**章节顺序与名称以模板里的提纲为准**，不要自己发明章节。典型提纲（扭摆法）：

| 节 | 怎么写 | 依据 |
|---|---|---|
| 一、实验目的 | 简单写（3～5 条） | 模板提纲 ＋ 教材【设计方案·目标任务】 |
| 二、实验基本原理 | **公式要完整**（原生公式），文字从简 | 教材原理部分 |
| 三、仪器及设备 | 简单写（一行罗列） | 教材 ＋ 报告书 |
| 四、实验操作步骤 | 简单写（4～6 步） | 教材步骤 ＋ 报告书操作记录 |
| **五、实验数据记录** | **把课堂报告书里的表格全部搬进来**（见第 3 节） | 课堂报告书 |
| 六、实验数据处理过程及结果、结论 | 简单写 ＋ 关键公式与结果 | 教材 ＋ 数据 |
| 七、问题与讨论 | 简单写（3～5 条，与实测数据挂钩） | 教材 ＋ 实测 |

- **除第五节外一律从简**，但公式必须完整、正确。
- 表头（实验名称/班级/学号/姓名/同组人）从**课堂报告书手写页**抄，逐一核对。
- **不要在第五节写"以下数据取自…""见文末附件"这类说明句**。
- 先 `python scripts/inspect_docx.py 模板.docx` 看清正文填在哪两个大格（常见：前四节一格、后三节一格）。

## 3. 第五节：把课堂报告书的表格提取出来嵌入正文

```bash
python scripts/extract_tables.py 课堂报告书.docx -o tables.json    # 提取全部表格（含合并关系）
python scripts/extract_tables.py 课堂报告书.docx                   # 先看摘要：表名、行列、合并数
```

- 表名默认从表格首行（整行合并那行）**提上来**，嵌入后会写在表格**上一行**；
- 空表默认跳过；要保留加 `--keep-empty`；
- 只有手写照片时：自己按原表**逐格**读出，手写 `tables.json`（`{name, cols, grid, merges}`，行列 1 起，被合并覆盖的格留空），**结构必须与原表一致**；
- **表内公式也要是原生公式**：原表里的 `J₁=1/8mD²` 往往只是文字，在 `tables.json` 里给它加
  `"formulas": {"2,5": "J_{1}=\\frac{1}{8}mD^{2}"}`（行列相对该表，1 起）；
- 原表上方的说明行（如"杆子和滑块总质量：685.43 g"）写进 `"notes": [...]`；
- 列宽不合适时用 `"colWidths": [10,15,15,14,28,18]`（百分比，只改尺寸不改格式）。

在 `map.json` 里**就地插入**（表格出现在这个位置，不是文末）：

```jsonc
{ "table": 2, "row": 6, "col": 1, "append": "五、实验数据记录" },
{ "table": 2, "row": 6, "col": 1, "insert_tables_file": "tables.json" },
{ "table": 2, "row": 6, "col": 1, "append": "六、实验数据处理过程及结果、结论" }
```

## 4. 附件：课堂报告书原件放在报告最后，且在表格框内

```bash
python scripts/add_attachment.py 成品.docx 课堂报告书页1.jpg 课堂报告书页2.jpg \
       --into "2,6,1" --apply
```

- `--into "表,行,列"` 指正文最后一个大格：附件写在**报告表格框内部**（用 `inspect_docx.py` 确认坐标）；不给则追加到文档末尾（框外）；
- 默认行为：正文之后写一行标签 **`附件`**（不分页），随后每张图**独占一页、满宽**；
- 标签文字用 `--label` 改；附件页数应与课堂报告书实际页数一致（1～2 页），别把教材页附进去。

## 5. 完整流程

```bash
S=<本 skill 目录>/scripts          # 下面用 $S 代指

python $S/doctor.py                                     # 环境体检
python $S/inspect_docx.py 模板.docx                      # 物理网格：正文在哪两格
# 读课堂报告书照片 → data.json（每个值带 source）
python $S/check_data.py data.json                        # 改到 0 error
python $S/extract_tables.py 课堂报告书.docx -o tables.json
# 写 map.json：表头 + 七节正文 + 公式 + insert_tables_file
python $S/fill_report.py 模板.docx --map map.json --data data.json             # 先出计划
python $S/fill_report.py 模板.docx --map map.json --data data.json \
       --apply -o 成品.docx --fit-rows "2:5,2:6"                                # 确认后落地
python $S/add_attachment.py 成品.docx 课堂报告书页*.jpg --into "2,6,1" --apply
python $S/audit_report.py 成品.docx --source 模板.docx --data data.json --require-attachment
python $S/inspect_docx.py 成品.docx                      # 最后核对一遍
```

- `--fit-rows "2:5,2:6"`：模板常给正文大格设"最小行高≈整页"，内容填不满会留下空白页；这个参数**只改行高（尺寸），不动边框/字体/合并（格式）**。
- 交付：**一份 docx**（公式、表格、附件都是原生的；需要 PDF 请用户自己用 Word/WPS 另存）。

## 6. 出问题怎么查

| 现象 | 处置 |
|---|---|
| `check_data.py` 报平均值不自洽 / 离群 | 回看该组 `source` 指的照片区域，逐格重认 |
| `check_data.py` 报与预期值相差太大 | 查公式、单位、抄录；确认无误再改 `expected` 并说明原因 |
| `fill_report.py` 报"超出网格" | `inspect_docx.py` 看该表行列与合并情况，或改用锚点 `find` |
| `audit_report.py` 报缺章节 | 该节没写，或标题写法与模板提纲不一致（以模板为准） |
| `audit_report.py` 报 LaTeX 残留 | 公式没转成原生：检查 `formulas` / `formula` 里的 LaTeX 是否有不支持的命令 |
| `audit_report.py` 报数据未命中 | 漏填，或写成了别的形式（`1.4091×10⁻³` 与 `0.0014091` 都认） |
| `audit_report.py` 报文末没有附件 | 忘了 `add_attachment.py`，或标签/图片不在文末 |
| 表格里的公式是文字 | 在 `tables.json` 的 `formulas` 里指定 LaTeX 后重跑 `fill_report.py` |
| 脚本报 `ModuleNotFoundError: docx` | 让用户装 `python-docx`（`pip install python-docx`） |

格式细节（`data.json` / `map.json`）见 `references/data-format.md`；
每个实验的公式与表格结构见 `references/cards/`（内置扭摆法一张）。

## 7. 边界

- 只做"**按模板填**"：没有模板就先请用户提供；不要另建报告。
- **不编造数据**：识别不出的格子留占位并在回复里说明，绝不猜一个数填进去。
- 用户没确认前不写文件（`fill_report.py` / `add_attachment.py` 的默认行为已保证）。
- 不认识的内容（不属于这三类材料的图）不要往报告里塞。
- 不承诺 PDF：需要时让用户自己另存。
