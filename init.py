from pathlib import Path
import re
import json
import shutil

pathstack = []

def concat(parent, child):
    return "/".join([parent] + pathstack + [child])

def matches(pathstr):
    return any([re.match(pattern, pathstr) for pattern in pickup])

def walk(location):
    for f in location.iterdir():
        if f.is_dir():
            pathstack.append(f.name)
            walk(f)
            pathstack.pop(-1)
        elif matches(concat("", f.name)[1:]):
            p = Path(concat(work_name, ""))
            if not p.exists():
                p.mkdir(parents=True)
            p = Path(str(p) + "/" + f.name)
            target_name = concat(origin_name, f.name)
            p.symlink_to(target_name)
            print("pick:" + target_name)

config_file = "settings.json"
with open(config_file, "r") as f:
    tmp = json.load(f)

pickup = [re.compile(x) for x in tmp["pickup"]]

origin = Path('.')
origin_name = str(origin.resolve())
work_name = origin_name + "/Workspace"

base = Path(work_name)
if base.exists():
    shutil.rmtree(work_name)
base.mkdir(exist_ok=True)
walk(origin)
