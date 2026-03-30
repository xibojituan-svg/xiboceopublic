import glob
import re

generic_css_pattern = re.compile(r'  <!-- 引入统一样式基础 -->\n.*?  </style>\n', re.DOTALL)

for filepath in glob.glob('*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if this file has specialized DARK MODE OVERRIDE but also the generic injected styles
    if '<!-- 引入统一样式基础(DARK MODE OVERRIDE) -->' in content and '<!-- 引入统一样式基础 -->' in content:
        # We must remove the generic one
        new_content = generic_css_pattern.sub('', content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Cleaned {filepath}")
