import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt


 
uploaded_file = st.file_uploader("CSV 파일을 선택하세요", type='csv')
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write(data)