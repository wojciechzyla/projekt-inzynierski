from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from stempel import StempelStemmer
import re
import os
from enum import Enum
from typing import List
import shutil

class PrepOption(Enum):
    LOWERCASE = 1
    STOPWORDS = 2
    STEM = 3
    INTERPUNCTION = 4
    TOKENIZE_WORDS = 5
    RUBBISH = 6
    NUMBERS = 7
    TOKENIZE_SENTENCE = 8
    LEMMA = 9


def preprocess_document(document: str, options: List[PrepOption], language: str, stopwords_list: List[str] = None, stemmer=None):
    if language == "polish":
        if stopwords_list is None:
            raise ValueError("When using polish language, stopwords list must be provided")
        if stemmer is None:
            raise ValueError("When using polish language, stemmer object must be provided")
        stop = stopwords_list
        stemmer = stemmer
    elif language == "english":
        stop = stopwords.words("english")
        stemmer = PorterStemmer()
    else:
        raise ValueError("Unknown language")

    lemmatizer = WordNetLemmatizer()
    sentences_preprocessed = []
    if PrepOption.TOKENIZE_SENTENCE in options:
        sentences = sent_tokenize(document, language)
    else:
        sentences = [document]

    for sent in sentences:
        if PrepOption.INTERPUNCTION in options:
            sent = re.sub(r"[^-\w\s]", " ", sent)
            sent = re.sub(r"-", " ", sent)
        if PrepOption.LOWERCASE in options:
            sent = " ".join([word.lower() for word in sent.split()])
        if language == "english" and PrepOption.LEMMA in options:
            sent = " ".join([lemmatizer.lemmatize(word) for word in sent.split()])
        elif PrepOption.STEM in options:
            words_stemmed = []
            for word in sent.split():
                stemmed = stemmer.stem(word)
                stemmed = stemmed if stemmed is not None else ""
                words_stemmed.append(stemmed)
            sent = " ".join(words_stemmed)
        if PrepOption.RUBBISH in options:
            sent = re.sub(r"[^a-zA-Z0-9.,?!AaĄąBbCcĆćDdEeĘęFfGgHhIiJjKkLlŁłMmNnŃńOoÓóPpRrSsŚśTtUuWwYyZzŹźŻż\s]", " ", sent)
            sent = re.sub(r"\w*[0-9]+\w*", " ", sent)
        if PrepOption.NUMBERS in options:
            sent = re.sub(r"[0-9]", " ", sent)
        if PrepOption.STOPWORDS in options:
            sent = " ".join([word for word in sent.split() if word not in stop])
        sent = re.sub(r"\s{2,}", " ", sent)
        if PrepOption.TOKENIZE_WORDS in options:
            sent = word_tokenize(sent, "english")
        sentences_preprocessed.append(sent)

    if PrepOption.TOKENIZE_SENTENCE in options:
        result = sentences_preprocessed
    else:
        result = sentences_preprocessed[0]
    return result


def preprocess_bbc_for_bert_notebook(dataset_path: str, peprocessed_path: str, options: List[PrepOption]):
    classes = {'entertainment': 0, 'business': 1, 'sport': 2, 'politics': 3, 'tech': 4}
    unopened_files = 0
    unopened_files_list = []
    options = list(filter(lambda x: x != PrepOption.TOKENIZE_SENTENCE and x != PrepOption.TOKENIZE_WORDS, options))

    for cl in classes.keys():
        class_path = os.path.join(dataset_path, cl)
        files = os.listdir(class_path)
        prepr_class_path = os.path.join(peprocessed_path, cl)
        if not os.path.exists(prepr_class_path):
            os.makedirs(prepr_class_path)

        for filename in files:
            full_path = os.path.join(class_path, filename)
            full_path_prepr = os.path.join(prepr_class_path, filename)
            try:
                with open(full_path, 'r') as f:
                    txt = f.read()
                    preprocessed = preprocess_document(txt, options, "english")
            except UnicodeDecodeError:
                unopened_files += 1
                unopened_files_list.append(full_path)
                continue

            with open(full_path_prepr, 'w') as f:
                f.write(preprocessed)

    log_unopened_files = ""
    for f in unopened_files_list:
        log_unopened_files += f"{f}\n"
    print(f"Couldn't read {unopened_files} files:\n{log_unopened_files}")


def preprocess_bbc_to_dict(dataset_path, options: List[PrepOption], sentence_tokenize=False):
    classes = ["business", "entertainment", "politics", "sport", "tech"]
    preprocessed_files = {
        "business":[],
        "entertainment":[],
        "politics":[],
        "sport":[],
        "tech":[]
    }
    
    unopened_files = 0
    unopened_files_list = []
    for cl in classes:
        class_path = os.path.join(dataset_path, cl)
        for filename in os.listdir(class_path):
            file_path = os.path.join(class_path,filename)
            with open(file_path, "r") as f:
                try:
                    txt = f.read()
                    if sentence_tokenize:
                        sentences = sent_tokenize(txt, "english")
                        sentences_preprocessed = []
                        for s in sentences:
                            preprocessed = preprocess_document(s, options, "english")
                            sentences_preprocessed.append(preprocessed)
                        preprocessed_files[cl].append(sentences_preprocessed)
                    else:
                        preprocessed = preprocess_document(txt, options, "english")
                        preprocessed_files[cl].append(preprocessed)
                except UnicodeDecodeError:
                    unopened_files += 1
                    unopened_files_list.append(file_path)
                    continue
                    
    log_unopened_files = ""
    for f in unopened_files_list:
        log_unopened_files += f"{f}\n"
    print(f"Couldn't read {unopened_files} files:\n{log_unopened_files}")
    return preprocessed_files

                
def remove_dir(path):
    shutil.rmtree(path)


def preprocess_klej(dataset, options, stopwords_path):
    stop = []
    with open(stopwords_path, "r") as f:
        for line in f:
            line = line if line[-1] != "\n" else line[:-1]
            stop.append(line)
    stemmer = StempelStemmer.polimorf()
    for i in range(dataset.shape[0]):
        dataset.at[i, "text"] = preprocess_document(dataset.iloc[i]["text"], options, "polish", stop, stemmer)
    return dataset
