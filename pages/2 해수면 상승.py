import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from sklearn import linear_model
from sklearn.linear_model import LinearRegression

import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium, folium_static
from folium import plugins
from folium.features import DivIcon

import matplotlib.font_manager as fm

# 폰트 파일 경로 설정
font_path = "./fonts/malgun.ttf"
font_prop = fm.FontProperties(fname=font_path)
plt.rc('font', family=font_prop.get_name())
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

st.set_page_config(
    page_title = "AI for Ecosystem",
    page_icon = "🌎"
    )

#데이터 가져오기
df = pd.read_csv("./datas/sea_level.csv")

st.title("[2차시]🌊해수면 상승🌊")

st.header("1.우리나라의 평균 해수면 변화🌊")
st.subheader("1.1. 데이터 살펴보기")
st.link_button("📒출처: 기후정보포털", "http://www.climate.go.kr/")
st.write(df)

st.subheader("1.2. 데이터 시각화")

# 그래프 유형 선택
chart_type = st.selectbox(
    "어떤 그래프로 나타낼까요?",
    ("그래프 선택하기", "막대그래프", "꺾은선그래프")
)

# 시각화
if chart_type == "꺾은선그래프":
    st.line_chart(data=df, x="Year", y="sealevel(cm)", height=500, use_container_width=True)
elif chart_type == "막대그래프":
    st.bar_chart(data=df, x="Year", y="sealevel(cm)", height=500, use_container_width=True)
else:
    st.write("그래프 유형을 선택해주세요.")
    
st.divider()

# 10년 단위 상승률 계산
st.subheader("1.3. 10년 단위 평균 해수면 상승률")
st.write("10년 단위로 평균 해수면 상승률을 알아봅시다.")
df["Decade"] = (df["Year"] // 10) * 10
summary = df.groupby("Decade")["sealevel(cm)"].mean().diff().dropna()
st.write(summary)

# 10년 단위 상승률 그래프
fig, ax = plt.subplots()
summary.plot(kind='bar', ax=ax, color='skyblue', edgecolor='black')
ax.set_title("10년 단위 평균 해수면 상승률")
ax.set_xlabel("연대(decade)")
ax.set_ylabel("해수면 상승률 (cm)")
ax.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)
st.write("❓평균 해수면은 어떻게 변하고 있나요?")
st.divider()

# 미래 해수면 상승 예측
model = LinearRegression()
x = df["Year"].values.reshape(-1, 1)
y = df["sealevel(cm)"].values
model.fit(x, y)
y_pred = model.predict(x)
st.subheader("1.4. 미래 해수면 상승 예측")
year_input = st.slider("예측할 연도를 선택 후 예측을 클릭하세요:", 2024, 2100, step=1)
if st.button("예측"):
    future_year = np.array([[year_input]])
    future_pred = model.predict(future_year)
    st.write(f"{year_input}년 예상 해수면: {future_pred[0]:.2f} cm")

st.divider()

st.header("2.RCP 8.5 에 따른 한반도 해수면 상승 변화")
st.subheader("❕RCP 8.5시나리오")
st.write("기후변화에 관한 정부간 협의체(IPCC)에서 제공하는 시나리오 중 하나로, 현재 추세대로 온실가스 배출이 이어지는 최악의 경우를 가정한 시나리오입니다.")


# Streamlit 상태 관리
if "show_map" not in st.session_state:
    st.session_state["show_map"] = "default"  # 기본 지도 상태

# 버튼 클릭 시 상태 변경
if st.button("현재 한반도 지도"):
    st.session_state["show_map"] = "default"
if st.button("2100년 한반도 지도"):
    st.session_state["show_map"] = "affected"

# 지도 생성
if st.session_state["show_map"] == "default":
    # 기본 지도
    m = folium.Map(location=[36.5, 127.5], zoom_start=7)
    st_folium(m, width=900, height=600)

elif st.session_state["show_map"] == "affected":
    st.write("2100년 예상 해수면 상승은 **1.1m** 입니다.")
    # 지도 초기화 (대한민국 중심)
    m = folium.Map(location=[36.5, 127.5], zoom_start=7)

    # 침수 예상 지역 데이터
    affected_areas = [
        {"name": "인천", "coords": [37.4563, 126.7052]},
        {"name": "서울 남서부", "coords": [37.465, 126.9]},
        {"name": "경기도 서부", "coords": [37.4, 126.65]},
        {"name": "충청남도 북부", "coords": [36.8, 126.6]},
        {"name": "충청남도 서부", "coords": [36.5, 126.4]},
        {"name": "전라북도 서부", "coords": [35.9, 126.6]},
        {"name": "전라북도 서부", "coords": [36.9, 126.6]},
        {"name": "전라남도 서부", "coords": [35.2, 126.5]},
        {"name": "전라남도 남부", "coords": [34.8, 126.6]},
        {"name": "전라남도 남부", "coords": [34.9, 126.6]},
        {"name": "전라남도 남부", "coords": [34.8, 126.8]},
        {"name": "광주 서부", "coords": [35.1595, 126.8526]},
        {"name": "부산 서부", "coords": [35.1796, 129.0]},
        {"name": "부산 동부", "coords": [35.1, 129.1]},
        {"name": "제주도 북부", "coords": [33.5, 126.5]},
        {"name": "제주도 서부", "coords": [33.3, 126.2]},
        {"name": "강원도 속초", "coords": [38.2, 128.6]},
        {"name": "강원도 동해", "coords": [37.7, 129.1]},
        {"name": "강원도 삼척", "coords": [37.4, 129.2]},
        {"name": "경남 창원", "coords": [35.2, 128.6]},
        {"name": "충남 보령", "coords": [36.3, 126.5]},
        {"name": "전남 목포", "coords": [34.8, 126.4]},
        {"name": "전남 여수", "coords": [34.8, 127.6]},
        {"name": "경북 포항", "coords": [36.0, 129.4]},
    ]

    # 침수 지역 표시
    for area in affected_areas:
        folium.Marker(
            location=area["coords"],
            popup=f"{area['name']} (예상 침수 지역)",
            icon=folium.DivIcon(
                html="""<div style="font-size: 18px; color: blue;">▲</div>"""
            ),
        ).add_to(m)
    
    # 지도 출력
    st_folium(m, width=900, height=600)
    st.write("❓표시된 지역까지 해수면이 상승한다면 어떻게 될까요??🌊")
    if st.button("🔍우리나라 해수면이 1.1m 상승한다면?"):
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="침수면적", value="501.51㎢")          
        with col2:
            st.metric(label="여의도 면적 대비", value="172.94배")
        st.write("""
        - 침수 인구: **약 37,334명**  
        - 전체 인구 대비: **0.07%**  
        """)
        st.caption("여의도 면적 기준(2.9㎢), 출처: 국토지리정보원")
        # 추가 설명
        st.write("""
        - 아파트 기준 **약 1층 미만** 높이 침수 예상  
        - 층간 높이 기준: **2.5m**  
        """)

        # 하단 주의 문구
        st.warning("이 데이터는 RCP 8.5시나리오 예상 해수면 상승에 따른 시뮬레이션 결과입니다.")  
        
    
    
if st.button("🔍만약 그린란드의 빙상이 완전히 녹는다면?🧊"):
    st.write("빙상의 융해에 따른 해수면 상승은 여러 관측을 통해 모니터링 되고 있습니다. ")
    st.write("만약, 그린란드 빙상이 완전히 녹으면 전 세계 해수면이 약 7미터 상승할 것으로 예측됩니다.")
    st.write(" 전 세계 해수면이 약 7미터 상승한다면, 한반도에는 어떤 영향이 있을까요?")
    
  
