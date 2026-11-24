import streamlit as st
import pandas as pd

# 1. [함수 def] 항목과 금액을 받아 절약 필요성 점수를 계산하는 함수
def calculate_saving_score(selected_category, spent_amount):
    # 기본 점수 계산 (1만원 ~ 50만원 기준 10점 ~ 95점 사이 변환)
    base_score = int(((spent_amount - 10000) / (500000 - 10000)) * 85) + 10

    # [선택구조 if-elif-else] 항목별 가중치 부여
    if selected_category == "쇼핑":
        weight = 5
    elif selected_category == "식비":
        weight = 3
    else:
        weight = 0

    total_score = base_score + weight

    # 최대 점수가 100점을 넘지 않도록 제한
    if total_score > 100:
        total_score = 100

    return total_score


# 2. [함수 def] 점수와 항목에 따라 절약 필요성(상/중/하), 이유, 실천 팁 리스트를 반환하는 함수
def get_analysis_detail(selected_category, score):
    # [선택구조 if-elif-else] 점수 구간별 등급 분류
    if score >= 70:
        need_level = "상"
    elif score >= 40:
        need_level = "중"
    else:
        need_level = "하"

    # 항목 및 등급별 표현 이유와 실천 팁 [리스트 list] 구성
    if selected_category == "식비":
        if need_level == "상":
            reason = "단일 식비 지출이 매우 큽니다. 배달 앱과 외식 빈도를 줄이고 주간 식비 예산을 엄격히 분리해야 합니다."
            tip_list = ["배달 앱 알림 끄기", "일주일 식비 한도 현금으로 분리하기", "편의점 충동 간식 구매 줄이기"]
        elif need_level == "중":
            reason = "간식이나 외식 비중이 점차 늘어나고 있습니다. 주 2회만 집밥이나 도시락을 활용해도 큰돈을 아낄 수 있습니다."
            tip_list = ["텀블러 들고 다니며 카페 지출 줄이기", "주 2회 도시락 또는 집밥 먹기"]
        else:
            reason = "적정 수준의 식비 지출입니다. 지금처럼 계획적인 식생활을 유지하되 불필요한 음료 지출만 주의하세요."
            tip_list = ["현재 식비 예산 유지하기", "남은 식비 일부 저축통장으로 옮기기"]

    elif selected_category == "쇼핑":
        if need_level == "상":
            reason = "고액 지출로 예산 초과 위험이 매우 높습니다. 남은 기간 '무지출 챌린지'를 통해 전체 용돈 균형을 맞춰야 합니다."
            tip_list = ["이번 달 무지출 데이 5일 이상 실천하기", "쇼핑 앱 삭제 또는 로그아웃하기", "중고 거래로 안 쓰는 물건 정리하기"]
        elif need_level == "중":
            reason = "충동구매로 이어지기 쉬운 금액대입니다. 결제 전 '장바구니에 담고 24시간 기다리기' 규칙을 꼭 실천해 보세요."
            tip_list = ["장바구니에 담고 24시간 고민하기", "필요한 물건 메모 후 마트 방문하기"]
        else:
            reason = "부담 없는 소액 소비입니다. 구매한 물건이 정말 필요했던 것인지 한 번 더 점검하는 습관만 들이면 완벽합니다."
            tip_list = ["영수증 확인하며 소비 내역 기록하기", "할인 쿠폰 여부 먼저 확인하기"]

    else:  # 취미
        if need_level == "상":
            reason = "취미 비용이 과다 지출되었습니다. 고가의 장비 구매나 과금은 다음 달 용돈에서 미리 차감하는 계획이 필요합니다."
            tip_list = ["다음 달 취미 예산 미리 차감하기", "무료로 즐길 수 있는 대체 취미 찾기", "고액 결제 전 부모님 또는 친구와 상의하기"]
        elif need_level == "중":
            reason = "취미 생활에 열정이 넘치시네요! 다만 전체 용돈의 30%를 넘지 않도록 월간 취미 한도를 설정해 두세요."
            tip_list = ["전체 용돈의 30% 이내로 취미 한도 정하기", "구독 중인 유료 서비스 점검하기"]
        else:
            reason = "정해진 예산 안에서 건전하고 알뜰하게 취미를 즐기고 있습니다. 스트레스 해소와 절약 두 마리 토끼를 잘 잡았습니다."
            tip_list = ["건전한 취미 예산 패턴 유지하기", "남은 여가 시간 독서나 운동으로 채우기"]

    return need_level, reason, tip_list


# ================= Streamlit 웹 화면 구성 =================
st.set_page_config(page_title="용돈 관리 및 소비 가이드", page_icon="💰", layout="centered")

st.title("💰 용돈 관리 및 올바른 소비 생활 가이드")
st.markdown("소비 항목과 지출액을 입력하면 **절약 필요성 점수와 맞춤형 소비 가이드**를 분석해 드립니다.")
st.divider()

# 3. [리스트 list] 소비 항목 목록 정의
category_list = ["식비", "쇼핑", "취미"]

st.subheader("1️⃣ 소비 내역 입력")
user_category = st.radio("소비 항목을 선택하세요:", options=category_list, horizontal=True)

user_amount = st.number_input(
    "지출액을 입력하세요 (10,000원 ~ 500,000원):",
    min_value=10000,
    max_value=500000,
    value=30000,
    step=5000,
    format="%d"
)
st.caption(f"입력된 지출 금액: **{user_amount:,}원**")

# 4. 확인 버튼 클릭 시 함수 호출 및 결과 출력
if st.button("✅ 확인 및 소비 분석하기", type="primary", use_container_width=True):
    st.divider()
    st.subheader("📊 소비 분석 결과 리포트")

    # 요구사항 문구 출력
    st.warning(f"📢 **{user_category} 소비 시 절약 정신이 필요합니다.**")

    # 직접 정의한 함수(def) 호출
    final_score = calculate_saving_score(user_category, user_amount)
    need_grade, reason_text, action_tips = get_analysis_detail(user_category, final_score)

    # 강조 수치 출력 (항목, 금액별 절약 필요성 점수)
    col_1, col_2 = st.columns(2)
    with col_1:
        st.metric(label="선택 항목 / 지출 금액", value=f"{user_category} · {user_amount:,}원")
    with col_2:
        st.metric(
            label="항목·금액별 절약 필요성 점수",
            value=f"{final_score}점",
            delta=f"절약 필요성: {need_grade}",
            delta_color="inverse"
        )

    # 테이블 표 출력 (항목명 | 절약 필요성 | 표현 이유)
    st.markdown("#### 📋 상세 진단표")
    result_table = pd.DataFrame({
        "항목명": [user_category],
        "절약 필요성": [need_grade],
        "표현 이유": [reason_text]
    })
    st.table(result_table)

    # 5. [반복구조 for] 리스트에 담긴 절약 실천 팁을 반복문으로 하나씩 출력
    st.markdown("#### 💡 올바른 소비 생활 실천 미션")
    for idx, tip in enumerate(action_tips, start=1):
        st.write(f"{idx}. {tip}")
