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
    .subtitle {{ font-size: 16px; color: #cbd5e1; font-weight: 500; line-height: 1.5; }}
    
    .category {{ margin-bottom: 40px; }}
    .cat-title {{ 
      font-size: 20px; color: var(--dark); 
      border-left: 4px solid var(--brand); 
      padding-left: 12px; margin-bottom: 8px; font-weight: 800; 
    }}
    .cat-desc {{
      font-size: 14px;
      color: var(--text-dim);
      margin-bottom: 20px;
      padding-left: 16px;
    }}
    .link-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px; }}
    .doc-link {{
      display: flex; flex-direction: column; padding: 20px;
      background: var(--bg); border: 1px solid var(--border);
      border-radius: 12px; color: var(--text);
      text-decoration: none; transition: all 0.2s;
    }}
    .doc-link:hover {{ 
      border-color: var(--brand); background: #ffffff;
      transform: translateY(-3px); box-shadow: 0 8px 20px rgba(249,115,22,0.1); 
    }}
    .doc-title {{ font-weight: 700; font-size: 16px; margin-bottom: 8px; color: var(--dark); display: flex; align-items: center; gap: 6px; }}
    .doc-desc {{ font-size: 13px; color: var(--text-dim); line-height: 1.5; flex-grow: 1; }}
    
    @media (max-width: 600px) {{
      .page-container {{ margin: 15px; padding: 20px; }}
      .header-banner {{ padding: 25px; }}
      h1 {{ font-size: 24px; }}
    }}
  </style>
</head>
<body>
  <script src="navbar.js"></script>

<!-- 全局统一导航栏 -->


<div class="page-container">
  <div class="header-banner">
    <h1>2026 业务重构与战略导航台</h1>
    <div class="subtitle">通过 ABCD 客群精准分层，消灭无效营销与服务内耗。<br/>核心主线：定义人群 → 定制服务策略 → 重构交付SOP → UE利润兜底。</div>
  </div>

  <div class="category">
    <div class="cat-title">第一层：战略原点与人群定义</div>
    <div class="cat-desc">弄清我们究竟该服务谁？不同阶层的底层痛点与消费意愿边界在哪里。</div>
    <div class="link-grid">
      <a href="user_segmentation_infographic.html" class="doc-link">
        <div class="doc-title">📊 ABCD人群分层全景图</div>
        <div class="doc-desc">核心战略定义！将全量用户按能力与心智切分为ABCD四类，作为所有业务的行动基准。</div>
      </a>
      <a href="student_psychology_map.html" class="doc-link">
        <div class="doc-title">🧠 学员心理诉求全息地图</div>
        <div class="doc-desc">深度挖掘不同人群“表层动机 vs 真实恐惧”，为前端获客与后端交付打下心智基础。</div>
      </a>
      <a href="segmentation_radarmap.html" class="doc-link">
        <div class="doc-title">🎯 用户分层维度雷达图</div>
        <div class="doc-desc">从基础能力、学习意愿、消费力等多维度透视各客群的边界。</div>
      </a>
    </div>
  </div>

  <div class="category">
    <div class="cat-title">第二层：基于分层的定向转化与服务策略</div>
    <div class="cat-desc">有了定义后，对优质人群（A/B/C）横向扩利，对高危人群（D类）果断阻断。</div>
    <div class="link-grid">
      <a href="user_conversion_insight_article.html" class="doc-link">
        <div class="doc-title">💡 全局用户转化洞察总纲</div>
        <div class="doc-desc">打通“高客单价+高毛利+高复购”的转化认知壁垒，构建产品全景。</div>
      </a>
      <a href="cross_business_conversion_strategy.html" class="doc-link">
        <div class="doc-title">🔄 跨业务线SKU组合与升频</div>
        <div class="doc-desc">面向高潜A/B类用户的多品类穿透打法，做大单客LTV。</div>
      </a>
      <a href="ai_short_video_conversion_insight.html" class="doc-link">
        <div class="doc-title">🎬 AI短视频转化洞察</div>
        <div class="doc-desc">垂直品类：针对工具能力型用户的变现路径与成单密码。</div>
      </a>
      <a href="ai_writing_conversion_insight.html" class="doc-link">
        <div class="doc-title">✍️ AI写作人群转化洞察</div>
        <div class="doc-desc">垂直品类：厘清网赚粉与能力成长粉的本质区别及话术侧重。</div>
      </a>
      <a href="d_user_optimization.html" class="doc-link">
        <div class="doc-title">🛑 D类用户熔断与防御机制</div>
        <div class="doc-desc">雷区红线！高投诉、多疑高危人群的拦截、劝退和止损策略。</div>
      </a>
    </div>
  </div>

  <div class="category">
    <div class="cat-title">第三层：流程再造与SOP支持体系</div>
    <div class="cat-desc">通过系统与制度的改写，让组织的执行动作不走样，杜绝过去的非标人效黑洞。</div>
    <div class="link-grid">
      <a href="new_business_process_infographic.html" class="doc-link">
        <div class="doc-title">🗺️ 新版业务全景协同流程图</div>
        <div class="doc-desc">基于人群分层重置的系统流转图：前端筛漏斗，中台打标签，后端定交付。</div>
      </a>
      <a href="live_sop_upgrade_plan.html" class="doc-link">
        <div class="doc-title">📺 体验营前端：直播SOP升级</div>
        <div class="doc-desc">扫除过度承诺，通过科学试听筛选验证心智，不再透支长期信任。</div>
      </a>
      <a href="live_stream_3day_sop.html" class="doc-link">
        <div class="doc-title">📅 体验营前端：3天合规转化SOP</div>
        <div class="doc-desc">精细到天与时刻的拉群、暖场与公开课成交标准打法。</div>
      </a>
      <a href="class_manager_analysis.html" class="doc-link">
        <div class="doc-title">🏫 重交付后端：班主任体系彻底重塑</div>
        <div class="doc-desc">杜绝1v1无底线毒性私聊，用分层群运营手段找回极度流失的人效。</div>
      </a>
      <a href="class_manager_kpi_analysis.html" class="doc-link">
        <div class="doc-title">📝 重交付后端：班主任行为与KPI矫正</div>
        <div class="doc-desc">重定指挥棒！设置退费暂扣期与服务红线，用机制根治违规逼单。</div>
      </a>
    </div>
  </div>

  <div class="category">
    <div class="cat-title">第四层：财务模型基石与竞争防线</div>
    <div class="cat-desc">商业本质是算账。必须建立 ROI 和退费的强监控，防范组织陷入虚假繁荣的同质化竞争陷阱。</div>
    <div class="link-grid">
      <a href="ue_model_comparison.html" class="doc-link">
        <div class="doc-title">💰 核心财务：新旧UE模型对照</div>
        <div class="doc-desc">算清前端获客与后端交付损耗，挤出水分，让真实净利润浮出水面。</div>
      </a>
      <a href="ue_funnel_simulator.html" class="doc-link">
        <div class="doc-title">📈 运营财务工具：UE漏斗模拟器</div>
        <div class="doc-desc">在线推盘！输入转化率、客单价推算从流量进线到留存结转的盈亏节点。</div>
      </a>
      <a href="channel_roi_cutoff_report.html" class="doc-link">
        <div class="doc-title">📉 流量风控：渠道ROI动态熔断</div>
        <div class="doc-desc">对各获客渠道设定死刑线，一旦跌破 ROI 阈值立刻止血的执行报告。</div>
      </a>
      <a href="competitor_shifang_lihua_analysis.html" class="doc-link">
        <div class="doc-title">⚔️ 竞争防线：“十方梨花”模式解剖</div>
        <div class="doc-desc">以此为鉴，拆解对手通过“重度销售+毒性陪伴”透支企业口碑的终局教训。</div>
      </a>
    </div>
  </div>

</div>
</body>
</html>"""

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
  <script src="navbar.js"></script>

    if '<!-- 全局统一导航栏 -->' not in content:
        content = re.sub(r'<body[^>
  <script src="navbar.js"></script>
]*>', lambda m: m.group(0) + '\n' + global_nav, content, flags=re.IGNORECASE|re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Site built successfully.")
