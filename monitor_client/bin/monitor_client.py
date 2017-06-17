#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
__author__ = "BIGNI"
__date__ = "2017/4/15 23:39"

import os
import sys
#当前文件绝对路径
current_path = os.path.abspath(__file__)
base_dir = os.path.dirname(os.path.dirname(current_path))
#设置client根路径
sys.path.append(base_dir)

from core import main


if __name__ == "__main__":
    client = main.main_command(sys.argv)


