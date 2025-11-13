import streamlit as st
from team.dsa_team import get_dsa_team_and_docker
from config.docker_utils import start_docker_container, stop_docker_container
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult
import asyncio

# Page configuration
st.set_page_config(
    page_title="AlgoBot - DSA Solver",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for liquid glass effect with white-to-blue gradient
st.markdown("""
    <style>
    /* Animated gradient background - White to Blue theme */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stApp {
        background: linear-gradient(-45deg, #ffffff, #e0f2fe, #bae6fd, #7dd3fc, #38bdf8, #0ea5e9);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        background-attachment: fixed;
    }
    
    /* Liquid Glass Effect Base */
    .glass-effect {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(59, 130, 246, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    /* Shimmering effect overlay */
    .glass-effect::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.3),
            transparent
        );
        transition: left 0.5s;
    }
    
    .glass-effect:hover::before {
        left: 100%;
    }
    
    /* Header styling with glass effect */
    .main-header {
        text-align: center;
        padding: 3rem 2rem;
        margin: 2rem auto;
        max-width: 900px;
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(25px) saturate(200%);
        -webkit-backdrop-filter: blur(25px) saturate(200%);
        border-radius: 25px;
        border: 2px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 8px 32px 0 rgba(59, 130, 246, 0.3),
                    inset 0 0 20px rgba(255, 255, 255, 0.2);
    }
    
    .main-header h1 {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 50%, #1e40af 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        filter: drop-shadow(2px 2px 4px rgba(59, 130, 246, 0.3));
    }
    
    .main-header p {
        font-size: 1.3rem;
        color: #1e40af;
        font-weight: 500;
        text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.5);
    }
    
    /* Input container with liquid glass */
    .input-container {
        background: rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(30px) saturate(180%);
        -webkit-backdrop-filter: blur(30px) saturate(180%);
        border-radius: 25px;
        padding: 2.5rem;
        box-shadow: 0 8px 32px 0 rgba(59, 130, 246, 0.25),
                    inset 0 0 30px rgba(255, 255, 255, 0.2);
        margin: 2rem auto;
        max-width: 900px;
        border: 2px solid rgba(255, 255, 255, 0.5);
        position: relative;
        overflow: hidden;
    }
    
    .input-container::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(59, 130, 246, 0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Label styling */
    .stTextInput > label {
        color: #1e40af !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        text-shadow: 0px 0px 10px rgba(255, 255, 255, 0.8);
        position: relative;
        z-index: 1;
    }
    
    /* Streamlit input field with glass effect and dark grey text */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
        border-radius: 15px !important;
        border: 2px solid rgba(59, 130, 246, 0.3) !important;
        padding: 1rem 1.5rem !important;
        font-size: 1.05rem !important;
        color: #1e293b !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        box-shadow: inset 0 2px 10px rgba(59, 130, 246, 0.05) !important;
        position: relative;
        z-index: 1;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #64748b !important;
        font-weight: 400 !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2),
                    inset 0 2px 10px rgba(59, 130, 246, 0.1) !important;
        background: rgba(255, 255, 255, 0.95) !important;
        color: #0f172a !important;
    }
    
    /* Button with liquid glass effect */
    .stButton > button {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.3), rgba(14, 165, 233, 0.3)) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        color: #1e40af !important;
        border: 2px solid rgba(59, 130, 246, 0.5) !important;
        border-radius: 15px !important;
        padding: 1rem 3rem !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        cursor: pointer !important;
        transition: all 0.4s ease !important;
        box-shadow: 0 8px 32px 0 rgba(59, 130, 246, 0.3),
                    inset 0 0 20px rgba(255, 255, 255, 0.2) !important;
        width: 100%;
        position: relative;
        z-index: 1;
        text-shadow: 0px 0px 10px rgba(255, 255, 255, 0.8);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 12px 40px 0 rgba(59, 130, 246, 0.4),
                    inset 0 0 30px rgba(255, 255, 255, 0.3) !important;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.4), rgba(14, 165, 233, 0.4)) !important;
        border-color: rgba(59, 130, 246, 0.7) !important;
        color: #1e3a8a !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(0.98) !important;
    }
    
    /* Feature cards with liquid glass */
    .feature-card {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(25px) saturate(180%);
        -webkit-backdrop-filter: blur(25px) saturate(180%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 8px 32px 0 rgba(59, 130, 246, 0.25),
                    inset 0 0 20px rgba(255, 255, 255, 0.2);
        border: 2px solid rgba(255, 255, 255, 0.4);
        transition: all 0.4s ease;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at top left, rgba(59, 130, 246, 0.2), transparent);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-10px) scale(1.03);
        box-shadow: 0 15px 50px 0 rgba(59, 130, 246, 0.35),
                    inset 0 0 30px rgba(255, 255, 255, 0.3);
        border-color: rgba(59, 130, 246, 0.5);
    }
    
    .feature-card:hover::before {
        opacity: 1;
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        filter: drop-shadow(2px 2px 8px rgba(59, 130, 246, 0.3));
    }
    
    .feature-card h3 {
        color: #1e40af;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.8);
    }
    
    .feature-card p {
        color: #1e3a8a;
        font-size: 1rem;
        line-height: 1.6;
        text-shadow: 0px 0px 5px rgba(255, 255, 255, 0.5);
    }
    
    /* Chat message with liquid glass */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.3) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        border-radius: 18px !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        box-shadow: 0 8px 32px 0 rgba(59, 130, 246, 0.25),
                    inset 0 0 20px rgba(255, 255, 255, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
    }
    
    /* Success/Info boxes with glass effect */
    .stSuccess, .stInfo {
        background: rgba(255, 255, 255, 0.3) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        border-radius: 15px !important;
        border: 2px solid rgba(59, 130, 246, 0.4) !important;
        box-shadow: 0 8px 32px 0 rgba(59, 130, 246, 0.3) !important;
        color: #1e40af !important;
    }
    
    /* Spinner container */
    .stSpinner > div {
        background: rgba(255, 255, 255, 0.3) !important;
        backdrop-filter: blur(15px) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
    }
    
    /* Loading animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .loading {
        animation: pulse 2s ease-in-out infinite;
    }
    
    /* Footer with glass effect */
    .footer-glass {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.4);
        box-shadow: 0 8px 32px 0 rgba(59, 130, 246, 0.25);
        padding: 2rem;
        margin: 3rem auto 2rem;
        max-width: 900px;
        text-align: center;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Markdown text in chat */
    .stChatMessage p, .stChatMessage div {
        color: #1e293b !important;
        text-shadow: 0px 0px 3px rgba(255, 255, 255, 0.8);
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="main-header">
        <h1>🤖 AlgoBot</h1>
        <p>Your AI-Powered DSA Problem Solver</p>
    </div>
""", unsafe_allow_html=True)

# Feature cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <h3>Fast Solutions</h3>
            <p>Get instant solutions to complex DSA problems</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h3>Accurate Code</h3>
            <p>Well-tested and optimized algorithms</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📚</div>
            <h3>Learn & Grow</h3>
            <p>Understand the logic behind solutions</p>
        </div>
    """, unsafe_allow_html=True)

# Main input area
st.markdown('<div class="input-container">', unsafe_allow_html=True)

task = st.text_input(
    "Enter your DSA problem or question:",
    value='Write a function to add two numbers',
    placeholder="e.g., Implement binary search in Python...",
    label_visibility="visible"
)

run_button = st.button("🚀 Solve Problem")

st.markdown('</div>', unsafe_allow_html=True)

async def run(team, docker, task):
    try:
        await start_docker_container(docker)
        async for message in team.run_stream(task=task):
            if isinstance(message, TextMessage):
                print(msg := f"{message.source} : {message.content}")
                yield msg
            elif isinstance(message, TaskResult):
                print(msg := f"Stop Reason: {message.stop_reason}")
                yield msg
        print("Task Completed")
    except Exception as e:
        print(f"Error: {e}")
        yield f"Error: {e}"
    finally:
        await stop_docker_container(docker)

if run_button:
    # Create a container for chat messages
    chat_container = st.container()
    
    with chat_container:
        st.markdown('<div class="loading">', unsafe_allow_html=True)
        with st.spinner('🔄 Processing your request...'):
            st.markdown('</div>', unsafe_allow_html=True)
            
            team, docker = get_dsa_team_and_docker()

            async def collect_messages():
                async for msg in run(team, docker, task):
                    if isinstance(msg, str):
                        if msg.startswith("user"):
                            with st.chat_message('user', avatar='👤'):
                                st.markdown(msg)
                        elif msg.startswith('DSA_Problem_Solver_Agent'):
                            with st.chat_message('assistant', avatar='🧑‍💻'):
                                st.markdown(msg)
                        elif msg.startswith('CodeExecutorAgent'):
                            with st.chat_message('assistant', avatar='🤖'):
                                st.markdown(msg)
                    elif isinstance(msg, TaskResult):
                        with st.chat_message('assistant', avatar='✅'):
                            st.success(f"✨ Task Completed Successfully!")
                            st.markdown(f"**Result:** {msg.stop_reason}")

            asyncio.run(collect_messages())

# Footer
st.markdown("""
    <div class="footer-glass">
        <p style="font-size: 1rem; color: #1e40af; margin: 0; text-shadow: 0px 0px 5px rgba(255, 255, 255, 0.8); font-weight: 600;">
            Powered by Autogen • Built with ❤️ by Ishant • © 2025 AlgoBot
        </p>
    </div>
""", unsafe_allow_html=True)