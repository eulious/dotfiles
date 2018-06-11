#!/usr/bin/env python
# coding:utf-8

import subprocess
import os

begin = [
    "\\begin{table}[H]",
    " \\begin{center}",
    "  \\caption{}",
    "   \\begin{tabular}{|",
]

end = [
    "   \\end{tabular}",
    "  \\label{",
    " \\end{center}",
    "\\end{table}",
]

subprocess.call('pbpaste > .log', shell=True)
f = open('.log', 'rt')
lines = f.readlines()
f.close()

for i in range(len(lines)):
    lines[i] = lines[i].replace('\t', ' & ')
    lines[i] = lines[i].replace('\n', '')
    lines[i] = '     ' + lines[i] + '\\\\ \\hline'
tabular = lines[0].count("&") + 1
begin[3] += "l|"*tabular + '} \\hline'
end[1] += "hyo" + '}'

fin2 = open('.log', 'wt')
for i in range(0, 4):
    print(begin[i], file=fin2)
for i in range(len(lines)):
    print(lines[i], file=fin2)
for i in range(0, 4):
    print(end[i], file=fin2)
fin2.close()

subprocess.call('cat .log | pbcopy', shell=True)
subprocess.call('cat .log', shell=True)
os.remove('.log')
