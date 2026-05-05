import streamlit as st

st.set_page_config(page_title="Управление заказами", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');

*, body, p, span, div, label, button {
    font-family: 'Montserrat', Arial, sans-serif !important;
}

[data-testid="stAppViewContainer"],
[data-testid="stHeader"] { background: rgb(244, 245, 249) !important; }

.block-container { padding: 2rem 3rem !important; max-width: 1100px !important; }

h1 { font-size: 2rem !important; font-weight: 700 !important; color: #000 !important; margin-bottom: 0 !important; }

/* кнопка Добавить */
[data-testid="stButton"] > button[kind="primary"] {
    background: rgb(255, 91, 0) !important; color: #fff !important;
    border: none !important; border-radius: 50px !important;
    font-weight: 600 !important; font-size: 0.9rem !important;
    white-space: nowrap !important; padding: 10px 20px !important;
    box-shadow: none !important;
}
[data-testid="stButton"] > button[kind="primary"]:hover { background: rgb(220, 75, 0) !important; }

/* белые панели */
[data-testid="stVerticalBlockBorderWrapper"] > div {
    background: rgb(255, 255, 255) !important;
    border-radius: 20px !important;
    border: 1px solid rgb(237, 237, 237) !important;
    box-shadow: rgba(56, 56, 56, 0.08) 0px 2px 8px !important;
    padding: 1.2rem 1.4rem !important;
}

/* pills — скрыть лейбл */
[data-testid="stPills"] { margin-bottom: 0 !important; }
[data-testid="stPills"] label { display: none !important; font-size: 0 !important; height: 0 !important; }
[data-testid="stPills"] button {
    border-radius: 50px !important; border: 1px solid rgb(237, 237, 237) !important;
    background: rgb(244, 245, 249) !important; color: rgb(148, 157, 168) !important;
    font-size: 0.85rem !important; font-weight: 600 !important; padding: 5px 16px !important;
}
[data-testid="stPills"] button[aria-selected="true"] {
    background: #fff !important; border-color: rgb(200, 200, 200) !important;
    color: rgb(56, 56, 56) !important; border-radius: 30px !important;
}

/* строка-кнопка */
[data-testid="stButton"] > button[kind="secondary"] {
    border: none !important;
    border-radius: 0 !important;
    background: transparent !important;
    text-align: left !important;
    padding: 10px 2px 10px 0 !important;
    width: 100% !important;
    justify-content: flex-start !important;
    align-items: flex-start !important;
    box-shadow: none !important;
    border-bottom: 1px solid rgb(237,237,237) !important;
    min-height: unset !important;
    margin-left: 0 !important;
}
[data-testid="stButton"] > button[kind="secondary"]:hover { background: rgb(250,250,252) !important; border-radius: 6px !important; }

/* выравнивание внутренних flex-контейнеров кнопки */
[data-testid="stButton"] > button[kind="secondary"] > div,
[data-testid="stButton"] > button[kind="secondary"] > div > span {
    align-items: flex-start !important;
    justify-content: flex-start !important;
    text-align: left !important;
    width: 100% !important;
}

/* p — стиль ДАТЫ */
[data-testid="stButton"] > button[kind="secondary"] p {
    font-size: 0.72rem !important;
    color: rgb(148, 157, 168) !important;
    font-weight: 500 !important;
    text-align: left !important;
    white-space: normal !important;
    margin: 0 !important;
    line-height: 1.4 !important;
    width: 100% !important;
}
/* strong — стиль ИМЕНИ */
[data-testid="stButton"] > button[kind="secondary"] p strong {
    font-size: 1.0rem !important;
    color: #000 !important;
    font-weight: 500 !important;
    display: block !important;
    line-height: 1.4 !important;
    margin-bottom: 0 !important;
}

/* убрать gap между строками */
[data-testid="stVerticalBlock"] > div { gap: 0 !important; }
/* убрать отступы в колонке с кнопкой */
[data-testid="stHorizontalBlock"] > div { gap: 4px !important; }

/* бейджи */
.badge {
    display: inline-block; border-radius: 50px;
    padding: 3px 12px; font-size: 0.75rem; font-weight: 600; white-space: nowrap;
}
.badge-prod { background: rgb(255,235,232); color: rgb(229,52,26); }
.badge-asm  { background: rgb(227,243,254); color: rgb(27,143,227); border-radius: 30px; }
.badge-del  { background: rgb(238,255,230); color: rgb(104,229,28); }
.badge-date { background: transparent; color: rgb(148,157,168); border: 1px solid rgb(148,157,168); border-radius: 30px; font-size: 0.65rem; padding: 2px 8px; }

/* детали */
.details-header { font-size: 1.05rem; font-weight: 600; color: rgb(56,56,56); margin-bottom: 1.2rem; }
.detail-label   { font-size: 0.68rem; color: rgb(148,157,168); margin-bottom: 3px; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 600; }
.detail-value   { font-size: 0.97rem; font-weight: 500; color: #000; margin-bottom: 14px; }

[data-testid="stToolbar"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

ORDERS = [
    {"id": 1, "name": "Капитан",      "date": "16.03.25", "status": None,            "exact_date": False},
    {"id": 2, "name": "Командор",     "date": "18.03.25", "status": "Производство",  "exact_date": False},
    {"id": 3, "name": "Чикен",        "date": "20.03.25", "status": "Сборка",        "exact_date": True},
    {"id": 4, "name": "Полет сервис", "date": "24.03.25", "status": "Доставка",      "exact_date": False},
    {"id": 5, "name": "Аэромил",      "date": "16.03.25", "status": None,            "exact_date": False},
    {"id": 6, "name": "СФУ",          "date": "24.03.25", "status": "Производство",  "exact_date": False},
    {"id": 7, "name": "Илим",         "date": "24.03.25", "status": "Доставка",      "exact_date": False},
]

BADGE = {
    "Производство": ("badge-prod", "Производство"),
    "Сборка":       ("badge-asm",  "Сборка"),
    "Доставка":     ("badge-del",  "Доставка"),
}
FILTERS = ["Все", "Производство", "Сборка", "Доставка"]

for key, default in [("active_filter", "Все"), ("selected_order", None), ("show_add_form", False)]:
    if key not in st.session_state:
        st.session_state[key] = default

# заголовок
hcol1, hcol2 = st.columns([4, 1])
with hcol1:
    st.title("Управление заказами")
with hcol2:
    st.write("")
    if st.button("+ Добавить заказ", type="primary", use_container_width=True):
        st.session_state.show_add_form = True
        st.session_state.selected_order = None

st.write("")

lcol, rcol = st.columns(2, gap="medium")

with lcol:
    with st.container(border=True):
        selected_filter = st.pills("filter", FILTERS, default=st.session_state.active_filter, label_visibility="collapsed")
        if selected_filter and selected_filter != st.session_state.active_filter:
            st.session_state.active_filter = selected_filter
            st.rerun()

        shown = [o for o in ORDERS
                 if st.session_state.active_filter == "Все"
                 or o["status"] == st.session_state.active_filter]

        for order in shown:
            c_btn, c_badge = st.columns([3, 1])

            date_suffix = "  ·  Четкая дата" if order["exact_date"] else ""
            # strong = имя (крупный чёрный), остальной текст p = дата (серый мелкий)
            label = f"**{order['name']}**\nдата заказа: {order['date']}{date_suffix}"

            with c_btn:
                if st.button(label, key=f"sel_{order['id']}", use_container_width=True):
                    st.session_state.selected_order = order["id"]
                    st.session_state.show_add_form  = False
                    st.rerun()

            with c_badge:
                if order["status"]:
                    cls, lbl = BADGE[order["status"]]
                    st.markdown(
                        f"<div style='display:flex;align-items:center;height:100%'>"
                        f"<span class='badge {cls}'>{lbl}</span></div>",
                        unsafe_allow_html=True,
                    )

with rcol:
    with st.container(border=True):
        st.markdown("<div class='details-header'>Детали заказа</div>", unsafe_allow_html=True)

        if st.session_state.show_add_form:
            with st.form("new_order"):
                name   = st.text_input("Название")
                date   = st.date_input("Дата заказа")
                status = st.selectbox("Статус", ["—", "Производство", "Сборка", "Доставка"])
                exact  = st.checkbox("Четкая дата")
                if st.form_submit_button("Сохранить", type="primary") and name:
                    ORDERS.append({
                        "id":         max(o["id"] for o in ORDERS) + 1,
                        "name":       name,
                        "date":       date.strftime("%d.%m.%y"),
                        "status":     None if status == "—" else status,
                        "exact_date": exact,
                    })
                    st.session_state.show_add_form = False
                    st.success("Заказ добавлен")
                    st.rerun()

        elif st.session_state.selected_order is not None:
            order = next((o for o in ORDERS if o["id"] == st.session_state.selected_order), None)
            if order:
                status_html = "—"
                if order["status"]:
                    cls, lbl = BADGE[order["status"]]
                    status_html = f"<span class='badge {cls}'>{lbl}</span>"
                st.markdown(f"""
<div class='detail-label'>Название</div>
<div class='detail-value'>{order['name']}</div>
<div class='detail-label'>Дата заказа</div>
<div class='detail-value'>{order['date']}</div>
<div class='detail-label'>Статус</div>
<div class='detail-value'>{status_html}</div>
<div class='detail-label'>Четкая дата</div>
<div class='detail-value'>{'Да' if order['exact_date'] else 'Нет'}</div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(
                "<div style='color:rgb(148,157,168);font-size:0.9rem;margin-top:0.5rem;'>"
                "Выберите заказ из списка</div>",
                unsafe_allow_html=True,
            )
