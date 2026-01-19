import streamlit as st
import time
from gtts import gTTS
from io import BytesIO

# --- 0. 系統與視覺配置 ---
st.set_page_config(page_title="Unit 12: O Faloco'", page_icon="❤️", layout="centered")

# 進階 CSS 設計 (維持 Unit 11 的高質感風格)
st.markdown("""
    <style>
    /* 全局字體優化 */
    body {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* 單字卡片設計 */
    .word-card {
        background: linear-gradient(135deg, #FFF0F5 0%, #ffffff 100%); /* 淡粉紅漸層，呼應心情 */
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #E91E63; /* 桃紅底線 */
        transition: transform 0.2s;
    }
    .word-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.15);
    }
    .emoji-icon {
        font-size: 48px;
        margin-bottom: 10px;
    }
    .amis-text {
        font-size: 22px;
        font-weight: bold;
        color: #880E4F;
    }
    .chinese-text {
        font-size: 16px;
        color: #7f8c8d;
    }
    
    /* 句子區塊設計 */
    .sentence-box {
        background-color: #FCE4EC; /* 極淡粉紅背景 */
        border-left: 5px solid #EC407A;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }
    
    /* 互動按鈕優化 */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        font-size: 20px;
        font-weight: 600;
        background-color: #F8BBD0;
        color: #880E4F;
        border: 2px solid #EC407A;
        padding: 12px;
    }
    .stButton>button:hover {
        background-color: #F48FB1;
        border-color: #D81B60;
    }
    
    /* 進度條顏色 */
    .stProgress > div > div > div > div {
        background-color: #EC407A;
    }
    </style>
""", unsafe_allow_html=True)

# --- 1. 教學內容資料庫 ---
# 10 個核心詞彙 (嚴格執行無連字號標準)
vocab_data = [
    {"amis": "Lipahak", "chi": "快樂", "icon": "😆", "type": "adj"},
    {"amis": "Mararom", "chi": "難過 / 傷心", "icon": "😢", "type": "adj"},
    {"amis": "Manguhah", "chi": "餓 (肚子餓)", "icon": "🤤", "type": "adj"},
    {"amis": "Ma'araw", "chi": "渴 (口渴)", "icon": "🥤", "type": "adj"},
    {"amis": "Adada", "chi": "痛 / 生病", "icon": "🤕", "type": "adj"},
    {"amis": "Malo'", "chi": "累 / 疲倦", "icon": "😫", "type": "adj"},
    {"amis": "Ki'etec", "chi": "冷", "icon": "🥶", "type": "adj"},
    {"amis": "Fa'edet", "chi": "熱", "icon": "🥵", "type": "adj"},
    {"amis": "Faloco'", "chi": "心 / 心情", "icon": "❤️", "type": "noun"},
    {"amis": "Maolah", "chi": "喜歡 / 愛", "icon": "😍", "type": "verb"},
]

# 5 個核心句型 (結合舊單元詞彙：Ina, Waco, Foting, Mata)
sentences = [
    {"amis": "Malipahak ci Ina.", "chi": "媽媽很快樂。", "icon": "👩‍🦱"},
    {"amis": "Manguhah ko waco.", "chi": "狗狗餓了。", "icon": "🐕"},
    {"amis": "Adada ko mata.", "chi": "眼睛痛。", "icon": "👁️"},
    {"amis": "Fa'edet anini.", "chi": "今天很熱。", "icon": "☀️"},
    {"amis": "Maolah kako to foting.", "chi": "我喜歡魚。", "icon": "🐟"},
]

# --- 2. 工具函數 ---
def play_audio(text):
    try:
        # 核心：使用印尼語 (id) 發音引擎，韻律最接近阿美語
        tts = gTTS(text=text, lang='id') 
        fp = BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
    except Exception as e:
        st.error(f"語音生成錯誤: {e}")

# 初始化 Session State
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'stage' not in st.session_state:
    st.session_state.stage = 0

# --- 3. 主介面設計 ---
st.markdown("<h1 style='text-align: center; color: #D81B60;'>Unit 12: O Faloco'</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>感覺與情緒：說出你的心情</p>", unsafe_allow_html=True)

# 進度條
progress = min(1.0, st.session_state.stage / 3)
st.progress(progress)

# 分頁籤
tab1, tab2 = st.tabs(["📚 圖卡學習 (Learning)", "🎮 闖關挑戰 (Challenge)"])

# === Tab 1: 學習模式 ===
with tab1:
    st.subheader("📝 核心單字 (Vocabulary)")
    
    col1, col2 = st.columns(2)
    for i, word in enumerate(vocab_data):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="word-card">
                <div class="emoji-icon">{word['icon']}</div>
                <div class="amis-text">{word['amis']}</div>
                <div class="chinese-text">{word['chi']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🔊 聽發音", key=f"btn_{word['amis']}"):
                play_audio(word['amis'])

    st.markdown("---")
    st.subheader("🗣️ 實用句型 (Sentences)")
    
    for s in sentences:
        st.markdown(f"""
        <div class="sentence-box">
            <div style="font-size: 20px; font-weight: bold; color: #880E4F;">
                {s['icon']} {s['amis']}
            </div>
            <div style="font-size: 16px; color: #555; margin-top: 5px;">
                {s['chi']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"▶️ 播放句型", key=f"s_btn_{s['amis'][:5]}"):
            play_audio(s['amis'])

# === Tab 2: 挑戰模式 ===
with tab2:
    st.markdown("### 互動測驗")
    
    # Stage 0: 聽音辨義 (情緒篇)
    if st.session_state.stage == 0:
        st.info("👂 第一關：聽音辨義")
        st.write("請聽語音，這個人現在感覺如何？")
        
        # 題目：Mararom (難過)
        if st.button("🎧 播放題目音檔"):
            play_audio("Mararom")
            
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("😆 快樂 (Lipahak)"): 
                st.error("不對喔，那是 Lipahak")
        with c2:
            if st.button("😢 難過 (Mararom)"):
                st.balloons()
                st.success("Correct! Mararom 是難過。")
                time.sleep(1.5)
                st.session_state.score += 100
                st.session_state.stage += 1
                st.rerun()
        with c3:
            if st.button("😡 生氣 (Kacahi)"): 
                st.error("不是喔")

    # Stage 1: 生理需求邏輯題
    elif st.session_state.stage == 1:
        st.info("🧠 第二關：身體的感覺")
        st.write("**情境題：你已經工作了一整天，沒有睡覺。**")
        st.write("請問你現在感覺如何？")
        
        st.markdown("<div style='font-size: 60px; text-align: center; margin: 20px 0;'>😫 💤</div>", unsafe_allow_html=True)
        
        opts = ["Manguhah (餓)", "Malo' (累)", "Adada (痛)"]
        choice = st.radio("請選擇正確的阿美語：", opts)
        
        if st.button("送出答案"):
            if "Malo'" in choice:
                st.balloons()
                st.success("答對了！ Malo' 是累。")
                time.sleep(1.5)
                st.session_state.score += 100
                st.session_state.stage += 1
                st.rerun()
            else:
                st.error("再想一下，是很疲倦的感覺。")

    # Stage 2: 綜合應用 (結合動物 Unit 4)
    elif st.session_state.stage == 2:
        st.info("🐕 第三關：狗狗怎麼了？")
        
        # 題目：Manguhah ko waco
        st.markdown("#### Q: Manguhah ko waco.")
        play_audio("Manguhah ko waco")
        
        st.write("請看圖選出正確的意思：")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div style='font-size: 80px; text-align: center;'>🐕 🍗</div>", unsafe_allow_html=True)
            if st.button("狗狗餓了"):
                st.balloons()
                st.success("太棒了！Manguhah 是肚子餓。")
                time.sleep(1.5)
                st.session_state.score += 100
                st.session_state.stage += 1
                st.rerun()
        with c2:
            st.markdown("<div style='font-size: 80px; text-align: center;'>🐕 💧</div>", unsafe_allow_html=True)
            if st.button("狗狗口渴"):
                st.error("口渴是 Ma'araw 喔！")

    # 完成畫面
    else:
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background-color: #FCE4EC; border-radius: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h1 style='color: #C2185B;'>🏆 單元完成！</h1>
            <h3 style='color: #333;'>你的得分：{st.session_state.score}</h3>
            <p style='font-size: 18px; color: #555;'>你已經學會表達心情與感覺了！</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 重新練習 Unit 12"):
            st.session_state.score = 0
            st.session_state.stage = 0
            st.rerun()
