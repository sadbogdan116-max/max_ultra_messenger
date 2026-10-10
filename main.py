# Давлатов Мансур МT-202 Антонов Александр Мт-202
import os
import re
from collections import Counter
import pandas as pd

from parser import EntityParser
from refactorizer import TextRefactorizer
from tokenizer import TextTokenizer


def get_top_n_raw(texts, n=20):
    words = []
    for t in texts:
        tokens = re.findall(r'\S+', str(t).lower())
        words.extend(tokens)
    return Counter(words).most_common(n)


def get_top_n_lemmas(lemmas_series, n=20):
    all_lemmas = []
    for l_list in lemmas_series:
        all_lemmas.extend(l_list)
    return Counter(all_lemmas).most_common(n)


def main():
    input_file = "03_dostavka_i_logistika.csv"
    output_file = "clean_messages.csv"

    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Файл {input_file} не найден в текущей директории!")

    parser = EntityParser()
    refactorizer = TextRefactorizer()
    tokenizer = TextTokenizer()

    df = parser.load_dataset(input_file)

    
    print("\n=== ВЫПОЛНЕНИЕ ПРЕДОБРАБОТКИ СООБЩЕНИЙ ===")
    
    extracted_urls = []
    extracted_emails = []
    extracted_phones = []
    extracted_dates = []
    extracted_prices = []
    anonymized_texts = []
    clean_texts = []
    token_lists = []
    lemma_lists = []

    for _, row in df.iterrows():
        msg = str(row['message'])

       
        entities = parser.extract_entities(msg)
        extracted_urls.append(entities['urls'])
        extracted_emails.append(entities['emails'])
        extracted_phones.append(entities['phones'])
        extracted_dates.append(entities['dates'])
        extracted_prices.append(entities['prices'])

      
        anon = refactorizer.anonymize_text(msg, entities)
        anonymized_texts.append(anon)

        
        clean = refactorizer.build_clean_text(anon)
        clean_texts.append(clean)

       
        toks = tokenizer.tokenize(clean)
        token_lists.append(toks)

        
        lems = tokenizer.lemmatize(toks)
        lemma_lists.append(lems)

    
    df['original_text'] = df['message']
    df['urls'] = extracted_urls
    df['emails'] = extracted_emails
    df['phones'] = extracted_phones
    df['dates'] = extracted_dates
    df['prices'] = extracted_prices
    df['anonymized_text'] = anonymized_texts
    df['clean_text'] = clean_texts
    df['tokens'] = token_lists
    df['lemmas'] = lemma_lists

    
    print("\n" + "=" * 50)
    print("ТОР-20 СЛОВ ДО ОЧИСТКИ (Исходный текст):")
    print("=" * 50)
    top_raw = get_top_n_raw(df['original_text'], 20)
    for rank, (word, count) in enumerate(top_raw, 1):
        print(f"{rank:2d}. {word:<20} : {count}")

    print("\n" + "=" * 50)
    print("ТОР-20 СЛОВ ПОСЛЕ ОЧИСТКИ И НОРМАЛИЗАЦИИ (Леммы):")
    print("=" * 50)
    top_clean = get_top_n_lemmas(df['lemmas'], 20)
    for rank, (lemma, count) in enumerate(top_clean, 1):
        print(f"{rank:2d}. {lemma:<20} : {count}")

    columns_to_export = [
        'message_id', 'channel', 'created_at', 'original_text',
        'urls', 'emails', 'phones', 'dates', 'prices',
        'anonymized_text', 'clean_text', 'tokens', 'lemmas'
    ]
    df[columns_to_export].to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\nОбработанный датасет сохранен в '{output_file}'.")


if __name__ == "__main__":
    main()
