import dotenv
dotenv.load_dotenv()

from decimal import Decimal
from datetime import date
import streamlit as st
from streamlit_app.style import apply_style
from streamlit_app.utils import sync, get_raw_material_service
from src.domain.raw_material import RawMaterialStock

apply_style()
service = get_raw_material_service()

for key, val in [("rms_selected", None), ("rms_add", False)]:
    if key not in st.session_state:
        st.session_state[key] = val

hcol1, hcol2 = st.columns([4, 1])
with hcol1:
    st.title("Склад сырья")
with hcol2:
    st.write("")
    if st.button("+ Добавить", type="primary", use_container_width=True):
        st.session_state.rms_add = True
        st.session_state.rms_selected = None

lcol, rcol = st.columns(2, gap="medium")

with lcol:
    with st.container(border=True):
        items = sync(service.get_stock())
        if not items:
            st.markdown("<p style='color:rgb(148,157,168)'>Нет записей</p>", unsafe_allow_html=True)
        for item in items:
            warn = " 🔴" if item.is_critical or item.is_expired else ""
            label = f"**{item.raw_material.name}**{warn}\n{item.amount_kg} кг  ·  до {item.expiry_date}"
            if st.button(label, key=f"rms_{item.id}", use_container_width=True):
                st.session_state.rms_selected = item.id
                st.session_state.rms_add = False
                st.rerun()

with rcol:
    with st.container(border=True):
        materials = sync(service.get_materials())
        material_map = {m.name: m for m in materials}

        if st.session_state.rms_add:
            st.markdown("<div class='detail-label'>НОВАЯ ЗАПИСЬ</div>", unsafe_allow_html=True)
            with st.form("rms_add_form"):
                mat_name = st.selectbox("Сырьё", list(material_map.keys()))
                amount = st.number_input("Количество (кг)", min_value=0.0, step=0.1)
                arrival = st.date_input("Дата поступления", value=date.today())
                comment = st.text_input("Комментарий")
                if st.form_submit_button("Сохранить", type="primary") and mat_name:
                    sync(service.create_stock_item(RawMaterialStock(
                        raw_material=material_map[mat_name],
                        amount_kg=Decimal(str(amount)),
                        arrival_date=arrival,
                        comment=comment,
                    )))
                    st.session_state.rms_add = False
                    st.rerun()

        elif st.session_state.rms_selected:
            item = next((i for i in sync(service.get_stock()) if i.id == st.session_state.rms_selected), None)
            if item:
                st.markdown(f"""
<div class='detail-label'>СРОК ГОДНОСТИ</div>
<div class='detail-value'>{'⚠️ Истёк' if item.is_expired else item.expiry_date}</div>
<div class='detail-label'>ОСТАТОК</div>
<div class='detail-value'>{'⚠️ Критический' if item.is_critical else 'В норме'}</div>
""", unsafe_allow_html=True)
                with st.form("rms_edit_form"):
                    mat_name = st.selectbox("Сырьё", list(material_map.keys()), index=list(material_map.keys()).index(item.raw_material.name))
                    amount = st.number_input("Количество (кг)", min_value=0.0, step=0.1, value=float(item.amount_kg))
                    arrival = st.date_input("Дата поступления", value=item.arrival_date)
                    comment = st.text_input("Комментарий", value=item.comment)
                    col_save, col_del = st.columns(2)
                    with col_save:
                        if st.form_submit_button("Сохранить", type="primary"):
                            sync(service.update_stock_item(RawMaterialStock(
                                id=item.id,
                                raw_material=material_map[mat_name],
                                amount_kg=Decimal(str(amount)),
                                arrival_date=arrival,
                                comment=comment,
                            )))
                            st.rerun()
                    with col_del:
                        if st.form_submit_button("Удалить"):
                            sync(service.delete_stock_item(item.id))
                            st.session_state.rms_selected = None
                            st.rerun()
        else:
            st.markdown("<p style='color:rgb(148,157,168);font-size:0.9rem'>Выберите запись</p>", unsafe_allow_html=True)
