import streamlit as st
import streamlit.components.v1 as components
import cv2
import time
import requests

from sant_engine import get_processed_stream

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="ClearWater AI", layout="wide", initial_sidebar_state="collapsed")

# --- HIGH-CONTRAST APPLE CSS ---
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", Arial, sans-serif !important;
        background-color: #FFFFFF !important; 
        color: #000000 !important;
    }
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .main { animation: slideUp 0.6s ease-out; }
    .stTabs [data-baseweb="tab-list"] {
        background-color: #F2F2F7;
        border-radius: 12px;
        padding: 5px;
        margin-bottom: 2rem;
        display: flex;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        color: #636366;
        padding: 8px 40px;
        transition: 0.2s ease-in-out;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0071E3 !important; 
        color: #FFFFFF !important;
        box-shadow: 0px 4px 12px rgba(0, 113, 227, 0.3) !important;
    }
    .stButton>button {
        width: 100%;
        background-color: #000000 !important; 
        color: #FFFFFF !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: 600 !important;
        height: 3.5em !important;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #333333 !important; transform: translateY(-2px); }
    .main-title { font-size: 52px; font-weight: 800; letter-spacing: -1.5px; text-align: center; margin-top: -20px; }
    </style>
""", unsafe_allow_html=True)

# --- GLOBAL HARDWARE CONFIG ---
st.sidebar.title("Hardware Link")
cam_ip = st.sidebar.text_input("Camera Core IP:", "192.168.43.101")
motor_ip = st.sidebar.text_input("Drive System IP:", "192.168.43.102")

# --- HEADER ---
st.markdown('<p class="main-title">ClearWater.</p>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #86868B; font-size: 20px;'>Autonomous Marine Waste Intelligence</p><br>", unsafe_allow_html=True)

# --- 2 TABS ---
tab_home, tab_live = st.tabs(["Overview", "Live Command"])

with tab_home:
    st.markdown("### Project Architecture")
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Optical Array", value="ESP32-CAM", delta="Live Stream")
    col2.metric(label="AI Vision", value="YOLOv8n", delta="98% Acc")
    col3.metric(label="Propulsion", value="Differential", delta="360° Turn")
        
    st.markdown("---")
    st.markdown("""
    ### 🌊 Purpose-Built for Conservation
    ClearWater AI is an autonomous catamaran designed to bridge the gap between computer vision and environmental robotics. 
    By processing video feeds on a localized neural network, the vessel identifies synthetic debris and actuates its collection trap with millisecond precision.
    """)

with tab_live:
    left_col, right_col = st.columns([2, 1])
    with left_col:
        st.markdown("### Neural Vision Feed")
        run_camera = st.checkbox("🟢 Initialize Vision Protocol")
        video_placeholder = st.empty()
        
        if run_camera:
            while run_camera:
                final_frame = get_processed_stream(cam_ip)
                if final_frame is not None:
                    final_frame_rgb = cv2.cvtColor(final_frame, cv2.COLOR_BGR2RGB)
                    video_placeholder.image(final_frame_rgb, use_column_width=True)
                else:
                    video_placeholder.error("Searching for Optical Stream... Check Hardware IP.")
                time.sleep(0.05)
        else:
            video_placeholder.info("Vision Core in Standby.")

    with right_col:
        st.markdown("### Collection Bay")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔓 OPEN GATE"):
                try: requests.get(f"http://{motor_ip}/open", timeout=0.5)
                except: pass
        with c2:
            if st.button("🔒 CLOSE GATE"):
                try: requests.get(f"http://{motor_ip}/close", timeout=0.5)
                except: pass
        
        st.markdown("<br>### Navigational Logic", unsafe_allow_html=True)
        joystick_html = f"""
        <script src="https://cdnjs.cloudflare.com/ajax/libs/nipplejs/0.10.0/nipplejs.min.js"></script>
        <div id="joystick" style="width: 100%; height: 200px; background: #F2F2F7; border-radius: 20px;"></div>
        <script>
            var manager = nipplejs.create({{ zone: document.getElementById('joystick'), color: '#0071E3', mode: 'static', position: {{left: '50%', top: '50%'}} }});
            manager.on('dir:up', function () {{ fetch("http://{motor_ip}/forward", {{mode: 'no-cors'}}); }});
            manager.on('dir:down', function () {{ fetch("http://{motor_ip}/backward", {{mode: 'no-cors'}}); }});
            manager.on('dir:left', function () {{ fetch("http://{motor_ip}/left", {{mode: 'no-cors'}}); }});
            manager.on('dir:right', function () {{ fetch("http://{motor_ip}/right", {{mode: 'no-cors'}}); }});
            manager.on('end', function () {{ fetch("http://{motor_ip}/stop", {{mode: 'no-cors'}}); }});
        </script>
        """
        components.html(joystick_html, height=220)


# ==========================================
# FOOTER (Team Credits)
# ==========================================
st.markdown("""
    <hr style='border: none; border-top: 1px solid #E5E5EA; margin-top: 60px; margin-bottom: 20px;'>
    <p style='text-align: center; color: #86868B; font-size: 14px; font-weight: 500; font-family: -apple-system, BlinkMacSystemFont, sans-serif;'>
        Engineered for the elements by<br>
        <span style='color: #000000; font-size: 16px; font-weight: 600;'>
            Akshadha • Krishna Priya • Mithul Raswanth • Mohit • Santosh Kamaraj
        </span>
    </p>
""", unsafe_allow_html=True)
