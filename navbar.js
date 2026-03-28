(function () {
    var currentPath = window.location.pathname.split('/').pop() || 'index.html';
    if (currentPath === '' || currentPath === '/') currentPath = 'index.html';

    function isActive(href) {
        return href === currentPath ? ' active' : '';
    }

    var navHtml = `
    <!-- 全局统一导航栏(DARK) -->
    <div class="bg-glow"></div>
    <nav class="site-nav">
      <div class="site-nav-inner">
        <a href="index.html" class="nav-logo">XIBO <span>NEXUS</span></a>
        <a href="index.html" class="nav-link` + isActive('index.html') + `">SP 2026-2028</a>
        <a href="user-segmentation-infographic.html" class="nav-link` + isActive('user-segmentation-infographic.html') + `">ABCD客群边界</a>
        <a href="ABCD_流程图.html" class="nav-link` + isActive('ABCD_流程图.html') + `">ABCD转化流程图</a>
        <a href="new_business_process_infographic.html" class="nav-link` + isActive('new_business_process_infographic.html') + `">S2B2C链条</a>
        <a href="ue_model_comparison.html" class="nav-link` + isActive('ue_model_comparison.html') + `">财务UE底线</a>
        <a href="dual_track_system.html" class="nav-link` + isActive('dual_track_system.html') + `">双轨制组织设计</a>
      </div>
    </nav>
    `;
    document.write(navHtml);
})();
