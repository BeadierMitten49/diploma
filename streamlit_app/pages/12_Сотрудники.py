import dotenv
dotenv.load_dotenv()

import streamlit as st
from streamlit_app.style import apply_style
from streamlit_app.utils import sync, get_employee_service, get_role_service
from src.domain.employee import Employee

apply_style()
employee_service = get_employee_service()
role_service = get_role_service()

for key, val in [("emp_selected", None), ("emp_add", False)]:
    if key not in st.session_state:
        st.session_state[key] = val

hcol1, hcol2 = st.columns([4, 1])
with hcol1:
    st.title("Сотрудники")
with hcol2:
    st.write("")
    if st.button("+ Добавить", type="primary", use_container_width=True):
        st.session_state.emp_add = True
        st.session_state.emp_selected = None

lcol, rcol = st.columns(2, gap="medium")

with lcol:
    with st.container(border=True):
        items = sync(employee_service.get_employees())
        if not items:
            st.markdown("<p style='color:rgb(148,157,168)'>Нет записей</p>", unsafe_allow_html=True)
        for item in items:
            label = f"**{item.name}**\n{item.role.name}"
            if st.button(label, key=f"emp_{item.id}", use_container_width=True):
                st.session_state.emp_selected = item.id
                st.session_state.emp_add = False
                st.rerun()

with rcol:
    with st.container(border=True):
        roles = sync(role_service.get_roles())
        role_map = {r.name: r for r in roles}

        if st.session_state.emp_add:
            st.markdown("<div class='detail-label'>НОВЫЙ СОТРУДНИК</div>", unsafe_allow_html=True)
            if not roles:
                st.warning("Сначала создайте роль")
            else:
                with st.form("emp_add_form"):
                    name = st.text_input("Имя")
                    role_name = st.selectbox("Роль", list(role_map.keys()))
                    if st.form_submit_button("Сохранить", type="primary") and name:
                        sync(employee_service.create_employee(
                            Employee(name=name, role=role_map[role_name])
                        ))
                        st.session_state.emp_add = False
                        st.rerun()

        elif st.session_state.emp_selected:
            item = next((i for i in sync(employee_service.get_employees()) if i.id == st.session_state.emp_selected), None)
            if item:
                with st.form("emp_edit_form"):
                    name = st.text_input("Имя", value=item.name)
                    role_name = st.selectbox(
                        "Роль", list(role_map.keys()),
                        index=list(role_map.keys()).index(item.role.name) if item.role.name in role_map else 0,
                    )
                    col_save, col_del = st.columns(2)
                    with col_save:
                        if st.form_submit_button("Сохранить", type="primary"):
                            sync(employee_service.update_employee(
                                Employee(id=item.id, name=name, role=role_map[role_name])
                            ))
                            st.rerun()
                    with col_del:
                        if st.form_submit_button("Удалить"):
                            sync(employee_service.delete_employee(item.id))
                            st.session_state.emp_selected = None
                            st.rerun()
        else:
            st.markdown("<p style='color:rgb(148,157,168);font-size:0.9rem'>Выберите сотрудника</p>", unsafe_allow_html=True)
