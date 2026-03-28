#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成用户分层分析可视化图表
简洁版 - 生成核心图表
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

# 设置中文字体和样式
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300

# 设置颜色主题
COLORS = {
    'primary': '#3a86ff',    # 蓝色
    'secondary': '#8338ec',  # 紫色  
    'success': '#06d6a0',    # 绿色
    'warning': '#ffd166',    # 黄色
    'danger': '#ef476f',     # 红色
    'dark': '#212529'        # 深色
}

SEGMENTATION_COLORS = {
    'A类': '#3a86ff',  # 蓝色 - 高价值潜力
    'B类': '#8338ec',  # 紫色 - 潜力型  
    'C类': '#06d6a0',  # 绿色 - 观察培育
    'D类': '#ef476f'   # 红色 - 风险/低价值
}

def create_main_dashboard():
    """创建主仪表板图表"""
    fig = plt.figure(figsize=(16, 12))
    fig.suptitle('用户分层分析核心仪表板', fontsize=20, fontweight='bold', y=0.98)
    
    # 创建网格布局
    gs = gridspec.GridSpec(2, 3, figure=fig, height_ratios=[1.2, 1], hspace=0.3, wspace=0.35)
    
    # 1. 各业务用户规模柱状图
    ax1 = fig.add_subplot(gs[0, 0])
    businesses = ['有声书', 'AI写作', 'AI短视频', '加微信未转化']
    user_counts = [2592, 20181, 26840, 73174]
    colors = [COLORS['primary'], COLORS['secondary'], COLORS['success'], COLORS['warning']]
    
    bars = ax1.bar(businesses, user_counts, color=colors, edgecolor='white', linewidth=2, alpha=0.85)
    ax1.set_title('📊 各业务用户规模', fontsize=14, fontweight='bold', pad=15)
    ax1.set_ylabel('用户数量', fontsize=12)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # 添加数值标签
    for bar, count in zip(bars, user_counts):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1000,
                f'{count:,}', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # 2. 转化率对比图
    ax2 = fig.add_subplot(gs[0, 1])
    conversion_businesses = ['有声书', 'AI写作', 'AI短视频']
    conversion_rates = [100.0, 5.8, 6.3]
    conversion_colors = [COLORS['primary'], COLORS['secondary'], COLORS['success']]
    
    bars2 = ax2.bar(conversion_businesses, conversion_rates, color=conversion_colors, 
                   edgecolor='white', linewidth=2, alpha=0.85)
    ax2.set_title('📈 各业务转化率对比', fontsize=14, fontweight='bold', pad=15)
    ax2.set_ylabel('转化率 (%)', fontsize=12)
    ax2.set_ylim(0, 110)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    
    # 添加数值标签
    for bar, rate in zip(bars2, conversion_rates):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # 3. 性别分布对比图
    ax3 = fig.add_subplot(gs[0, 2])
    
    # 业务性别分布数据
    gender_data = {
        '有声书': {'女': 71.1, '男': 28.9},
        'AI写作': {'女': 46.5, '男': 53.5},
        'AI短视频': {'女': 41.7, '男': 58.3}
    }
    
    businesses_gender = list(gender_data.keys())
    female_percentages = [gender_data[b]['女'] for b in businesses_gender]
    male_percentages = [gender_data[b]['男'] for b in businesses_gender]
    
    x = np.arange(len(businesses_gender))
    width = 0.35
    
    bars_female = ax3.bar(x - width/2, female_percentages, width, 
                         label='女性', color='#ff6b8b', edgecolor='white', linewidth=1, alpha=0.85)
    bars_male = ax3.bar(x + width/2, male_percentages, width, 
                       label='男性', color=COLORS['primary'], edgecolor='white', linewidth=1, alpha=0.85)
    
    ax3.set_title('👥 性别分布对比', fontsize=14, fontweight='bold', pad=15)
    ax3.set_ylabel('占比 (%)', fontsize=12)
    ax3.set_xticks(x)
    ax3.set_xticklabels(businesses_gender, fontsize=11)
    ax3.legend(loc='upper right', fontsize=10)
    ax3.grid(axis='y', alpha=0.3, linestyle='--')
    
    # 4. ABCD用户分层柱状图（占据第二行全部宽度）
    ax4 = fig.add_subplot(gs[1, :])
    
    segmentation_labels = ['A类 (高价值潜力)', 'B类 (潜力型)', 'C类 (观察培育)', 'D类 (风险/低价值)']
    segmentation_sizes = [3888, 21952, 17656, 4414]
    segmentation_colors = [SEGMENTATION_COLORS['A类'], SEGMENTATION_COLORS['B类'], 
                          SEGMENTATION_COLORS['C类'], SEGMENTATION_COLORS['D类']]
    
    bars4 = ax4.bar(segmentation_labels, segmentation_sizes, color=segmentation_colors, 
                   edgecolor='white', linewidth=2, alpha=0.85)
    ax4.set_title('🏆 ABCD用户分层规模', fontsize=16, fontweight='bold', pad=20)
    ax4.set_ylabel('用户数量', fontsize=12)
    ax4.set_xlabel('用户分层类型', fontsize=12)
    ax4.tick_params(axis='x', rotation=15)
    ax4.grid(axis='y', alpha=0.3, linestyle='--')
    
    # 添加数值标签和百分比
    for i, (bar, size) in enumerate(zip(bars4, segmentation_sizes)):
        height = bar.get_height()
        percentage = (size / sum(segmentation_sizes)) * 100
        ax4.text(bar.get_x() + bar.get_width()/2., height + 200,
                f'{size:,}\n({percentage:.1f}%)', ha='center', va='bottom', 
                fontweight='bold', fontsize=10, linespacing=0.9)
    
    plt.tight_layout()
    plt.savefig('user_segmentation_dashboard.png', bbox_inches='tight', dpi=300, facecolor='white')
    plt.show()
    
    print("✅ 仪表板图表已保存为: user_segmentation_dashboard.png")
    return fig

def create_insight_infographic():
    """创建洞察信息图表"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    fig.suptitle('用户分层分析关键洞察', fontsize=18, fontweight='bold', y=0.98)
    
    # 洞察1：三大业务画像
    axes[0].axis('off')
    insight1 = """🎯 三大业务画像差异显著

• 有声书转化用户:
  女性71% · 40-50岁38%
  已婚76% · 一线城市18.9%
  站内渠道38%

• AI写作转化用户:
  男性54% · 25-40岁均匀
  B站68% · 本科49%

• AI短视频转化用户:
  男性58% · 25-29岁27%
  B站75% · 本科45%"""
    
    axes[0].text(0.05, 0.95, insight1, transform=axes[0].transAxes, fontsize=10.5,
                verticalalignment='top', linespacing=1.5,
                bbox=dict(boxstyle='round', facecolor='#f0f8ff', 
                         edgecolor=COLORS['primary'], linewidth=2, alpha=0.9))
    
    # 洞察2：渠道表现
    axes[1].axis('off')
    insight2 = """📊 渠道表现差异显著

✅ 高转化渠道:
• 站内资源位: 38.0%
• 直播渠道: 17.2%

⚠️ 高流量低转化:
• B站渠道: AI业务68-75%
• 转化率: 仅5-6%

🎯 待激活用户:
• 73,174人加微信未转化
• 更年轻: 18-29岁35%
• 直播触达不足: 仅8%
• 未婚比例: 35%"""
    
    axes[1].text(0.05, 0.95, insight2, transform=axes[1].transAxes, fontsize=10.5,
                verticalalignment='top', linespacing=1.5,
                bbox=dict(boxstyle='round', facecolor='#fff0f5', 
                         edgecolor=COLORS['danger'], linewidth=2, alpha=0.9))
    
    # 洞察3：年龄婚姻分析
    axes[2].axis('off')
    insight3 = """👥 年龄与婚姻状态

• 35-50岁已婚用户:
  转化率最高

• 30岁+用户占比:
  ✅ 转化成功: 71.6%
  ⚠️ 未转化: 58.4%

• 已婚用户转化优势:
  ✅ 转化成功: 76.0%
  ⚠️ 未转化: 64.9%

• 一线城市用户:
  ✅ 转化成功: 18.9%
  ⚠️ 未转化: 11.7%"""
    
    axes[2].text(0.05, 0.95, insight3, transform=axes[2].transAxes, fontsize=10.5,
                verticalalignment='top', linespacing=1.5,
                bbox=dict(boxstyle='round', facecolor='#f0fff0', 
                         edgecolor=COLORS['success'], linewidth=2, alpha=0.9))
    
    # 洞察4：行动建议
    axes[3].axis('off')
    insight4 = """🚀 行动建议

🔴 P0 (最高优先级):
1. 激活B类用户
   • 73,174人定向直播邀约
   • 目标: 转化3,600-5,800人

2. 优化B站渠道
   • 转化率提升2-3%

🟡 P1 (重要):
1. 深化A类服务
   • VIP服务，榜样体系
   • 复购路径优化

2. 培育C类用户
   • 年轻高学历用户
   • 6个月转化20-30%"""
    
    axes[3].text(0.05, 0.95, insight4, transform=axes[3].transAxes, fontsize=10.5,
                verticalalignment='top', linespacing=1.5,
                bbox=dict(boxstyle='round', facecolor='#fffacd', 
                         edgecolor=COLORS['warning'], linewidth=2, alpha=0.9))
    
    plt.tight_layout()
    plt.savefig('user_insights_infographic.png', bbox_inches='tight', dpi=300, facecolor='white')
    plt.show()
    
    print("✅ 洞察信息图表已保存为: user_insights_infographic.png")
    return fig

def create_segmentation_pie_chart():
    """创建分层饼图"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    # 饼图1：ABCD分层比例
    labels = ['A类', 'B类', 'C类', 'D类']
    sizes = [3888, 21952, 17656, 4414]
    colors = [SEGMENTATION_COLORS['A类'], SEGMENTATION_COLORS['B类'], 
             SEGMENTATION_COLORS['C类'], SEGMENTATION_COLORS['D类']]
    
    wedges, texts, autotexts = ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                       startangle=90, shadow=False, textprops={'fontsize': 11})
    
    # 美化饼图
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(10)
    
    ax1.set_title('🍰 ABCD用户分层比例', fontsize=14, fontweight='bold', pad=20)
    
    # 饼图2：三大业务比例
    ax2.pie([2592, 20181, 26840], labels=['有声书', 'AI写作', 'AI短视频'], 
           colors=[COLORS['primary'], COLORS['secondary'], COLORS['success']],
           autopct='%1.1f%%', startangle=90, shadow=False, textprops={'fontsize': 11})
    ax2.set_title('📊 三大业务用户分布', fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('user_segmentation_pie_charts.png', bbox_inches='tight', dpi=300, facecolor='white')
    plt.show()
    
    print("✅ 饼图已保存为: user_segmentation_pie_charts.png")
    return fig

def main():
    """主函数"""
    print("=" * 60)
    print("🎨 用户分层分析可视化图表生成器")
    print("=" * 60)
    
    try:
        # 生成所有图表
        print("\n1. 生成主仪表板图表...")
        create_main_dashboard()
        
        print("\n2. 生成洞察信息图表...")
        create_insight_infographic()
        
        print("\n3. 生成分层饼图...")
        create_segmentation_pie_chart()
        
        print("\n" + "=" * 60)
        print("✅ 所有图表已生成完成！")
        print("=" * 60)
        print("\n生成的文件：")
        print("1. user_segmentation_dashboard.png - 主仪表板")
        print("2. user_insights_infographic.png - 洞察信息图表")
        print("3. user_segmentation_pie_charts.png - 分层饼图")
        print("\n📁 文件保存在当前目录：D:\\xibo2026public")
        
    except Exception as e:
        print(f"\n❌ 生成图表时出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()