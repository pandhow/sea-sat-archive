#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复东南亚卫星日报存量报告在浅色模式下的对比度问题。"""
from pathlib import Path

TARGETS = [
    Path(r"D:\Harry的文件"),
    Path(r"D:\Workbuddy\Claw\sea-sat-archive\issues"),
]

CONTRAST_STYLE = """<style id="light-contrast-fix">
/* 修复浅色模式下手机端文字对比度不足 */
.pts,.pts li{color:var(--txt)!important;}
.biz{color:var(--txt)!important;background:rgba(176,125,18,.12)!important;border-left-color:var(--gold)!important;}
.biz b{color:var(--gold)!important;}
.src{color:var(--sub)!important;}
.sub-title{color:var(--sub)!important;}
.card .sm{color:var(--sub)!important;}
a{color:#1a4db5!important;text-decoration:underline!important;}
</style>
"""


def fix_file(p: Path) -> bool:
    s = p.read_text(encoding="utf-8")
    if 'id="light-contrast-fix"' in s:
        return False  # already fixed
    if '<style id="light-override">' not in s:
        return False  # not our target format
    marker = "</head>"
    if marker not in s:
        return False
    s2 = s.replace(marker, CONTRAST_STYLE + "\n" + marker, 1)
    if s2 == s:
        return False
    p.write_text(s2, encoding="utf-8")
    return True


def main():
    files = []
    src = Path(r"D:\Harry的文件")
    if src.exists():
        files += sorted(src.glob("东南亚卫星产业动态_*.html"))
    issues = Path(r"D:\Workbuddy\Claw\sea-sat-archive\issues")
    if issues.exists():
        files += sorted(issues.glob("*.html"))
    # dedupe by absolute path
    seen = set()
    unique = []
    for p in files:
        rp = p.resolve()
        if rp not in seen:
            seen.add(rp)
            unique.append(p)
    changed = 0
    for p in unique:
        if fix_file(p):
            print(f"[FIXED] {p}")
            changed += 1
        else:
            print(f"[SKIP]  {p}")
    print(f"--- 完成：共 {len(unique)} 个文件，修复 {changed} 个 ---")


if __name__ == "__main__":
    main()
