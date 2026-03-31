(function () {
    var currentPath = decodeURIComponent(window.location.pathname.split('/').pop() || 'index.html');
    if (currentPath === '' || currentPath === '/') currentPath = 'index.html';

    function isActive(href) {
        return href === currentPath ? ' active' : '';
    }

    // 注入全局导航样式（!important 防止子页面本地 CSS 覆盖）
    var styleHtml = `
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;900&display=swap" rel="stylesheet">
    <style id="navbar-global-style">
      /* 预占位防止 nav 注入时的布局跳动 */
      body { padding-top: 60px !important; }
      .bg-glow {
        position: fixed; top: -20vh; left: 50%; transform: translateX(-50%);
        width: 100vw; height: 60vh;
        background: radial-gradient(ellipse at bottom, rgba(239,68,68,0.06) 0%, rgba(9,9,11,0) 70%);
        z-index: -1; pointer-events: none;
      }
      .site-nav {
        position: fixed !important; top: 0 !important; left: 0 !important; right: 0 !important;
        z-index: 9999 !important;
        background: rgba(9,9,11,0.92) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border-bottom: 1px solid rgba(255,255,255,0.07) !important;
        padding: 0 clamp(16px,4vw,32px) !important;
        font-family: 'Inter', -apple-system, 'PingFang SC', sans-serif !important;
        box-sizing: border-box !important;
      }
      .site-nav-inner {
        max-width: 1400px !important; margin: 0 auto !important;
        display: flex !important; align-items: center !important;
        height: 60px !important; gap: 6px !important;
        overflow-x: auto !important; scrollbar-width: none !important;
      }
      .site-nav-inner::-webkit-scrollbar { display: none !important; }
      .nav-logo {
        font-family: 'Inter', -apple-system, 'PingFang SC', sans-serif !important;
        font-size: 16px !important; font-weight: 900 !important;
        color: #f4f4f5 !important; white-space: nowrap !important;
        text-decoration: none !important; margin-right: 16px !important;
        display: flex !important; align-items: center !important; gap: 6px !important;
        flex-shrink: 0 !important; letter-spacing: -0.5px !important;
      }
      .nav-logo span { color: #f97316 !important; }
      .nav-link {
        font-family: 'Inter', -apple-system, 'PingFang SC', sans-serif !important;
        display: flex !important; align-items: center !important;
        padding: 6px 13px !important; border-radius: 100px !important;
        font-size: 13px !important; font-weight: 500 !important;
        color: #a1a1aa !important; text-decoration: none !important;
        white-space: nowrap !important; transition: background 0.2s, color 0.2s !important;
        background: transparent !important;
      }
      .nav-link:hover {
        color: #f4f4f5 !important;
        background: rgba(255,255,255,0.08) !important;
      }
      /* 当前页高亮：红色底色 + 白色加粗文字 */
      .nav-link.active {
        background: #ef4444 !important;
        color: #ffffff !important;
        font-weight: 700 !important;
      }
      .nav-link.active:hover {
        background: #dc2626 !important;
        color: #ffffff !important;
      }
    </style>`;

    var navHtml = styleHtml + `
    <!-- 全局统一导航栏(DARK) -->
    <div class="bg-glow"></div>
    <nav class="site-nav">
      <div class="site-nav-inner">
        <a href="index.html" class="nav-logo">XIBO <span>CEO</span></a>
        <a href="index.html" class="nav-link` + isActive('index.html') + `">SP 2026-2028</a>
        <a href="user-segmentation-infographic.html" class="nav-link` + isActive('user-segmentation-infographic.html') + `">ABCD客群边界</a>
        <a href="ABCD_流程图.html" class="nav-link` + isActive('ABCD_流程图.html') + `">ABCD转化流程图</a>
        <a href="new_business_process_infographic.html" class="nav-link` + isActive('new_business_process_infographic.html') + `">S2B2C链条</a>
        <a href="financial_ue_dashboard.html" class="nav-link` + isActive('financial_ue_dashboard.html') + `">财务UE预演</a>
        <a href="refund_analysis_dashboard.html" class="nav-link` + isActive('refund_analysis_dashboard.html') + `">退费熔断看板</a>
        <a href="dual_track_system.html" class="nav-link` + isActive('dual_track_system.html') + `">双轨制组织设计</a>
      </div>
    </nav>
    `;
    document.write(navHtml);
})();

