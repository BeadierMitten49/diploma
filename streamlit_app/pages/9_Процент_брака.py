import dotenv
dotenv.load_dotenv()

from decimal import Decimal
import streamlit as st
from streamlit_app.style import apply_style
from streamlit_app.utils import sync, get_defect_rate_service
from src.domain.defect_rate import DefectRate

apply_style()
service = get_defect_rate_service()

st.title("Процент брака")

current = sync(service.get())

with st.container(border=True):
    if current:
        st.markdown(
            f"<div class='detail-label'>ТЕКУЩЕЕ ЗНАЧЕНИЕ</div>"
            f"<div class='detail-value'>{float(current.rate) * 100:.2f}%</div>",
            unsafe_allow_html=True,
        )
        with st.form("defect_form"):
            rate_pct = st.number_input("Процент брака (%)", min_value=0.0, max_value=100.0,
                                        step=0.1, value=float(current.rate) * 100)
            if st.form_submit_button("Сохранить", type="primary"):
                sync(service.update(DefectRate(id=current.id, rate=Decimal(str(rate_pct / 100)))))
                st.rerun()
    else:
        st.markdown("<p style='color:rgb(148,157,168)'>Значение не задано. Создайте запись через seed.</p>", unsafe_allow_html=True)
