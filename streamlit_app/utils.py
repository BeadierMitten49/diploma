import asyncio
import streamlit as st

from src.infrastructure.database.database_setup import async_session
from src.infrastructure.database.repositories.raw_material import RawMaterialRepository, RawMaterialStockRepository
from src.infrastructure.database.repositories.package import PackageRepository, PackageStockRepository
from src.infrastructure.database.repositories.product import ProductRepository, PackagingRepository, ProductStockRepository
from src.infrastructure.database.repositories.craft import CraftRepository
from src.infrastructure.database.repositories.defect_rate import DefectRateRepository
from src.infrastructure.database.repositories.customer import CustomerRepository
from src.infrastructure.database.repositories.employee import RoleRepository, EmployeeRepository
from src.infrastructure.database.repositories.task import TaskRepository
from src.application.raw_material import RawMaterialService
from src.application.package import PackageService
from src.application.product import ProductService
from src.application.craft import CraftService
from src.application.defect_rate import DefectRateService
from src.application.customer import CustomerService
from src.application.employee import RoleService, EmployeeService
from src.application.task import TaskService


def sync(coro):
    return asyncio.run(coro)


@st.cache_resource
def get_raw_material_service() -> RawMaterialService:
    return RawMaterialService(
        RawMaterialRepository(async_session),
        RawMaterialStockRepository(async_session),
    )


@st.cache_resource
def get_package_service() -> PackageService:
    return PackageService(
        PackageRepository(async_session),
        PackageStockRepository(async_session),
    )


@st.cache_resource
def get_product_service() -> ProductService:
    return ProductService(
        ProductRepository(async_session),
        PackagingRepository(async_session),
        ProductStockRepository(async_session),
    )


@st.cache_resource
def get_craft_service() -> CraftService:
    return CraftService(CraftRepository(async_session))


@st.cache_resource
def get_defect_rate_service() -> DefectRateService:
    return DefectRateService(DefectRateRepository(async_session))


@st.cache_resource
def get_customer_service() -> CustomerService:
    return CustomerService(CustomerRepository(async_session))


@st.cache_resource
def get_role_service() -> RoleService:
    return RoleService(RoleRepository(async_session))


@st.cache_resource
def get_employee_service() -> EmployeeService:
    return EmployeeService(EmployeeRepository(async_session))


@st.cache_resource
def get_task_service() -> TaskService:
    return TaskService(TaskRepository(async_session))
