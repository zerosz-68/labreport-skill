#!/usr/bin/env python
"""在报告末尾追加附件（标签一行 + 每页一张满宽图，可放进表格框内）

用法：python scripts/add_attachment.py <参数…>        （例：python scripts/add_attachment.py --help）

本脚本只把参数转发给仓库内 lib/ 的实现；**不需要安装任何东西**，
也没有 labreport 这个命令——skill 里直接用 python 调用即可。
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "lib"))

from labreport.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main(["attach"] + sys.argv[1:]))
