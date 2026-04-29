import re


def pascal_to_snake_case(pascal_case_string: str) -> str:
    return re.sub(r'([a-z])([A-Z])', r'\1_\2', pascal_case_string).lower()
