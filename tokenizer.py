# Исаев Максим 

import re
from typing import List

DEFAULT_STOP_WORDS = {
    'и', 'в', 'во', 'не', 'что', 'он', 'на', 'я', 'с', 'со', 'как', 'а', 'то', 'все', 'она',
    'так', 'его', 'но', 'да', 'ты', 'к', 'у', 'же', 'вы', 'за', 'бы', 'по', 'только', 'ее',
    'мне', 'было', 'вот', 'от', 'меня', 'еще', 'ещё', 'о', 'из', 'ему', 'теперь', 'когда',
    'даже', 'ну', 'вдруг', 'ли', 'если', 'уже', 'или', 'ни', 'быть', 'был', 'него', 'до',
    'вас', 'нибудь', 'опять', 'уж', 'вам', 'ведь', 'там', 'потом', 'себя', 'ничего', 'ей',
    'может', 'они', 'тут', 'где', 'есть', 'надо', 'ней', 'для', 'мы', 'тебя', 'их', 'чем',
    'была', 'сам', 'чтоб', 'без', 'будто', 'чего', 'раз', 'тоже', 'себе', 'под', 'будет',
    'ж', 'тогда', 'кто', 'этот', 'того', 'потому', 'этого', 'какой', 'совсем', 'ним', 'здесь',
    'этом', 'один', 'почти', 'мой', 'тем', 'чтобы', 'нее', 'сейчас', 'были', 'куда', 'зачем',
    'всех', 'никогда', 'можно', 'при', 'наконец', 'два', 'об', 'другой', 'хоть', 'после',
    'над', 'больше', 'тот', 'через', 'эти', 'нас', 'про', 'всего', 'них', 'какая', 'много',
    'разве', 'три', 'эту', 'моя', 'впрочем', 'хорошо', 'свою', 'этой', 'перед', 'иногда',
    'лучше', 'чуть', 'том', 'нельзя', 'такой', 'им', 'более', 'всегда', 'конечно', 'всю',
    'между', 'это'
}


class TextTokenizer:
    def __init__(self, custom_stop_words=None):
        self.stop_words = set(DEFAULT_STOP_WORDS)
        if custom_stop_words:
            self.stop_words.update(custom_stop_words)

        self.lemmatizer = None
        self._init_lemmatizer()

    def _init_lemmatizer(self):
        try:
            import pymorphy3
            self.morph = pymorphy3.MorphAnalyzer()
            self.lemmatizer = lambda w: self.morph.parse(w)[0].normal_form
            return
        except ImportError:
            pass

        try:
            import pymorphy2
            self.morph = pymorphy2.MorphAnalyzer()
            self.lemmatizer = lambda w: self.morph.parse(w)[0].normal_form
            return
        except ImportError:
            pass

        try:
            from nltk.stem.snowball import RussianStemmer
            stemmer = RussianStemmer()
            self.lemmatizer = lambda w: stemmer.stem(w)
        except Exception:
            self.lemmatizer = lambda w: w

    def tokenize(self, text: str) -> List[str]:
        if not text:
            return []

        raw_words = re.findall(r'\b[а-яёa-z0-9]+\b', text.lower())
        tokens = [
            w for w in raw_words
            if w not in self.stop_words and len(w) > 1 and not w.isdigit()
        ]
        return tokens

    def lemmatize(self, tokens: List[str]) -> List[str]:
        return [self.lemmatizer(token) for token in tokens]
