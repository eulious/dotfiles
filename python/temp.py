#!/usr/bin/env python
# coding:utf-8

# テンプレートを標準出力・クリップボードに貼り付け

import os
import re
import sys
import subprocess

# tempフォルダのリストを作成
dir = os.path.expanduser("~/Dropbox/.set/python/temp/")
files = os.listdir(dir)

# 引数が無い時テンプレートの一覧を表示
# C-vをするとtempフォルダに移動
if len(sys.argv) != 2:
    files.pop(0)
    for i in range(len(files)):
        files[i] = re.sub('\..+$', '', files[i])
    print(files)
    subprocess.call('echo cd ~/dropbox/.set/python/temp | pbcopy', shell=True)
    sys.exit()

# 引数のテンプレートファイルを読み込み
for file in files:
    m = re.search(sys.argv[1], file)
    if m:
        f = open(dir + file, 'rt')
        lines = f.readlines()
        f.close()

# .logにテンプレートを書き出す
f = open('.log', 'wt')
for line in lines:
    line = line.replace("\n", "")
    print(line)
    print(line, file=f)
f.close()

# catコマンドで表示、その後logを削除
subprocess.call('cat .log | pbcopy', shell=True)
os.remove('.log')
