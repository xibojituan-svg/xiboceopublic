import re
import os

filepath = r"d:\xibo2026public\ABCD_流程图.html"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# 1. 替换 STYLE 块
new_style = """<style>
  :root {
    --a: #3b82f6; --a-light: rgba(59,130,246,0.15); --a-mid: rgba(59,130,246,0.5);
    --b: #10b981; --b-light: rgba(16,185,129,0.15); --b-mid: rgba(16,185,129,0.5);
    --c1: #f97316; --c1-light: rgba(249,115,22,0.15); --c1-mid: rgba(249,115,22,0.5);
    --c2: #ec4899; --c2-light: rgba(236,72,153,0.15); --c2-mid: rgba(236,72,153,0.5);
    --d: #ef4444; --d-light: rgba(239,68,68,0.15); --d-mid: rgba(239,68,68,0.5);
    --gray: #3f3f46; --bg: #09090b; --card: #18181b;
    --header: rgba(24, 24, 27, 0.85); --text: #f4f4f5; --muted: #a1a1aa;
    --border: #3f3f46;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: "Inter", "PingFang SC", "Microsoft YaHei", sans-serif;
    background: var(--bg); color: var(--text); line-height: 1.5;
  }

  /* ── NAV ── */
  .nav {
    position: sticky; top: 61px; z-index: 100;
    background: var(--header); display: flex; align-items: center;
    padding: 0 32px; border-bottom: 1px solid var(--border);
    backdrop-filter: blur(12px);
  }
  .nav-brand { color: #fff; font-size: 16px; font-weight: 700; padding: 14px 0; margin-right: 40px; }
  .nav-brand span { opacity: .6; font-weight: 400; color: var(--c1); }
  .tab-btn {
    color: rgba(255,255,255,.65); font-size: 14px; padding: 16px 20px;
    border: none; background: none; cursor: pointer; border-bottom: 3px solid transparent;
    transition: all .2s;
  }
  .tab-btn.active { color: #fff; border-bottom-color: var(--a); }
  .tab-btn:hover { color: #fff; }

  /* ── SECTIONS ── */
  .section { display: none; padding: 32px; max-width: 1400px; margin: 0 auto; }
  .section.active { display: block; animation: fadeUp 0.6s ease-out; }

  .page-title { font-size: 28px; font-weight: 800; color: #fff; margin-bottom: 6px; }
  .page-sub { color: var(--muted); font-size: 14px; margin-bottom: 28px; }

  /* ── LEGEND ── */
  .legend { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 28px; }
  .legend-item {
    display: flex; align-items: center; gap: 8px;
    background: var(--card); border-radius: 20px; border: 1px solid var(--border);
    padding: 6px 14px; font-size: 13px; font-weight: 500;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
  }
  .legend-dot { width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0; }

  /* ── DIAGRAM 1: CONVERSION FUNNEL ── */
  .funnel-wrap {
    background: var(--card); border-radius: 16px; border: 1px solid var(--border);
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    padding: 32px; overflow-x: auto;
  }
  .mermaid { min-width: 700px; }

  /* ── DIAGRAM 2: SERVICE JOURNEY ── */
  .journey-grid {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 20px;
  }
  @media (max-width: 900px) { .journey-grid { grid-template-columns: 1fr; } }

  .journey-card {
    background: var(--card); border-radius: 16px; border: 1px solid var(--border);
    box-shadow: 0 10px 30px rgba(0,0,0,0.5); overflow: hidden;
  }
  .journey-header {
    padding: 16px 24px; display: flex; align-items: center; gap: 12px; border-bottom: 1px solid rgba(255,255,255,0.05);
  }
  .journey-header h2 { color: #fff; font-size: 17px; font-weight: 700; }
  .journey-header .badge {
    background: rgba(255,255,255,.1); color: #fff; border: 1px solid rgba(255,255,255,0.2);
    font-size: 11px; padding: 3px 10px; border-radius: 12px;
  }
  .journey-body { padding: 20px 24px 24px; }

  /* Timeline */
  .timeline { position: relative; padding-left: 32px; }
  .timeline::before {
    content: ""; position: absolute; left: 10px; top: 12px; bottom: 12px;
    width: 2px; background: linear-gradient(180deg, var(--line-color) 0%, rgba(255,255,255,0.05) 100%);
  }
  .tl-item { position: relative; margin-bottom: 16px; }
  .tl-item:last-child { margin-bottom: 0; }
  .tl-dot {
    position: absolute; left: -28px; top: 10px;
    width: 18px; height: 18px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 10px; font-weight: 700; color: #fff; flex-shrink: 0;
    box-shadow: 0 0 0 3px var(--card);
  }
  .tl-box {
    border-radius: 10px; padding: 10px 14px;
    border-left: 3px solid var(--line-color);
  }
  .tl-box .tl-head {
    font-size: 13px; font-weight: 700; margin-bottom: 4px; color: #fff;
  }
  .tl-box .tl-detail {
    font-size: 12px; color: var(--muted); line-height: 1.6;
  }
  .tl-box .tl-kpi {
    margin-top: 6px; display: inline-block;
    font-size: 11px; font-weight: 600; padding: 2px 10px;
    border-radius: 10px; background: var(--line-color);
    color: #fff;
  }

  /* ── RISK BOX ── */
  .risk-box {
    background: rgba(249,115,22,0.1); border: 1.5px dashed var(--c1);
    border-radius: 10px; padding: 12px 16px; margin-bottom: 20px;
    font-size: 13px; color: var(--text);
  }
  .risk-box strong { color: var(--c1); }

  /* ── METRIC CARDS ── */
  .metrics { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 20px; }
  .metric-card {
    flex: 1; min-width: 120px; border-radius: 12px; border: 1px solid var(--border);
    padding: 12px 16px; text-align: center;
  }
  .metric-card .m-val { font-size: 22px; font-weight: 800; }
  .metric-card .m-label { font-size: 11px; color: var(--muted); margin-top: 2px; }

  /* ── SECTION 3: COMPARISON ── */
  .compare-grid { display: grid; grid-template-columns: repeat(5,1fr); gap: 16px; margin-bottom: 24px; }
  .compare-col { border-radius: 12px; overflow: hidden; border: 1px solid var(--border); box-shadow: 0 4px 16px rgba(0,0,0,0.5); }
  .compare-col-header { padding: 14px 12px; text-align: center; color: #fff; font-weight: 700; font-size: 14px; }
  .compare-col-body { background: var(--card); }
  .compare-row { padding: 10px 12px; border-bottom: 1px solid var(--border); font-size: 12px; }
  .compare-row:last-child { border-bottom: none; }
  .compare-row .cr-label { color: var(--muted); font-size: 11px; margin-bottom: 3px; }
  .compare-row .cr-val { font-weight: 600; color: var(--text); }
  @keyframes fadeUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>"""

content = re.sub(r'<style>.*?</style>', new_style, content, flags=re.DOTALL)

# 2. 替换内联样式的残余 (比如浅灰色的背景 #F5F5F5 -> var(--border), 阴影等)
content = content.replace("box-shadow:0 2px 16px rgba(0,0,0,.08)", "box-shadow:0 10px 30px rgba(0,0,0,.5); border: 1px solid var(--border)")
content = content.replace("background:#e0e0e0", "background:rgba(255,255,255,0.1); border: 1px solid var(--border)")
content = content.replace("color:#888", "color:var(--text-dim)")
content = content.replace("color:#555", "color:var(--text)")
content = content.replace("border-top:1px solid #eee", "border-top:1px solid var(--border)")

# 3. 替换 Mermaid 主题
old_mermaid = r'%%{init: {"theme":"base","themeVariables":{"primaryColor":"#E3F2FD","primaryTextColor":"#1a1a1a","primaryBorderColor":"#90CAF9","lineColor":"#90A4AE","secondaryColor":"#F5F5F5","tertiaryColor":"#fff","fontSize":"14px"}}}%%'
new_mermaid = r'%%{init: {"theme":"dark","themeVariables":{"primaryColor":"#18181b","primaryTextColor":"#f4f4f5","primaryBorderColor":"#3f3f46","lineColor":"#a1a1aa","secondaryColor":"#27272a","tertiaryColor":"#09090b","fontSize":"14px"}}}%%'
content = content.replace(old_mermaid, new_mermaid)

# 4. 替换 Mermaid classDef 为暗黑版
mermaid_classes = """    classDef entry    fill:#27272a,stroke:#3b82f6,color:#f4f4f5,font-weight:bold
    classDef process  fill:#18181b,stroke:#8b5cf6,color:#f4f4f5,font-weight:bold
    classDef decision fill:#27272a,stroke:#f97316,color:#f4f4f5,font-weight:bold
    classDef aClass   fill:#18181b,stroke:#3b82f6,color:#3b82f6,font-weight:bold
    classDef bClass   fill:#18181b,stroke:#10b981,color:#10b981,font-weight:bold
    classDef c1Class  fill:#18181b,stroke:#f97316,color:#f97316,font-weight:bold
    classDef c2Class  fill:#18181b,stroke:#ec4899,color:#ec4899,font-weight:bold
    classDef dClass   fill:#18181b,stroke:#ef4444,color:#ef4444,font-weight:bold
    classDef aResult  fill:rgba(59,130,246,0.1),stroke:#3b82f6,color:#60a5fa,font-weight:bold
    classDef bResult  fill:rgba(16,185,129,0.1),stroke:#10b981,color:#34d399,font-weight:bold
    classDef c1Result fill:rgba(249,115,22,0.1),stroke:#f97316,color:#fb923c,font-weight:bold
    classDef c2Result fill:rgba(236,72,153,0.1),stroke:#ec4899,color:#f472b6,font-weight:bold
    classDef dResult  fill:rgba(239,68,68,0.1),stroke:#ef4444,color:#f87171,font-weight:bold"""

# 匹配并替换从 classDef entry 到 classDef dResult
content = re.sub(
    r'    classDef entry.*?classDef dResult.*?\n', 
    mermaid_classes + '\n', 
    content, 
    flags=re.DOTALL
)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Rewrote ABCD_流程图.html to use the full global Dark Theme preset.")
