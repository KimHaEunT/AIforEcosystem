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

# 페이지 제목
st.title("[4차시]나의 탄소 발자국👣🌎")
if st.button("🔍탄소 발자국은 무엇일까? 어떤 의미가 있을까?👣🌎"):
    st.write("**탄소 발자국**이란 우리가 사용하는 에너지와 자원이 환경에 미치는 영향(이산화탄소(CO₂) 배출량)을 나타내는 수치입니다.")
    st.image("images/탄소발자국.png")

st.divider()

st.write("아래 항목을 입력하여 나의 탄소발자국을 계산해보세요!")

# 입력 항목
st.subheader("1. 에너지 사용")
electricity = st.number_input("1개월 전기 사용량 (kWh):", min_value=0.0, step=0.1, format="%.1f")
gas = st.number_input("1개월 도시가스 사용량 (m³):", min_value=0.0, step=0.1, format="%.1f")
water = st.number_input("1개월 물 사용량 (m³):", min_value=0.0, step=0.1, format="%.1f")

st.subheader("2. 교통 수단 이용")
car_km = st.number_input("1개월 자동차 주행 거리 (km):", min_value=0.0, step=0.1, format="%.1f")
public_transport = st.number_input("1개월 대중교통 이용 거리 (km):", min_value=0.0, step=0.1, format="%.1f")
flight_hours = st.number_input("1년 항공기 이용 시간 (시간):", min_value=0.0, step=0.1, format="%.1f")

st.subheader("3. 음식 소비")
meat_meals = st.number_input("1주일 육류 섭취 횟수:", min_value=0, step=1, format="%d")
vegetarian_meals = st.number_input("1주일 채식 섭취 횟수:", min_value=0, step=1, format="%d")

# 탄소 배출 계수 (대략적인 값)
CO2_FACTORS = {
    "electricity": 0.5,  # kg CO2 per kWh
    "gas": 2.0,  # kg CO2 per m³
    "water": 0.3,  # kg CO2 per m³
    "car": 0.2,  # kg CO2 per km
    "public_transport": 0.1,  # kg CO2 per km
    "flight": 90.0,  # kg CO2 per flight hour
    "meat": 5.0,  # kg CO2 per meat meal
    "vegetarian": 2.0,  # kg CO2 per vegetarian meal
}

# 탄소발자국 계산
if st.button("탄소발자국 계산하기"):
    total_CO2 = 0

    # 에너지 사용
    energy_CO2 = (
        electricity * CO2_FACTORS["electricity"]
        + gas * CO2_FACTORS["gas"]
        + water * CO2_FACTORS["water"]
    )
    total_CO2 += energy_CO2

    # 교통
    transport_CO2 = (
        car_km * CO2_FACTORS["car"]
        + public_transport * CO2_FACTORS["public_transport"]
        + flight_hours * CO2_FACTORS["flight"]
    )
    total_CO2 += transport_CO2

    # 음식 소비
    food_CO2 = (
        meat_meals * 52 * CO2_FACTORS["meat"]  # 1년 기준
        + vegetarian_meals * 52 * CO2_FACTORS["vegetarian"]  # 1년 기준
    )
    total_CO2 += food_CO2

    # 결과 출력
    st.subheader("🌱 결과")
    st.write(f"총 탄소발자국: **{total_CO2:,.2f} kg CO2**")
    st.write("🌲친구와 탄소 발자국을 비교해봅시다. 우리의 탄소 발자국을 줄이기 위해 어떤 노력을 할 수 있을까요??🌲")
    st.image("images/탄소발자국2.png")
