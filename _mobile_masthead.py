#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把东南亚卫星日报存量报告（issues/ + D:\\Harry的文件\\）改造为：
- 浅色调（保留既有 light-override 变量）
- 移动端对齐海垦日报：上方固定模块 ≤1/3，下方可滑动
实现方式：注入"移动端专用运行时脚本"，在手机宽度下自动把
  [标题 + 核心看点 + 矩阵] 包成 .masthead，其余包成 .body，
  配合 @media 固定顶部 + 可滑动 CSS。对所有结构代（早期/最新）均生效。
幂等：已含 SEA-MOBILE-V2 标记则跳过。
"""
import re, pathlib

MARK = "SEA-MOBILE-V2"

NEW_STYLE = """<style id="light-override">
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
/* SEA-MOBILE-V2 对齐海垦日报：上方固定≤1/3，下方可滑动 */
@media (max-width:600px){
  html,body{height:100%!important;overflow:hidden!important;}
  body{padding:0!important;}
  .wrap{max-width:100%!important;margin:0!important;padding:0!important;height:100vh!important;display:flex!important;flex-direction:column!important;overflow:hidden!important;}
  .masthead{position:relative;z-index:5;background:var(--bg);border-bottom:1px solid var(--line);max-height:33vh;overflow:auto;-webkit-overflow-scrolling:touch;padding:14px 14px 8px;flex:0 0 auto;}
  .body{flex:1 1 auto;overflow:auto;-webkit-overflow-scrolling:touch;padding:16px 14px 48px;}
  header{border-radius:0!important;margin-bottom:12px!important;padding:20px 16px!important;}
  h1{font-size:22px!important;}
  h2{font-size:18px!important;margin:22px 0 10px!important;}
  h3{font-size:16px!important;}
  .cards,.grid{grid-template-columns:1fr!important;}
  .card,.domain{padding:14px!important;}
  table,.matrix{font-size:12px!important;}
  th,td{padding:8px 6px!important;}
  .item .inner,.inner,.overview{padding:14px 16px!important;}
  .sub-title{margin:16px 0 8px!important;}
  .biz,.item{margin-top:12px!important;}
}
</style>"""

SCRIPT = """<script>
/* SEA-MOBILE-V2 runtime masthead splitter (对齐海垦日报: 上方固定≤1/3, 下方可滑动) */
(function(){
  function isCountryHeading(el){
    if(!el || !el.tagName) return false;
    var t = el.tagName.toLowerCase();
    if(t!=='h2' && t!=='h3') return false;
    if(el.classList && el.classList.contains('country')) return true;
    var txt = el.textContent || '';
    if(/\\uD83C\\uDDF9\\uD83C\\uDDED|\\uD83C\\uDDEE\\uD83C\\uDDE9|\\uD83C\\uDDF2\\uD83C\\uDDFE|\\uD83C\\uDDF8\\uD83C\\uDDEC|\\uD83C\\uDDF0\\uD83C\\uDDED|\\uD83C\\uDDFB\\uD83C\\uDDF3/.test(txt)) return true;
    return false;
  }
  function setup(){
    if(window.__seaMastheadDone) return;
    var wrap = document.querySelector('.wrap');
    if(!wrap) return;
    if(wrap.children.length && wrap.children[0].classList && wrap.children[0].classList.contains('masthead')){
      window.__seaMastheadDone = true; return;
    }
    if(!window.matchMedia || !window.matchMedia('(max-width:600px)').matches) return;
    var mast = document.createElement('div'); mast.className = 'masthead';
    var body = document.createElement('div'); body.className = 'body';
    var kids = Array.prototype.slice.call(wrap.children);
    var splitAt = kids.length;
    for(var i=0;i<kids.length;i++){ if(isCountryHeading(kids[i])){ splitAt = i; break; } }
    for(var i=0;i<splitAt;i++) mast.appendChild(kids[i]);
    for(var i=splitAt;i<kids.length;i++) body.appendChild(kids[i]);
    wrap.appendChild(mast);
    wrap.appendChild(body);
    window.__seaMastheadDone = true;
  }
  if(document.readyState!=='loading') setup();
  else document.addEventListener('DOMContentLoaded', setup);
  window.addEventListener('resize', function(){
    if(window.matchMedia && window.matchMedia('(max-width:600px)').matches) setup();
  });
})();
</script>"""

TARGETS = [
    pathlib.Path(r"D:\Workbuddy\Claw\sea-sat-archive\issues"),
    pathlib.Path(r"D:\Harry的文件"),
]

def migrate(p: pathlib.Path):
    data = p.read_text(encoding="utf-8")
    if MARK in data:
        return "skip"
    if 'light-override' not in data:
        return "no-light"
    # 替换 light-override 整块
    data = re.sub(r'<style id="light-override">.*?</style>',
                  NEW_STYLE, data, count=1, flags=re.S)
    # 在 </body> 前注入运行时脚本
    data = data.replace("</body>", SCRIPT + "\n</body>", 1)
    p.write_text(data, encoding="utf-8")
    return "ok"

if __name__ == "__main__":
    total = {"ok":0, "skip":0, "no-light":0}
    for d in TARGETS:
        if not d.exists():
            print(f"[SKIP] 目录不存在: {d}")
            continue
        # issues 目录下的所有 html；D:\Harry的文件 下的东南亚卫星产业动态_*.html
        if d.name == "issues":
            files = sorted(d.glob("*.html"))
        else:
            files = sorted(d.glob("东南亚卫星产业动态_*.html"))
        for f in files:
            r = migrate(f)
            total[r] = total.get(r, 0) + 1
            print(f"  {r:8s} {f.name}")
    print("汇总:", total)
