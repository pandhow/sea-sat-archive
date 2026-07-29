#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""还原「东南亚手机端对齐海垦」改动：
- 把 light-override 换回 浅色变量 + 普通移动端@media（无 masthead 固定顶部）
- 删除 SEA-MOBILE-V2 的 <script> 切分器
保留：浅色主题、越南、4板块、改名、正文搜索索引（SPA 侧）
"""
import re, pathlib

NEW_LIGHT = """<style id="light-override">
:root{
  --bg:#eef1f7;--bg2:#e3e9f4;--card:#ffffff;--card2:#f3f6fc;
  --panel:#ffffff;--panel2:#f3f6fc;--line:#dde3ef;
  --txt:#1b2440;--sub:#62708f;--dim:#8593ad;
  --sat:#2c6fd6;--hi:#c08a16;--ok:#0f9d8c;--bad:#e03131;
  --th:#2c6fd6;--id:#0f9d8c;--my:#7a3fb0;--sg:#8a5cd0;--kh:#d6418f;
  --gold:#b07d12;--com:#2c6fd6;--nav:#0f9d8c;--rs:#d6418f;--launch:#e8833a;
}
body{background:var(--bg)!important;color:var(--txt)!important;}
header{background:var(--panel2)!important;color:var(--txt)!important;}
header .meta,header .tag,header h1,header h2,header h3,header .sub,header .flag{color:var(--txt)!important;}
a{color:var(--com)!important;}
/* 普通移动端适配（仅手机宽度，无固定顶部 masthead 结构） */
@media (max-width:600px){
  .wrap{max-width:100%;padding:16px 12px 40px;}
  header{padding:20px 16px;}
  h1{font-size:22px;}
  h2{font-size:18px;margin:24px 0 12px;}
  h3{font-variant:normal;}
  h3{font-size:16px;}
  .cards,.grid{grid-template-columns:1fr;}
  .card,.domain,.item{padding:14px;}
  table,.matrix{font-size:12px;}
  th,td{padding:8px 6px;}
  .inner,.overview{padding:14px 16px;}
}
</style>"""

TARGETS = [
    pathlib.Path(r"D:\Workbuddy\Claw\sea-sat-archive\issues"),
    pathlib.Path(r"D:\Harry的文件"),
]

def revert(p: pathlib.Path):
    data = p.read_text(encoding="utf-8")
    if 'SEA-MOBILE-V2' not in data and '<script>' not in data:
        return "skip"
    # 1) 换回普通移动端 light-override（去掉 masthead 固定顶部规则）
    if 'light-override' in data:
        data = re.sub(r'<style id="light-override">.*?</style>', NEW_LIGHT, data, count=1, flags=re.S)
    # 2) 删除 masthead 切分脚本
    data = re.sub(r'<script>.*?</script>', '', data, count=1, flags=re.S)
    p.write_text(data, encoding="utf-8")
    return "ok"

if __name__ == "__main__":
    total = {}
    for d in TARGETS:
        if not d.exists():
            print(f"[SKIP] 目录不存在: {d}")
            continue
        files = sorted(d.glob("*.html")) if d.name == "issues" else sorted(d.glob("东南亚卫星产业动态_*.html"))
        for f in files:
            r = revert(f)
            total[r] = total.get(r, 0) + 1
            print(f"  {r:6s} {f.name}")
    print("汇总:", total)
