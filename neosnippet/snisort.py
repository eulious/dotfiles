#!/usr/bin/env python
# coding:utf-8

import re
import sys
import os
import subprocess
from os.path import join, relpath
from glob import glob


def snisort(name):
    # nameのスニペットをソートする
    # 変数
    a = []
    a2 = []
    b = []
    dic = {}
    dic2 = {}

    # ファイル読み込み
    f = open(name, 'rt')
    line = f.readlines()
    f.close()

    snippet = re.compile(r"snippet")
    for i in range(len(line)):
        line[i] = line[i].replace("\n", "")
        m = snippet.match(line[i])
        if m:
            a.append(i)

    for i in range(len(a)):
        b.append(line[a[i]])
        b[i] = re.sub('^snippet[\t\ ]+', '', b[i])
        dic[b[i]] = a[i]
        a2.append(a[i]-1)

    a2.pop(0)
    a2.append(len(line))
    for i in range(len(a2)):
        dic2[b[i]] = a2[i]

    # 書き込み
    f = open(name, 'wt')
    b.sort()
    for j in range(len(a)):
        for i in range(dic[b[j]], dic2[b[j]]):
            print(line[i], file=f)
        print("", file=f)
    f.close()

    print(" ", b)

if __name__ == '__main__':
    # カレントディレクトリのファイルリストを取得
    path = '.'
    files = [relpath(x, path) for x in glob(join(path, '*'))]

    # snipだけのリストを作成
    yes_snip = []
    for file in files:
        m = re.search('snip', file)
        if m:
            yes_snip.append(file)
    for snip_num in yes_snip:
        files.remove(snip_num)

    # ここにソートしたくないファイルを書く
    #   例： files.remove('python.py')

    # texファイルを同じ内容にする
    tex_time = os.stat('tex.snip').st_mtime
    plaintex_time = os.stat('plaintex.snip').st_mtime
    if tex_time > plaintex_time:
        subprocess.call('cat tex.snip>plaintex.snip', shell=True)
    elif tex_time > plaintex_time:
        subprocess.call('cat plaintex.snip>tex.snip', shell=True)

    # 並び替え
    for snip_num in yes_snip:
        print(snip_num)
        snisort(snip_num)
