#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户分层分析可视化图表 - 简化版
不使用表情符号，避免编码问题
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
}

SEGMENTATION_COLORS = {
    'A类': '#3a86ff',  # 蓝色 - 高价值潜力
    'B类': '#8338ec',  # 紫色 - 潜力型  
    'C类': '#06d6a0',  # 绿色 - 观察培育
    'D类': '#ef476f'   # 红色 - 风险/低价值
}

def create_dashboard():
    """创建仪表板图表"""
    print("正在生成仪表板图表...")
    
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
    ax1.set_title('各业务用户规模', fontsize=14, fontweight='bold', pad=15)
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
    ax2.set_title('各业务转化率对比', fontsize=14, fontweight='bold', pad=15)
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
    
    ax3.set_title('性别分布对比', fontsize=14, fontweight='bold', pad=15)
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
    ax4.set_title('ABCD用户分层规模', fontsize=16, fontweight='bold', pad=20)
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
    output_file = 'user_segmentation_dashboard.png'
    plt.savefig(output_file, bbox_inches='tight', dpi=300, facecolor='white')
    plt.close(fig)  # 关闭图形避免显示
    
    print(f"仪表板图表已保存为: {output_file}")
    return output_file

def create_summary_chart():
    """创建总结图表"""
    print("正在生成总结图表...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    fig.suptitle('用户分层分析总结', fontsize=18, fontweight='bold', y=0.98)
    
    # 饼图1：ABCD分层比例
    labels = ['A类', 'B类', 'C类', 'D类']
    sizes = [3888, 21952, 17656, 4414]
    colors = [SEGMENTATION_COLORS['A类'], SEGMENTATION_COLORS['B类'], 
             SEGMENTATION_COLORS['C类'], SEGMENTATION_COLORS['D类']]
    
    wedges, texts, autotexts = axes[0].pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                           startangle=90, shadow=False, textprops={'fontsize': 11})
    
    # 美化饼图
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(10)
    
    axes[0].set_title('ABCD用户分层比例', fontsize=14, fontweight='bold', pad=20)
    
    # 饼图2：三大业务比例
    axes[1].pie([2592, 20181, 26840], labels=['有声书', 'AI写作', 'AI短视频'], 
               colors=[COLORS['primary'], COLORS['secondary'], COLORS['success']],
               autopct='%1.1f%%', startangle=90, shadow=False, textprops={'fontsize': 11})
    axes[1].set_title('三大业务用户分布', fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    output_file = 'user_segmentation_summary.png'
    plt.savefig(output_file, bbox_inches='tight', dpi=300, facecolor='white')
    plt.close(fig)
    
    print(f"总结图表已保存为: {output_file}")
    return output_file

def main():
    """主函数"""
    print("=" * 60)
    print("用户分层分析可视化图表生成器")
    print("=" * 60)
    
    try:
        # 生成图表
        dashboard_file = create_dashboard()
        summary_file = create_summary_chart()
        
        print("\n" + "=" * 60)
        print("所有图表已生成完成！")
        print("=" * 60)
        print("\n生成的文件：")
        print(f"1. {dashboard_file} - 主仪表板")
        print(f"2. {summary_file} - 总结图表")
        print(f"\n文件保存在目录：D:\\xibo2026public")
        
        # 尝试显示文件信息
        import os
        print(f"\n文件大小：")
        print(f"- {dashboard_file}: {os.path.getsize(dashboard_file):,} bytes")
        print(f"- {summary_file}: {os.path.getsize(summary_file):,} bytes")
        
    except Exception as e:
        print(f"\n生成图表时出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()