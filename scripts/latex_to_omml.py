#!/usr/bin/env python
"""LaTeX → Word 原生公式（OMML），内置转换，不依赖 pandoc

用法：python scripts/latex_to_omml.py <参数…>        （例：python scripts/latex_to_omml.py --help）

本脚本只把参数转发给仓库内 lib/ 的实现；**不需要安装任何东西**，
也没有 labreport 这个命令——skill 里直接用 python 调用即可。
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "lib"))

from labreport.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main(["omml"] + sys.argv[1:]))
