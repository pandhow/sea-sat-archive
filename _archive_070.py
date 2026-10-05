# -*- coding: utf-8 -*-
import json, shutil
from pathlib import Path

BASE = Path(r"D:\Workbuddy\Claw\sea-sat-archive")
SRC = Path(r"D:\Harry的文件\东南亚卫星产业动态_2026-10-05.html")
DST = BASE / "issues" / "2026-10-05.html"
MANIFEST = BASE / "data" / "manifest.json"

# 1) copy html into issues/
DST.write_bytes(SRC.read_bytes())
print("copied ->", DST, DST.stat().st_size, "bytes")

# 2) insert manifest entry at head
data = json.loads(MANIFEST.read_text(encoding="utf-8"))
entry = {
    "date": "2026-10-05",
    "issue_no": "070",
    "title": "台风博罗依重创越南北中部；Starlink越南正式商用；LOTUSat-1雷达星2027年底待发；北斗农机强制预装口径经核修正",
    "tags": ["越南","卫星通信","导航","北斗","遥感","发射","Starlink","台风博罗依","北斗农机","LOTUSat","VNSC","苏林"],
    "file": "issues/2026-10-05.html",
}
data["issues"].insert(0, entry)
MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("manifest head issue_no =", data["issues"][0]["issue_no"], "| total issues =", len(data["issues"]))
