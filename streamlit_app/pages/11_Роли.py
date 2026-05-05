import dotenv
dotenv.load_dotenv()

import streamlit as st
from streamlit_app.style import apply_style
from streamlit_app.utils import sync, get_role_service
from src.domain.employee import Permission, Role

apply_style()
service = get_role_service()

PERMISSION_LABELS = {
    Permission.RAW_MATERIAL:       "Сырьё",
    Permission.RAW_MATERIAL_STOCK: "Склад сырья",
    Permission.PACKAGE:            "Упаковка",
    Permission.PACKAGE_STOCK:      "Склад упаковки",
    Permission.PRODUCT:            "Продукция",
    Permission.PACKAGING:          "Фасовка",
    Permission.PRODUCT_STOCK:      "Склад продукции",
    Permission.CRAFT:              "Крафт",
    Permission.DEFECT_RATE:        "Процент брака",
    Permission.CUSTOMERS:          "Заказчики",
    Permission.TASKS:              "Задачи производства",
}
ALL_PERMISSIONS = list(Permission)

for key, val in [("role_selected", None), ("role_add", False)]:
    if key not in st.session_state:
        st.session_state[key] = val

hcol1, hcol2 = st.columns([4, 1])
with hcol1:
    st.title("Роли")
with hcol2:
    st.write("")
    if st.button("+ Добавить", type="primary", use_container_width=True):
        st.session_state.role_add = True
        st.session_state.role_selected = None

lcol, rcol = st.columns(2, gap="medium")

with lcol:
    with st.container(border=True):
        items = sync(service.get_roles())
        if not items:
            st.markdown("<p style='color:rgb(148,157,168)'>Нет записей</p>", unsafe_allow_html=True)
        for item in items:
            label = f"**{item.name}**\n{len(item.permissions)} из {len(ALL_PERMISSIONS)} доступов"
            if st.button(label, key=f"role_{item.id}", use_container_width=True):
                st.session_state.role_selected = item.id
                st.session_state.role_add = False
                st.rerun()

with rcol:
    with st.container(border=True):
        if st.session_state.role_add:
            st.markdown("<div class='detail-label'>НОВАЯ РОЛЬ</div>", unsafe_allow_html=True)
            with st.form("role_add_form"):
                name = st.text_input("Название роли")
                selected = st.multiselect(
                    "Доступы",
                    options=ALL_PERMISSIONS,
                    format_func=lambda p: PERMISSION_LABELS[p],
                )
                if st.form_submit_button("Сохранить", type="primary") and name:
                    sync(service.create_role(Role(name=name, permissions=selected)))
                    st.session_state.role_add = False
                    st.rerun()

        elif st.session_state.role_selected:
            item = next((i for i in sync(service.get_roles()) if i.id == st.session_state.role_selected), None)
            if item:
                with st.form("role_edit_form"):
                    name = st.text_input("Название роли", value=item.name)
                    selected = st.multiselect(
                        "Доступы",
                        options=ALL_PERMISSIONS,
                        default=item.permissions,
                        format_func=lambda p: PERMISSION_LABELS[p],
                    )
                    col_save, col_del = st.columns(2)
                    with col_save:
                        if st.form_submit_button("Сохранить", type="primary"):
                            sync(service.update_role(Role(id=item.id, name=name, permissions=selected)))
                            st.rerun()
                    with col_del:
                        if st.form_submit_button("Удалить"):
                            sync(service.delete_role(item.id))
                            st.session_state.role_selected = None
                            st.rerun()
        else:
            st.markdown("<p style='color:rgb(148,157,168);font-size:0.9rem'>Выберите роль</p>", unsafe_allow_html=True)
