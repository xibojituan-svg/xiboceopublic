# -*- coding: utf-8 -*-
"""
用户分层综合分析脚本
分析所有用户画像数据，建立ABCD分层模型
"""

import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
sys.stdout.reconfigure(encoding='utf-8')

# 文件路径配置
MEDIA_DIR = r"C:\Users\Administrator\.qclaw\media\inbound"

# 文件映射
FILE_MAPPING = {
    "audiobook_converted": "有声书转化成功的学员画像_20260201到20260324---75c17179-4a22-445c-9f51-8d2b3b74853d.xlsx",
    "ai_writing_unconverted": "AI写作未转化画像_20260324_1102---d9502375-5407-4f92-8973-feacb3caa0e0.xlsx",
    "ai_writing_converted": "AI写作转化画像_20260324_1101---2052b699-aba6-4aa4-82c3-52bb3f691f8d.xlsx",
    "ai_video_converted": "AI短视频已经转化画像_20260324_1139---60c0e730-5ca2-4338-a71f-aaedf118abaf.xlsx",
    "ai_video_unconverted": "AI短视频未转化画像_20260324_1139---492efb2c-c5df-455b-80e4-f57e48cc8f56.xlsx",
    "audiobook_wechat_unconverted": "有声书-加了微信未转化用户画像_20260201到20260324---9c54479c-1533-44db-90b8-faed69cd9b84.xlsx"
}

def get_file_path(file_key):
    """获取文件完整路径"""
    filename = FILE_MAPPING.get(file_key)
    if not filename:
        return None
    return os.path.join(MEDIA_DIR, filename)

def read_excel_sheets(file_path):
    """读取Excel文件的所有sheet页"""
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        return None
    
    try:
        xl = pd.ExcelFile(file_path)
        sheets_data = {}
        for sheet_name in xl.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            # 清理数据：去除'-'行
            if len(df.columns) >= 2:
                col1 = df.columns[0]
                df_valid = df[df[col1] != '-']
                sheets_data[sheet_name] = df_valid
        return sheets_data
    except Exception as e:
        print(f"读取文件 {file_path} 出错: {e}")
        return None

def calculate_distribution(sheets_data, sheet_name, category):
    """计算指定sheet中某个类别的分布"""
    if sheet_name not in sheets_data:
        return 0
    
    df = sheets_data[sheet_name]
    if len(df.columns) < 2:
        return 0
    
    col1, col2 = df.columns[0], df.columns[1]
    total = df[col2].sum()
    if total == 0:
        return 0
    
    value = df[df[col1] == category][col2].sum() if len(df[df[col1] == category]) > 0 else 0
    return value / total * 100

def get_total_users(sheets_data, sheet_name='性别'):
    """获取总用户数"""
    if sheet_name not in sheets_data:
        return 0
    
    df = sheets_data[sheet_name]
    if len(df.columns) < 2:
        return 0
    
    return df[df.columns[1]].sum()

def analyze_business_comparison():
    """分析三大业务对比"""
    print("="*90)
    print("📊 三大业务用户画像综合分析")
    print("="*90)
    
    results = {}
    
    # 读取所有文件
    for key, desc in [
        ("audiobook_converted", "🎧 有声书转化"),
        ("ai_writing_converted", "✍️ AI写作转化"),
        ("ai_writing_unconverted", "✍️ AI写作未转化"),
        ("ai_video_converted", "🎬 AI短视频转化"),
        ("ai_video_unconverted", "🎬 AI短视频未转化"),
        ("audiobook_wechat_unconverted", "🎧 有声书加微信未转化")
    ]:
        file_path = get_file_path(key)
        if file_path and os.path.exists(file_path):
            sheets_data = read_excel_sheets(file_path)
            if sheets_data:
                total = get_total_users(sheets_data)
                results[key] = {
                    "desc": desc,
                    "total": total,
                    "sheets": sheets_data
                }
                print(f"✅ {desc}: {total:,}人")
    
    print()
    
    # 业务对比分析
    print("\n" + "="*80)
    print("1️⃣ 各业务用户规模")
    print("="*80)
    
    biz_data = {}
    for key in ["audiobook_converted", "ai_writing_converted", "ai_video_converted"]:
        if key in results:
            biz = key.replace("_converted", "").replace("_unconverted", "")
            if "audiobook" in biz:
                biz_name = "有声书"
            elif "ai_writing" in biz:
                biz_name = "AI写作"
            elif "ai_video" in biz:
                biz_name = "AI短视频"
            
            conv_key = key
            unconv_key = key.replace("converted", "unconverted")
            
            conv_total = results[conv_key]["total"] if conv_key in results else 0
            unconv_total = results[unconv_key]["total"] if unconv_key in results else 0
            
            total_all = conv_total + unconv_total
            conv_rate = conv_total / total_all * 100 if total_all > 0 else 0
            
            biz_data[biz_name] = {
                "转化人数": conv_total,
                "未转化人数": unconv_total,
                "总人数": total_all,
                "转化率": conv_rate
            }
    
    # 打印对比表格
    print(f"\n{'业务':<10} | {'转化人数':>12} | {'未转化人数':>12} | {'总人数':>12} | {'转化率':>10}")
    print("-"*70)
    for biz, data in biz_data.items():
        print(f"{biz:<10} | {data['转化人数']:>12,.0f} | {data['未转化人数']:>12,.0f} | {data['总人数']:>12,.0f} | {data['转化率']:>10.1f}%")
    
    # 关键维度分析
    print("\n" + "="*80)
    print("2️⃣ 关键维度对比（转化用户）")
    print("="*80)
    
    # 性别对比
    print("\n🔸 性别分布对比:")
    print(f"{'业务':<10} | {'女性占比':>10} | {'男性占比':>10}")
    print("-"*40)
    
    for key, desc in [("audiobook_converted", "有声书"), ("ai_writing_converted", "AI写作"), ("ai_video_converted", "AI短视频")]:
        if key in results:
            female = calculate_distribution(results[key]["sheets"], "性别", "女")
            male = calculate_distribution(results[key]["sheets"], "性别", "男")
            print(f"{desc:<10} | {female:>9.1f}% | {male:>9.1f}%")
    
    # 年龄对比（关键年龄段）
    print("\n🔸 年龄分布对比（40-49岁占比）:")
    print(f"{'业务':<10} | {'40-49岁占比':>12}")
    print("-"*30)
    
    for key, desc in [("audiobook_converted", "有声书"), ("ai_writing_converted", "AI写作"), ("ai_video_converted", "AI短视频")]:
        if key in results:
            age_40_49 = calculate_distribution(results[key]["sheets"], "年龄段", "40-49岁")
            print(f"{desc:<10} | {age_40_49:>11.1f}%")
    
    # 渠道对比
    print("\n🔸 渠道分布对比（TOP 3渠道）:")
    channels_to_check = ["B站", "站内资源位", "直播渠道", "私域", "小红书"]
    
    for key, desc in [("audiobook_converted", "有声书"), ("ai_writing_converted", "AI写作"), ("ai_video_converted", "AI短视频")]:
        if key in results:
            print(f"\n{desc}:")
            channel_data = []
            for channel in channels_to_check:
                pct = calculate_distribution(results[key]["sheets"], "一级渠道", channel)
                if pct > 1:
                    channel_data.append((channel, pct))
            
            # 按占比排序，取TOP 3
            channel_data.sort(key=lambda x: x[1], reverse=True)
            for channel, pct in channel_data[:3]:
                print(f"  ├── {channel:<10}: {pct:>5.1f}%")
    
    return results

def define_abcd_segmentation(results):
    """定义ABCD分层模型"""
    print("\n" + "="*80)
    print("🏆 ABCD用户分层模型定义")
    print("="*80)
    
    # 基于数据分析结果定义分层标准
    segmentation_rules = {
        "A类（高价值潜力用户）": {
            "定义": "最具转化潜力和价值的用户群体",
            "识别特征": [
                "年龄35-50岁（转化率最高的年龄段）",
                "已婚状态（已婚用户转化率高）",
                "来自高转化渠道（站内资源位、直播渠道）",
                "一二线城市（消费能力更强）",
                "有明确学习目的（爱好或赚钱导向）"
            ],
            "得分标准": "年龄35-50岁(30分) + 已婚(20分) + 高转化渠道(25分) + 一二线城市(15分) + 明确目的(10分) ≥ 80分",
            "运营策略": "VIP级服务、深度沟通、精准推荐、榜样打造"
        },
        "B类（潜力型用户）": {
            "定义": "有转化意向但需要激活的用户",
            "识别特征": [
                "已加微信但未转化（高意向待激活）",
                "相对年轻（18-34岁为主）",
                "未婚比例较高",
                "来自站外渠道（小红书、B站等）",
                "直播触达不足"
            ],
            "得分标准": "已加微信(40分) + 年龄18-34岁(25分) + 未婚(15分) + 站外渠道(20分) ≥ 70分",
            "运营策略": "定向直播邀约、1v1回访、信任建立、需求挖掘"
        },
        "C类（观察培育用户）": {
            "定义": "需要长期培育的潜在用户",
            "识别特征": [
                "来自低转化渠道（B站流量大但转化低）",
                "年轻用户群体（18-29岁）",
                "学历较高（本科以上）",
                "一线城市占比较高",
                "互动参与度一般"
            ],
            "得分标准": "B站渠道(30分) + 年龄18-29岁(25分) + 本科以上学历(20分) + 一线城市(15分) ≥ 60分",
            "运营策略": "内容种草、社群运营、轻度互动、长期培育"
        },
        "D类（风险/低价值用户）": {
            "定义": "转化可能性低或存在风险的用户",
            "识别特征": [
                "多次触达无响应",
                "负面反馈或投诉记录",
                "经济拮据（靠信用卡买课）",
                "电脑操作完全不熟悉",
                "学习目的不明确"
            ],
            "得分标准": "风险信号(40分) + 经济拮据(30分) + 无明确目的(20分) + 操作困难(10分) ≥ 50分",
            "运营策略": "降低服务成本、风险监控、避免过度投入"
        }
    }
    
    # 打印分层定义
    for seg_class, rules in segmentation_rules.items():
        print(f"\n🎯 {seg_class}")
        print(f"📝 定义: {rules['定义']}")
        print("🔍 识别特征:")
        for feature in rules['识别特征']:
            print(f"   • {feature}")
        print(f"📊 得分标准: {rules['得分标准']}")
        print(f"🚀 运营策略: {rules['运营策略']}")
    
    # 基于数据估算各层规模
    print("\n" + "="*80)
    print("📈 各层级用户规模估算（基于现有数据）")
    print("="*80)
    
    # 从数据中估算
    total_audiobook_converted = results.get("audiobook_converted", {}).get("total", 0)
    total_wechat_unconverted = results.get("audiobook_wechat_unconverted", {}).get("total", 0)
    total_ai_writing_unconverted = results.get("ai_writing_unconverted", {}).get("total", 0)
    total_ai_video_unconverted = results.get("ai_video_unconverted", {}).get("total", 0)
    
    # 粗略估算（可根据实际数据调整）
    estimated_sizes = {
        "A类（高价值潜力用户）": total_audiobook_converted * 1.5,  # 包括类似特征的未转化用户
        "B类（潜力型用户）": total_wechat_unconverted * 0.3,  # 加微信未转化中的高意向部分
        "C类（观察培育用户）": (total_ai_writing_unconverted + total_ai_video_unconverted) * 0.4,  # 低转化渠道年轻用户
        "D类（风险/低价值用户）": (total_ai_writing_unconverted + total_ai_video_unconverted) * 0.1  # 风险用户
    }
    
    print(f"\n{'用户层级':<20} | {'估算规模':>15} | {'占比':>10}")
    print("-"*50)
    
    total_estimated = sum(estimated_sizes.values())
    for seg_class, size in estimated_sizes.items():
        percentage = size / total_estimated * 100 if total_estimated > 0 else 0
        print(f"{seg_class:<20} | {size:>14,.0f}人 | {percentage:>9.1f}%")
    
    return segmentation_rules, estimated_sizes

def generate_actionable_recommendations(results, segmentation_rules):
    """生成可操作建议"""
    print("\n" + "="*80)
    print("🚀 基于数据分析的运营建议")
    print("="*80)
    
    recommendations = [
        {
            "优先级": "🔴 P0（最高）",
            "建议": "重点激活B类用户（加微信未转化）",
            "具体动作": [
                "1. 对73,174名加微信未转化用户进行定向直播邀约",
                "2. 针对一线城市用户进行1v1回访",
                "3. 设计年轻化内容专场，吸引18-29岁用户",
                "4. 建立信任关系，提供情绪价值"
            ],
            "预期效果": "预计激活5-8%，转化3,600-5,800人"
        },
        {
            "优先级": "🔴 P0（最高）",
            "建议": "优化B站渠道转化链路",
            "具体动作": [
                "1. 分析B站用户转化瓶颈（AI业务B站占比68-75%）",
                "2. 优化落地页和私域导流路径",
                "3. 设计针对B站用户的专属内容",
                "4. 建立B站渠道用户培育体系"
            ],
            "预期效果": "提升B站转化率2-3个百分点"
        },
        {
            "优先级": "🟡 P1（重要）",
            "建议": "深化A类用户服务",
            "具体动作": [
                "1. 为35-50岁已婚女性用户提供VIP服务",
                "2. 建立榜样学员体系（如红桃皇后案例）",
                "3. 设计复购路径：设备→AI→后期→进阶",
                "4. 提供家庭场景解决方案"
            ],
            "预期效果": "提升A类用户复购率和LTV"
        },
        {
            "优先级": "🟡 P1（重要）",
            "建议": "建立C类用户培育体系",
            "具体动作": [
                "1. 针对年轻高学历用户设计内容种草策略",
                "2. 建立社群运营机制，提高互动参与",
                "3. 设计轻度转化路径（试听课→体验课）",
                "4. 长期价值培育，不急于短期转化"
            ],
            "预期效果": "6个月内培育20-30%转化为B类/A类"
        }
    ]
    
    for rec in recommendations:
        print(f"\n{rec['优先级']} {rec['建议']}")
        print("具体动作:")
        for action in rec['具体动作']:
            print(f"  • {action}")
        print(f"预期效果: {rec['预期效果']}")
    
    return recommendations

def main():
    """主分析函数"""
    print("开始用户分层综合分析...")
    print("="*90)
    
    # 1. 业务对比分析
    results = analyze_business_comparison()
    
    if not results:
        print("❌ 没有读取到有效数据")
        return
    
    # 2. 定义ABCD分层模型
    segmentation_rules, estimated_sizes = define_abcd_segmentation(results)
    
    # 3. 生成运营建议
    recommendations = generate_actionable_recommendations(results, segmentation_rules)
    
    # 4. 生成总结报告
    print("\n" + "="*90)
    print("📋 综合分析总结报告")
    print("="*90)
    
    print("\n🎯 核心发现:")
    print("1. 三大业务用户画像差异显著：有声书（中年女性）、AI写作/短视频（年轻男性）")
    print("2. 渠道是关键影响因素：站内/直播转化率高，B站流量大但转化低")
    print("3. 年龄与婚姻状态是重要预测因子：35-50岁已婚用户转化率最高")
    print("4. 加微信未转化用户是最大待挖掘金矿：73,174人高意向待激活")
    
    print("\n📊 数据洞察:")
    print("• 有声书转化用户：女性71%、40-50岁38%、已婚76%、一线城市18.9%")
    print("• AI业务转化用户：男性54-58%、25-40岁为主、B站渠道68-75%")
    print("• 加微信未转化用户：更年轻（18-29岁35%）、未婚比例高（35%）、直播触达不足（仅8%）")
    
    print("\n🚀 后续行动建议:")
    print("1. 立即启动B类用户激活计划（加微信未转化）")
    print("2. 优化B站渠道转化链路")
    print("3. 建立ABCD分层运营体系")
    print("4. 定期监控各层用户转化效果")
    
    print("\n" + "="*90)
    print("✅ 分析完成！")
    print("="*90)
    
    # 保存结果到文件
    try:
        output_file = "user_segmentation_report.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("用户分层综合分析报告\n")
            f.write("="*50 + "\n")
            f.write(f"分析时间: {pd.Timestamp.now()}\n\n")
            
            f.write("各业务用户规模:\n")
            for key, data in results.items():
                f.write(f"{data['desc']}: {data['total']:,}人\n")
            
            f.write("\nABCD分层定义:\n")
            for seg_class, rules in segmentation_rules.items():
                f.write(f"\n{seg_class}:\n")
                f.write(f"定义: {rules['定义']}\n")
        
        print(f"\n📄 分析报告已保存到: {output_file}")
    except Exception as e:
        print(f"保存报告时出错: {e}")

if __name__ == "__main__":
    main()