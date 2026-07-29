# 东南亚卫星产业动态 · 历史归档（最小 SPA 骨架）

![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-已上线-brightgreen) ![自动归档](https://img.shields.io/badge/每日%2021:30-自动同步-blue)

> 🌐 **公网版（自定义域名）**：https://sat.dhow.ink/ ｜ 备用地址：https://pandhow.github.io/sea-sat-archive/ ｜ 由「东南亚卫星·归档+公网同步」自动化每日 21:30 后自动发布（日报生成 21:30 → 本地归档 → 推公网）

一个**纯前端 SPA**，归档「东南亚卫星产业动态」每日自动生成的 HTML 报告（监测泰国、印度尼西亚、马来西亚、新加坡、柬埔寨、越南在卫星通信 / 导航（GNSS·北斗）/ 遥感 / 发射与卫星 四大领域的动态）。浅色调、移动端适配、支持正文关键词搜索。零后端、零数据库、零构建工具——双击或起个静态服务就能跑。

## 目录结构

```
sea-sat-archive/
├── index.html              # 外壳：顶栏 + 期次列表 + 内容查看区
├── app.js                  # SPA 运行时：拉 manifest → 渲染列表 → 哈希路由 → iframe 载入
├── styles.css              # 归档站自身样式（深空科技风）
├── archive_sync.py         # 自动归档脚本：扫 D:\Harry的文件\东南亚卫星产业动态_*.html → issues/ + 重生成 manifest
├── data/
│   └── manifest.json       # 期次清单（日期/标题/标签/文件路径），由脚本维护
├── issues/
│   └── YYYY-MM-DD.html     # 每期报告独立 HTML（iframe 载入）
├── CNAME                   # 自定义域名 sat.dhow.ink（GitHub Pages）
└── README.md
```

## 本地运行

```bash
cd sea-sat-archive
python -m http.server 8080
# 浏览器打开 http://localhost:8080
```

## 新增一期（自动，推荐）

「东南亚卫星产业动态」自动化每日 21:30 生成 `D:\Harry的文件\东南亚卫星产业动态_YYYY-MM-DD.html`，归档只需一句：

```bash
cd sea-sat-archive
python archive_sync.py
```

脚本会：扫描源文件 → 把新一期复制进 `issues/YYYY-MM-DD.html` → 重生成 `data/manifest.json`（按日期降序、期号自动 +1）。标题/标签优先级：sidecar JSON → HTML `<meta archive-title/archive-tags>` → 兜底（扫描国家/领域关键词）。**已归档期次的标题/标签永不被覆盖，内容一致自动跳过（幂等）。**

## 新增一期（手动，备用）

1. 把报告 HTML 复制进 `issues/`，命名 `YYYY-MM-DD.html`
2. 在 `data/manifest.json` 的 `issues` 数组**顶部**加一条：
   ```json
   {
     "date": "2026-07-24",
     "issue_no": "001",
     "title": "一句话概括当天核心看点",
     "tags": ["标签1", "标签2"],
     "file": "issues/2026-07-24.html"
   }
   ```
3. 刷新页面，新期次出现在列表顶部

## 部署（GitHub Pages）

仓库 `pandhow/sea-sat-archive`（public，main 分支根目录托管），自定义域名 `sat.dhow.ink`。
同步脚本 `sync_to_github.py`（与本仓库同目录的父级 `D:\Workbuddy\Claw\`）经 REST Contents API 把静态站推上公网（绕开沙箱拦截的 git 协议）。

## 后续可扩展
- ✅ 全文搜索：已落地 `data/index.json` + `build_index.py`，搜索可命中正文关键词（见 app.js）
- 期次封面图 / 活跃度矩阵可视化
- RSS / 订阅提醒
- 双端同步：归档站更新后，可触发同步到飞书/ima（沿用既有「双端文档同步」技能）
