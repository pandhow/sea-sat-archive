#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一次性迁移脚本：把存量「东南亚卫星产业动态」日报统一为浅色调 + 移动端适配，
并将 SmarCo -> Astrolink、SEA SATELLITE WEEKLY -> ASEAN SAT. DAILY。

策略：在原 <style> 之后追加一段 light-override，重定义所有已知 CSS 变量为浅色，
并强制 body/header 浅底深字、注入 @media(max-width:600px) 移动端规则。
这样无论各期原 :root 变量名如何（--bg/--card/--panel/--sat...），都能被统一覆盖。

同时把文本中的 SmarCo / SEA SATELLITE WEEKLY 做全局替换。

注意：必须同时改归档副本(issues/)与源文件(D:\\Harry的文件\\)，
否则夜间 archive_sync 会用深色源文件覆盖回浅色副本。
"""
import sys
from pathlib import Path

OVERRIDE = """
<style id="light-override">
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
header .meta,header .tag,header h1,header h2,header h3,header .sub{color:var(--txt)!important;}
a{color:var(--com)!important;}
@media (max-width:600px){
  .wrap,.container{max-width:100%!important;padding:16px 12px 40px!important;margin:0!important;}
  header{padding:22px 16px!important;}
  h1{font-size:22px!important;}
  h2{font-size:18px!important;margin:26px 0 12px!important;}
  h3,.country{font-size:16px!important;}
  .cards,.core{grid-template-columns:1fr!important;}
  .card,.c,.item,.sec{padding:14px!important;}
  table{font-size:12px!important;}
  th,td{padding:8px 6px!important;}
  .item .inner,.inner{padding:14px!important;}
  .sub-title{margin:16px 0 8px!important;}
}
</style>
"""

# (目录, 文件名匹配模式)
TARGETS = [
    (Path(r"D:\Harry的文件"), "东南亚卫星产业动态_*.html"),
    (Path(r"D:\Workbuddy\Claw\sea-sat-archive\issues"), "*.html"),
]


def migrate_file(p: Path) -> bool:
    html = p.read_text(encoding="utf-8", errors="ignore")
    orig = html
    html = html.replace("SmarCo", "Astrolink")
    html = html.replace("SEA SATELLITE WEEKLY", "ASEAN SAT. DAILY")
    if "light-override" not in html:
        html = html.replace("</head>", OVERRIDE + "\n</head>", 1)
    if html != orig:
        p.write_text(html, encoding="utf-8")
        return True
    return False


def main():
    total = 0
    changed = 0
    for d, pat in TARGETS:
        if not d.exists():
            print(f"[SKIP] 目录不存在: {d}")
            continue
        for f in sorted(d.glob(pat)):
            total += 1
            if migrate_file(f):
                changed += 1
                print(f"[OK]   {f}")
    print(f"\n扫描 {total} 个文件，修改 {changed} 个。")


if __name__ == "__main__":
    main()
