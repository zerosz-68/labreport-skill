#!/usr/bin/env python
"""成品自检：结构、公式、按模板提纲核对章节、占位、数据回读、文末附件

用法：python scripts/audit_report.py <参数…>        （例：python scripts/audit_report.py --help）

本脚本只把参数转发给仓库内 lib/ 的实现；**不需要安装任何东西**，
也没有 labreport 这个命令——skill 里直接用 python 调用即可。
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "lib"))

from labreport.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main(["audit"] + sys.argv[1:]))
