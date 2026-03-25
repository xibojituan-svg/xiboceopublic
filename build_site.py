import os
import glob
import re

SITE_DIR = "."

generic_css = """
  <!-- 引入统一样式基础 -->
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #f8fafc; --surface: #ffffff; --border: #e2e8f0;
      --text: #0f172a; --text-dim: #64748b; --text-light: #94a3b8;
      --brand: #f97316; --dark: #1e293b;
    }
    body {
      font-family: 'Inter', -apple-system, 'PingFang SC', sans-serif !important;
    }
    /* Nav */
    .site-nav {
      position: sticky; top: 0; z-index: 9999;
      background: rgba(30,41,59,0.95); backdrop-filter: blur(12px);
      border-bottom: 1px solid rgba(255,255,255,0.08);
      padding: 0 clamp(12px, 4vw, 32px);
    }
    .site-nav-inner {
      max-width: 1280px; margin: 0 auto;
      display: flex; align-items: center; height: 50px;
      gap: 4px; overflow-x: auto; scrollbar-width: none;
    }
    .site-nav-inner::-webkit-scrollbar { display: none; }
    .nav-logo { font-size: 13px; font-weight: 800; color: var(--brand); white-space: nowrap; margin-right: 10px; text-decoration: none; }
    .nav-divider { width: 1px; height: 18px; background: rgba(255,255,255,0.18); margin: 0 6px; flex-shrink: 0; }
    .nav-link {
      display: flex; align-items: center; gap: 4px;
      padding: 4px 11px; border-radius: 20px;
      font-size: 12px; font-weight: 600; color: #94a3b8;
      text-decoration: none; white-space: nowrap; transition: all 0.2s; flex-shrink: 0;
    }
    .nav-link:hover { color: #fff; background: rgba(249,115,22,0.15); }
    .nav-link.active { color: #fff; background: rgba(249,115,22,0.2); border: 1px solid rgba(249,115,22,0.4); }
  </style>
"""

global_nav = """
<!-- 全局统一导航栏 -->
<nav class="site-nav">
  <div class="site-nav-inner">
    <a href="index.html" class="nav-logo">喜播集团 ⚡</a>
    <div class="nav-divider"></div>
    <a href="index.html" class="nav-link">🏠 战略导航台</a>
    <a href="abcd_process_cfo_cho.html" class="nav-link">⚙️ ABCD重构</a>
    <a href="new_business_process_infographic.html" class="nav-link">🗺️ 业务全景</a>
    <a href="abcd_ai_bootcamp_poster.html" class="nav-link">🤖 AI分层</a>
    <a href="ue_model_comparison.html" class="nav-link">💰 UE财务对照</a>
    <a href="d_user_optimization.html" class="nav-link">🛑 拦截D类</a>
    <a href="class_manager_analysis.html" class="nav-link">🏫 班主任重塑</a>
  </div>
</nav>
"""

index_html = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
  <title>喜播集团 2026 战略导航台</title>
  {generic_css}
  <style>
    body {{ background: #f1f5f9; }}
    .page-container {{
      max-width: 900px;
      margin: 40px auto;
      padding: 30px;
      background: #fff;
      border-radius: 16px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }}
    .header-banner {{
      background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
      color: white;
      padding: 40px;
      border-radius: 16px;
      margin-bottom: 40px;
      position: relative;
      overflow: hidden;
    }}
    .header-banner::after {{
      content: '2026'; position: absolute; right: -20px; bottom: -40px;
      font-size: 150px; font-weight: 900; opacity: 0.05;
    }}
    h1 {{ font-size: 32px; margin-bottom: 12px; font-weight: 800; letter-spacing: -0.5px; }}
    .subtitle {{ font-size: 16px; color: #cbd5e1; font-weight: 500; }}
    
    .category {{ margin-bottom: 40px; }}
    .cat-title {{ 
      font-size: 20px; color: var(--dark); 
      border-left: 4px solid var(--brand); 
      padding-left: 12px; margin-bottom: 20px; font-weight: 800; 
    }}
    .link-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 16px; }}
    .doc-link {{
      display: block; padding: 20px;
      background: var(--bg); border: 1px solid var(--border);
      border-radius: 12px; color: var(--text);
      text-decoration: none; transition: all 0.2s;
    }}
    .doc-link:hover {{ 
      border-color: var(--brand); background: #ffffff;
      transform: translateY(-3px); box-shadow: 0 8px 20px rgba(249,115,22,0.1); 
    }}
    .doc-title {{ font-weight: 700; font-size: 16px; margin-bottom: 8px; color: var(--dark); display: flex; align-items: center; gap: 6px; }}
    .doc-desc {{ font-size: 13px; color: var(--text-dim); line-height: 1.5; }}
    
    @media (max-width: 600px) {{
      .page-container {{ margin: 15px; padding: 20px; }}
      .header-banner {{ padding: 25px; }}
      h1 {{ font-size: 24px; }}
    }}
  </style>
</head>
<body>
{global_nav}
<div class="page-container">
  <div class="header-banner">
    <h1>CEO 战略导航作战台</h1>
    <div class="subtitle">ABCD分层体系 · UE漏洞修复 · 商业底层逻辑</div>
  </div>

  <div class="category">
    <div class="cat-title">1. 第四大战略战役：ABCD人群运营重构</div>
    <div class="link-grid">
      <a href="new_business_process_infographic.html" class="doc-link">
        <div class="doc-title">🗺️ 新版业务全景图</div>
        <div class="doc-desc">基于ABCD分层与前后端连轴转的终极战略设计。</div>
      </a>
      <a href="abcd_process_cfo_cho.html" class="doc-link">
        <div class="doc-title">⚙️ 组织财务双模重构</div>
        <div class="doc-desc">解决：谁来服务(CHO)、花多少钱赚什么钱(CFO)。</div>
      </a>
      <a href="abcd_ai_bootcamp_poster.html" class="doc-link">
        <div class="doc-title">🤖 AI分层判别海报</div>
        <div class="doc-desc">体验营里的风控拦截体系，产品级落地大纲。</div>
      </a>
      <a href="segmentation_radarmap.html" class="doc-link">
        <div class="doc-title">📊 用户切片雷达图</div>
        <div class="doc-desc">底层消费能力与意愿画像分析。</div>
      </a>
    </div>
  </div>

  <div class="category">
    <div class="cat-title">2. 财务风控与UE生命线</div>
    <div class="link-grid">
      <a href="ue_model_comparison.html" class="doc-link">
        <div class="doc-title">💰 新旧UE模型财务对照</div>
        <div class="doc-desc">清算前端投放、后端退单，重构健康利润池。</div>
      </a>
      <a href="d_user_optimization.html" class="doc-link">
        <div class="doc-title">🛑 D类用户熔断策略</div>
        <div class="doc-desc">高危客群的一票否决合规防线。</div>
      </a>
      <a href="ue_funnel_simulator.html" class="doc-link">
        <div class="doc-title">📈 漏斗与留存模拟器</div>
        <div class="doc-desc">在线推演利润与流失率节点变化。</div>
      </a>
    </div>
  </div>

  <div class="category">
    <div class="cat-title">3. 原来端业务与组织复盘</div>
    <div class="link-grid">
      <a href="class_manager_analysis.html" class="doc-link">
        <div class="doc-title">🏫 班主任体系总诊断</div>
        <div class="doc-desc">寻回被吞噬的人效黑洞（1v1无效私聊）。</div>
      </a>
      <a href="class_manager_kpi_analysis.html" class="doc-link">
        <div class="doc-title">📝 班主任KPI考核解剖</div>
        <div class="doc-desc">用退费暂扣期掐灭错误逼单预期。</div>
      </a>
      <a href="live_sop_upgrade_plan.html" class="doc-link">
        <div class="doc-title">📺 直播间合规清洗</div>
        <div class="doc-desc">扫除过度承诺，建立不虚假且高转化的交付。</div>
      </a>
    </div>
  </div>

  <div class="category">
    <div class="cat-title">4. 产品品类深度洞察</div>
    <div class="link-grid">
      <a href="ai_short_video_conversion_insight.html" class="doc-link">
        <div class="doc-title">🎬 AI短视频洞察</div>
        <div class="doc-desc">基于短视频链路的漏斗梳理。</div>
      </a>
      <a href="ai_writing_conversion_insight.html" class="doc-link">
        <div class="doc-title">✍️ AI写作人群洞察</div>
        <div class="doc-desc">网赚粉与能力粉的剥离。</div>
      </a>
      <a href="competitor_shifang_lihua_analysis.html" class="doc-link">
        <div class="doc-title">⚔️ 十方梨花竞品剖析</div>
        <div class="doc-desc">拆解对手通过毒性陪伴透支口碑的警示教训。</div>
      </a>
    </div>
  </div>

</div>
</body>
</html>
"""

with open(os.path.join(SITE_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)

# Update sub-pages
for filepath in glob.glob(os.path.join(SITE_DIR, "*.html")):
    if filepath.endswith("index.html"): continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # remove old nav variations
    content = re.sub(r'<nav[^>]*>.*?</nav>', '', content, flags=re.DOTALL)
    
    # insert generic css
    if '<!-- 引入统一样式基础 -->' not in content:
        content = re.sub(r'</head>', generic_css + '\n</head>', content, flags=re.IGNORECASE)
    
    # insert global nav after <body>
    if '<!-- 全局统一导航栏 -->' not in content:
        content = re.sub(r'<body[^>]*>', lambda m: m.group(0) + '\n' + global_nav, content, flags=re.IGNORECASE|re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Site built successfully.")
