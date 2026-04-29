import dotenv
dotenv.load_dotenv()

from decimal import Decimal
import streamlit as st
from streamlit_app.style import apply_style
from streamlit_app.utils import sync, get_raw_material_service
from src.domain.raw_material import RawMaterial

apply_style()
service = get_raw_material_service()

for key, val in [("rm_selected", None), ("rm_add", False)]:
    if key not in st.session_state:
        st.session_state[key] = val

hcol1, hcol2 = st.columns([4, 1])
with hcol1:
    st.title("Сырьё")
with hcol2:
    st.write("")
    if st.button("+ Добавить", type="primary", use_container_width=True):
        st.session_state.rm_add = True
        st.session_state.rm_selected = None

lcol, rcol = st.columns(2, gap="medium")

with lcol:
    with st.container(border=True):
        items = sync(service.get_materials())
        if not items:
            st.markdown("<p style='color:rgb(148,157,168)'>Нет записей</p>", unsafe_allow_html=True)
        for item in items:
            label = f"**{item.name}**\nКрит. остаток: {item.critical_amount} кг  ·  Срок: {item.shelf_life_days} дн."
            if st.button(label, key=f"rm_{item.id}", use_container_width=True):
                st.session_state.rm_selected = item.id
                st.session_state.rm_add = False
                st.rerun()

with rcol:
    with st.container(border=True):
        if st.session_state.rm_add:
            st.markdown("<div class='detail-label'>НОВАЯ ЗАПИСЬ</div>", unsafe_allow_html=True)
            with st.form("rm_add_form"):
                name = st.text_input("Наименование")
                critical = st.number_input("Критический остаток (кг)", min_value=0.0, step=0.1)
                shelf = st.number_input("Срок годности (дней)", min_value=1, step=1)
                if st.form_submit_button("Сохранить", type="primary") and name:
                    sync(service.create_material(
                        RawMaterial(name=name, critical_amount=Decimal(str(critical)), shelf_life_days=int(shelf))
                    ))
                    st.session_state.rm_add = False
                    st.rerun()

        elif st.session_state.rm_selected:
            item = next((i for i in sync(service.get_materials()) if i.id == st.session_state.rm_selected), None)
            if item:
                with st.form("rm_edit_form"):
                    name = st.text_input("Наименование", value=item.name)
                    critical = st.number_input("Критический остаток (кг)", min_value=0.0, step=0.1, value=float(item.critical_amount))
                    shelf = st.number_input("Срок годности (дней)", min_value=1, step=1, value=item.shelf_life_days)
                    col_save, col_del = st.columns(2)
                    with col_save:
                        if st.form_submit_button("Сохранить", type="primary"):
                            sync(service.update_material(
                                RawMaterial(id=item.id, name=name, critical_amount=Decimal(str(critical)), shelf_life_days=int(shelf))
                            ))
                            st.rerun()
                    with col_del:
                        if st.form_submit_button("Удалить"):
                            sync(service.delete_material(item.id))
                            st.session_state.rm_selected = None
                            st.rerun()
        else:
            st.markdown(
                "<p style='color:rgb(148,157,168);font-size:0.9rem;margin-top:0.5rem'>Выберите запись</p>",
                unsafe_allow_html=True,
            )
