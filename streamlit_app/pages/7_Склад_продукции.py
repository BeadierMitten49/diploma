import dotenv
dotenv.load_dotenv()

from datetime import date
import streamlit as st
from streamlit_app.style import apply_style
from streamlit_app.utils import sync, get_product_service
from src.domain.product import ProductStock

apply_style()
service = get_product_service()

for key, val in [("ps_selected", None), ("ps_add", False)]:
    if key not in st.session_state:
        st.session_state[key] = val

hcol1, hcol2 = st.columns([4, 1])
with hcol1:
    st.title("Склад продукции")
with hcol2:
    st.write("")
    if st.button("+ Добавить", type="primary", use_container_width=True):
        st.session_state.ps_add = True
        st.session_state.ps_selected = None

lcol, rcol = st.columns(2, gap="medium")

with lcol:
    with st.container(border=True):
        items = sync(service.get_stock())
        if not items:
            st.markdown("<p style='color:rgb(148,157,168)'>Нет записей</p>", unsafe_allow_html=True)
        for item in items:
            warn = " 🔴" if item.is_critical or item.is_expired else ""
            label = f"**{item.product.name}**{warn}\n{item.full_boxes} кор. + {item.remaining_pieces} шт.  ·  партия {item.batch_number}"
            if st.button(label, key=f"ps_{item.id}", use_container_width=True):
                st.session_state.ps_selected = item.id
                st.session_state.ps_add = False
                st.rerun()

with rcol:
    with st.container(border=True):
        products = sync(service.get_products())
        packagings = sync(service.get_packagings())
        product_map = {p.name: p for p in products}
        packaging_map = {p.product.name: p for p in packagings}

        if st.session_state.ps_add:
            st.markdown("<div class='detail-label'>НОВАЯ ЗАПИСЬ</div>", unsafe_allow_html=True)
            with st.form("ps_add_form"):
                prod_name = st.selectbox("Продукт", list(product_map.keys()))
                amount = st.number_input("Количество (шт.)", min_value=0, step=1)
                batch = st.text_input("Номер партии")
                arrival = st.date_input("Дата поступления", value=date.today())
                comment = st.text_input("Комментарий")
                if st.form_submit_button("Сохранить", type="primary") and prod_name and batch:
                    packaging = packaging_map.get(prod_name)
                    if not packaging:
                        st.error(f"Для продукта «{prod_name}» не задана фасовка")
                    else:
                        sync(service.create_stock_item(ProductStock(
                            product=product_map[prod_name],
                            amount_pieces=int(amount),
                            batch_number=batch,
                            arrival_date=arrival,
                            packaging=packaging,
                            comment=comment,
                        )))
                        st.session_state.ps_add = False
                        st.rerun()

        elif st.session_state.ps_selected:
            item = next((i for i in sync(service.get_stock()) if i.id == st.session_state.ps_selected), None)
            if item:
                st.markdown(f"""
<div class='detail-label'>ОСТАТОК</div>
<div class='detail-value'>{item.full_boxes} кор. + {item.remaining_pieces} шт.</div>
<div class='detail-label'>СРОК ГОДНОСТИ</div>
<div class='detail-value'>{'⚠️ Истёк' if item.is_expired else item.expiry_date}</div>
""", unsafe_allow_html=True)
                with st.form("ps_edit_form"):
                    prod_name = st.selectbox("Продукт", list(product_map.keys()), index=list(product_map.keys()).index(item.product.name))
                    amount = st.number_input("Количество (шт.)", min_value=0, step=1, value=item.amount_pieces)
                    batch = st.text_input("Номер партии", value=item.batch_number)
                    arrival = st.date_input("Дата поступления", value=item.arrival_date)
                    comment = st.text_input("Комментарий", value=item.comment)
                    col_save, col_del = st.columns(2)
                    with col_save:
                        if st.form_submit_button("Сохранить", type="primary"):
                            packaging = packaging_map.get(prod_name)
                            if packaging:
                                sync(service.update_stock_item(ProductStock(
                                    id=item.id,
                                    product=product_map[prod_name],
                                    amount_pieces=int(amount),
                                    batch_number=batch,
                                    arrival_date=arrival,
                                    packaging=packaging,
                                    comment=comment,
                                )))
                                st.rerun()
                    with col_del:
                        if st.form_submit_button("Удалить"):
                            sync(service.delete_stock_item(item.id))
                            st.session_state.ps_selected = None
                            st.rerun()
        else:
            st.markdown("<p style='color:rgb(148,157,168);font-size:0.9rem'>Выберите запись</p>", unsafe_allow_html=True)
