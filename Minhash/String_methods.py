from nltk import SnowballStemmer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import string
import re

stemmer = SnowballStemmer("russian")
stopwords_mass = stopwords.words('russian')

def delete_eng_word(string_req: str):
    new_string = ""
    en_word = ""

    for i in range(len(string_req)):
        ch = string_req[i]
        ch_ord = ord(ch)
        if ch_ord >= 97 and ch_ord <= 122:
            en_word = en_word + ch
        else:
            if len(en_word) > 0:
                new_string = new_string + lat2cyr(en_word)
                en_word = ""
            new_string = new_string + ch

    if len(en_word) > 0:
        new_string = new_string + lat2cyr(en_word)
    return new_string


def string_in_ordnung(string_req: str, with_numbers=False):
    # транслитерируем все англ слова

    string_req = delete_eng_word(string_req.lower())
    clean_new_next_str = string_req.translate(str.maketrans('', '', string.punctuation)).lower()
    filtered = ''.join([x for x in clean_new_next_str if x.isalnum() or x == " "])
    kjsbfsf = word_tokenize(filtered)
    str_split = lemmatizer(clean_string(kjsbfsf))
    if with_numbers:
        numbers, digits = share_number_massive(str_split)
        return " ".join(numbers), " ".join(digits)

    return " ".join(str_split)


def share_number_massive(list_of_strings_request):
    list_of_strings = []
    list_of_numbers = []
    digit = ""
    letter = ""

    for x in list_of_strings_request:
        for y in x:
            if y.isdigit():
                if len(letter) > 0:
                    list_of_strings.append(letter)
                    letter = ""
                digit = digit + y
            else:
                if len(digit) > 0:
                    list_of_numbers.append(digit)
                    digit = ""
                letter = letter + y

    if len(letter) > 0:
        list_of_strings.append(letter)
    if len(digit) > 0:
        list_of_numbers.append(digit)

    return list_of_numbers,  list_of_strings


def list_to_string(list_of_hash: list, list_of_strings: list, sub=False):
    for sublist in list_of_hash:
        its_list = bool(max(1 if type(x) == list else 0 for x in sublist))
        if its_list:
            subres = []
            list_to_string(sublist, subres)
            if len(subres) > 0:
                list_str = "{" + ','.join(str(x) for x in subres) + "}"
                list_of_strings.append(list_str)

        else:
            new_list = "{" + ','.join(str(x) for x in sublist) + "}"
            list_of_strings.append(new_list)



def clean_string(string_req):
    return [word for word in string_req if not word in stopwords_mass]


def lemmatizer(list_of_word: list):
    return [stemmer.stem(word) for word in list_of_word]


def lat2cyr(s_text: str):
    new_string = ""
    i = 0

    while i < len(s_text):  # Идем по строке слева направо. В принципе, подходит для обработки потока
        ch = s_text[i]
        if ch == "j" and i+1 < len(s_text):  # Префиксная нотация вначале
            i += 1  # преходим ко второму символу сочетания
            ch = s_text[i]
            match ch:
                case "o":
                    new_string = new_string + "ё"
                case "h":
                    if i+1 < len(s_text) and s_text[i+1] == "H":  # проверка на постфикс (вариант JHH)
                        new_string = new_string + "ъ"
                        i += 1  # пропускаем постфикс
                    else:
                        new_string = new_string + "ь"
                case "u":
                    new_string = new_string + "ю"
                case "a":
                    new_string = new_string + "я"

        elif i+1 < len(s_text) and s_text[i+1] == "h":  # Постфиксная нотация, требует информации о двух следующих символах. Для потока придется сделать обертку с очередью из трех символов.
            match ch:
                case "z":
                    new_string = new_string + "ж"
                case 'k':
                    new_string = new_string + "х"
                case 'c':
                    new_string = new_string + "ч"
                case 's':
                    if i+2 < len(s_text) and s_text[i+2] == "h":  # проверка на двойной постфикс
                        new_string = new_string + "щ"
                        i += 1  # пропускаем первый постфикс
                    else:
                        new_string = new_string + "ш"
                case 'e':
                    new_string = new_string + "э"
                case 'i':
                    new_string = new_string + "ы"

            i += 1  # пропускаем постфикс
        else:  # одиночные символы
            match ch:
                case 'a':
                    new_string = new_string + "а"
                case 'b':
                    new_string = new_string + "б"
                case 'v':
                    new_string = new_string + "в"
                case 'g':
                    new_string = new_string + "г"
                case 'd':
                    new_string = new_string + "д"
                case 'e':
                    new_string = new_string + "е"
                case 'z':
                    new_string = new_string + "з"
                case 'i':
                    new_string = new_string + "и"
                case 'y':
                    new_string = new_string + "й"
                case 'k':
                    new_string = new_string + "к"
                case 'l':
                    new_string = new_string + "л"
                case 'm':
                    new_string = new_string + "м"
                case 'n':
                    new_string = new_string + "н"
                case 'o':
                    new_string = new_string + "о"
                case 'p':
                    new_string = new_string + "п"
                case 'r':
                    new_string = new_string + "р"
                case 's':
                    new_string = new_string + "с"
                case 't':
                    new_string = new_string + "т"
                case 'u':
                    new_string = new_string + "у"
                case 'f':
                    new_string = new_string + "ф"
                case 'c':
                    new_string = new_string + "ц"
                case 'j':
                    new_string = new_string + "ж"
                case _:
                    new_string = new_string + ch

        i += 1  # переходим к следующему символу

    return new_string