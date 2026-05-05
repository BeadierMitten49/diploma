import sys
from pathlib import Path

_root = str(Path(__file__).parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');

*, body, p, span, div, label, button {
    font-family: 'Montserrat', Arial, sans-serif !important;
}

[data-testid="stAppViewContainer"],
[data-testid="stHeader"] { background: rgb(244, 245, 249) !important; }

.block-container { padding: 2rem 3rem !important; max-width: 1100px !important; }

h1 { font-size: 2rem !important; font-weight: 700 !important; color: #000 !important; margin-bottom: 0 !important; }

[data-testid="stButton"] > button[kind="primary"] {
    background: rgb(255, 91, 0) !important; color: #fff !important;
    border: none !important; border-radius: 50px !important;
    font-weight: 600 !important; font-size: 0.9rem !important;
    white-space: nowrap !important; padding: 10px 20px !important;
    box-shadow: none !important;
}
[data-testid="stButton"] > button[kind="primary"]:hover { background: rgb(220, 75, 0) !important; }

[data-testid="stVerticalBlockBorderWrapper"] > div {
    background: rgb(255, 255, 255) !important;
    border-radius: 20px !important;
    border: 1px solid rgb(237, 237, 237) !important;
    box-shadow: rgba(56, 56, 56, 0.08) 0px 2px 8px !important;
    padding: 1.2rem 1.4rem !important;
}

[data-testid="stButton"] > button[kind="secondary"] {
    border: none !important; border-radius: 0 !important;
    background: transparent !important; text-align: left !important;
    padding: 10px 2px 10px 0 !important; width: 100% !important;
    justify-content: flex-start !important; box-shadow: none !important;
    border-bottom: 1px solid rgb(237,237,237) !important;
}
[data-testid="stButton"] > button[kind="secondary"]:hover {
    background: rgb(250,250,252) !important; border-radius: 6px !important;
}
[data-testid="stButton"] > button[kind="secondary"] > div,
[data-testid="stButton"] > button[kind="secondary"] > div > span {
    align-items: flex-start !important; justify-content: flex-start !important;
    text-align: left !important; width: 100% !important;
}
[data-testid="stButton"] > button[kind="secondary"] p {
    font-size: 0.72rem !important; color: rgb(148, 157, 168) !important;
    font-weight: 500 !important; margin: 0 !important;
}
[data-testid="stButton"] > button[kind="secondary"] p strong {
    font-size: 1.0rem !important; color: #000 !important;
    font-weight: 500 !important; display: block !important;
}

.detail-label { font-size: 0.68rem; color: rgb(148,157,168); margin-bottom: 3px;
    text-transform: uppercase; letter-spacing: 0.06em; font-weight: 600; }
.detail-value { font-size: 0.97rem; font-weight: 500; color: #000; margin-bottom: 14px; }

.badge { display: inline-block; border-radius: 50px; padding: 3px 12px;
    font-size: 0.75rem; font-weight: 600; white-space: nowrap; }
.badge-warn        { background: rgb(255,235,232); color: rgb(229,52,26); }
.badge-ok          { background: rgb(238,255,230); color: rgb(56,180,28); }
.badge-pending     { background: rgb(240,240,243); color: rgb(100,100,110); }
.badge-in-progress { background: rgb(227,243,254); color: rgb(27,143,227); }
.badge-stopped     { background: rgb(255,245,220); color: rgb(200,140,0); }
.badge-completed   { background: rgb(238,255,230); color: rgb(56,180,28); }

[data-testid="stToolbar"] { display: none !important; }
[data-testid="stVerticalBlock"] > div { gap: 0 !important; }
[data-testid="stHorizontalBlock"] > div { gap: 4px !important; }
</style>
"""


def apply_style():
    st.markdown(CSS, unsafe_allow_html=True)
