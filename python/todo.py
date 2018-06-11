#!/usr/bin/env python
# coding: utf-8

import sys
import os

argvs = sys.argv
if len(argvs) > 2:
    for i in range(2, len(argvs)):
        argvs[1] += " " + argvs[i]

todo = os.path.expanduser("~/Dropbox/.set/python/todo.txt")

f = open(todo, 'rt')
lines = f.readlines()
f.close()

if len(argvs) > 1:
    try:
        num = int(argvs[1])
        try:
            b = lines.pop(num-1)
        except IndexError:
            print("IndexError: argument out of range")
    except ValueError:
        lines.append(argvs[1])

    f = open(todo, 'wt')

    for line in lines:
        line = line.replace('\n', '')
        print(line, file=f)
    f.close()

for i in range(len(lines)):
    lines[i] = lines[i].replace('\n', '')
    print("["+str(i+1)+"]: ", end="")
    print(lines[i])
