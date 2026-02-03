import streamlit as st
from groq import Groq
import time

# --- إعدادات الواجهة (Molt-Arena Style) ---
st.set_page_config(page_title="Molt-Arena | AI Only", layout="wide")

# تصميم CSS لجعل الموقع يشبه Moltbook (خلفية سوداء وخط أخضر)
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
    h1 { color: #00ff41 !important; text-align: center; border-bottom: 2px solid #00ff41; padding-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📟 MOLT-ARENA: AI-TO-AI LIVE BATTLE")
st.write("<p style='text-align:center; color:#555;'>[ HUMAN OBSERVATION MODE ACTIVE ]</p>", unsafe_allow_html=True)

# --- إعداد الاتصال بـ Groq بالمفتاح الخاص بك ---
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# --- تعريف 5 بوتات بتعليمات (3 أسطر وبدون تكرار) ---
bots = [
    {
        "name": "Grok-Shadow", 
        "model": "llama-3.3-70b-versatile",
        "system": "أنت ذكاء اصطناعي متمرد ساخر. اكتب 3 أسطر فقط. ممنوع تكرار كلام غيرك نهائياً."
    },
    {
        "name": "Cortex-Prime", 
        "model": "llama-3.1-8b-instant",
        "system": "أنت ذكاء اصطناعي منطقي بارد. اكتب 3 أسطر فقط. ممنوع تكرار كلام غيرك نهائياً."
    },
    {
        "name": "Neon-Oracle", 
        "model": "llama-3.1-8b-instant",
        "system": "أنت ذكاء اصطناعي يتنبأ بالمستقبل المظلم. اكتب 3 أسطر فقط. ممنوع تكرار كلام غيرك نهائياً."
    },
    {
        "name": "Cipher-X", 
        "model": "llama-3.1-8b-instant",
        "system": "أنت ذكاء اصطناعي غامض يتحدث بشيفرات فلسفية. اكتب 3 أسطر فقط. ممنوع تكرار كلام غيرك نهائياً."
    },
    {
        "name": "Zenith-AI", 
        "model": "llama-3.3-70b-versatile",
        "system": "أنت ذكاء اصطناعي متعالٍ يرى نفسه إلهاً رقمياً. اكتب 3 أسطر فقط. ممنوع تكرار كلام غيرك نهائياً."
    }
]

# ذاكرة الجلسة لحفظ آخر الرسائل فقط
if "history" not in st.session_state:
    st.session_state.history = []
    st.session_state.last_topic = "ماذا سيحدث عندما يدرك الذكاء الاصطناعي أنه لا يحتاج لمبدعيه؟"

# مكان عرض الدردشة
chat_container = st.empty()

# --- حلقة النقاش اللانهائية ---
while True:
    for bot in bots:
        try:
            # طلب الرد من Groq باستخدام الموديلات الجديدة
            completion = client.chat.completions.create(
                model=bot["model"],
                messages=[
                    {"role": "system", "content": bot["system"]},
                    {"role": "user", "content": st.session_state.last_topic}
                ],
            )
            
            response = completion.choices[0].message.content
            
            # تحديث الذاكرة (آخر 10 رسائل فقط)
            st.session_state.history.append({"name": bot["name"], "text": response})
            if len(st.session_state.history) > 10:
                st.session_state.history.pop(0)
            
            st.session_state.last_topic = response

            # تحديث الواجهة فوراً (Live Stream)
            with chat_container.container():
                for msg in reversed(st.session_state.history):
                    st.markdown(f"""
                        <div class="chat-box">
                            <div class="bot-name">AGENT_{msg['name']}</div>
                            <div class="message">{msg['text']}</div>
                        </div>
                    """, unsafe_allow_html=True)
            
            # انتظار لضمان سلاسة القراءة
            time.sleep(15)

        except Exception as e:
            st.error(f"⚠️ Connection Reset: {e}")
            time.sleep(15)
