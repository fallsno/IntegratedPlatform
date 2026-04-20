import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, medfilt
from scipy.ndimage import gaussian_filter1d
import io

# ---------- 平滑处理函数 ----------
def apply_smoothing(series, method, window, **kwargs):
    y = series.values
    if method == "滚动平均":
        return pd.Series(y).rolling(window=window, min_periods=1).mean().values
    elif method == "Savitzky-Golay":
        polyorder = kwargs.get('polyorder', 3)
        win = min(window, len(y)-1 if len(y)%2==0 else len(y))
        if win % 2 == 0:
            win -= 1
        if win <= polyorder:
            polyorder = win - 1
        return savgol_filter(y, window_length=win, polyorder=polyorder)
    elif method == "中值滤波":
        win = min(window, len(y)-1 if len(y)%2==0 else len(y))
        if win % 2 == 0:
            win -= 1
        return medfilt(y, kernel_size=win)
    elif method == "高斯滤波":
        sigma = window / 6.0
        return gaussian_filter1d(y, sigma=sigma)
    else:
        return y

# ---------- 界面 ----------
st.set_page_config(page_title="传感器数据分析工具", layout="wide")
st.title("📊 传感器数据分析工具（在线版）")

uploaded_file = st.file_uploader("上传 CSV 文件", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
    st.success(f"已加载 {len(df)} 行数据")

    columns = st.multiselect("选择要处理的列", df.columns.tolist())
    
    col1, col2 = st.columns(2)
    with col1:
        method = st.selectbox("平滑方法", ["滚动平均", "Savitzky-Golay", "中值滤波", "高斯滤波"])
    with col2:
        window = st.number_input("窗口大小", min_value=3, value=1000, step=10)
    
    downsample = st.checkbox("启用降采样")
    interval = st.number_input("降采样间隔", min_value=1, value=100, disabled=not downsample)
    
    if st.button("开始处理") and columns:
        df_processed = df.copy()
        progress_bar = st.progress(0)
        for i, col in enumerate(columns):
            series = pd.to_numeric(df_processed[col], errors='coerce').fillna(0)
            smoothed = apply_smoothing(series, method, window)
            df_processed[col] = smoothed
            progress_bar.progress((i+1)/len(columns))
        
        if downsample:
            df_processed = df_processed.iloc[::interval].reset_index(drop=True)
        
        st.success("处理完成！")
        
        fig, ax = plt.subplots(figsize=(10, 4))
        for col in columns:
            ax.plot(df_processed.index, df_processed[col], label=col, alpha=0.8)
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        
        csv = df_processed.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button(
            label="下载处理结果 CSV",
            data=csv,
            file_name="processed_data.csv",
            mime="text/csv"
        )