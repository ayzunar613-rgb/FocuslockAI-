import streamlit as st
import time
import pandas as pd
import os
import matplotlib.pyplot as plt

# ===== 页面设置 =====
st.set_page_config(
    page_title="FocusLock AI",
    page_icon="🔒",
    layout="wide"
)

st.title("🔒 FocusLock AI - Smart Focus System")
st.markdown("🧠 AI-powered study focus & productivity tracker")

# ===== 初始化分心记录 =====
if "distraction" not in st.session_state:
    st.session_state.distraction = 0

if "running" not in st.session_state:
    st.session_state.running = False

# ===== 输入学习时间 =====
minutes = st.number_input(
    "Study Time (minutes)",
    min_value=1,
    max_value=180,
    value=1
)

# ===== 专注评分 =====
st.subheader("⭐ Focus Rating")
score = st.slider("Rate your focus (1-10)", 1, 10, 7)

# ===== AI建议 =====
st.markdown("---")
st.subheader("🤖 AI Study Assistant")

if st.button("💡 Get AI Suggestion"):

    if score >= 8:
        st.success("Great focus! Keep studying 25–30 min sessions.")
    elif score >= 5:
        st.info("Try shorter sessions (15–20 min) and remove distractions.")
    else:
        st.warning("Take a break, relax, then restart focus mode.")

# ===== 分心记录 =====
st.markdown("---")
st.subheader("⚠️ Distraction Tracker")

if st.button("😵 I got distracted"):
    st.session_state.distraction += 1

st.metric("Distraction Count", st.session_state.distraction)

# ===== 开始专注 =====
if st.button("🚀 Start Focus Mode"):
    st.session_state.running = True

if st.session_state.running:

    timer = st.empty()
    total_seconds = minutes * 60

    for sec in range(total_seconds, 0, -1):

        mins = sec // 60
        secs = sec % 60

        timer.metric("Remaining Time", f"{mins:02}:{secs:02}")
        time.sleep(1)

    st.success("🎉 Session Complete!")

    # ===== 保存记录 =====
    if os.path.exists("study_log.csv"):
        df = pd.read_csv("study_log.csv")
    else:
        df = pd.DataFrame(columns=["minutes"])

    df.loc[len(df)] = [minutes]
    df.to_csv("study_log.csv", index=False)

    st.session_state.running = False

# ===== 数据分析 =====
if os.path.exists("study_log.csv"):

    df = pd.read_csv("study_log.csv")

    # 总时间
    total_time = df["minutes"].sum()
    st.metric("📈 Total Study Time", f"{total_time} min")

    # 学习次数
    session_count = len(df)
    st.metric("📊 Study Sessions", f"{session_count} times")

    # 平均时间
    avg_time = df["minutes"].mean()
    st.metric("📘 Average Session", f"{avg_time:.1f} min")

    # 图表
    st.subheader("📊 Study Progress")

    fig, ax = plt.subplots()

    ax.plot(range(1, len(df) + 1), df["minutes"])

    ax.set_xlabel("Session")
    ax.set_ylabel("Minutes")
    ax.set_title("Study Sessions")

    st.pyplot(fig)