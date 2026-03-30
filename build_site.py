import os
import glob
import re

SITE_DIR = "."

global_nav = '<script src="navbar.js?v=20260328"></script>'
icons_html = """  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">"""

print("Starting to update site files safely...")

for filepath in glob.glob(os.path.join(SITE_DIR, "*.html")):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False

    # 1. 确保 navbar.js 存在于 <body> 内
    # 首先移除旧格式的 navbar script (如果有不同版本的参数)
    # content = re.sub(r'<script src="navbar\.js[^>]*></script>', '', content)
    # 但由于可能有多种，仅仅在没有完整版的时候插入即可
    if "navbar.js" not in content:
        # 尝试在 <body> 后立即插入
        content = re.sub(r'(<body[^>]*>)', r'\1\n  ' + global_nav, content, flags=re.IGNORECASE|re.DOTALL)
        modified = True
    elif global_nav not in content:
        # 如果有旧的 navbar.js，替换为最新的
        content = re.sub(r'<script src=["\']navbar\.js[^>]*></script>', global_nav, content)
        modified = True

    # 2. 确保 icon 标签存在于 <head> 内
    if "favicon.ico" not in content:
        content = re.sub(r'(</head>)', icons_html + r'\n\1', content, flags=re.IGNORECASE)
        modified = True

    # 保存文件如果发生了改动
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")

print("Site built successfully. User styles and custom edits have been strictly preserved.")
