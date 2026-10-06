#!/usr/bin/env python
"""按物理网格填写：文本/公式/嵌入表格/行高列宽；默认只出计划

用法：python scripts/fill_report.py <参数…>        （例：python scripts/fill_report.py --help）

本脚本只把参数转发给仓库内 lib/ 的实现；**不需要安装任何东西**，
也没有 labreport 这个命令——skill 里直接用 python 调用即可。
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "lib"))

from labreport.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main(["fill"] + sys.argv[1:]))
