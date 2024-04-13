import json

from app.models import Language


def load_translations(locale: Language) -> dict:
    translation_file_path = f"translations/{locale.value}.json"
    try:
        with open(translation_file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        # Failsafe to avoid crashing the application when translations are not found
        return {}


# If you wish to add a new language, you need to add a new line here and complete the TRANSLATIONS dictionary
translations_french = load_translations(Language.FR)

# Translations are stored in a table to avoid loading them multiple times
TRANSLATIONS = {
    Language.FR: translations_french,
}
