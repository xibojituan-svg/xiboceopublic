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

global_nav = '<script src="navbar.js"></script>'

# Update sub-pages
for filepath in glob.glob(os.path.join(SITE_DIR, "*.html")):
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # remove old nav variations
    content = re.sub(r'<nav[^>]*>.*?</nav>', '', content, flags=re.DOTALL)
    
    # insert generic css
    skip_inject = filepath.endswith(("index.html", "presentation_2026.html", "course_product_review.html", "product_portfolio_proposal.html", "apple_pricing_analysis.html"))
    if '<!-- 引入统一样式基础 -->' not in content and not skip_inject:
        content = re.sub(r'</head>', generic_css + '\n</head>', content, flags=re.IGNORECASE)

    # insert robots noindex tag globally
    if '<meta name="robots" content="noindex, nofollow" />' not in content:
        content = re.sub(r'</head>', '  <meta name="robots" content="noindex, nofollow" />\n</head>', content, flags=re.IGNORECASE)
    
    # insert global nav after <body>
    if '<script src="navbar.js"></script>' not in content and not skip_inject:
        content = re.sub(r'<body[^>]*>', lambda m: m.group(0) + '\n' + global_nav, content, flags=re.IGNORECASE|re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Site built successfully.")
