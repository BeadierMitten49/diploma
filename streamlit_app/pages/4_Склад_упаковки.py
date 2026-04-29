import dotenv
dotenv.load_dotenv()

import streamlit as st
from streamlit_app.style import apply_style
from streamlit_app.utils import sync, get_package_service
from src.domain.package import PackageStock

apply_style()
service = get_package_service()

for key, val in [("pkgs_selected", None), ("pkgs_add", False)]:
    if key not in st.session_state:
        st.session_state[key] = val

hcol1, hcol2 = st.columns([4, 1])
with hcol1:
    st.title("Склад упаковки")
with hcol2:
    st.write("")
    if st.button("+ Добавить", type="primary", use_container_width=True):
        st.session_state.pkgs_add = True
        st.session_state.pkgs_selected = None

lcol, rcol = st.columns(2, gap="medium")

with lcol:
    with st.container(border=True):
        items = sync(service.get_stock())
        if not items:
            st.markdown("<p style='color:rgb(148,157,168)'>Нет записей</p>", unsafe_allow_html=True)
        for item in items:
            warn = " 🔴" if item.is_critical else ""
            label = f"**{item.package.name}**{warn}\n{item.amount} шт."
            if st.button(label, key=f"pkgs_{item.id}", use_container_width=True):
                st.session_state.pkgs_selected = item.id
                st.session_state.pkgs_add = False
                st.rerun()

with rcol:
    with st.container(border=True):
        packages = sync(service.get_packages())
        package_map = {p.name: p for p in packages}

        if st.session_state.pkgs_add:
            st.markdown("<div class='detail-label'>НОВАЯ ЗАПИСЬ</div>", unsafe_allow_html=True)
            with st.form("pkgs_add_form"):
                pkg_name = st.selectbox("Упаковка", list(package_map.keys()))
                amount = st.number_input("Количество (шт.)", min_value=0, step=1)
                comment = st.text_input("Комментарий")
                if st.form_submit_button("Сохранить", type="primary") and pkg_name:
                    sync(service.create_stock_item(PackageStock(
                        package=package_map[pkg_name],
                        amount=int(amount),
                        comment=comment,
                    )))
                    st.session_state.pkgs_add = False
                    st.rerun()

        elif st.session_state.pkgs_selected:
            item = next((i for i in sync(service.get_stock()) if i.id == st.session_state.pkgs_selected), None)
            if item:
                with st.form("pkgs_edit_form"):
                    pkg_name = st.selectbox("Упаковка", list(package_map.keys()), index=list(package_map.keys()).index(item.package.name))
                    amount = st.number_input("Количество (шт.)", min_value=0, step=1, value=item.amount)
                    comment = st.text_input("Комментарий", value=item.comment)
                    col_save, col_del = st.columns(2)
                    with col_save:
                        if st.form_submit_button("Сохранить", type="primary"):
                            sync(service.update_stock_item(PackageStock(
                                id=item.id, package=package_map[pkg_name],
                                amount=int(amount), comment=comment,
                            )))
                            st.rerun()
                    with col_del:
                        if st.form_submit_button("Удалить"):
                            sync(service.delete_stock_item(item.id))
                            st.session_state.pkgs_selected = None
                            st.rerun()
        else:
            st.markdown("<p style='color:rgb(148,157,168);font-size:0.9rem'>Выберите запись</p>", unsafe_allow_html=True)
