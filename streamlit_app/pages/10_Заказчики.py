import dotenv
dotenv.load_dotenv()

import streamlit as st
from streamlit_app.style import apply_style
from streamlit_app.utils import sync, get_customer_service
from src.domain.customer import Customer

apply_style()
service = get_customer_service()

for key, val in [("cust_selected", None), ("cust_add", False)]:
    if key not in st.session_state:
        st.session_state[key] = val

hcol1, hcol2 = st.columns([4, 1])
with hcol1:
    st.title("Заказчики")
with hcol2:
    st.write("")
    if st.button("+ Добавить", type="primary", use_container_width=True):
        st.session_state.cust_add = True
        st.session_state.cust_selected = None

lcol, rcol = st.columns(2, gap="medium")

with lcol:
    with st.container(border=True):
        items = sync(service.get_customers())
        if not items:
            st.markdown("<p style='color:rgb(148,157,168)'>Нет записей</p>", unsafe_allow_html=True)
        for item in items:
            label = f"**{item.name}**\n{item.address}"
            if st.button(label, key=f"cust_{item.id}", use_container_width=True):
                st.session_state.cust_selected = item.id
                st.session_state.cust_add = False
                st.rerun()

with rcol:
    with st.container(border=True):
        if st.session_state.cust_add:
            st.markdown("<div class='detail-label'>НОВАЯ ЗАПИСЬ</div>", unsafe_allow_html=True)
            with st.form("cust_add_form"):
                name = st.text_input("Наименование")
                address = st.text_input("Адрес")
                comment = st.text_input("Комментарий")
                if st.form_submit_button("Сохранить", type="primary") and name:
                    sync(service.create_customer(Customer(name=name, address=address, comment=comment)))
                    st.session_state.cust_add = False
                    st.rerun()

        elif st.session_state.cust_selected:
            item = next((i for i in sync(service.get_customers()) if i.id == st.session_state.cust_selected), None)
            if item:
                with st.form("cust_edit_form"):
                    name = st.text_input("Наименование", value=item.name)
                    address = st.text_input("Адрес", value=item.address)
                    comment = st.text_input("Комментарий", value=item.comment)
                    col_save, col_del = st.columns(2)
                    with col_save:
                        if st.form_submit_button("Сохранить", type="primary"):
                            sync(service.update_customer(Customer(id=item.id, name=name, address=address, comment=comment)))
                            st.rerun()
                    with col_del:
                        if st.form_submit_button("Удалить"):
                            sync(service.delete_customer(item.id))
                            st.session_state.cust_selected = None
                            st.rerun()
        else:
            st.markdown("<p style='color:rgb(148,157,168);font-size:0.9rem'>Выберите запись</p>", unsafe_allow_html=True)
