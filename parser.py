"""
Модуль parser.py
Кравченко Андрей мт-202
Отвечает за загрузку исходных данных, первичный анализ структуры и
извлечение именованных сущностей (URL, Email, Phone, Date, Price)
с помощью оптимизированных регулярных выражений.
"""

import re
import pandas as pd
from typing import Dict, List, Any


class EntityParser:
    def __init__(self):
        # 1. URLs (http, https, www)
        self.url_pattern = re.compile(
            r'(?:https?://|www\.)[^\s;,]+',
            flags=re.IGNORECASE
        )

        # 2. Email-адреса
        self.email_pattern = re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
            flags=re.IGNORECASE
        )

        # 3. Номера телефонов (+7..., 8..., с пробелами, дефисами, скобками)
        self.phone_pattern = re.compile(
            r'(?:\+7|8)[\s\-]*(?:\(?\d{3}\)?[\s\-]*)?\d{3}[\s\-]*\d{2}[\s\-]*\d{2}|\b8\d{10}\b|\b\+7\d{10}\b'
        )

        # 4. Даты (форматы YYYY-MM-DD, DD-MM-YYYY, DD/MM/YYYY, DD.MM.YYYY, DD-MM-YY)
        self.date_pattern = re.compile(
            r'\b(?:\d{4}[-/.]\d{2}[-/.]\d{2}|\d{2}[-/.]\d{2}[-/.]\d{2,4})\b'
        )

        # 5. Цены (числа с пробелами-разделителями + руб, рублей, RUB, ₽)
        self.price_pattern = re.compile(
            r'\b\d+(?:[\s\xa0]\d+)*(?:\s*(?:руб(?:лей|ля|\.)?|rub|₽))(?!\w)',
            flags=re.IGNORECASE
        )

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Извлекает все сущности из переданной строки.
        Возвращает словарь со списками найденных сущностей.
        """
        if not isinstance(text, str):
            text = str(text) if text is not None else ""

        # Чистим крайние знаки препинания в URL, попавшие при парсинге
        raw_urls = self.url_pattern.findall(text)
        cleaned_urls = [u.rstrip('.,);!#') for u in raw_urls]

        emails = self.email_pattern.findall(text)
        phones = self.phone_pattern.findall(text)
        dates = self.date_pattern.findall(text)
        prices = self.price_pattern.findall(text)

        return {
            'urls': cleaned_urls,
            'emails': emails,
            'phones': phones,
            'dates': dates,
            'prices': prices
        }

    @staticmethod
    def load_dataset(file_path: str) -> pd.DataFrame:
        """
        Загружает CSV-файл с автоопределением кодировки UTF-8 with BOM / UTF-8
        и выводит первичную сводку (типы, пропуски, размерность).
        """
        df = pd.read_csv(file_path, encoding='utf-8-sig')
        print("=== ПЕРВИЧНЫЙ АНАЛИЗ ДАТАСЕТА ===")
        print(f"Размерность данных: {df.shape[0]} строк, {df.shape[1]} колонок.")
        print("\nТипы данных и пропуски:")
        print(df.info())
        print("\nКоличество пропусков по колонкам:")
        print(df.isnull().sum())
        return df
