"""
Модуль refactorizer.py
Исмаилов Богдан мт-202
Выполняет приведение регистра, удаление лишних пробелов,
повторяющейся пунктуации, эмодзи, обезличивание (анонимизацию)
и формирование очищенного текста (clean_text) для анализа.
"""

import re
from typing import Dict, List


class TextRefactorizer:
    def __init__(self):
        # Маркеры и служебные лейблы, предшествующие сущностям
        self.service_labels = re.compile(
            r'\b(?:ссылка|url|e-mail|email|почта|телефон|тел|звонить|мой номер|номер|'
            r'дата|оформлено|нужно на|цена|сумма|стоимость|списали|смотрите|страница)\b[:=\s]*',
            flags=re.IGNORECASE
        )

    def clean_noise(self, text: str) -> str:
        """
        Удаляет спецсимволы, эмодзи, повторяющиеся знаки препинания
        и схлопывает множественные пробелы.
        """
        if not text:
            return ""
        text = re.sub(r'[\U00010000-\U0010ffff]', '', text)
        text = re.sub(r'[\ufe00-\ufe0f]', '', text)
        text = re.sub(r'([!?.,*#=/|-])\1+', r'\1', text)
        text = re.sub(r'[\*#|~_/]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def anonymize_text(self, text: str, entities: Dict[str, List[str]]) -> str:
        """
        Заменяет найденные сущности на соответствующие маркеры:
        [URL], [EMAIL], [PHONE], [DATE], [PRICE].
        """
        result = text

        for url in entities.get('urls', []):
            result = result.replace(url, '[URL]')

        for email in entities.get('emails', []):
            result = result.replace(email, '[EMAIL]')

        for phone in entities.get('phones', []):
            result = result.replace(phone, '[PHONE]')

        for price in entities.get('prices', []):
            result = result.replace(price, '[PRICE]')

        for date in entities.get('dates', []):
            result = result.replace(date, '[DATE]')

        result = self.clean_noise(result)
        return result

   def build_clean_text(self, anonymized_text: str) -> str:
        text = anonymized_text.lower()
        placeholders = ['[url]', '[email]', '[phone]', '[date]', '[price]']
        for p in placeholders:
            text = text.replace(p, ' ')
        text = self.service_labels.sub(' ', text)
        text = re.sub(r'[^\w\s]', ' ', text) 
        text = re.sub(r'\b\d+\b', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
