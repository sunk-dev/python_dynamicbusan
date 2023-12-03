
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import folium


# 사이드바, 검색조건 설정하기
# 일단 조건별로 

def filteringMap():
    st.write(st.checkbox.__name__)

st.sidebar.title("검색 조건 사이드바")
ticker = st.sidebar.text_input("Enter a ticker (e. g. AAPL)", value = "AAPL")
st.sidebar.markdown('Tickers Link : [All Stock Symbols](https://stockanalysis.com/stocks/)')
start_date = st.sidebar.date_input("시작 날짜: ", value = pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("종료 날짜: ", value = pd.to_datetime("2023-07-28"))

options = st.multiselect(
    '검색조건',
    ['Green', 'Yellow', 'Red', 'Blue'],
    ['Yellow', 'Red'])



is_wheelchiar_available=st.sidebar.checkbox('휠체어 이동 가능' ,on_change=filteringMap,key='휠체어이동가능여부')
is_brailleroad_available=st.sidebar.checkbox('점자도로이용가능' ,on_change=filteringMap)
is_storage_available=st.sidebar.checkbox('물품보관함 이용가능' ,on_change=filteringMap)
is_nursingroom_available=st.sidebar.checkbox('수유실 이용 가능' ,on_change=filteringMap)
is_infantstand_available=st.sidebar.checkbox('유아거치대 이용 가능' ,on_change=filteringMap)




# csv 파일, 지도 업로드 부분
 

data = pd.read_csv('./BusanHotelFirst.csv')
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
