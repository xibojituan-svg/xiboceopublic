import os
import glob
import re

SITE_DIR = "."

DARK_CSS = """
  <!-- 引入统一样式基础(DARK MODE OVERRIDE) -->
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #09090b;
      --bg-surface: #18181b;
      --bg-surface-hover: #27272a;
      --border: #3f3f46;
      --text: #f4f4f5;
      --text-dim: #a1a1aa;
      --text-muted: #71717a;
      
      --brand-primary: #ef4444; 
      --brand-secondary: #f97316; 
      --brand-accent: #10b981; 
      --brand-glow: rgba(239, 68, 68, 0.2);

      /* PAGE SPECIFIC OVERRIDES */
      --text-main: var(--text) !important;
      --text-light: var(--text-dim) !important;
      --border-line: var(--border) !important;
      --bg-body: var(--bg) !important;
      --bg-card: var(--bg-surface) !important;
      --table-header: #1e1e24 !important;
      --insight-bg: rgba(155, 81, 224, 0.05) !important; 
      --insight-border: #9b51e0 !important;
      --primary-blue: #60a5fa !important;
    }

    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    body {
      font-family: 'Inter', -apple-system, 'PingFang SC', sans-serif !important;
      background-color: var(--bg) !important;
      color: var(--text) !important;
      line-height: 1.6;
    }

    /* Background FX */
    .bg-glow {
      position: fixed; top: -20vh; left: 50%; transform: translateX(-50%);
      width: 100vw; height: 60vh;
      background: radial-gradient(ellipse at bottom, rgba(249, 115, 22, 0.15) 0%, rgba(9, 9, 11, 0) 70%);
      z-index: -1; pointer-events: none;
    }

    /* Nav */
    .site-nav {
      position: sticky; top: 0; z-index: 9999;
      background: rgba(9, 9, 11, 0.8); backdrop-filter: blur(16px);
      border-bottom: 1px solid rgba(255,255,255,0.05);
      padding: 0 clamp(16px, 4vw, 32px);
    }
    .site-nav-inner {
      max-width: 1400px; margin: 0 auto;
      display: flex; align-items: center; height: 60px;
      gap: 12px; overflow-x: auto; scrollbar-width: none;
    }
    .site-nav-inner::-webkit-scrollbar { display: none; }
    .nav-logo { font-size: 16px; font-weight: 900; color: var(--text); white-space: nowrap; text-decoration: none; margin-right: 20px; display: flex; align-items: center; gap: 8px;}
    .nav-logo span { color: var(--brand-secondary); }
    .nav-link {
      display: flex; align-items: center; gap: 6px;
      padding: 6px 14px; border-radius: 100px;
      font-size: 13px; font-weight: 600; color: var(--text-dim);
      text-decoration: none; white-space: nowrap; transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .nav-link:hover { color: var(--text); background: rgba(255,255,255,0.1); }
    .nav-link.active { color: #fff; background: var(--brand-primary); box-shadow: 0 0 20px var(--brand-glow); }

    /* GLOBAL OVERRIDES */
    body, p, div, span, li, td, article, main, section {
        color: rgba(255, 255, 255, 0.85) !important;
    }
    h1, h2, h3, h4, .title, strong, b, .card-title, .node-q, .branch-label { color: #ffffff !important; }
    
    /* COMPREHENSIVE SUBSTRING MATCHING FOR CONTAINER BACKGROUNDS */
    .report-container, .page-container, .dashboard-container, .process-container, .map-container, 
    .container, .tree-section, .node-content, .branch-item, .panel, table, .table-wrapper, .page,
    [class*="card"]:not(.card-d), [class*="-box"]:not(.action-box), [class*="-wrap"], 
    [class*="bg-gray-"], [class*="bg-blue-"], [class*="bg-red-"], [class*="bg-orange-"], [class*="bg-white"],
    [class*="lane"], [class*="-step"], [class*="-track"], [class*="tag"], [class*="badge"],
    [class*="alert"], [class*="-block"], [class*="banner"], [class*="reasoning"], [class*="insight"],
    [class*="greeting"], [class*="recalibrate"], [class*="hook-"], input, select, textarea, button,
    div[style*="background:#FFF"], div[style*="background-color: #FFF"] {
       background-color: var(--bg-surface) !important;
       border-color: var(--border) !important;
       box-shadow: 0 4px 20px rgba(0,0,0,0.5) !important;
    }

    /* EXCEPTIONS & SPECIAL HIGHLIGHTS */
    .logic-banner {
       background: linear-gradient(135deg, #1e1e24, #09090b) !important;
       box-shadow: 0 10px 40px rgba(0,0,0,0.5) !important;
    }
    .branch-item { background-color: #27272a !important; }
    .card-d { background-color: #2e1010 !important; border-color: #ef4444 !important;}
    .formula { background: rgba(255,255,255,0.05) !important; color: #facc15 !important; }
    
    /* TABLE STYLES */
    td, .text-content, p { border-color: var(--border) !important;}
    th { background: #18181b !important; border-color: var(--border) !important; color: #ffffff !important;}
    table { border-collapse: collapse; }
    
    /* INSIGHT METRICS & DEFAULTS */
    .insight-cell, .insight-cell p, .insight-cell div, .insight-cell span { 
        color: #e9d5ff !important; 
        background-color: rgba(155, 81, 224, 0.05) !important;
    }
    .insight-tag { color: #ffffff !important; }
    .note, .meta-info, .desc, .text-muted, .text-light, .text-dim, .definition, [class*="text-gray-"], [class*="text-secondary"] { 
        color: #a1a1aa !important; 
    }
    a { color: #60a5fa !important; }

    .main-container {
      max-width: 1400px;
      margin: 0 auto;
      padding: 40px 24px;
    }
  </style>
"""

DARK_NAV = """
<!-- 全局统一导航栏(DARK) -->
<div class="bg-glow"></div>
<nav class="site-nav">
  <div class="site-nav-inner">
    <a href="index.html" class="nav-logo">XIBO <span>NEXUS</span></a>
    <a href="index.html" class="nav-link">SP 2026-2028</a>
    <a href="user-segmentation-infographic.html" class="nav-link">ABCD客群边界</a>
    <a href="new_business_process_infographic.html" class="nav-link">S2B2C链条</a>
    <a href="ue_model_comparison.html" class="nav-link">财务UE底线</a>
  </div>
</nav>
"""

for filepath in glob.glob(os.path.join(SITE_DIR, "*.html")):
    if filepath.endswith("index.html"): continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Strip the old nav and glow if it exists
    content = re.sub(r'<nav class="site-nav">.*?</nav>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div class="bg-glow"></div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<!-- 全局统一导航栏 -->.*?(?:<nav.*?>.*?</nav>)?', '', content, flags=re.DOTALL)
    content = re.sub(r'<!-- 全局统一导航栏\(DARK\) -->', '', content, flags=re.DOTALL)

    # 2. Strip old css
    content = re.sub(r'<!-- 引入统一样式基础 -->.*?</style>', '', content, flags=re.DOTALL)
    content = re.sub(r'<!-- 引入统一样式基础\(DARK MODE OVERRIDE\) -->.*?</style>', '', content, flags=re.DOTALL)

    # 3. Inject new css just before closing HEAD
    content = re.sub(r'</head>', DARK_CSS + '\n</head>', content, flags=re.IGNORECASE)
    
    # 4. Inject new nav just after opening BODY
    content = content.replace("<body>", "<body>\n" + DARK_NAV)
    
    # Edge case: If <body> was uppercase or had attributes
    if "<body>" not in content.lower():
        content = re.sub(r'<body[^>]*>', lambda m: m.group(0) + '\n' + DARK_NAV, content, flags=re.IGNORECASE|re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Applied dark CEO dashboard theme to all sub-pages.")
