#!/usr/bin/env python
"""校验 data.json：单位归一化、平均值自洽、离群、公式重算比对

用法：python scripts/check_data.py <参数…>        （例：python scripts/check_data.py --help）

本脚本只把参数转发给仓库内 lib/ 的实现；**不需要安装任何东西**，
也没有 labreport 这个命令——skill 里直接用 python 调用即可。
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "lib"))

from labreport.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main(["data"] + sys.argv[1:]))
