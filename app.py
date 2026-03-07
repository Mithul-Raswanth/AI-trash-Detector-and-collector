import streamlit as st
import streamlit.components.v1 as components
import cv2
import time
import requests

# Import Sant's engine (which already connects to Mith's AI)
from sant_engine import get_processed_stream

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="ClearWater AI", layout="wide", initial_sidebar_state="collapsed")

# --- CUSTOM CSS FOR ARIAL FONT & CLEAN UI TRANSITIONS ---
st.markdown("""
    <style>
    /* Force Arial font globally */
    html, body, [class*="css"]  {
        font-family: 'Arial', sans-serif !important;
    }
    
    /* Make the tabs look like professional software buttons with transitions */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        padding-bottom: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        background-color: #1e1e1e;
        border-radius: 5px;
        color: white;
        transition: all 0.3s ease-in-out; /* Smooth transition effect */
        border: 1px solid #333;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #333;
        transform: translateY(-2px);
    }
    .stTabs [aria-selected="true"] {
        background-color: #00ccff !important;
        color: black !important;
        font-weight: bold;
        border: none;
        box-shadow: 0px 4px 10px rgba(0, 204, 255, 0.4);
    }
    
    /* Clean up the metric cards */
    div[data-testid="metric-container"] {
        background-color: #1e1e1e;
        border: 1px solid #333;
        padding: 15px;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR (Hardware Config hidden by default for clean look) ---
st.sidebar.title("⚙️ Hardware Link")
st.sidebar.info("Enter IPs from MO's microcontrollers.")
cam_ip = st.sidebar.text_input("Camera IP:", "192.168.43.101")
motor_ip = st.sidebar.text_input("Motor IP:", "192.168.43.102")

# --- CREATE THE 2 TABS ---
tab_home, tab_live = st.tabs(["🏠 HOME: Project Architecture", "🔴 GO LIVE: Command Center"])

# ==========================================
# TAB 1: HOME (Graphical & Self-Explanatory)
# ==========================================
with tab_home:
    st.title("🌊 ClearWater AI: Autonomous Marine Collector")
    st.markdown("An AI-Powered, IoT-Enabled Surface Cleansing Vessel designed to autonomously detect and collect marine macro-plastics.")
    st.markdown("---")
    
    # Graphical Flow using Columns and Info Boxes
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("### 1. The Eyes (IoT)\nAn **ESP32-CAM** streams real-time, low-latency video over a localized Wi-Fi mesh network directly from the bow of the catamaran.")
    with col2:
        st.warning("### 2. The Brain (AI)\nA **YOLOv8 Neural Network** processes the video frame-by-frame, distinguishing between hazardous synthetic trash and natural marine elements.")
    with col3:
        st.success("### 3. The Brawn (Robotics)\nA servo-actuated **Hydrodynamic Trapdoor** secures the debris, while differential thrust motors provide 360-degree maneuverability.")
        
    st.markdown("---")
    st.markdown("### 📊 System Workflow Architecture")
    
    # This acts as your visual diagram for the professor
    st.markdown("""
    > **[ ESP32 Camera ]** 📡 *(Wireless Video Stream)* ➡️ **[ YOLOv8 AI Core ]** 🧠 *(Bounding Box Detection)* ➡️ **[ Control Dashboard ]** 💻 *(Operator)* ➡️ 📡 *(Wireless HTTP Commands)* ➡️ **[ ESP32 Motor Controller ]** ⚙️ *(Actuates Propellers & Trapdoor)*
    """)



# ==========================================
# TAB 2: GO LIVE (Command Center)
# ==========================================
with tab_live:
    st.title("🔴 Live Command Center")
    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        st.subheader("Live AI Vision Feed")
        # Clean checkbox instead of clunky buttons
        run_camera = st.checkbox("🟢 Connect to ESP32-CAM & Initiate AI Scan")
        video_placeholder = st.empty()
        
        if run_camera:
            while run_camera:
                final_frame = get_processed_stream(cam_ip)
                if final_frame is not None:
                    final_frame_rgb = cv2.cvtColor(final_frame, cv2.COLOR_BGR2RGB)
                    video_placeholder.image(final_frame_rgb, channels="RGB", use_column_width=True)
                else:
                    video_placeholder.error("Connection Lost. Check IP or Hotspot.")
                time.sleep(0.05)
        else:
            video_placeholder.info("Camera offline. Check the box above to initiate the sequence.")

    with right_col:
        st.subheader("⚙️ Collection Trap")
        c_open, c_close = st.columns(2)
        with c_open:
            if st.button("🔓 Open Trap", use_container_width=True):
                try: requests.get(f"http://{motor_ip}/open", timeout=1)
                except: pass
        with c_close:
            if st.button("🔒 Close Trap", use_container_width=True):
                try: requests.get(f"http://{motor_ip}/close", timeout=1)
                except: pass
        
        st.markdown("---")
        st.subheader("🕹️ Navigation")
        # Direct JavaScript Joystick Injection
        joystick_html = f"""
        <!DOCTYPE html>
        <html>
        <head><script src="https://cdnjs.cloudflare.com/ajax/libs/nipplejs/0.10.0/nipplejs.min.js"></script></head>
        <body style="background-color: transparent;">
            <div id="joystick" style="width: 100%; height: 200px;"></div>
            <script>
                var manager = nipplejs.create({{ zone: document.getElementById('joystick'), color: '#00ccff' }});
                manager.on('dir:up', function () {{ fetch("http://{motor_ip}/forward", {{mode: 'no-cors'}}); }});
                manager.on('dir:down', function () {{ fetch("http://{motor_ip}/backward", {{mode: 'no-cors'}}); }});
                manager.on('dir:left', function () {{ fetch("http://{motor_ip}/left", {{mode: 'no-cors'}}); }});
                manager.on('dir:right', function () {{ fetch("http://{motor_ip}/right", {{mode: 'no-cors'}}); }});
                manager.on('end', function () {{ fetch("http://{motor_ip}/stop", {{mode: 'no-cors'}}); }});
            </script>
        </body>
        </html>
        """
        components.html(joystick_html, height=250)
