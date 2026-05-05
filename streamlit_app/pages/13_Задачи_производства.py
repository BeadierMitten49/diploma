import dotenv
dotenv.load_dotenv()

from datetime import date
from decimal import Decimal

import streamlit as st
from streamlit_app.style import apply_style
from streamlit_app.utils import (
    sync, get_task_service, get_product_service,
    get_craft_service, get_defect_rate_service, get_employee_service,
)
from src.domain.employee import Permission
from src.domain.exceptions import EmployeePermissionError, InvalidTaskStatusError
from src.domain.task import Task, TaskMaterial, TaskStatus

apply_style()
task_service     = get_task_service()
product_service  = get_product_service()
craft_service    = get_craft_service()
dr_service       = get_defect_rate_service()
employee_service = get_employee_service()

STATUS_LABEL = {
    TaskStatus.PENDING:     "Ожидает",
    TaskStatus.IN_PROGRESS: "В работе",
    TaskStatus.STOPPED:     "Остановлена",
    TaskStatus.COMPLETED:   "Завершена",
}
STATUS_BADGE = {
    TaskStatus.PENDING:     "badge-pending",
    TaskStatus.IN_PROGRESS: "badge-in-progress",
    TaskStatus.STOPPED:     "badge-stopped",
    TaskStatus.COMPLETED:   "badge-completed",
}
FILTERS = ["Все"] + [STATUS_LABEL[s] for s in TaskStatus]

for key, val in [
    ("task_selected", None), ("task_add", False),
    ("task_filter", "Все"), ("task_stop_mode", False),
    ("task_create_product_id", None),
]:
    if key not in st.session_state:
        st.session_state[key] = val

hcol1, hcol2 = st.columns([4, 1])
with hcol1:
    st.title("Задачи производства")
with hcol2:
    st.write("")
    if st.button("+ Создать", type="primary", use_container_width=True):
        st.session_state.task_add = True
        st.session_state.task_selected = None
        st.session_state.task_stop_mode = False
        st.session_state.task_create_product_id = None

lcol, rcol = st.columns(2, gap="medium")

# ── ЛЕВАЯ ПАНЕЛЬ ──────────────────────────────────────────────────────────────
with lcol:
    with st.container(border=True):
        selected_filter = st.pills("filter", FILTERS, default=st.session_state.task_filter, label_visibility="collapsed")
        if selected_filter and selected_filter != st.session_state.task_filter:
            st.session_state.task_filter = selected_filter
            st.rerun()

        tasks = sync(task_service.get_tasks())
        label_to_status = {v: k for k, v in STATUS_LABEL.items()}
        if st.session_state.task_filter != "Все":
            tasks = [t for t in tasks if STATUS_LABEL[t.status] == st.session_state.task_filter]

        if not tasks:
            st.markdown("<p style='color:rgb(148,157,168)'>Нет задач</p>", unsafe_allow_html=True)

        for task in tasks:
            c_btn, c_badge = st.columns([3, 1])
            boxes = task.planned_boxes
            remainder = task.planned_remainder_pieces
            qty = f"{boxes} кор." + (f" + {remainder} шт." if remainder else "")
            label = f"**{task.product.name}**\n{qty}  ·  {task.employee.name}  ·  до {task.deadline.strftime('%d.%m.%y')}"
            with c_btn:
                if st.button(label, key=f"task_{task.id}", use_container_width=True):
                    st.session_state.task_selected = task.id
                    st.session_state.task_add = False
                    st.session_state.task_stop_mode = False
                    st.rerun()
            with c_badge:
                cls = STATUS_BADGE[task.status]
                lbl = STATUS_LABEL[task.status]
                st.markdown(
                    f"<div style='display:flex;align-items:center;height:100%'>"
                    f"<span class='badge {cls}'>{lbl}</span></div>",
                    unsafe_allow_html=True,
                )

# ── ПРАВАЯ ПАНЕЛЬ ─────────────────────────────────────────────────────────────
with rcol:
    with st.container(border=True):

        # ── ФОРМА СОЗДАНИЯ ────────────────────────────────────────────────────
        if st.session_state.task_add:
            st.markdown("<div class='detail-label'>НОВАЯ ЗАДАЧА</div>", unsafe_allow_html=True)

            products = sync(product_service.get_products())
            packagings = sync(product_service.get_packagings())
            packaging_by_product = {p.product.id: p for p in packagings}
            # только продукты у которых есть фасовка
            products_with_pkg = [p for p in products if p.id in packaging_by_product]

            employees = sync(employee_service.get_employees())
            task_employees = [e for e in employees if Permission.TASKS in e.role.permissions]

            if not products_with_pkg:
                st.warning("Нет продуктов с настроенной фасовкой")
            elif not task_employees:
                st.warning("Нет сотрудников с доступом к задачам производства")
            else:
                product_map = {p.name: p for p in products_with_pkg}
                emp_map = {e.name: e for e in task_employees}

                product_name = st.selectbox("Продукт", list(product_map.keys()), key="task_create_product_name")
                selected_product = product_map[product_name]
                packaging = packaging_by_product[selected_product.id]

                boxes = st.number_input("Количество коробок", min_value=1, step=1, value=1, key="task_create_boxes")
                planned_pieces = boxes * packaging.pieces_per_box
                st.markdown(
                    f"<div class='detail-label'>Штук итого</div>"
                    f"<div class='detail-value'>{planned_pieces} шт.</div>",
                    unsafe_allow_html=True,
                )

                # расчёт сырья
                crafts = sync(craft_service.get_crafts_by_product(selected_product.id))
                defect_rate = sync(dr_service.get())
                multiplier = Decimal(1) + (Decimal(str(defect_rate.percentage)) / 100 if defect_rate else Decimal(0))

                if crafts:
                    st.markdown("<div class='detail-label'>Расчётное сырьё</div>", unsafe_allow_html=True)
                    materials = []
                    for craft in crafts:
                        amount = Decimal(planned_pieces) * craft.amount_per_piece * multiplier
                        materials.append(TaskMaterial(raw_material=craft.raw_material, planned_amount=amount.quantize(Decimal("0.001"))))
                        st.markdown(
                            f"<div style='font-size:0.9rem;margin-bottom:4px'>"
                            f"{craft.raw_material.name}: <b>{amount.quantize(Decimal('0.001'))} кг</b></div>",
                            unsafe_allow_html=True,
                        )
                else:
                    materials = []
                    st.markdown("<p style='color:rgb(148,157,168);font-size:0.85rem'>Крафт не настроен для этого продукта</p>", unsafe_allow_html=True)

                emp_name = st.selectbox("Исполнитель", list(emp_map.keys()), key="task_create_emp")
                planned_start = st.date_input("Дата начала", value=date.today(), key="task_create_start")
                deadline = st.date_input("Дедлайн", value=date.today(), key="task_create_deadline")
                comment = st.text_input("Комментарий", key="task_create_comment")

                if st.button("Сохранить", type="primary"):
                    try:
                        sync(task_service.create_task(Task(
                            product=selected_product,
                            packaging=packaging,
                            employee=emp_map[emp_name],
                            planned_pieces=planned_pieces,
                            planned_start_date=planned_start,
                            deadline=deadline,
                            status=TaskStatus.PENDING,
                            materials=materials,
                            stops=[],
                            comment=comment or None,
                        )))
                        st.session_state.task_add = False
                        st.rerun()
                    except EmployeePermissionError as e:
                        st.error(str(e))

        # ── ДЕТАЛИ ЗАДАЧИ ─────────────────────────────────────────────────────
        elif st.session_state.task_selected:
            task = sync(task_service.get_task(st.session_state.task_selected))
            if task:
                boxes = task.planned_boxes
                remainder = task.planned_remainder_pieces
                qty = f"{boxes} кор." + (f" + {remainder} шт." if remainder else "")
                cls = STATUS_BADGE[task.status]
                lbl = STATUS_LABEL[task.status]

                st.markdown(f"""
<div class='detail-label'>Продукт</div>
<div class='detail-value'>{task.product.name}</div>
<div class='detail-label'>Количество</div>
<div class='detail-value'>{qty} ({task.planned_pieces} шт.)</div>
<div class='detail-label'>Исполнитель</div>
<div class='detail-value'>{task.employee.name}</div>
<div class='detail-label'>Дата начала</div>
<div class='detail-value'>{task.planned_start_date.strftime('%d.%m.%Y')}</div>
<div class='detail-label'>Дедлайн</div>
<div class='detail-value'>{task.deadline.strftime('%d.%m.%Y')}</div>
<div class='detail-label'>Статус</div>
<div class='detail-value'><span class='badge {cls}'>{lbl}</span></div>
""", unsafe_allow_html=True)

                if task.comment:
                    st.markdown(f"<div class='detail-label'>Комментарий</div><div class='detail-value'>{task.comment}</div>", unsafe_allow_html=True)

                if task.materials:
                    st.markdown("<div class='detail-label'>Расчётное сырьё</div>", unsafe_allow_html=True)
                    for m in task.materials:
                        st.markdown(f"<div style='font-size:0.9rem;margin-bottom:4px'>{m.raw_material.name}: <b>{m.planned_amount} кг</b></div>", unsafe_allow_html=True)

                if task.stops:
                    st.markdown("<div class='detail-label'>Остановки</div>", unsafe_allow_html=True)
                    for s in task.stops:
                        resumed = s.resumed_at.strftime('%d.%m.%Y %H:%M') if s.resumed_at else "не возобновлена"
                        st.markdown(
                            f"<div style='font-size:0.85rem;margin-bottom:6px;color:rgb(100,100,110)'>"
                            f"⏸ {s.stopped_at.strftime('%d.%m.%Y %H:%M')} → {resumed}<br>"
                            f"<i>{s.reason}</i></div>",
                            unsafe_allow_html=True,
                        )

                st.write("")

                # ── кнопки действий ───────────────────────────────────────────
                if task.status == TaskStatus.PENDING:
                    if st.button("▶ Начать", type="primary"):
                        try:
                            sync(task_service.start_task(task.id))
                            st.rerun()
                        except InvalidTaskStatusError as e:
                            st.error(str(e))

                elif task.status == TaskStatus.IN_PROGRESS:
                    if not st.session_state.task_stop_mode:
                        if st.button("⏸ Остановить"):
                            st.session_state.task_stop_mode = True
                            st.rerun()
                    else:
                        with st.form("stop_form"):
                            reason = st.text_input("Причина остановки")
                            c1, c2 = st.columns(2)
                            with c1:
                                if st.form_submit_button("Подтвердить", type="primary") and reason:
                                    try:
                                        sync(task_service.stop_task(task.id, reason))
                                        st.session_state.task_stop_mode = False
                                        st.rerun()
                                    except InvalidTaskStatusError as e:
                                        st.error(str(e))
                            with c2:
                                if st.form_submit_button("Отмена"):
                                    st.session_state.task_stop_mode = False
                                    st.rerun()

                elif task.status == TaskStatus.STOPPED:
                    if st.button("▶ Возобновить", type="primary"):
                        try:
                            sync(task_service.resume_task(task.id))
                            st.rerun()
                        except InvalidTaskStatusError as e:
                            st.error(str(e))

        else:
            st.markdown("<p style='color:rgb(148,157,168);font-size:0.9rem'>Выберите задачу</p>", unsafe_allow_html=True)
