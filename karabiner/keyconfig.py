#!/usr/bin/env python
# coding:utf-8

"""
6/26: conditionsのtypeに未対応の条件を指定するとルール全体が無効になる
device_if, device_unlessが未対応?として扱われているため設定すると反応しなくなる

6/26: MacではGHUBでG600が認識しない
WindowsでG HUBでオンボードを設定する。プロファイル全てに同じ物を設定する
DPIとLEDカラーのみ反映される。色はオフにするとバグるので黒色に設定する
GUIで設定するsimple modificationsはデバイス毎に設定できるのでmagickeybordの数字キーをNumpadにする

9/18: 全てのキーボードが英字キーボードとして認識されてしまうため、一部のショートカットキーはクリスタ側で他のキーに割り当てる必要がある
12/11: TODO: file_pathsをチルダ展開
"""

from csv import reader
from json import dump, load
from yaml import safe_load
from os.path import expanduser, dirname

DIR = f"{dirname(__file__)}/220626"
TARGET = expanduser("~/.config/karabiner/karabiner.json")

d = load(open(TARGET))
rules = d["profiles"][0]["complex_modifications"]["rules"]

for config in  safe_load(open(f"{DIR}/config.yml"))["rules"]:
    out = []

    if "modifiers" in config:
        for from_key, to_key in config["modifiers"].items():
            out.append({
                "type": "basic",
                "conditions": config["conditions"],
                "from": {"key_code": from_key, "modifiers": {"optional": ["any"]}},
                "to": [{"key_code": to_key }],
            })

    cr = reader(open(f"{DIR}/{config['file']}"))
    cr.__next__()
    for [from_mod, from_key, to_mod1, to_mod2, to_key, detail] in cr:
        if to_key == "":
            if  detail != "":
                print("warning:", detail)
            continue
        obj = {
            "type": "basic",
            "conditions": config["conditions"],
            "from": {"key_code": from_key},
            "to": [{"key_code": to_key}],
        }
        if "button" in from_key:
            obj["from"]["pointing_button"] = obj["from"].pop("key_code")
        if "button" in to_key:
            obj["to"][0]["pointing_button"] = obj["to"][0].pop("key_code")
        if from_mod:
            if "modifiers" in config and from_mod in config["modifiers"]:
                from_mod = config["modifiers"][from_mod]
            obj["from"]["modifiers"] = {"mandatory": [from_mod]}
        if to_mod1:
            obj["to"][0]["modifiers"] = [to_mod1]
        if to_mod2:
            obj["to"][0]["modifiers"].append(to_mod2)
        if "shell" in to_mod1:
            obj["to"] =  [{"shell_command": to_key}]
        out.append(obj)

    for i in range(len(rules)):
        if rules[i]["description"] == config["description"]:
            d["profiles"][0]["complex_modifications"]["rules"][i]["manipulators"] = out
            break
    else:
        wrap = {"description": config["description"], "manipulators": out}
        d["profiles"][0]["complex_modifications"]["rules"].append(wrap)
    print("configured:", config["description"])

dump(d, open(TARGET, "wt"), indent=4, ensure_ascii=False)