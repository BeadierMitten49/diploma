import sys
from pathlib import Path
_root = str(Path(__file__).parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

import dotenv
dotenv.load_dotenv()

import streamlit as st
from streamlit_app.style import apply_style
import src.infrastructure.database.models  # регистрирует все ORM модели в metadata
from src.infrastructure.database.database_setup import init_db

init_db()
apply_style()

st.title("Складской учёт")
st.markdown(
    "<p style='color:rgb(148,157,168);margin-top:0.5rem'>"
    "Выберите раздел в боковом меню</p>",
    unsafe_allow_html=True,
)
