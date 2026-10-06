#!/usr/bin/env python
"""读 Word 模板结构：表格物理网格、合并单元格、嵌套表、公式、图片、占位

用法：python scripts/inspect_docx.py <参数…>        （例：python scripts/inspect_docx.py --help）

本脚本只把参数转发给仓库内 lib/ 的实现；**不需要安装任何东西**，
也没有 labreport 这个命令——skill 里直接用 python 调用即可。
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "lib"))

from labreport.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main(["inspect"] + sys.argv[1:]))
