from dataclasses import dataclass, field
from enum import StrEnum


class Permission(StrEnum):
    RAW_MATERIAL = "raw_material"
    RAW_MATERIAL_STOCK = "raw_material_stock"
    PACKAGE = "package"
    PACKAGE_STOCK = "package_stock"
    PRODUCT = "product"
    PACKAGING = "packaging"
    PRODUCT_STOCK = "product_stock"
    CRAFT = "craft"
    DEFECT_RATE = "defect_rate"
    CUSTOMERS = "customers"
    TASKS = "tasks"


@dataclass
class Role:
    """Роль сотрудника с набором прав доступа."""
    id: int | None = field(default=None, kw_only=True)
    name: str
    permissions: list[Permission]


@dataclass
class Employee:
    """Сотрудник."""
    id: int | None = field(default=None, kw_only=True)
    name: str
    role: Role
