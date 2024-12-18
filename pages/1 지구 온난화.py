import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc

# 한국어 폰트 설정
rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False  # 한글 폰트 사용 시 마이너스 기호 깨짐 방지

st.set_page_config(
    page_title = "AI for Ecosystem",
    page_icon = "🌎"
    )

# 데이터 가져오기
df1 = pd.read_csv("./datas/temp_seoul.csv")
df2 = pd.read_csv("./datas/CO2.csv")

st.title("[1차시]🌎지구온난화🔥")

# 1. 서울 지역의 평균 기온 변화
st.header("1. 서울 지역의 평균 기온 변화🌡️")
st.subheader("1.1. 데이터 살펴보기")
st.link_button("📒출처: 기상자료개방포털", "data.kma.go.kr")
st.write(df1)

st.subheader("1.2. 데이터 시각화")

# 시각화 데이터 선택
temp_column = st.radio(
    "어떤 데이터를 시각화할까요?",
    ("평균기온(℃)", "평균최저기온(℃)", "평균최고기온(℃)")
)

# 그래프 유형 선택
chart_type = st.selectbox(
    "어떤 그래프로 나타낼까요?",
    ("그래프 선택하기", "막대그래프", "꺾은선그래프"),
    key="temp_chart"
)

# 시각화
if chart_type == "꺾은선그래프":
    st.line_chart(data=df1, x="연도", y=temp_column, color=["#FF0000"], height=500, use_container_width=True)
elif chart_type == "막대그래프":
    st.bar_chart(data=df1, x="연도", y=temp_column, color=["#FF0000"], height=500, use_container_width=True)
else:
    st.write("그래프 유형을 선택해주세요.")

st.write("❓서울의 평균 기온은 어떻게 변하고 있나요?")

if st.button("🔍지구의 평균 기온은 어떻게 변하고 있을까?"):
    st.write("빙하기와 간빙기가 반복되면서 지구 기온은 변하고 있습니다.")
    st.write("다만, 최근 100여 년간 지구 기온의 증가 폭은 이전에 볼 수 없엇던 높은 수치이며, 증가 속도가 매우 빨라지고 있습니다.")
    st.image("images/지구기온.png", caption="[과거 온도 변화와 최근 지구 표면 연평균 온도 변화]")
st.divider()

# 2. 대기 중 CO2 농도 변화
st.header("2. 대기 중 CO2 농도 변화🏭")
st.subheader("2.1. 데이터 살펴보기")
st.link_button("📒출처: 하와이 마우나로아 관측소에서 측정한 이산화탄소(CO2) 농도", "datahub.io/core/co2-ppm")
st.write(df2)

st.subheader("2.2. 데이터 시각화")

# 그래프 유형 선택
chart_type2 = st.selectbox(
    "CO2 데이터를 어떤 그래프로 나타낼까요?",
    ("그래프 선택하기", "막대그래프", "꺾은선그래프"),
    key="co2_chart"
)

# 시각화
if chart_type2 == "꺾은선그래프":
    st.line_chart(data=df2, x="연도", y="CO2(ppm)", height=500, use_container_width=True)
elif chart_type2 == "막대그래프":
    st.bar_chart(data=df2, x="연도", y="CO2(ppm)", height=500, use_container_width=True)
else:
    st.write("그래프 형을 선택해주세요.")

st.write("❓대기 중 CO2 농도는 어떻게 변하고 있나요? ")
if st.button("🔍대기 중 CO2 농도 변화는 기온 증가 패턴과 어떤 관련이 있나요?"):
    st.write("위에서 살펴본 기온의 증가 패턴과 대기 중 CO2 농도의 변화는 매우 흡사합니다. ")
    st.write("CO2 농도 변화 곡선은 이 관측을 주도한 기후학자의 이름을 따서 킬링 곡선이라고 부릅니다.")
    st.write("1958년 이후 CO2 농도는 꾸준히 증가하고 있으며 이 킬링 곡선의 상승은 곧 지구 기온 상승을 의미합니다.")
    st.image("images/CO2증가에따른표면온도증가.png", caption="[CO2 증가에 따른 표면 온도 증가]")