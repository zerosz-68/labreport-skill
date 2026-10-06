#!/usr/bin/env python
"""环境体检：Python 版本、必需包、可选程序、中文字体

用法：python scripts/doctor.py <参数…>        （例：python scripts/doctor.py --help）

本脚本只把参数转发给仓库内 lib/ 的实现；**不需要安装任何东西**，
也没有 labreport 这个命令——skill 里直接用 python 调用即可。
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "lib"))

from labreport.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main(["doctor"] + sys.argv[1:]))
