from dataclasses import dataclass, field


@dataclass
class Package:
    """Справочник упаковки."""
    id: int | None = field(default=None, kw_only=True)
    name: str
    critical_amount: int


@dataclass
class PackageStock:
    """Складская запись упаковки."""
    id: int | None = field(default=None, kw_only=True)
    package: Package
    amount: int
    comment: str = ""

    @property
    def is_critical(self) -> bool:
        return self.amount <= self.package.critical_amount
