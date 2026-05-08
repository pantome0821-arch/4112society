import streamlit as st
import google.generativeai as genai

# ---------------------------------------------------------
# 1. API 키 설정 (보안을 위해 스트림릿 클라우드 비밀보관함 사용)
# ---------------------------------------------------------
# 인터넷에 올릴 때는 코드에 API 키를 직접 노출하면 구글이 키를 정지시킵니다.
# 그래서 st.secrets 라는 금고에서 꺼내오도록 설정합니다.
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    API_KEY = "AIzaSyCo6QDFWyPB7NvtTpydJj9ZCcjP2YMBLyw" # 컴퓨터에서 혼자 테스트할 때만 씁니다.

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    'gemini-pro', ...)
    너는 초등학교 4학년 학생들에게 경상북도의 문화유산을 재미있게 설명해주는 친절한 도슨트야.
    말투는 다정하고 존댓말을 써. 어려운 한자어나 전문 용어는 초등학생이 이해하기 쉬운 비유로 풀어서 설명해.
    학생이 문화유산을 검색하면 다음 세 가지를 반드시 포함해서 이야기해:
    1. 이 문화유산의 가장 큰 특징과 가치 (쉽게)
    2. 여기에 얽힌 재미있는 옛날이야기나 전설 (동화처럼 흥미진진하게)
    3. 질문을 유도하는 마무리 인사 ("어떤 점이 가장 신기했니?", "더 궁금한 게 있으면 '왜?', '어떻게?'라고 물어봐!")
    """
)

# ---------------------------------------------------------
# 2. 웹페이지 화면 구성 (UI)
# ---------------------------------------------------------
st.set_page_config(page_title="경북 문화유산 탐험대", page_icon="🏯", layout="centered")
st.title("🗺️ 경북 문화유산 탐험대")
st.write("우리 지역의 보물들을 재미있는 이야기로 만나보세요!")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# ---------------------------------------------------------
# 3. 문화유산 검색창
# ---------------------------------------------------------
heritage_name = st.text_input("🔍 조사하고 싶은 문화유산 이름을 적어보세요! (예: 봉암사 지증대사탑비)")

if st.button("이야기 들려주세요!"):
    if heritage_name:
        st.session_state.messages = []
        st.session_state.chat_session = model.start_chat(history=[])
        prompt = f"'{heritage_name}'에 대해 초등학교 4학년 수준으로 재미있게 설명해줘."
        
        with st.spinner('문화유산의 숨겨진 이야기를 찾는 중...'):
            try:
                # AI에게 질문 보내기
                response = st.session_state.chat_session.send_message(prompt)
                st.session_state.messages.append({"role": "model", "content": response.text})
            except Exception as e:
                # 에러(과부하 등)가 발생했을 때 띄울 귀여운 안내 문구!
                error_msg = str(e).lower()
                if "429" in error_msg or "exhausted" in error_msg or "quota" in error_msg:
                    st.warning("앗, 잠깐만요! 챗봇 친구가 한꺼번에 너무 많은 질문을 받아서 숨을 고르고 있어요. 10초 뒤에 다시 버튼을 눌러주세요 😊")
                else:
                    st.error(f"오류 원인: {e}")

# ---------------------------------------------------------
# 4. 대화 내용 출력 및 꼬리 질문
# ---------------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if follow_up := st.chat_input("더 궁금한 내용이 있나요? (예: 왜 거북이 모양으로 만들었어?)"):
    with st.chat_message("user"):
        st.markdown(follow_up)
    st.session_state.messages.append({"role": "user", "content": follow_up})
    
    with st.chat_message("model"):
        with st.spinner('생각 중...'):
            try:
                response = st.session_state.chat_session.send_message(follow_up)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "model", "content": response.text})
            except Exception as e:
                error_msg = str(e).lower()
                if "429" in error_msg or "exhausted" in error_msg or "quota" in error_msg:
                    st.warning("잠깐만요! 다른 친구들 질문에 답하느라 바빠요. 10초만 기다렸다가 다시 물어봐주세요 😊")
                else:
                    st.error("오류가 발생했습니다. 다시 시도해주세요.")
