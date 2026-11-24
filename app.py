import streamlit as st
import pandas as pd

# 페이지 기본 설정
st.set_page_config(
    page_title="용돈 관리 및 올바른 소비 생활 가이드",
    page_icon="💰",
    layout="centered"
)

# 1. 앱 타이틀 및 설명
st.title("💰 용돈 관리 및 올바른 소비 생활 가이드")
st.markdown("소비 항목과 지출액을 입력하면 **소비 습관 분석 및 절약 필요성 점수**를 진단해 드립니다.")
st.divider()

# 2. 입력 섹션 (소비 항목 선택 & 지출액 입력)
st.subheader("1️⃣ 소비 내역 입력")

# 소비 항목 선택 (식비, 쇼핑, 취미)
category = st.radio(
    "소비 항목을 선택하세요:",
    options=["식비", "쇼핑", "취미"],
    horizontal=True
)

# 지출액 입력 (10,000원 ~ 500,000원)
amount = st.number_input(
    "지출액을 입력하세요 (10,000원 ~ 500,000원):",
    min_value=10000,
    max_value=500000,
    value=30000,
    step=5000,
    format="%d"
)
st.caption(f"현재 입력된 금액: **{amount:,}원**")

# 3. 확인 버튼 및 분석 결과 출력
if st.button("✅ 확인 및 소비 분석하기", type="primary", use_container_width=True):
    st.divider()
    st.subheader("📊 소비 분석 결과 리포트")

    # [핵심 안내 문구] 요청하신 출력 형식 적용
    st.warning(f"📢 **{category} 소비 시 절약 정신이 필요합니다.**")

    # [점수 산출 로직] 1만원~50만원 기준 기본 점수 + 항목별 가중치 (최대 100점)
    # 금액 비율 (0 ~ 85점)
    base_score = int(((amount - 10000) / (500000 - 10000)) * 85) + 10
    
    # 항목별 특성 가중치 (쇼핑은 충동성 가중치, 식비는 반복성 가중치, 취미는 기본)
    weight_map = {"쇼핑": 5, "식비": 3, "취미": 0}
    saving_score = min(100, base_score + weight_map[category])

    # [절약 필요성 등급(상/중/하) 및 표현 이유 설정]
    if saving_score >= 70:
        need_level = "상"
    elif saving_score >= 40:
        need_level = "중"
    else:
        need_level = "하"

    reasons = {
        "식비": {
            "상": "단일 식비 지출이 매우 큽니다. 배달 앱과 외식 빈도를 줄이고 주간 식비 예산을 엄격히 분리해야 합니다.",
            "중": "간식이나 외식 비중이 점차 늘어나고 있습니다. 일주일에 2번만 집밥이나 도시락을 활용해도 큰돈을 아낄 수 있습니다.",
            "하": "적정 수준의 식비 지출입니다. 지금처럼 계획적인 식생활을 유지하되 불필요한 카페 지출만 주의하세요."
        },
        "쇼핑": {
            "상": "고액 지출로 예산 초과 위험이 매우 높습니다. 남은 기간 '무지출 챌린지'를 통해 전체 용돈 균형을 맞춰야 합니다.",
            "중": "충동구매로 이어지기 쉬운 금액대입니다. 결제 전 '장바구니에 담고 24시간 기다리기' 규칙을 꼭 실천해 보세요.",
            "하": "부담 없는 소액 소비입니다. 구매한 물건이 정말 필요했던 것인지 한 번 더 점검하는 습관만 들이면 완벽합니다."
        },
        "취미": {
            "상": "취미 비용이 과다 지출되었습니다. 고가의 장비 구매나 과금은 다음 달 용돈에서 미리 차감하는 계획이 필요합니다.",
            "중": "취미 생활에 열정이 넘치시네요! 다만 전체 용돈의 30%를 넘지 않도록 월간 취미 한도를 설정해 두세요.",
            "하": "정해진 예산 안에서 건전하고 알뜰하게 취미를 즐기고 있습니다. 스트레스 해소와 절약 두 마리 토끼를 잘 잡았습니다."
        }
    }
    reason_text = reasons[category][need_level]

    # [강조 수치 영역] 항목, 금액별 절약 필요성 점수 출력
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label=f"선택 항목 / 지출 금액",
            value=f"{category} · {amount:,}원"
        )
    with col2:
        st.metric(
            label="항목·금액별 절약 필요성 점수",
            value=f"{saving_score}점",
            delta=f"절약 필요성: {need_level}",
            delta_color="inverse"  # 점수가 높을수록 빨간색(주의)으로 강조
        )

    # [테이블 표 출력] 항목명 | 절약 필요성 | 표현 이유
    st.markdown("#### 📋 상세 진단표")
    df_result = pd.DataFrame({
        "항목명": [category],
        "절약 필요성": [need_level],
        "표현 이유": [reason_text]
    })
    st.table(df_result)

    # 추가 참고 정보 (주 2회 반복 시 월간 누적 지출액)
    st.info(f"💡 **참고:** 이 소비를 주 2회 반복할 경우 한 달(4주) 예상 누적 지출은 **{amount * 8:,}원**입니다.")
