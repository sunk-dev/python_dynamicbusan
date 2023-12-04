
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import folium
import openpyxl
from pyxlsb import open_workbook as open_xlsb
# 권한주기
from io import BytesIO

# csv 파일, 지도 업로드 부분
data = pd.read_csv('./BusanHotelFirst.csv')
st.write(data)
filter_data=data
# 사이드바, 검색조건 설정하기
# 일단 조건별로 
if(len(filter_data)==0):
    filter_data=data

def filteringMap():
    st.write(st.checkbox.__name__)

st.sidebar.title("검색 조건 사이드바")
ticker = st.sidebar.text_input("Enter a ticker (e. g. AAPL)", value = "AAPL")
st.sidebar.markdown('Tickers Link : [All Stock Symbols](https://stockanalysis.com/stocks/)')
start_date = st.sidebar.date_input("시작 날짜: ", value = pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("종료 날짜: ", value = pd.to_datetime("2023-07-28"))


options = st.sidebar.multiselect(
    '검색조건',
    ['휠체어 이동 가능', '점자도로이용가능', '물품보관함 이용가능', '수유실 이용 가능'])
st.write(options)


# 검색조건별로 컬럼 엮는 딕셔너리

options_value={
    '휠체어 이동 가능':'휠체어이동가능여부',
    '점자도로이용가능':'점자유도로유무',
    '물품보관함 이용가능':'물품보관함유무',
    '수유실 이용 가능':'수유실유무'

}


state_options=data['시군구명'].unique()
town_options=data['읍면동명'].unique()
state_name_options=st.sidebar.selectbox(
    '시군구명',
    state_options

)





def save_data():
    st.write('여기로옴..')

    file_name=state_name_options+'_'
    for i in town_name_options:
        file_name+=i
    st.write(file_name)
    filter_data.to_excel(
        excel_writer='C:\\'
         f'{file_name}.xlsx')


# 시군구별 읍면동명 데이터
town_groupby_state_data=data.groupby('시군구명')['읍면동명'].unique()

st.write(town_groupby_state_data)

if(state_name_options is not None):
     town_options=town_groupby_state_data[state_name_options]
     town_name_options=st.sidebar.multiselect(
     '읍면동명',
     town_options
     )


show_data_count_bar=st.sidebar.slider('추출개수',min_value=1)




# 검색조건이 있으면 그에 대응하는 칼럼으로 조건식 졸려서 map에 적용
# data->원본  filter_data -> data에 조건식 들어간거 filter data를 집어 넣기

st.write(filter_data)
if (options is not None):

    for i in options:
        col=options_value[i]
        filter_data=filter_data[filter_data[col]=='Y']

# 시군구별 지도 필터링

if(state_name_options is not None):
    filter_data=filter_data[filter_data['시군구명']==state_name_options]


# 읍면동별 지도 필터링
if (len(town_name_options)!=0):
    filter_data=filter_data[filter_data['읍면동명'].isin(town_name_options)]

#df[df['country'].isin(country_list)]


# 다운 받는 방법찯음
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)
    writer.close()
    processed_data = output.getvalue()
    return processed_data
df_xlsx = to_excel(filter_data)
st.sidebar.download_button(label='📥 Download Current Result',
                                data=df_xlsx ,
                                file_name= 'df_test.xlsx')

map=folium.Map(location=[filter_data['위도'].mean(),filter_data['경도'].mean()], zoom_start=10)
for n in filter_data.index:
    name=filter_data.loc[n,'업체명'] # n번 행의 상호명
    address=filter_data.loc[n,'도로명'] # n번 행의 도로명주소
    popup=f"{name}-{address}" # 상호명과 도로명주소 이어붙이기
    location=[filter_data.loc[n,'위도'],filter_data.loc[n,'경도']] # n번 행의 위도, 경도
    folium.Marker(
        location=location, # 위도 경도 위치에
        popup=popup, # 상호명과 도로명 주소 popup 띄우기
        icon=folium.Icon(color='red', icon='plus', prefix='fa')
    ).add_to(map) # 마커를 지도에 추가하기
st.components.v1.html(map._repr_html_(), width=800, height=600)




# 필터링 끝난뒤에 현재 위경도 거리에서 거리순으로 나열하는거 필터링

data_count=len(filter_data)

if show_data_count_bar>data_count:
    show_data_count_bar=data_count
st.write(filter_data.head(show_data_count_bar))


# last_execl_save_data

