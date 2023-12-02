import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import folium

 
uploaded_file = st.file_uploader("CSV 파일을 선택하세요", type='csv')
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write(data)

map=folium.Map(location=[data['위도'].mean(),data['경도'].mean()], zoom_start=10)
for n in data.index:
    name=data.loc[n,'업체명'] # n번 행의 상호명
    address=data.loc[n,'도로명'] # n번 행의 도로명주소
    popup=f"{name}-{address}" # 상호명과 도로명주소 이어붙이기
    location=[data.loc[n,'위도'],data.loc[n,'경도']] # n번 행의 위도, 경도
    folium.Marker(
        location=location, # 위도 경도 위치에
        popup=popup, # 상호명과 도로명 주소 popup 띄우기
        icon=folium.Icon(color='red', icon='plus', prefix='fa')
    ).add_to(map) # 마커를 지도에 추가하기
st.components.v1.html(map._repr_html_(), width=800, height=600)
