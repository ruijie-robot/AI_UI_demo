import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.dates as mdates

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 生成时间序列数据（最近3年，按月）
def generate_time_series(start_date='2021-01-01', periods=36):
    dates = pd.date_range(start=start_date, periods=periods, freq='M')
    return dates

# 生成模拟数据
def generate_mock_data(dates, base_value, volatility):
    np.random.seed(42)
    trend = np.linspace(0, 2, len(dates))
    noise = np.random.randn(len(dates)) * volatility
    values = base_value + trend + noise
    return values

# 生成周期性数据
def generate_cyclical_data(dates, base_value, amplitude, cycle_years, noise_level, phase_shift=0):
    """
    生成周期性曲线
    dates: 时间序列
    base_value: 基准值
    amplitude: 振幅
    cycle_years: 周期长度（年）
    noise_level: 噪音水平
    phase_shift: 相位偏移
    """
    # 将日期转换为数值（年份）
    start_date = dates[0]
    days_since_start = (dates - start_date).days.values
    years = days_since_start / 365.25

    # 生成周期性波动
    cycle_component = amplitude * np.sin(2 * np.pi * years / cycle_years + phase_shift)

    # 添加趋势
    trend = np.linspace(-1, 1, len(dates))

    # 添加噪音
    np.random.seed(42)
    noise = np.random.randn(len(dates)) * noise_level

    values = base_value + cycle_component + trend + noise
    return values

# 生成相关性高的数据
def generate_correlated_data(reference_data, correlation=0.85, base_shift=0, amplitude_ratio=1.0):
    """
    生成与参考数据相关性高的数据
    reference_data: 参考数据
    correlation: 相关系数 (0-1)
    base_shift: 基准值偏移
    amplitude_ratio: 振幅比例
    """
    np.random.seed(123)
    # 标准化参考数据
    ref_normalized = (reference_data - np.mean(reference_data)) / np.std(reference_data)

    # 生成独立噪音
    independent_noise = np.random.randn(len(reference_data))

    # 混合相关和独立成分
    correlated_component = correlation * ref_normalized
    independent_component = np.sqrt(1 - correlation**2) * independent_noise

    # 组合并调整
    combined = correlated_component + independent_component
    result = combined * np.std(reference_data) * amplitude_ratio + np.mean(reference_data) + base_shift

    return result

# 图1: 宏观角度看创新药
def plot_macro_innovation():
    # 时间从2000到2025，每月一个数据点
    dates = pd.date_range(start='2000-01-01', end='2025-12-31', freq='ME')

    # 生成4条周期性折线的数据
    # M2同比：不要太大噪音的一条有周期的曲线（7年周期，小噪音）
    m2_growth = generate_cyclical_data(dates, base_value=9.0, amplitude=3.0,
                                       cycle_years=7, noise_level=0.3, phase_shift=0)

    # 社融同比：一条有周期的曲线（6年周期）
    social_finance = generate_cyclical_data(dates, base_value=11.0, amplitude=4.0,
                                           cycle_years=6, noise_level=0.8, phase_shift=1.0)

    # 出口增速：一条有周期的曲线（5年周期）
    export_growth = generate_cyclical_data(dates, base_value=6.0, amplitude=5.0,
                                          cycle_years=5, noise_level=1.2, phase_shift=2.0)

    # 投资增速：一条有周期的曲线（8年周期）
    investment_growth = generate_cyclical_data(dates, base_value=7.5, amplitude=3.5,
                                              cycle_years=8, noise_level=0.9, phase_shift=3.0)

    plt.figure(figsize=(14, 7))
    plt.plot(dates, m2_growth, label='M2同比', linewidth=2, alpha=0.8)
    plt.plot(dates, social_finance, label='社融同比', linewidth=2, alpha=0.8)
    plt.plot(dates, export_growth, label='出口增速', linewidth=2, alpha=0.8)
    plt.plot(dates, investment_growth, label='投资增速', linewidth=2, alpha=0.8)

    plt.xlabel('时间', fontsize=12)
    plt.ylabel('增长率 (%)', fontsize=12)
    # 无标题
    plt.legend(loc='best', fontsize=11)
    plt.grid(True, alpha=0.3)

    # 格式化x轴日期 - 每2年显示
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator(2))
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig('宏观角度看创新药.jpg', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 已生成: 宏观角度看创新药.jpg")

# 图2: 六周期模型
def plot_six_cycle_model():
    # 时间从2000到2025，每月一个数据点
    dates = pd.date_range(start='2000-01-01', end='2025-12-31', freq='ME')

    # 生成3条折线的数据
    # 货币：一条平滑的有周期的曲线（9年周期，极小噪音）
    currency = generate_cyclical_data(dates, base_value=50, amplitude=15,
                                     cycle_years=9, noise_level=0.2, phase_shift=0)

    # 信用：不要太大噪音的一条有周期的曲线（7年周期，小噪音）
    credit = generate_cyclical_data(dates, base_value=55, amplitude=18,
                                   cycle_years=7, noise_level=0.4, phase_shift=1.5)

    # 增长：不要太大噪音的一条有周期的曲线（6年周期，小噪音）
    growth = generate_cyclical_data(dates, base_value=48, amplitude=16,
                                   cycle_years=6, noise_level=0.4, phase_shift=3.0)

    plt.figure(figsize=(14, 7))
    plt.plot(dates, currency, label='货币', linewidth=2, color='#1f77b4', alpha=0.8)
    plt.plot(dates, credit, label='信用', linewidth=2, color='#ff7f0e', alpha=0.8)
    plt.plot(dates, growth, label='增长', linewidth=2, color='#2ca02c', alpha=0.8)

    plt.xlabel('时间', fontsize=12)
    plt.ylabel('指数值', fontsize=12)
    # 无标题
    plt.legend(loc='best', fontsize=11)
    plt.grid(True, alpha=0.3)

    # 格式化x轴日期 - 每2年显示
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator(2))
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig('六周期模型.jpg', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 已生成: 六周期模型.jpg")

# 图3: 海外热钱周期
def plot_hot_money_cycle():
    # 时间从2000到2025，每月一个数据点
    dates = pd.date_range(start='2000-01-01', end='2025-12-31', freq='ME')

    # 生成FED流动性指标：不要太大噪音的一条有周期的曲线（10年周期，小噪音）
    fed_liquidity = generate_cyclical_data(dates, base_value=100, amplitude=25,
                                          cycle_years=10, noise_level=0.5, phase_shift=0)

    # 生成中国主权CDS利差：和FED流动性指标相关性高的曲线
    china_cds = generate_correlated_data(fed_liquidity, correlation=0.85,
                                        base_shift=-40, amplitude_ratio=0.6)

    fig, ax1 = plt.subplots(figsize=(14, 7))

    # 第一条折线（左y轴）
    color1 = '#1f77b4'
    ax1.set_xlabel('时间', fontsize=12)
    ax1.set_ylabel('FED流动性指标', fontsize=12, color=color1)
    line1 = ax1.plot(dates, fed_liquidity, label='FED流动性指标',
                     linewidth=2, color=color1, alpha=0.8)
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, alpha=0.3)

    # 第二条折线（右y轴）
    ax2 = ax1.twinx()
    color2 = '#ff7f0e'
    ax2.set_ylabel('中国主权CDS利差 (bps)', fontsize=12, color=color2)
    line2 = ax2.plot(dates, china_cds, label='中国主权CDS利差',
                     linewidth=2, color=color2, alpha=0.8)
    ax2.tick_params(axis='y', labelcolor=color2)

    # 合并图例
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='best', fontsize=11)

    # 无标题

    # 格式化x轴日期 - 每2年显示
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax1.xaxis.set_major_locator(mdates.YearLocator(2))
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig('海外热钱周期.jpg', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 已生成: 海外热钱周期.jpg")

# 主函数
if __name__ == '__main__':
    print("开始生成折线图...")
    print()

    # 生成3个图表
    plot_macro_innovation()
    plot_six_cycle_model()
    plot_hot_money_cycle()

    print()
    print("所有图表已成功生成！")
    print("- 宏观角度看创新药.jpg")
    print("- 六周期模型.jpg")
    print("- 海外热钱周期.jpg")
