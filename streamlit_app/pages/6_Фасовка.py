import dotenv
dotenv.load_dotenv()

import streamlit as st
from streamlit_app.style import apply_style
from streamlit_app.utils import sync, get_product_service
from src.domain.product import Packaging

apply_style()
service = get_product_service()

for key, val in [("pack_selected", None), ("pack_add", False)]:
    if key not in st.session_state:
        st.session_state[key] = val

hcol1, hcol2 = st.columns([4, 1])
with hcol1:
    st.title("Фасовка")
with hcol2:
    st.write("")
    if st.button("+ Добавить", type="primary", use_container_width=True):
        st.session_state.pack_add = True
        st.session_state.pack_selected = None

lcol, rcol = st.columns(2, gap="medium")

with lcol:
    with st.container(border=True):
        items = sync(service.get_packagings())
        if not items:
            st.markdown("<p style='color:rgb(148,157,168)'>Нет записей</p>", unsafe_allow_html=True)
        for item in items:
            label = f"**{item.product.name}**\n{item.pieces_per_box} шт. в коробке"
            if st.button(label, key=f"pack_{item.id}", use_container_width=True):
                st.session_state.pack_selected = item.id
                st.session_state.pack_add = False
                st.rerun()

with rcol:
    with st.container(border=True):
        products = sync(service.get_products())
        product_map = {p.name: p for p in products}

        if st.session_state.pack_add:
            st.markdown("<div class='detail-label'>НОВАЯ ЗАПИСЬ</div>", unsafe_allow_html=True)
            with st.form("pack_add_form"):
                prod_name = st.selectbox("Продукт", list(product_map.keys()))
                pieces = st.number_input("Штук в коробке", min_value=1, step=1)
                if st.form_submit_button("Сохранить", type="primary") and prod_name:
                    sync(service.create_packaging(Packaging(product=product_map[prod_name], pieces_per_box=int(pieces))))
                    st.session_state.pack_add = False
                    st.rerun()

        elif st.session_state.pack_selected:
            item = next((i for i in sync(service.get_packagings()) if i.id == st.session_state.pack_selected), None)
            if item:
                with st.form("pack_edit_form"):
                    prod_name = st.selectbox("Продукт", list(product_map.keys()), index=list(product_map.keys()).index(item.product.name))
                    pieces = st.number_input("Штук в коробке", min_value=1, step=1, value=item.pieces_per_box)
                    col_save, col_del = st.columns(2)
                    with col_save:
                        if st.form_submit_button("Сохранить", type="primary"):
                            sync(service.update_packaging(Packaging(id=item.id, product=product_map[prod_name], pieces_per_box=int(pieces))))
                            st.rerun()
                    with col_del:
                        if st.form_submit_button("Удалить"):
                            sync(service.delete_packaging(item.id))
                            st.session_state.pack_selected = None
                            st.rerun()
        else:
            st.markdown("<p style='color:rgb(148,157,168);font-size:0.9rem'>Выберите запись</p>", unsafe_allow_html=True)
