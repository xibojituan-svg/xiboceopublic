import re
import os

filepath = r"d:\xibo2026public\ABCD_流程图.html"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add missing vars and site-nav CSS
nav_css = """
  :root {
    --orange: #f97316;
    --green: #10b981;
  }
  
  /* BG FX */
  .bg-glow {
    position: fixed; top: -20vh; left: 50%; transform: translateX(-50%);
    width: 100vw; height: 60vh;
    background: radial-gradient(ellipse at bottom, rgba(16,185,129,0.08) 0%, rgba(9,9,11,0) 70%);
    z-index: -1; pointer-events: none;
  }

  /* NAV */
  .site-nav {
    position: sticky; top: 0; z-index: 9999;
    background: rgba(9,9,11,0.85); backdrop-filter: blur(16px);
    border-bottom: 1px solid rgba(255,255,255,0.05);
    padding: 0 clamp(16px,4vw,32px);
  }
  .site-nav-inner {
    max-width: 1400px; margin: 0 auto;
    display: flex; align-items: center; height: 60px; gap: 12px; overflow-x: auto; scrollbar-width: none;
  }
  .site-nav-inner::-webkit-scrollbar { display: none; }
  .nav-logo { font-size: 16px; font-weight: 900; color: var(--text); white-space: nowrap; text-decoration: none; margin-right: 20px; display: flex; align-items: center; gap: 8px; }
  .nav-logo span { color: var(--orange); }
  .nav-link {
    display: flex; align-items: center; gap: 6px; padding: 6px 14px; border-radius: 100px;
    font-size: 13px; font-weight: 600; color: var(--text-dim); text-decoration: none; white-space: nowrap; transition: all 0.3s;
  }
  .nav-link:hover { color: var(--text); background: rgba(255,255,255,0.08); }
  .nav-link.active { color: #fff; background: var(--green); }
"""

if ".site-nav {" not in content:
    content = content.replace("  /* ── NAV ── */", nav_css + "\n  /* ── NAV ── */")

# 2. Fix mermaid initialize script
content = content.replace("theme: 'base'", "theme: 'dark'")
content = content.replace("fontFamily: '\"PingFang SC\",\"Microsoft YaHei\",sans-serif',", """fontFamily: '"PingFang SC","Microsoft YaHei",sans-serif',
        primaryColor: '#18181b',
        primaryTextColor: '#f4f4f5',
        primaryBorderColor: '#3f3f46',
        lineColor: '#a1a1aa',
        secondaryColor: '#27272a',
        tertiaryColor: '#09090b',""")

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
print("Added site-nav CSS and fixed Mermaid theme.")
