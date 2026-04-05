(function () {
    var currentPath = decodeURIComponent(window.location.pathname.split('/').pop() || 'index.html');
    if (currentPath === '' || currentPath === '/') currentPath = 'index.html';

    function isActive(href) {
        return href === currentPath ? ' active' : '';
    }

    function isGroupActive(hrefs) {
        return hrefs.includes(currentPath) ? ' active' : '';
    }

    // 1. 注入 CSS 核心样式
    var style = document.createElement('style');
    style.innerHTML = `
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;900&display=swap');
      
      body { padding-top: 60px !important; margin: 0; }
      
      /* 使用唯一前缀避免与页面原有 CSS 冲突 */
      .xibo-nav-container {
        position: fixed; top: 0; left: 0; right: 0;
        z-index: 99999 !important;
        background: rgba(9, 9, 11, 0.85);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        font-family: 'Inter', -apple-system, sans-serif;
        overflow: visible !important;
      }
      .xibo-nav-header { display: none; }
      .xibo-nav-inner {
        max-width: 1240px; margin: 0 auto;
        display: flex; align-items: center;
        min-height: 60px; padding: 0 20px; gap: 4px;
        overflow: visible !important;
      }
      .xibo-nav-logo {
        font-size: 16px; font-weight: 900; color: #fff;
        text-decoration: none; margin-right: 20px;
        letter-spacing: -0.5px; display: flex; align-items: center;
      }
      .xibo-nav-logo span { color: #f97316; }

      .xibo-nav-item { position: relative; height: 100%; display: flex; align-items: center; overflow: visible !important; }
      .xibo-nav-link, .xibo-nav-trigger {
        padding: 6px 14px; border-radius: 100px;
        font-size: 13px; font-weight: 500; color: #a1a1aa;
        text-decoration: none; transition: all 0.2s ease;
        cursor: pointer; border: none; background: transparent;
        display: flex; align-items: center; gap: 6px;
        white-space: nowrap;
      }
      .xibo-nav-link:hover, .xibo-nav-trigger:hover {
        color: #fff; background: rgba(255, 255, 255, 0.08);
      }
      .xibo-nav-item.active .xibo-nav-link, .xibo-nav-item.active .xibo-nav-trigger {
        background: #ef4444; color: #fff; font-weight: 600;
      }
      
      .xibo-nav-trigger::after {
        content: "▾"; font-size: 10px; opacity: 0.5; transition: transform 0.2s;
      }
      .xibo-nav-item:hover .xibo-nav-trigger::after { transform: rotate(180deg); opacity: 1; }
      .xibo-nav-item.mobile-dropdown-open .xibo-nav-trigger::after { transform: rotate(180deg); opacity: 1; }

      .xibo-dropdown-menu {
        position: absolute; top: 100%; left: 0;
        min-width: 200px; background: rgba(18, 18, 20, 0.98);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px; box-shadow: 0 20px 40px rgba(0,0,0,0.5);
        padding: 8px; margin-top: 4px;
        opacity: 0; visibility: hidden; transform: translateY(10px);
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        display: flex; flex-direction: column; gap: 2px;
        z-index: 100000;
      }
      
      @media (min-width: 1025px) {
        .xibo-nav-item:hover .xibo-dropdown-menu {
          opacity: 1; visibility: visible; transform: translateY(0);
        }
      }

      .xibo-dropdown-link {
        padding: 10px 12px; border-radius: 8px;
        font-size: 13px; color: #a1a1aa; text-decoration: none;
        transition: all 0.2s; display: flex; align-items: center;
        white-space: nowrap;
      }
      .xibo-dropdown-link:hover {
        background: rgba(255, 255, 255, 0.06); color: #fff; transform: translateX(4px);
      }
      .xibo-dropdown-link.active {
        background: rgba(239, 68, 68, 0.1); color: #ef4444; font-weight: 600;
      }
      
      .xibo-bg-glow-static {
        position: fixed; top: 0; left: 0; right: 0; height: 300px;
        background: radial-gradient(circle at 50% 0%, rgba(239,68,68,0.05) 0%, transparent 70%);
        pointer-events: none; z-index: -1;
      }

      /* 隐藏页面上可能存在的旧导航栏，避免重复 */
      .site-nav, .navbar, #site-nav { display: none !important; }

      /* Mobile styles */
      @media (max-width: 1024px) {
        .xibo-nav-header {
          display: flex; align-items: center; justify-content: space-between;
          height: 60px; padding: 0 20px;
        }
        .xibo-mobile-toggle {
          background: transparent; border: none; color: #fff;
          font-size: 24px; cursor: pointer; padding: 0; display: flex; align-items: center; justify-content: center; width: 40px; height: 40px;
        }
        .xibo-nav-inner {
          display: none;
          flex-direction: column; align-items: flex-start;
          height: auto; padding: 10px 20px 20px 20px; gap: 8px;
          background: rgba(18, 18, 20, 0.98);
          position: absolute; top: 60px; left: 0; right: 0;
          border-bottom: 1px solid rgba(255, 255, 255, 0.08);
          max-height: calc(100vh - 60px); overflow-y: auto !important;
        }
        .xibo-nav-inner.mobile-open {
          display: flex;
        }
        .xibo-nav-logo.desktop-only { display: none !important; }
        .xibo-nav-item { width: 100%; flex-direction: column; align-items: flex-start; height: auto; }
        .xibo-nav-link, .xibo-nav-trigger { width: 100%; box-sizing: border-box; padding: 12px 14px; font-size: 15px; }
        
        .xibo-dropdown-menu {
          position: static; opacity: 1; visibility: visible; transform: none;
          display: none;
          width: 100%; box-sizing: border-box; background: transparent; border: none; box-shadow: none;
          padding: 0 0 0 16px; margin: 0;
        }
        .xibo-nav-item.mobile-dropdown-open .xibo-dropdown-menu {
          display: flex;
        }
      }
    `;
    document.head.appendChild(style);

    // 2. 构建 HTML
    var navHtml = `
      <div class="xibo-bg-glow-static"></div>
      <div class="xibo-nav-container">
        <!-- 移动端 Header -->
        <div class="xibo-nav-header">
          <a href="index.html" class="xibo-nav-logo"><img src="logo.png" alt="Logo" style="height: 24px; margin-right: 8px;">XIBO <span>CEO</span></a>
          <button class="xibo-mobile-toggle">☰</button>
        </div>
        <nav class="xibo-nav-inner">
          <a href="index.html" class="xibo-nav-logo desktop-only"><img src="logo.png" alt="Logo" style="height: 24px; margin-right: 8px;">XIBO <span>CEO</span></a>
          
          <div class="xibo-nav-item ${isActive('index.html')}">
            <a href="index.html" class="xibo-nav-link">战略总纲图</a>
          </div>

          <div class="xibo-nav-item ${isGroupActive(['user-segmentation-infographic.html', 'ABCD_流程图.html', 'student_psychology_map.html', 'user_decoder_dashboard.html', 'sales_team_audit.html', 'case_studies_index.html'])}">
            <div class="xibo-nav-trigger">客群战略矩阵</div>
            <div class="xibo-dropdown-menu">
              <a href="user-segmentation-infographic.html" class="xibo-dropdown-link ${isActive('user-segmentation-infographic.html')}">ABCD 客群边界</a>
              <a href="ABCD_流程图.html" class="xibo-dropdown-link ${isActive('ABCD_流程图.html')}">ABCD 转化漏斗</a>
              <a href="student_psychology_map.html" class="xibo-dropdown-link ${isActive('student_psychology_map.html')}">学员心理地图</a>
              <a href="user_decoder_dashboard.html" class="xibo-dropdown-link ${isActive('user_decoder_dashboard.html')}">🧠 用户深度解码</a>
              <a href="sales_team_audit.html" class="xibo-dropdown-link ${isActive('sales_team_audit.html')}">🦸 销售团队评审</a>
              <a href="case_studies_index.html" class="xibo-dropdown-link ${isActive('case_studies_index.html')}">📋 用户案例库</a>
            </div>
          </div>

          <div class="xibo-nav-item ${isGroupActive(['financial_ue_dashboard.html', 'refund_analysis_dashboard.html'])}">
            <div class="xibo-nav-trigger">财务UE与熔断</div>
            <div class="xibo-dropdown-menu">
              <a href="financial_ue_dashboard.html" class="xibo-dropdown-link ${isActive('financial_ue_dashboard.html')}">全链路财务UE预演</a>
              <a href="refund_analysis_dashboard.html" class="xibo-dropdown-link ${isActive('refund_analysis_dashboard.html')}">动态退费黑洞监控</a>
            </div>
          </div>

          <div class="xibo-nav-item ${isGroupActive(['dual_track_system.html', 'new_business_process_infographic.html'])}">
            <div class="xibo-nav-trigger">组织架构图谱</div>
            <div class="xibo-dropdown-menu">
              <a href="dual_track_system.html" class="xibo-dropdown-link ${isActive('dual_track_system.html')}">双轨制组织矩阵</a>
              <a href="new_business_process_infographic.html" class="xibo-dropdown-link ${isActive('new_business_process_infographic.html')}">S2B2C 商业穿透链</a>
            </div>
          </div>

          <div class="xibo-nav-item ${isActive('ai_native_three_axes.html')}">
            <a href="ai_native_three_axes.html" class="xibo-nav-link">⚔️ AI三板斧</a>
          </div>

          <div class="xibo-nav-item ${isGroupActive(['incentive_plan_v1.html', 'class_manager_best_practices.html'])}">
            <div class="xibo-nav-trigger">🎯 激励与考核</div>
            <div class="xibo-dropdown-menu">
              <a href="incentive_plan_v1.html" class="xibo-dropdown-link ${isActive('incentive_plan_v1.html')}">📊 激励考核方案 V1.0</a>
              <a href="class_manager_best_practices.html" class="xibo-dropdown-link ${isActive('class_manager_best_practices.html')}">🏅 班主任最佳实践</a>
            </div>
          </div>
        </nav>
      </div>
    `;

    // 3. 安全注入 (代替 document.write)
    function injectNav() {
        if (document.getElementById('g-nav-wrapper')) return;
        
        // 自动移除页面中可能存在的硬编码旧导航栏
        var oldNavs = document.querySelectorAll('.site-nav, .navbar, #site-nav');
        oldNavs.forEach(nav => nav.style.display = 'none');

        var navWrapper = document.createElement('div');
        navWrapper.id = 'g-nav-wrapper';
        navWrapper.innerHTML = navHtml;
        if (document.body) {
            document.body.prepend(navWrapper);
        } else {
            window.addEventListener('DOMContentLoaded', function() {
                if (!document.getElementById('g-nav-wrapper')) {
                    document.body.prepend(navWrapper);
                }
            });
        }
    }

    // 立即尝试注入，如果失败则等待 DOM
    if (document.readyState === 'loading') {
        window.addEventListener('DOMContentLoaded', injectNav);
    } else {
        injectNav();
    }

    // 4. 增加移动端触碰支持与汉堡菜单逻辑
    window.addEventListener('load', function() {
        // Toggle mobile menu
        var mobileToggle = document.querySelector('.xibo-mobile-toggle');
        var navInner = document.querySelector('.xibo-nav-inner');
        if (mobileToggle && navInner) {
            mobileToggle.addEventListener('click', function(e) {
                navInner.classList.toggle('mobile-open');
                mobileToggle.innerHTML = navInner.classList.contains('mobile-open') ? '✕' : '☰';
                e.stopPropagation();
            });
        }

        // Toggle mobile dropdowns
        document.querySelectorAll('.xibo-nav-trigger').forEach(trigger => {
            trigger.addEventListener('click', function(e) {
                if (window.innerWidth <= 1024) {
                    var parentItem = this.closest('.xibo-nav-item');
                    var isOpen = parentItem.classList.contains('mobile-dropdown-open');
                    
                    // 关闭其他已打开的菜单
                    document.querySelectorAll('.xibo-nav-item').forEach(item => {
                        item.classList.remove('mobile-dropdown-open');
                    });
                    
                    if (!isOpen) {
                        parentItem.classList.add('mobile-dropdown-open');
                    }
                    e.stopPropagation();
                } else {
                    var menu = this.nextElementSibling;
                    var isVisible = window.getComputedStyle(menu).visibility === 'visible';
                    document.querySelectorAll('.xibo-dropdown-menu').forEach(m => {
                        m.style.visibility = 'hidden';
                        m.style.opacity = '0';
                    });
                    if (!isVisible) {
                        menu.style.visibility = 'visible';
                        menu.style.opacity = '1';
                        menu.style.transform = 'translateY(0)';
                    }
                    e.stopPropagation();
                }
            });
        });

        // Click outside to close mobile menu
        document.addEventListener('click', function(e) {
            if (window.innerWidth <= 1024) {
                if (!e.target.closest('.xibo-nav-container') && navInner && navInner.classList.contains('mobile-open')) {
                    navInner.classList.remove('mobile-open');
                    if (mobileToggle) mobileToggle.innerHTML = '☰';
                }
            } else {
                document.querySelectorAll('.xibo-dropdown-menu').forEach(m => {
                    m.style.visibility = '';
                    m.style.opacity = '';
                    m.style.transform = '';
                });
            }
        });
    });
})();
