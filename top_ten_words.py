import os
from chardet.universaldetector import UniversalDetector


def get_files():
    result = []
    for name in os.listdir("./"):
        if name.endswith(".txt"):
            result.append(name)
    return result


def get_encoding_from_files(files):
    result = {}
    for name in files:
        detector = UniversalDetector()
        with open(name, 'rb') as fh:
            for line in fh:
                detector.feed(line)
                if detector.done:
                    break
        detector.close()
        result[name] = detector.result
    return result


def get_words_frequency(string, len_limit=0):
    word_frequency = {}
    for word in string:
        if len(word) > len_limit:
            if word in word_frequency:
                word_frequency[word] += 1
            else:
                word_frequency[word] = 1
    return word_frequency


def get_top_words(string, n, len_limit=0):
    words_frequency = get_words_frequency(string, len_limit)
    frequency = sorted(words_frequency.values(), reverse=True)
    top = {}
    for i in range(n):
        top[frequency[i]] = []
    for word, frequency in words_frequency.items():
        if frequency in top:
            top[frequency].append(word)
    top_words = {}
    for frequency, words in top.items():
        for el in words:
            top_words[el] = frequency
            if len(top_words) == n:
                break
        if len(top_words) == n:
            break
    return top_words


n = int(input("Введите количество слов в топ: "))  # 10
len_limit = int(input("Введите ограничение на длину слова: "))  # 6
encodings = get_encoding_from_files(get_files())
for file_name, result_encoding in encodings.items():
    with open(file_name, encoding=result_encoding["encoding"]) as f:
        top_words = get_top_words(f.read().split(), n, len_limit)
        print("Для файла {} топ {} часто встречаемых слов длиннее {} симолов:".format(file_name,
                                                                                      n,
                                                                                      len_limit))
        text = '{}. "{}", количество повторений - {}'
        index = 1
        for word, frequency in top_words.items():
            print(text.format(index, word, frequency))
            index += 1
        print()
