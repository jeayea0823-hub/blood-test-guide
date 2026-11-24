import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="혈액검사 수치 및 맞춤형 관리방법 가이드",
    page_icon="🩸",
    layout="centered"
)


# 관리방법 리스트
management_list = {

    "혈당": [
        {
            "관리방법": "식후 간단한 산책",
            "추천하는 방법": "식후 가볍게 걷기",
            "중요도": "상",
            "이유": "식후 혈당 급상승 방지"
        },
        {
            "관리방법": "당음료 섭취 줄이기",
            "추천하는 방법": "탄산음료 대신 물 마시기",
            "중요도": "중",
            "이유": "당류 섭취 감소에 도움"
        }
    ],

    "헤모글로빈": [
        {
            "관리방법": "철분이 풍부한 음식 섭취",
            "추천하는 방법": "살코기, 시금치 등 섭취",
            "중요도": "상",
            "이유": "헤모글로빈 생성에 필요한 철분 공급"
        },
        {
            "관리방법": "비타민 C 섭취",
            "추천하는 방법": "오렌지, 키위 등 섭취",
            "중요도": "중",
            "이유": "철분 흡수에 도움"
        }
    ],

    "콜레스테롤": [
        {
            "관리방법": "기름진 음식 줄이기",
            "추천하는 방법": "튀김과 가공식품 섭취 줄이기",
            "중요도": "상",
            "이유": "포화지방 섭취 감소"
        },
        {
            "관리방법": "규칙적인 운동",
            "추천하는 방법": "하루 30분 걷기",
            "중요도": "중",
            "이유": "혈중 지질 개선에 도움"
        }
    ]
}


# 혈액검사 결과 분석 함수
def check_blood(item, value):

    score = 60
    warning = ""
    message = ""

    # 혈당 검사
    if item == "혈당":

        if value >= 126:
            score += 20
            warning = "혈당 수치가 높습니다."
            message = "혈당수치 관리가 필요합니다."

        elif value >= 100:
            score += 10
            warning = "혈당 수치에 주의가 필요합니다."
            message = "혈당 관리에 관심을 가져주세요."

        else:
            message = "혈당 수치가 설정한 기준 범위에 해당합니다."

    # 헤모글로빈 검사
    elif item == "헤모글로빈":

        if value < 12:
            score += 20
            warning = "헤모글로빈 수치가 낮습니다."
            message = "빈혈 여부를 확인할 필요가 있습니다."

        elif value < 13.5:
            score += 10
            warning = "헤모글로빈 수치에 주의가 필요합니다."
            message = "헤모글로빈 수치를 관찰해 주세요."

        else:
            message = "헤모글로빈 수치가 설정한 기준 범위에 해당합니다."

    # 콜레스테롤 검사
    elif item == "콜레스테롤":

        if value >= 240:
            score += 20
            warning = "콜레스테롤 수치가 높습니다."
            message = "콜레스테롤 관리가 필요합니다."

        elif value >= 200:
            score += 10
            warning = "콜레스테롤 수치에 주의가 필요합니다."
            message = "식습관과 운동을 관리해 주세요."

        else:
            message = "콜레스테롤 수치가 설정한 기준 범위에 해당합니다."

    # 최대 점수 100점 제한
    score = min(score, 100)

    return score, warning, message


# 메인 화면 함수
def blood_guide():

    st.title("혈액검사 수치 및 맞춤형 관리방법 가이드")

    st.write(
        "혈액검사 수치를 입력하면 검사 결과와 "
        "맞춤형 관리방법을 확인할 수 있습니다."
    )

    st.divider()

    # 1. 검사 항목 선택
    st.subheader("1. 검사 항목 선택")

    item = st.selectbox(
        "검사 항목을 선택하세요.",
        ["혈당", "헤모글로빈", "콜레스테롤"]
    )

    # 2. 검사 수치 입력
    st.subheader("2. 혈액검사 수치 입력")

    if item == "헤모글로빈":

        value = st.slider(
            "헤모글로빈 수치 (g/dL)",
            min_value=5.0,
            max_value=25.0,
            value=14.0,
            step=0.1
        )

    else:

        value = st.slider(
            "검사 수치 (mg/dL)",
            min_value=50,
            max_value=250,
            value=100,
            step=1
        )

    st.write("선택한 검사 항목:", item)
    st.write("입력한 검사 수치:", value)

    st.divider()

    # 3. 분석하기 버튼
    if st.button("분석하기", use_container_width=True):

        # 검사 결과 분석
        score, warning, message = check_blood(item, value)

        st.subheader("3. 검사 결과")

        # 결과 메시지 출력
        st.success(message)

        # 경고 문구 출력
        if warning:
            st.warning(warning)

        # 위험도 점수 출력
        st.subheader("위험도 점수")

        st.metric(
            label="건강 위험도 점수",
            value=str(score) + "점"
        )

        # 위험도 진행 막대
        st.progress(score / 100)

        # 점수에 따른 안내
        if score >= 80:
            st.error("높은 주의가 필요한 결과입니다.")

        elif score >= 70:
            st.warning("건강관리에 주의를 기울여 주세요.")

        else:
            st.info("꾸준한 건강관리를 유지하세요.")

        st.divider()

        # 4. 맞춤형 관리방법 출력
        st.subheader("4. 맞춤형 관리방법")

        # 표 생성을 위한 데이터 리스트
        table_data = []

        # for문으로 관리방법 리스트 순회
        for management in management_list[item]:

            table_data.append({
                "관리방법 항목": management["관리방법"],
                "추천하는 방법": management["추천하는 방법"],
                "중요도": management["중요도"],
                "이유": management["이유"]
            })

        # 데이터프레임으로 변환
        df = pd.DataFrame(table_data)

        # 표 출력
        st.table(df)

        st.info("꾸준한 건강관리가 건강한 생활의 시작입니다!")

        st.caption(
            "※ 본 프로그램은 교육용 예시이며 의료 진단을 대신하지 않습니다."
        )


# 프로그램 실행
blood_guide()
