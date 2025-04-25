import streamlit as st
import math

# --- 页面配置 (可选，但建议) ---
st.set_page_config(
    page_title="圆柱体体积计算器",
    page_icon="🧮",  # 可以用 emoji 做图标
    layout="centered",  # 页面布局: centered 或 wide
    initial_sidebar_state="auto",  # 侧边栏状态: auto, expanded, collapsed
)

# --- 应用标题 ---
st.title("圆柱体填充体积计算器 🧮")
st.write("输入圆柱体的参数，计算实际填充部分的体积。")

# --- 参数输入 ---
st.header("参数输入")

# 使用列布局让输入框并排显示，更紧凑
col1, col2, col3 = st.columns(3)

with col1:
    diameter = st.number_input(
        label="直径 (Diameter)",
        min_value=0.0,  # 最小值不能为负数或零
        value=3.5,  # 默认值
        step=0.1,  # 步长
        format="%.2f",  # 显示格式 (两位小数)
        help="请输入圆柱体的直径，必须大于0",
    )

with col2:
    total_height = st.number_input(
        label="总高度 (Total Height)",
        min_value=0.0,
        value=7.6,
        step=0.1,
        format="%.2f",
        help="请输入圆柱体的总高度，必须大于0",
    )

with col3:
    empty_height = st.number_input(
        label="空高 (Empty Height)",
        min_value=0.0,
        value=2.55,
        step=0.1,
        format="%.2f",
        help="请输入圆柱体顶部未填充部分的高度，不能为负数",
    )

# --- 计算逻辑与结果显示 ---
st.header("计算结果")

# 输入验证
is_valid = True
if diameter <= 0:
    st.error("错误：直径必须大于 0。")
    is_valid = False
if total_height <= 0:
    st.error("错误：总高度必须大于 0。")
    is_valid = False
# empty_height >= 0 通过 min_value 保证了

if is_valid and empty_height > total_height:
    st.error(f"错误：空高 ({empty_height:.2f}) 不能大于总高度 ({total_height:.2f})。")
    is_valid = False

# 只有在所有输入都有效时才进行计算和显示
if is_valid:
    # 计算
    radius = diameter / 2

    sin_angle = (
        math.sqrt(2 * empty_height * radius - empty_height**2) * 1.0 / (radius * 1.0)
    )

    angle = math.asin(sin_angle)  # 弧度制

    filled_volume = (
        math.pi * (radius**2)
        - (empty_height - radius) * radius * sin_angle
        - (radius**2) * (math.pi - angle)
    ) * total_height

    # 使用 st.metric 显示结果，更美观
    st.metric(
        label="实际填充体积 (Volume)", value=f"{filled_volume:.3f}"
    )  # 保留三位小数


else:
    st.warning("请输入有效的参数以进行计算。")


st.caption(f"π ≈ {math.pi:.5f}")
