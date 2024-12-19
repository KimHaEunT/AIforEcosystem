import streamlit as st
import pandas as pd
import numpy as np
from numpy.polynomial.polynomial import Polynomial
from streamlit_sortables import sort_items
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import rc

import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium, folium_static
from folium import plugins
from folium.features import DivIcon

import matplotlib.font_manager as fm

# 현재 파일의 절대 경로 기준으로 폰트 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(current_dir, 'fonts', 'malgun.ttf')

# 폰트 파일 존재 여부 확인
if not os.path.exists(font_path):
    raise FileNotFoundError(f"폰트 파일을 찾을 수 없습니다: {font_path}")

# matplotlib 폰트 설정
font_prop = fm.FontProperties(fname=font_path)
plt.rc('font', family=font_prop.get_name())
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지
# matplotlib 폰트 설정
plt.rc('font', family=font_prop.get_name())
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

st.set_page_config(
    page_title = "AI for Ecosystem",
    page_icon = "🌎"
    )
#데이터 가져오기
df = pd.read_csv("./datas/flowers.csv")

st.title("[3차시]🌸꽃의 개화 시기🌸")

st.header("1.어느 꽃이 먼저 필까?")
# 이미지 파일 로드
flower_images = {
    "개나리": "./images/개나리.png",
    "진달래": "./images/진달래.png",
    "벚꽃": "./images/벚꽃.png",
}

# 정답 순서
correct_order = ["개나리", "진달래", "벚꽃"]

# 이미지를 섞어서 표시
shuffled_order = ["진달래", "벚꽃", "개나리"]

# 보기 섹션
st.write("""
         - **기온량**은 날이 따뜻해지면서 식물이 받는 온기가 얼마나 되는지를 계산한 수치이다. 
         - 어느 꽃이 먼저 필지 기온량(℃)을 비교해서 생각해보자.
          """)
columns = st.columns(3)
columns[0].image(flower_images["개나리"], caption="개나리\n84.2℃", width=150)
columns[1].image(flower_images["진달래"], caption="진달래\n96.1℃", width=150)
columns[2].image(flower_images["벚꽃"], caption="벚꽃\n106.2℃", width=150)

# 드래그 앤 드롭 인터페이스
st.write("**❓어느 꽃이 먼저 필까요?**")
user_order = sort_items(shuffled_order)

# 정렬된 순서의 이미지를 표시
columns = st.columns(len(user_order))
for i, flower in enumerate(user_order):
    with columns[i]:
        st.image(flower_images[flower], caption=flower, width=150)
        
# 제출 버튼
if st.button("제출"):
    if user_order == correct_order:
        st.success("정답입니다! 🌼")
    else:
        st.error("틀렸습니다. 다시 시도해보세요! 🌸")

st.write("❓겨울이 너무 따뜻하면 꽃은 언제 필까? 어떤 영향이 있을까?🥀")

st.divider()

st.header("2.내년 봄꽃은 언제 필까??")
st.subheader("2.1. 데이터 살펴보기")
st.write("개나리, 진달래, 벚꽃의 개화일 평년 편차 데이터를 살펴보자. ")
st.link_button("📒출처: 기상자료개방포털", "data.kma.go.kr")

st.write(df)

st.subheader("2.1. 데이터 시각화")
# 추세선 보기 여부
show_trend = st.button("추세선 보기")

# 그래프 생성
fig, ax = plt.subplots(figsize=(12, 6))

# 컬러 매핑
colors = {"개나리": "yellow", "진달래": "magenta", "벚꽃": "pink"}

# 각 꽃에 대해 그래프 그리기
for column in df.columns[1:]:
    if column in colors:
        # 원래 데이터 플롯
        ax.plot(df['년도'], df[column], label=column, color=colors[column])
        
        # 추세선 추가 (버튼 클릭 시)
        if show_trend:
            z = np.polyfit(df['년도'], df[column], 1)  # 1차원 다항식 추세선
            p = np.poly1d(z)
            ax.plot(df['년도'], p(df['년도']), linestyle="--", color=colors[column], alpha=0.7, label=f"{column} 추세선")

# 그래프 설정
ax.set_title('개나리, 진달래, 벚꽃의 평년 편차 (일)', fontsize=14)
ax.set_xlabel('연도', fontsize=12)
ax.set_ylabel('평년 편차 (일)', fontsize=12)
ax.invert_yaxis()  # Y축 방향 반전
ax.legend(title='꽃 종류', loc='lower right', frameon=False)
ax.grid(axis='y', linestyle='--', alpha=0.7)

#그래프 표시
st.pyplot(fig)

st.write("❓봄꽃의 개화 시기는 어떻게 변하고 있나요?🌸")

if st.button("🔍봄꽂 동시 개화??🌺"):
    st.write("진달래는 개나리보다 늦게 개화하는 데, 2080년 이후에는 개나리와 진달래가 동시 개화하거나, 진달래가 더 빨리 개화할 것으로 예상됩니다.")
    st.write("과거에는 30일 편차로 피던 개나리와 벚꽃이 2010년 이후에는 1주일 간격으로 거의 동시에 개화하고 있습니다.")
    st.image("images/봄꽃개화시기.png", caption="[연대별 봄꽃 개화 시기 변화]")
    

st.header("3.개화 시기는 왜 빨라질까??")
st.write("❓어떤 데이터를 가져와볼까?")

# 데이터 불러오기
temp_data = pd.read_csv("./datas/temp_seoul.csv")  # 평균 기온 데이터
flowers_data = pd.read_csv("./datas/flowers.csv")  # 개화 시기 데이터

# 버튼 생성
selected_button = st.radio(
    "비교할 데이터를 선택하세요:",
    ("1. 평균 기온", "2. CO₂ 농도 변화", "3. 해수면 변화")
)

# 1. 평균 기온 버튼 선택 시 시각화
if selected_button == "1. 평균 기온":
    st.subheader("연도별 평균 기온과 꽃 개화 시기 비교")

    # 데이터 병합 (공통 연도 기준)
    merged_data = pd.merge(temp_data, flowers_data, left_on="연도", right_on="년도", how="inner")

    # 시각화
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # 평균 기온 꺾은선 그래프
    ax1.plot(merged_data["연도"], merged_data["평균기온(℃)"], color="red", label="평균기온(℃)", linewidth=2)
    ax1.set_xlabel("연도", fontsize=12)
    ax1.set_ylabel("평균기온(℃)", fontsize=12, color="red")
    ax1.tick_params(axis="y", labelcolor="red")

    # 개화 시기 추가 (개나리, 진달래, 벚꽃)
    ax2 = ax1.twinx()  # 두 번째 y축
    ax2.plot(merged_data["연도"], merged_data["개나리"], color="orange", label="개나리 개화", linestyle="--")
    ax2.plot(merged_data["연도"], merged_data["진달래"], color="purple", label="진달래 개화", linestyle="--")
    ax2.plot(merged_data["연도"], merged_data["벚꽃"], color="pink", label="벚꽃 개화", linestyle="--")
    ax2.set_ylabel("개화 시기 (편차)", fontsize=12, color="blue")
    ax2.tick_params(axis="y", labelcolor="blue")

    # y축 범위 설정 (-20 ~ 20)
    ax2.set_ylim(-20, 20)
    ax2.invert_yaxis()  # y축 반전

    # 범례 추가
    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))

    # 그래프 출력
    st.pyplot(fig)

elif selected_button == "2. CO₂ 농도 변화":
    st.subheader("데이터를 다시 선택해봅시다.")
elif selected_button == "3. 해수면 변화":
    st.subheader("데이터를 다시 선택해봅시다.")
else:
    st.write("어떤 데이터를 비교해볼까요?")

if st.button("🔍봄꽃 개화 시기는 왜 빨라질까?🌺"):
    st.write("봄꽃의 개화 시기가 매년 빨라지는 것은 높은 기온과 긴 일조 시간 때문입니다.")
    st.write("겨울 기온이 지속해 상승하고 건조한 날씨가 이어지며 일조량도 길어져 봄꽃이 빨리 피고 있습니다.")
    
st.write("❓꽃의 개화 시기가 빨라지면 우리 생활에 어떤 변화가 있을까?")
    
