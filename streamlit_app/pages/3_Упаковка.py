import dotenv
dotenv.load_dotenv()

import streamlit as st
from streamlit_app.style import apply_style
from streamlit_app.utils import sync, get_package_service
from src.domain.package import Package

apply_style()
service = get_package_service()

for key, val in [("pkg_selected", None), ("pkg_add", False)]:
    if key not in st.session_state:
        st.session_state[key] = val

hcol1, hcol2 = st.columns([4, 1])
with hcol1:
    st.title("Упаковка")
with hcol2:
    st.write("")
    if st.button("+ Добавить", type="primary", use_container_width=True):
        st.session_state.pkg_add = True
        st.session_state.pkg_selected = None

lcol, rcol = st.columns(2, gap="medium")

with lcol:
    with st.container(border=True):
        items = sync(service.get_packages())
        if not items:
            st.markdown("<p style='color:rgb(148,157,168)'>Нет записей</p>", unsafe_allow_html=True)
        for item in items:
            label = f"**{item.name}**\nКрит. остаток: {item.critical_amount} шт."
            if st.button(label, key=f"pkg_{item.id}", use_container_width=True):
                st.session_state.pkg_selected = item.id
                st.session_state.pkg_add = False
                st.rerun()

with rcol:
    with st.container(border=True):
        if st.session_state.pkg_add:
            st.markdown("<div class='detail-label'>НОВАЯ ЗАПИСЬ</div>", unsafe_allow_html=True)
            with st.form("pkg_add_form"):
                name = st.text_input("Наименование")
                critical = st.number_input("Критический остаток (шт.)", min_value=0, step=1)
                if st.form_submit_button("Сохранить", type="primary") and name:
                    sync(service.create_package(Package(name=name, critical_amount=int(critical))))
                    st.session_state.pkg_add = False
                    st.rerun()

        elif st.session_state.pkg_selected:
            item = next((i for i in sync(service.get_packages()) if i.id == st.session_state.pkg_selected), None)
            if item:
                with st.form("pkg_edit_form"):
                    name = st.text_input("Наименование", value=item.name)
                    critical = st.number_input("Критический остаток (шт.)", min_value=0, step=1, value=item.critical_amount)
                    col_save, col_del = st.columns(2)
                    with col_save:
                        if st.form_submit_button("Сохранить", type="primary"):
                            sync(service.update_package(Package(id=item.id, name=name, critical_amount=int(critical))))
                            st.rerun()
                    with col_del:
                        if st.form_submit_button("Удалить"):
                            sync(service.delete_package(item.id))
                            st.session_state.pkg_selected = None
                            st.rerun()
        else:
            st.markdown("<p style='color:rgb(148,157,168);font-size:0.9rem'>Выберите запись</p>", unsafe_allow_html=True)
