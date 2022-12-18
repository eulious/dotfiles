#!/usr/bin/env python
# coding:utf-8

from pyperclip import copy, paste

input_text = paste()

out = ""
quoteFlag = False
for line in input_text.split("\n"):
    line = line.strip()

    hyphen_flag = False
    new_line = ""
    for s in line:
        if hyphen_flag:
            hyphen_flag = False
            new_line += s.upper()
        elif s == "-":
            hyphen_flag = True
        else:
            new_line += s

    line = new_line.replace(";", "")
    if "{" in line:
        selector = line.replace("{", "").strip()
        if selector[0] == "." or selector[0] == "#":
            selector = selector[1:]
        elif selector[0] == "&":
            quoteFlag = True
            selector = f'"{selector}"'
        if quoteFlag:
            line = f"{selector}: {{"
        else:
            line = f"{selector}: css({{"
    elif ":" in line:
        attr, value = line.split(":")
        line = f'{attr}: "{value.strip()}",'
    elif "}" in line:
        if quoteFlag:
            quoteFlag = False
            line = "},"
        else:
            line = "}),"
    out += line + "\n"

print(out)
copy(out)