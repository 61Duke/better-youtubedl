# -*- coding: utf-8 -*-
import argparse
import math
import re
from os import path
from sys import stdout
from time import clock


def safe_filename(text, max_length=200):
    """消除许多操作系统的文件名。
     ：params text：未经批准的文件名。
    """
    # 整理丑化格式的文件名。
    text = text.replace('_', ' ')
    text = text.replace(':', ' -')
    # NTFS禁止包含0-31（0x00-0x1F）范围内的字符的文件名
    # NTFS新技术文件系统是Windows NT家族（如，Windows 2000、Windows XP、
    # Windows Vista、Windows 7和 windows 8.1）等的限制级专用的文件系统
    # （操作系统所在的盘符的文件系统必须格式化为NTFS的文件系统，4096簇环境下）
    ntfs = [chr(i) for i in range(0, 31)]

    # 删除这些应该使大多数文件名安全的广泛的操作系统。
    paranoid = ['\"', '\#', '\$', '\%', '\'', '\*', '\,', '\.', '\/', '\:',
                '\;', '\<', '\>', '\?', '\\', '\^', '\|', '\~', '\\\\']

    blacklist = re.compile('|'.join(ntfs + paranoid), re.UNICODE)
    filename = blacklist.sub('', text)
    return filename[:max_length]
