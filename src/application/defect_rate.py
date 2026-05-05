from src.domain.defect_rate import DefectRate
from src.infrastructure.database.repositories.defect_rate import DefectRateRepository


class DefectRateService:
    def __init__(self, defect_rate_repo: DefectRateRepository):
        self.defect_rate_repo = defect_rate_repo

    async def get(self) -> DefectRate | None:
        return await self.defect_rate_repo.get()

    async def update(self, defect_rate: DefectRate) -> DefectRate:
        return await self.defect_rate_repo.update(defect_rate)
