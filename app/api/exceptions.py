from fastapi import HTTPException, status

from app.api.translations import TRANSLATIONS
from app.models import DEFAULT_LANGUAGE, Language


class HTTPException(HTTPException):
    def __init__(
        self, status_code: int, detail: str, locale: Language = DEFAULT_LANGUAGE
    ):
        translation_table: dict = TRANSLATIONS.get(locale, {})
        detail = translation_table.get(detail, detail)

        super().__init__(status_code=status_code, detail=detail)


class HTTPNotEnoughPermissions(HTTPException):
    def __init__(self, locale: Language = DEFAULT_LANGUAGE):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Current user do not have enough privilege",
            locale=locale,
        )


# TODO: Can be interesting to make this generic like cruds
# Items
class HTTPItemNotFound(HTTPException):
    def __init__(self, locale: Language = DEFAULT_LANGUAGE):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
            locale=locale,
        )


# Users
class HTTPUserNotFound(HTTPException):
    def __init__(self, locale: Language = DEFAULT_LANGUAGE):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
            locale=locale,
        )
