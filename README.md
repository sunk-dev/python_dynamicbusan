

# **Dynamic Busan 숙박업소 검색 웹 어플리케이션**

## **"편의에 맞게 검색하고, 지도에서 확인하자!"**

[웹 사이트](https://dataanlysic-seon.streamlit.app/)
![image](https://github.com/sunk-dev/dataanlysic/assets/103514806/6817dfff-7aa6-4b45-a60b-2b18cb680525)


- 이용 데이터 자료
  
[부산관광공사_부산지역 숙박분야 업체_20220101](https://www.data.go.kr/data/15096728/fileData.do)

### 간략 설명

- python과 streamlit(데이터 기반 웹 애플리케이션을 만드는 도구) 을 이용하여 편의 시설, 시도별 부산 숙박업소 조회 웹사이트 개발

---

**1. 소개**

- 부산 숙박업소 데이터를 활용한  검색 웹 어플리케이션 소개

---

**2. 어플리케이션 기능**

- **다양한 편의시설 선택 가능**
    - 휠체어 이동 가능, 점자도로 이용 가능 등
- **지도 상에서 검색 조건에 맞는 숙박업소 표시**
    - 선택한 조건에 따라 지도 상에 마커로 표시
- **시군구 및 읍면동별 검색 조건 지원**
    - 사이드바에서 시군구명 및 읍면동명 선택 가능
- **엑셀 다운로드 기능**
    - 현재 필터링된 결과를 엑셀 파일로 다운로드

---

**3. 코드 동작 과정**

- **데이터 로드 및 초기 설정**
    - Plotly, Pandas, Streamlit 등의 라이브러리 사용
- **검색 조건 설정**
    - 편의시설 및 지역 선택을 위한 사이드바 제공
- **데이터 필터링**
    - 선택한 조건에 따라 데이터를 필터링하여 지도 및 결과에 반영
- **지도 표시**
    - Folium 라이브러리를 사용하여 숙박업소 위치를 지도 상에 표시
- **결과 표시 및 다운로드**
    - 필터링된 결과를 화면에 표시하고, 다운로드 버튼으로 엑셀 파일

### 상세설명

### 1. 데이터 전처리

### **1. 환경 설정 및 데이터 불러오기**

```python
pythonCopy code
# 필요한 라이브러리 임포트
import pandas as pd
import koreanize_matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import set_matplotlib_formats

# Colab에서 사용하는 한글 폰트 설정
plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)
set_matplotlib_formats('retina')

# 데이터 불러오기
df = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/BusanHotel.csv", encoding='cp949')
df1 = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/koreaLibrary.csv", encoding='cp949')

```

### **2. 데이터 전처리**

```python
pythonCopy code
# 필요 없는 열 삭제
clean_data = df.drop(['필지고유번호', '법정동코드', '행정동코드', '도로명코드', '등록일자'], axis=1)

# '카테고리명'이 '문화관광/명소'인 행 제거
clean_data = clean_data[clean_data['카테고리명'] != '문화관광/명소']

# '폐업여부'가 'Y'인 행 제거
clean_data = clean_data[clean_data['폐업여부'] != 'Y']

# 결측값 처리
clean_data['주차가능여부'] = clean_data['주차가능여부'].fillna('N')
clean_data['화장실유무'] = clean_data['화장실유무'].fillna('N')
# ... (이하 생략)

```

### **3. Folium을 사용한 지도 시각화**

```python
pythonCopy code
import folium

# 데이터의 위도, 경도 평균값을 중심으로 지도 생성
map = folium.Map(location=[clean_data['위도'].mean(), clean_data['경도'].mean()], zoom_start=7)

# 지도에 마커 추가
for n in clean_data.index:
    name = clean_data.loc[n, '업체명']
    address = clean_data.loc[n, '도로명']
    popup = f"{name}-{address}"
    location = [clean_data.loc[n, '위도'], clean_data.loc[n, '경도']]
    folium.Marker(
        location=location,
        popup=popup,
        icon=folium.Icon(color='red', icon='plus', prefix='fa')
    ).add_to(map)

# 지도 출력
map

```

### **4. 데이터 분석 및 시각화**

```python
pythonCopy code
# 시군구명 별 읍면동 명 분류 및 출력
table = pd.pivot_table(clean_data, index=['시군구명'], values=['읍면동명'], aggfunc='count')
print(table)

```

### **5. Excel 파일로 데이터 저장**

```python
pythonCopy code
# 엑셀에 저장될 데이터 가공
adress_roadname = clean_data['도로명'] + clean_data['도로명상세']
adress = clean_data['시도명'] + clean_data['시군구명'] + clean_data['읍면동명'] + clean_data['번지']

clean_data['일반주소'] = adress
clean_data['도로명주소'] = adress_roadname

down_data = clean_data[['업체명', '일반주소', '도로명주소', '전화번호', '홈페이지주소']]
down_data.fillna('', inplace=True)

```

위 코드는 데이터를 불러오고 전처리한 뒤, 지도 시각화와 간단한 데이터 분석을 수행하며 최종적으로 Excel 파일로 저장하는 과정을 담고 있습니다. 코드의 주석과 출력 결과를 통해 각 단계에서 어떤 작업이 수행되고 있는지 확인할 수 있습니다.

### **6. 데이터 전처리**

```python
pythonCopy code
# '등록일자' 열 삭제
clean_data = clean_data.drop(['등록일자'], axis=1)

```

- '등록일자' 열을 삭제하는 부분입니다. 이 열은 데이터에서 제거되어 더 이상 사용되지 않게 됩니다.

### **7. Excel 파일로 데이터 저장**

```python
pythonCopy code
# '일반주소'와 '도로명주소' 열 추가 및 결측값 처리
adress_roadname = clean_data['도로명'] + clean_data['도로명상세']
adress = clean_data['시도명'] + clean_data['시군구명'] + clean_data['읍면동명'] + clean_data['번지']

clean_data['일반주소'] = adress
clean_data['도로명주소'] = adress_roadname

# '업체명', '일반주소', '도로명주소', '전화번호', '홈페이지주소' 열 선택
down_data = clean_data[['업체명', '일반주소', '도로명주소', '전화번호', '홈페이지주소']]
down_data.fillna('', inplace=True)

```

- '일반주소' 및 '도로명주소' 열을 새로 만들고, 결측값을 처리하는 부분입니다.
- 최종적으로 '업체명', '일반주소', '도로명주소', '전화번호', '홈페이지주소' 열을 선택하여 데이터프레임을 만듭니다.

이 부분에서는 열을 조작하여 주소 관련 정보를 새로운 열로 추가하고, 필요한 열만 선택하여 최종 데이터를 정리하는 작업을 수행합니다.

### 2. streamlit 구축

### **1. 라이브러리 및 데이터 로드**

```python
pythonCopy code
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import folium
import openpyxl
from pyxlsb import open_workbook as open_xlsb
from io import BytesIO
from xlsxwriter import Workbook

```

- **plotly, pandas, streamlit, folium 등의 라이브러리를 사용하여 데이터 시각화 및 웹 애플리케이션 개발에 필요한 모듈 로드**

---

### **2. Streamlit 웹 애플리케이션 구성**

```python
pythonCopy code
st.title('Dynamic Busan ☀️')
st.subheader('원하는 조건의 부산 숙박업소를 쉽게 검색해봐요! 😎', anchor=None, help=None, divider=False)

```

- **웹 애플리케이션의 제목과 부제 설정**

---

### **3. 데이터 로드 및 필터링**

```python
pythonCopy code
data = pd.read_csv('./BusanHotelFirst.csv')
filter_data = data

```

- **CSV 파일에서 부산 숙박업소 데이터 로드**
- **`filter_data` 변수에 초기 데이터 설정**

---

### **4. 검색 조건 설정**

```python
pythonCopy code
options = st.sidebar.multiselect(
    '편의시설',
    ['휠체어 이동 가능', '점자도로이용가능', '물품보관함 이용가능', '수유실 이용 가능'])

```

- **`st.sidebar.multiselect`을 사용하여 편의시설에 대한 다중 선택 기능 구현**

---

### **5. 검색 조건에 따른 데이터 필터링**

```python
pythonCopy code
if (options is not None):
    for i in options:
        col = options_value[i]
        filter_data = filter_data[filter_data[col] == 'Y']

```

- **선택한 편의시설에 따라 데이터를 필터링**

---

### **6. 지도 상에 숙박업소 표시**

```python
pythonCopy code
map = folium.Map(location=[filter_data['위도'].mean(), filter_data['경도'].mean()], zoom_start=10)
for n in filter_data.index:
    name = filter_data.loc[n, '업체명']
    address = filter_data.loc[n, '도로명']

    popup = folium.Popup(f'<i>{name}-{address}</i>', max_width=600, max_height=600)
    location = [filter_data.loc[n, '위도'], filter_data.loc[n, '경도']]
    folium.Marker(
        location=location,
        popup=popup,
        icon=folium.Icon(color='red', icon='plus', prefix='fa')
    ).add_to(map)

```

- **Folium을 사용하여 지도를 생성하고, 필터링된 데이터에 대한 마커 표시**

---

### **7. 결과 및 다운로드 기능**

```python
pythonCopy code
df_xlsx = to_excel(process_down_data(filter_data))
st.sidebar.download_button(label='📥 Download Current Result',
                            data=df_xlsx,
                            file_name='df_test.xlsx')

```
