import dotenv
dotenv.load_dotenv()

from decimal import Decimal
import streamlit as st
from streamlit_app.style import apply_style
from streamlit_app.utils import sync, get_craft_service, get_product_service, get_raw_material_service
from src.domain.craft import Craft

apply_style()
craft_service = get_craft_service()
product_service = get_product_service()
material_service = get_raw_material_service()

for key, val in [("craft_selected", None), ("craft_add", False)]:
    if key not in st.session_state:
        st.session_state[key] = val

hcol1, hcol2 = st.columns([4, 1])
with hcol1:
    st.title("Крафт")
with hcol2:
    st.write("")
    if st.button("+ Добавить", type="primary", use_container_width=True):
        st.session_state.craft_add = True
        st.session_state.craft_selected = None

lcol, rcol = st.columns(2, gap="medium")

with lcol:
    with st.container(border=True):
        items = sync(craft_service.get_crafts())
        if not items:
            st.markdown("<p style='color:rgb(148,157,168)'>Нет записей</p>", unsafe_allow_html=True)
        for item in items:
            label = f"**{item.product.name}**\n{item.raw_material.name}: {item.amount_per_piece} кг/шт."
            if st.button(label, key=f"craft_{item.id}", use_container_width=True):
                st.session_state.craft_selected = item.id
                st.session_state.craft_add = False
                st.rerun()

with rcol:
    with st.container(border=True):
        products = sync(product_service.get_products())
        materials = sync(material_service.get_materials())
        product_map = {p.name: p for p in products}
        material_map = {m.name: m for m in materials}

        if st.session_state.craft_add:
            st.markdown("<div class='detail-label'>НОВАЯ ЗАПИСЬ</div>", unsafe_allow_html=True)
            with st.form("craft_add_form"):
                prod_name = st.selectbox("Продукт", list(product_map.keys()))
                mat_name = st.selectbox("Сырьё", list(material_map.keys()))
                amount = st.number_input("Кг сырья на штуку", min_value=0.0, step=0.001, format="%.5f")
                if st.form_submit_button("Сохранить", type="primary"):
                    sync(craft_service.create_craft(Craft(
                        product=product_map[prod_name],
                        raw_material=material_map[mat_name],
                        amount_per_piece=Decimal(str(amount)),
                    )))
                    st.session_state.craft_add = False
                    st.rerun()

        elif st.session_state.craft_selected:
            item = next((i for i in sync(craft_service.get_crafts()) if i.id == st.session_state.craft_selected), None)
            if item:
                with st.form("craft_edit_form"):
                    prod_name = st.selectbox("Продукт", list(product_map.keys()), index=list(product_map.keys()).index(item.product.name))
                    mat_name = st.selectbox("Сырьё", list(material_map.keys()), index=list(material_map.keys()).index(item.raw_material.name))
                    amount = st.number_input("Кг сырья на штуку", min_value=0.0, step=0.001, format="%.5f", value=float(item.amount_per_piece))
                    col_save, col_del = st.columns(2)
                    with col_save:
                        if st.form_submit_button("Сохранить", type="primary"):
                            sync(craft_service.update_craft(Craft(
                                id=item.id,
                                product=product_map[prod_name],
                                raw_material=material_map[mat_name],
                                amount_per_piece=Decimal(str(amount)),
                            )))
                            st.rerun()
                    with col_del:
                        if st.form_submit_button("Удалить"):
                            sync(craft_service.delete_craft(item.id))
                            st.session_state.craft_selected = None
                            st.rerun()
        else:
            st.markdown("<p style='color:rgb(148,157,168);font-size:0.9rem'>Выберите запись</p>", unsafe_allow_html=True)
