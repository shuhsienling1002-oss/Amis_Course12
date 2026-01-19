import streamlit as st
import time
from gtts import gTTS
from io import BytesIO

# --- 0. 系統與視覺配置 ---
st.set_page_config(page_title="Unit 12: O Faloco'", page_icon="❤️", layout="centered")

# CSS 設計 (保持高質感，無連字號風格)
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    
    /* 來源標籤樣式 */
    .source-tag {
        font-size: 12px;
        color: #aaa;
        text-align: right;
        font-style: italic;
        margin-top: 4px;
    }
    
    /* 單字卡片 */
    .word-card {
        background: linear-gradient(135deg, #FFF0F5 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #E91E63;
        transition: transform 0.2s;
    }
    .word-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.15);
    }
    
    /* 文字樣式 */
    .emoji-icon { font-size: 48px; margin-bottom: 10px; }
    .amis-text { font-size: 22px; font-weight: bold; color: #880E4F; }
    .chinese-text { font-size: 16px; color: #7f8c8d; }
    
    /* 按鈕樣式 */
    .stButton>button {
        width: 100%; border-radius: 12px; font-size: 20px; font-weight: 600;
        background-color: #F8BBD0; color: #880E4F; border: 2px solid #EC407A; padding: 12px;
    }
    .stButton>button:hover { background-color: #F48FB1; border-color: #D81B60; }
    
    /* 進度條 */
    .stProgress > div > div > div > div { background-color: #EC407A; }
    </style>
""", unsafe_allow_html=True)

# --- 1. 資料庫 (Strictly from data.csv & No Hyphens) ---
# 來源：您的 data.csv 檔案
# 處理：手動移除 csv 原始資料中的連字號 "-"
vocab_data = [
    {"amis": "Mararom", "chi": "難過", "icon": "😢", "source": "Row 243"},
    {"amis": "Macahiw", "chi": "餓", "icon": "🤤", "source": "Row 363"},
    {"amis": "Si'enaw", "chi": "冷 (天氣)", "icon": "🥶", "source": "Row 255"},
    {"amis": "Fa'edet", "chi": "熱", "icon": "🥵", "source": "Row 538"},
    {"amis": "Adada", "chi": "痛 / 生病", "icon": "🤕", "source": "Row 273"},
    {"amis": "Karoray", "chi": "累 (常用否定 caay karoray)", "icon": "😫", "source": "Row 245"},
    {"amis": "Maolah", "chi": "喜歡 / 愛", "icon": "😍", "source": "Row 18"},
    {"amis": "Matawa", "chi": "笑", "icon": "😆", "source": "Row 5"},
    {"amis": "Mafana'", "chi": "知道", "icon": "💡", "source": "Row 6"},
    {"amis": "Maketer", "chi": "生氣", "icon": "😡", "source": "Row 1514"},
]

# 句子資料庫 (Strictly from data.csv & No Hyphens)
# 注意：ci-mama-an 改為 ci mama an，符合無連字號書寫習慣
sentences = [
    {"amis": "Mararom kako.", "chi": "我難過。", "icon": "😢", "source": "Row 243"},
    {"amis": "Macahiw kako.", "chi": "我餓了。", "icon": "🤤", "source": "Row 363 (改寫)"},
    {"amis": "Si'enaw ko romi'ad.", "chi": "天氣冷。", "icon": "🥶", "source": "Row 255"},
    {"amis": "Maolah kako ci mama an.", "chi": "我喜歡爸爸。", "icon": "😍", "source": "Row 207"},
    {"amis": "Matawa ci Panay takowanan.", "chi": "Panay 笑我。", "icon": "😆", "source": "Row 5"},
]

# --- 2. 工具函數 ---
def play_audio(text):
    try:
        # 使用印尼語 (id) 發音，接近阿美語韻律
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
    except:
        st.error("語音生成暫時無法使用")

# 初始化 Session
if 'score' not in st.session_state: st.session_state.score = 0
if 'stage' not in st.session_state: st.session_state.stage = 0

# --- 3. 主介面 ---
st.markdown("<h1 style='text-align: center; color: #D81B60;'>Unit 12: O Faloco'</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>感覺與情緒 (來源：data.csv)</p>", unsafe_allow_html=True)

progress = min(1.0, st.session_state.stage / 3)
st.progress(progress)

tab1, tab2 = st.tabs(["📚 詞彙學習 (Learning)", "🎮 闖關挑戰 (Challenge)"])

# === Tab 1: 學習模式 ===
with tab1:
    st.subheader("📝 核心單字 (無連字號)")
    col1, col2 = st.columns(2)
    for i, word in enumerate(vocab_data):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="word-card">
                <div class="emoji-icon">{word['icon']}</div>
                <div class="amis-text">{word['amis']}</div>
                <div class="chinese-text">{word['chi']}</div>
                <div class="source-tag">src: {word['source']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔊 聽發音", key=f"btn_{word['amis']}"):
                play_audio(word['amis'])

    st.markdown("---")
    st.subheader("🗣️ 實用句型")
    for s in sentences:
        st.markdown(f"""
        <div style="background-color: #FCE4EC; border-left: 5px solid #EC407A; padding: 15px; margin: 10px 0; border-radius: 0 10px 10px 0;">
            <div style="font-size: 20px; font-weight: bold; color: #880E4F;">{s['icon']} {s['amis']}</div>
            <div style="font-size: 16px; color: #555; margin-top: 5px;">{s['chi']}</div>
            <div class="source-tag">src: {s['source']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"▶️ 播放句型", key=f"s_btn_{s['amis'][:5]}"):
            play_audio(s['amis'])

# === Tab 2: 挑戰模式 ===
with tab2:
    st.markdown("### 互動測驗")
    
    # Stage 0: 聽力 (Mararom) - Row 243
    if st.session_state.stage == 0:
        st.info("👂 Q1: 聽音辨義")
        st.write("請聽：**Mararom kako**")
        if st.button("🎧 播放題目"): play_audio("Mararom kako")
            
        c1, c2 = st.columns(2)
        with c1:
            if st.button("😢 我很難過"):
                st.balloons()
                st.success("答對了！Mararom (難過) - src: Row 243")
                time.sleep(1.5)
                st.session_state.score += 100
                st.session_state.stage += 1
                st.rerun()
        with c2:
            if st.button("😆 我很快樂"): st.error("不對喔，Mararom 是難過")

    # Stage 1: 狀態判斷 (Macahiw) - Row 363
    elif st.session_state.stage == 1:
        st.info("🤤 Q2: 生理需求")
        st.write("想吃飯的時候，你會說什麼？")
        st.markdown("<div style='font-size: 60px; text-align: center;'>🍚 🥢</div>", unsafe_allow_html=True)
        
        # 選項中也確保無連字號
        opts = ["Macahiw kako (我餓了)", "Si'enaw kako (我冷)"]
        choice = st.radio("請選擇 (Based on Row 363)：", opts)
        
        if st.button("送出答案"):
            if "Macahiw" in choice:
                st.balloons()
                st.success("正確！Macahiw kako.")
                time.sleep(1.5)
                st.session_state.score += 100
                st.session_state.stage += 1
                st.rerun()
            else: st.error("Si'enaw 是冷喔 (Row 255)！")

    # Stage 2: 句型重組 (Maolah) - Row 207
    elif st.session_state.stage == 2:
        st.info("😍 Q3: 表達愛意")
        st.write("如何用阿美語說：**「我喜歡爸爸」**？")
        st.caption("提示：Maolah (喜歡)")
        
        st.markdown("<div style='font-size: 60px; text-align: center;'>👨‍👧</div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            # 確保無連字號書寫：ci mama an
            if st.button("Maolah kako ci mama an"):
                st.balloons()
                st.success("太棒了！(src: Row 207)")
                time.sleep(1.5)
                st.session_state.score += 100
                st.session_state.stage += 1
                st.rerun()
        with c2:
            if st.button("Maketer kako ci mama an"): 
                st.error("Maketer 是生氣喔 (Row 1514)！不要生氣爸爸！")

    else:
        st.success(f"🏆 挑戰完成！總分：{st.session_state.score}")
        if st.button("重玩"):
            st.session_state.score = 0
            st.session_state.stage = 0
            st.rerun()
