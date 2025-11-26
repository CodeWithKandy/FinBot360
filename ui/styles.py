
"""
FinBot360 Pro - Premium Styles
"""

PREMIUM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    /* Global Reset & Font */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0E1117; 
    }
    ::-webkit-scrollbar-thumb {
        background: #262730; 
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #4F8BF9; 
    }

    /* Gradient Text */
    .gradient-text {
        background: linear-gradient(135deg, #4F8BF9 0%, #9B5DE5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 40px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }

    /* Metric Containers */
    [data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 16px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #4F8BF9 0%, #2D5BFF 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 10px;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(45, 91, 255, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(45, 91, 255, 0.5);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }

    /* Inputs */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        color: white;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4F8BF9;
        box-shadow: 0 0 0 1px #4F8BF9;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px;
        color: #FAFAFA;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background-color: transparent;
        color: #4F8BF9;
        border-bottom: 2px solid #4F8BF9;
    }

</style>
"""

def apply_styles():
    import streamlit as st
    st.markdown(PREMIUM_CSS, unsafe_allow_html=True)
