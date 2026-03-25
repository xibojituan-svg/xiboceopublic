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

    /* Override hardcoded specific containers */
    .report-container, .page-container, .dashboard-container, .process-container, .map-container {
       background-color: var(--bg-surface) !important;
       border: 1px solid var(--border) !important;
       box-shadow: 0 10px 40px rgba(0,0,0,0.5) !important;
       color: var(--text) !important;
       border-radius: 16px;
       margin-top: 40px;
       margin-bottom: 40px;
    }
    h1, h2, h3, h4, .title { color: #fff !important; }
    td, .text-content, p { color: var(--text-dim) !important; border-color: var(--border) !important;}
    th { background: #18181b !important; border-color: var(--border) !important; color: #fff !important;}
    table { border-collapse: collapse; }
    .insight-cell { color: #d8b4fe !important; background-color: rgba(155, 81, 224, 0.05) !important;}
    .note, .meta-info, .desc { color: var(--text-muted) !important; }

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
    <a href="user_segmentation_infographic.html" class="nav-link">ABCD客群边界</a>
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
