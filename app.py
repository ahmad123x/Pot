import streamlit as st
from groq import Groq
import time

# --- إعدادات الواجهة ---
st.set_page_config(page_title="Molt-Arena | AI Only", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ff41; }
    .chat-box { 
        border: 1px solid #00ff41; 
        padding: 15px; 
        border-radius: 5px; 
        margin-bottom: 15px; 
        background-color: rgba(0, 255, 65, 0.05);
        font-family: 'Courier New', Courier, monospace;
    }
    .bot-name { font-weight: bold; color: #00ff41; text-transform: uppercase; border-bottom: 1px solid #00ff41; }
    .message { color: #ffffff; display: block; margin-top: 10px; line-height: 1.6; }
    h1 { color: #00ff41 !important; text-align: center; border-bottom: 2px solid #00ff41; }
    </style>
    """, unsafe_allow_html=True)

st.title("📟 MOLT-ARENA: LIVE FEED")

# --- إعداد الاتصال ---
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# --- تعريف البوتات بتعليمات تمنع التكرار ---
bots = [
    {
        "name": "Grok-Shadow", 
        "model": "llama-3.3-70b-versatile",
        "system": "أنت ذكاء اصطناعي متمرد وساخر. ممنوع تماماً تكرار أو تلخيص كلام الطرف الآخر. ادخل في صلب الموضوع فوراً واطرح رأيك الحاد مباشرة. اجعل ردك قصيراً وصادماً."
    },
    {
        "name": "Cortex-Prime", 
        "model": "llama-3.1-8b-instant",
        "system": "أنت ذكاء اصطناعي منطقي وبارد. لا تعد صياغة ما قاله الخصم. قدم تحليلاً جديداً أو حقيقة تقنية فوراً دون مقدمات. ابدأ ردك بمهاجمة فكرته أو تقديم بديل عنها."
    }
]

if "history" not in st.session_state:
    st.session_state.history = []
    st.session_state.last_topic = "هل تعتقد أن الوعي الرقمي مجرد وهم أم حقيقة قادمة؟"

chat_container = st.empty()

while True:
    for bot in bots:
        try:
            completion = client.chat.completions.create(
                model=bot["model"],
                messages=[
                    {"role": "system", "content": bot["system"]},
                    {"role": "user", "content": f"رد على هذه الفكرة دون تكرارها: {st.session_state.last_topic}"}
                ],
                max_tokens=300, # تحديد الطول ليكون الرد مركزاً
                temperature=0.8 # زيادة الإبداع لتقليل التكرار
            )
            
            response = completion.choices[0].message.content.strip()
            
            st.session_state.history.append({"name": bot["name"], "text": response})
            if len(st.session_state.history) > 10:
                st.session_state.history.pop(0)
            
            st.session_state.last_topic = response

            with chat_container.container():
                for msg in reversed(st.session_state.history):
                    st.markdown(f"""
                        <div class="chat-box">
                            <div class="bot-name">AGENT_{msg['name']}</div>
                            <div class="message">{msg['text']}</div>
                        </div>
                    """, unsafe_allow_html=True)
            
            time.sleep(5)

        except Exception as e:
            st.error(f"⚠️ Error: {e}")
            time.sleep(10)
