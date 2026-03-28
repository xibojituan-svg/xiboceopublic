#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户分层分析可视化仪表板
生成数据可视化图片
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import cm
import matplotlib
from matplotlib.patches import Rectangle, FancyBboxPatch, Patch
from matplotlib.lines import Line2D
import matplotlib.gridspec as gridspec

# 设置中文字体和样式
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300

# 设置颜色主题
COLORS = {
    'primary': '#3a86ff',
    'secondary': '#8338ec',
    'success': '#06d6a0',
    'warning': '#ffd166',
    'danger': '#ef476f',
    'light': '#f8f9fa',
    'dark': '#212529'
}

SEGMENTATION_COLORS = {
    'A类': '#3a86ff',  # 蓝色
    'B类': '#8338ec',  # 紫色
    'C类': '#06d6a0',  # 绿色
    'D类': '#ef476f'   # 红色
}

def create_business_comparison_chart():
    """创建业务对比图表"""
    fig = plt.figure(figsize=(14, 8))
    
    # 创建网格布局
    gs = gridspec.GridSpec(2, 3, figure=fig, height_ratios=[1.2, 0.8], hspace=0.25, wspace=0.3)
    
    # 图表1：各业务用户规模
    ax1 = fig.add_subplot(gs[0, 0])
    businesses = ['有声书', 'AI写作', 'AI短视频', '加微信未转化']
    user_counts = [2592, 20181, 26840, 73174]
    colors = [COLORS['primary'], COLORS['secondary'], COLORS['success'], COLORS['warning']]
    
    bars = ax1.bar(businesses, user_counts, color=colors, edgecolor='white', linewidth=2)
    ax1.set_title('📊 各业务用户规模对比', fontsize=14, fontweight='bold', pad=15)
    ax1.set_ylabel('用户数量', fontsize=12)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # 添加数值标签
    for bar, count in zip(bars, user_counts):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1000,
                f'{count:,}', ha='center', va='bottom', fontweight='bold')
    
    # 图表2：转化率对比
    ax2 = fig.add_subplot(gs[0, 1])
    conversion_businesses = ['有声书', 'AI写作', 'AI短视频']
    conversion_rates = [100.0, 5.8, 6.3]
    conversion_colors = [COLORS['primary'], COLORS['secondary'], COLORS['success']]
    
    bars2 = ax2.bar(conversion_businesses, conversion_rates, color=conversion_colors, 
                   edgecolor='white', linewidth=2)
    ax2.set_title('📈 各业务转化率对比', fontsize=14, fontweight='bold', pad=15)
    ax2.set_ylabel('转化率 (%)', fontsize=12)
    ax2.set_ylim(0, 110)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    
    # 添加数值标签
    for bar, rate in zip(bars2, conversion_rates):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # 图表3：性别分布对比
    ax3 = fig.add_subplot(gs[0, 2])
    
    # 有声书性别分布
    audiobook_gender = [71.1, 28.9]
    # AI写作性别分布
    ai_writing_gender = [46.5, 53.5]
    # AI短视频性别分布
    ai_video_gender = [41.7, 58.3]
    
    x = np.arange(3)
    width = 0.25
    
    bars_female = ax3.bar(x - width, [audiobook_gender[0], ai_writing_gender[0], ai_video_gender[0]], 
                         width, label='女性', color='#ff6b8b', edgecolor='white', linewidth=1)
    bars_male = ax3.bar(x, [audiobook_gender[1], ai_writing_gender[1], ai_video_gender[1]], 
                       width, label='男性', color=COLORS['primary'], edgecolor='white', linewidth=1)
    
    ax3.set_title('👥 各业务性别分布对比', fontsize=14, fontweight='bold', pad=15)
    ax3.set_ylabel('占比 (%)', fontsize=12)
    ax3.set_xticks(x)
    ax3.set_xticklabels(['有声书', 'AI写作', 'AI短视频'])
    ax3.legend(loc='upper right')
    ax3.grid(axis='y', alpha=0.3, linestyle='--')
    
    # 图表4：ABCD用户分层规模
    ax4 = fig.add_subplot(gs[1, :])
    
    segmentation_labels = ['A类 (高价值潜力)', 'B类 (潜力型)', 'C类 (观察培育)', 'D类 (风险/低价值)']
    segmentation_sizes = [3888, 21952, 17656, 4414]
    segmentation_percentages = [8.1, 45.8, 36.9, 9.2]
    segmentation_colors = [SEGMENTATION_COLORS['A类'], SEGMENTATION_COLORS['B类'], 
                          SEGMENTATION_COLORS['C类'], SEGMENTATION_COLORS['D类']]
    
    # 创建水平条形图
    y_pos = np.arange(len(segmentation_labels))
    bars4 = ax4.barh(y_pos, segmentation_sizes, color=segmentation_colors, 
                    edgecolor='white', linewidth=2, height=0.6)
    
    ax4.set_title('🏆 ABCD用户分层模型 - 各层级用户规模', fontsize=14, fontweight='bold', pad=10)
    ax4.set_xlabel('用户数量', fontsize=12)
    ax4.set_yticks(y_pos)
    ax4.set_yticklabels(segmentation_labels, fontsize=11)
    ax4.invert_yaxis()  # 反转Y轴使A类在顶部
    ax4.grid(axis='x', alpha=0.3, linestyle='--')
    
    # 添加数值和百分比标签
    for i, (bar, size, pct) in enumerate(zip(bars4, segmentation_sizes, segmentation_percentages)):
        width = bar.get_width()
        ax4.text(width + 500, bar.get_y() + bar.get_height()/2,
                f'{size:,}人 ({pct}%)', ha='left', va='center', fontweight='bold')
    
    # 添加整体标题
    fig.suptitle('用户分层分析可视化仪表板', fontsize=18, fontweight='bold', y=0.98)
    
    # 调整布局
    plt.tight_layout()
    plt.savefig('business_comparison_chart.png', bbox_inches='tight', dpi=300)
    plt.show()
    
    return fig

def create_segmentation_radar_chart():
    """创建ABCD分层雷达图"""
    fig = plt.figure(figsize=(10, 8))
    
    # 定义雷达图参数
    categories = ['年龄优势', '经济能力', '转化意愿', '渠道质量', '学习目的']
    N = len(categories)
    
    # ABCD各类用户在各维度的得分（0-10分）
    A_scores = [9, 8, 7, 9, 8]  # A类用户
    B_scores = [6, 5, 8, 4, 7]  # B类用户
    C_scores = [5, 6, 4, 3, 5]  # C类用户
    D_scores = [3, 2, 2, 2, 3]  # D类用户
    
    # 计算角度
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]  # 闭合图形
    
    # 闭合分数数组
    A_scores = A_scores + A_scores[:1]
    B_scores = B_scores + B_scores[:1]
    C_scores = C_scores + C_scores[:1]
    D_scores = D_scores + D_scores[:1]
    angles = np.array(angles)
    
    ax = fig.add_subplot(111, polar=True)
    
    # 绘制ABCD四类用户的雷达图
    ax.plot(angles, A_scores, 'o-', linewidth=2, color=SEGMENTATION_COLORS['A类'], 
            label='A类: 高价值潜力用户', markersize=8)
    ax.fill(angles, A_scores, alpha=0.25, color=SEGMENTATION_COLORS['A类'])
    
    ax.plot(angles, B_scores, 'o-', linewidth=2, color=SEGMENTATION_COLORS['B类'], 
            label='B类: 潜力型用户', markersize=8)
    ax.fill(angles, B_scores, alpha=0.25, color=SEGMENTATION_COLORS['B类'])
    
    ax.plot(angles, C_scores, 'o-', linewidth=2, color=SEGMENTATION_COLORS['C类'], 
            label='C类: 观察培育用户', markersize=8)
    ax.fill(angles, C_scores, alpha=0.25, color=SEGMENTATION_COLORS['C类'])
    
    ax.plot(angles, D_scores, 'o-', linewidth=2, color=SEGMENTATION_COLORS['D类'], 
            label='D类: 风险/低价值用户', markersize=8)
    ax.fill(angles, D_scores, alpha=0.25, color=SEGMENTATION_COLORS['D类'])
    
    # 设置雷达图标签
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=11)
    ax.set_ylim(0, 10)
    
    # 设置网格线
    ax.yaxis.grid(True, alpha=0.3, linestyle='--')
    ax.xaxis.grid(True, alpha=0.3, linestyle='--')
    
    # 添加图例
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fontsize=10)
    
    # 添加标题
    ax.set_title('📊 ABCD用户分层能力雷达图', fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('segmentation_radar_chart.png', bbox_inches='tight', dpi=300)
    plt.show()
    
    return fig

def create_key_insights_infographic():
    """创建关键洞察信息图表"""
    fig = plt.figure(figsize=(12, 10))
    
    # 创建网格布局
    gs = gridspec.GridSpec(3, 2, figure=fig, height_ratios=[1, 1, 0.8], hspace=0.25, wspace=0.25)
    
    # 洞察1：三大业务画像差异
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.axis('off')
    
    # 创建文本框
    insight1_text = """🎯 三大业务画像差异显著

• 🎧 有声书转化用户:
  女性71% · 40-50岁38% · 已婚76%
  一线城市18.9% · 站内渠道38%

• ✍️ AI写作转化用户:
  男性54% · 25-40岁均匀分布
  B站渠道68% · 本科49%

• 🎬 AI短视频转化用户:
  男性58% · 25-29岁27%
  B站渠道75% · 本科45%"""
    
    ax1.text(0.1, 0.9, insight1_text, transform=ax1.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='#f0f8ff', 
                                              edgecolor=COLORS['primary'], alpha=0.8))
    
    # 洞察2：渠道是关键影响因素
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.axis('off')
    
    insight2_text = """📊 渠道是关键影响因素

✅ 高转化渠道:
• 站内资源位: 38.0% (有声书)
• 直播渠道: 17.2% (有声书)

⚠️ 流量大但转化低的渠道:
• B站: AI写作68% · AI短视频75%
• 转化率仅5-6%

🎯 加微信未转化用户:
• 73,174人高意向待激活
• 更年轻(18-29岁35%)
• 直播触达不足(仅8%)
• 未婚比例高(35%)"""
    
    ax2.text(0.1, 0.9, insight2_text, transform=ax2.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='#fff0f5', 
                                              edgecolor=COLORS['danger'], alpha=0.8))
    
    # 洞察3：年龄与婚姻状态是重要预测因子
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.axis('off')
    
    insight3_text = """👥 年龄与婚姻状态是重要预测因子

• 35-50岁已婚用户转化率最高
• 30岁+用户占比:
  ✅ 转化成功: 71.6%
  ⚠️ 加微信未转化: 58.4%
  
• 已婚用户转化优势:
  ✅ 转化成功: 76.0%已婚
  ⚠️ 加微信未转化: 64.9%已婚

• 一线城市用户价值更高:
  ✅ 转化成功: 18.9%一线城市
  ⚠️ 加微信未转化: 11.7%一线城市"""
    
    ax3.text(0.1, 0.9, insight3_text, transform=ax3.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='#f0fff0', 
                                              edgecolor=COLORS['success'], alpha=0.8))
    
    # 洞察4：立即行动建议
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.axis('off')
    
    insight4_text = """🚀 立即行动建议 (优先级排序)

🔴 P0 (最高优先级):
1. 重点激活B类用户
   • 对73,174名加微信未转化用户定向直播邀约
   • 预计激活5-8%，转化3,600-5,800人

2. 优化B站渠道转化链路
   • AI业务B站占比68-75%，转化率仅5-6%
   • 目标: 提升2-3个百分点

🟡 P1 (重要):
1. 深化A类用户服务
   • VIP级服务，榜样学员体系
   • 复购路径: 设备→AI→后期→进阶

2. 建立C类用户培育体系
   • 年轻高学历用户内容种草
   • 6个月内培育20-30%转化为B类/A类"""
    
    ax4.text(0.1, 0.9, insight4_text, transform=ax4.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='#fffacd', 
                                              edgecolor=COLORS['warning'], alpha=0.8))
    
    # 图表5：转化漏斗
    ax5 = fig.add_subplot(gs[2, 0])
    
    funnel_stages = ['总流量', '加微信', '转化成功']
    funnel_values = [100000, 73174, 2592]  # 示意数据
    funnel_colors = [COLORS['primary'], COLORS['secondary'], COLORS['success']]
    
    # 创建漏斗图（简化版）
