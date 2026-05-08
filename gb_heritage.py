import streamlit as st
import google.generativeai as genai

# 1. API 키 설정 (금고에서 꺼내오기)
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    API_KEY = "AIzaSyDIkKKu5-wPNzfJlji1jIdEsZV2moJaqdY"

genai.configure(api_key=API_KEY)

# 에러의 주범이었던 복잡한 역할 설정(system_instruction)을 완전히 빼버렸습니다!
# 가장 빠르고 똑똑한 최신 모델의 이름만 단순하게 적어줍니다.
model = genai.GenerativeModel('gemini-2.0-flash-lite')

# 2. 웹페이지 화면 구성 (UI)
st.set_page_config(page_title="경북 문화유산 탐험대", page_icon="🏯", layout="centered")
st.title("🗺️ 경북 문화유산 탐험대")
st.write("우리 지역의 보물들을 재미있는 이야기로 만나보세요!")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 3. 문화유산 검색창
heritage_name = st.text_input("🔍 조사하고 싶은 문화유산 이름을 적어보세요! (예: 봉암사 지증대사탑비)")

if st.button("이야기 들려주세요!"):
    if heritage_name:
        st.session_state.messages = []
        st.session_state.chat_session = model.start_chat(history=[])
        
        # [핵심] AI에게 역할을 몰래 속삭이는 '주문'을 만들고, 아이들의 검색어를 덧붙입니다.
        secret_prompt = f"너는 초등학교 4학년 학생들에게 설명해주는 친절한 도슨트야. 어려운 한자어 없이 동화처럼 다정하게 존댓말로 설명해줘. 꼭 3가지(1.특징과 가치 2.옛날이야기나 전설 3.꼬리질문 유도하는 인사)를 포함해서 '{heritage_name}'에 대해 알려줘."
        
        with st.spinner('문화유산의 숨겨진 이야기를 찾는 중...'):
            try:
                # 겉으로는 문화유산 이름만 보낸 것 같지만, 실제로는 길고 꼼꼼한 주문을 보냅니다.
                response = st.session_state.chat_session.send_message(secret_prompt)
                
                # 하지만 아이들 화면에는 아이들이 검색한 단어만 깔끔하게 보여줍니다!
                st.session_state.messages.append({"role": "user", "content": heritage_name})
                st.session_state.messages.append({"role": "model", "content": response.text})
            except Exception as e:
                st.error(f"앗, 에러가 났어요: {e}")

# 4. 대화 내용 출력 및 꼬리 질문
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if follow_up := st.chat_input("더 궁금한 내용이 있나요? (예: 왜 거북이 모양이야?)"):
    with st.chat_message("user"):
        st.markdown(follow_up)
    st.session_state.messages.append({"role": "user", "content": follow_up})
    
    with st.chat_message("model"):
        with st.spinner('생각 중...'):
            try:
                # 꼬리 질문을 할 때도 4학년 눈높이를 까먹지 않게 살짝 덧붙여줍니다.
                reminder_prompt = f"초등학교 4학년 눈높이에 맞춰서 다정하게 대답해줘: {follow_up}"
                response = st.session_state.chat_session.send_message(reminder_prompt)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "model", "content": response.text})
            except Exception as e:
                st.error(f"앗, 에러가 났어요: {e}")
