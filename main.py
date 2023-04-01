
from pprint import pprint
import csv
import re

def find_names(line):
    """
    Ищет Фамилию Имя Отчество в строке
    :param line:
    :return:
    """
    words = re.findall("[а-я]+", line, re.I)
    if len(words) > 2: return words[0], words[1], words[2]
    if len(words) > 1: return words[0], words[1], ""
    if len(words) > 0: return words[0], "", ""
    return None, None, None

def normalize_phonenum(phnum):
    """
    Нормализует номер телефона (Приводит к виду +7(999)999-99-99)
    :param phnum:
    :return:
    """
    words = re.findall("[\d+\-() ]+", phnum)
    if len(words) == 0: return ""
    if len(words) > 0:
        words[0] = re.sub("[+\- ()]", "", words[0])
        words[0] = "+7(" + words[0][1:4] + ')' + words[0][4:7] + '-' + words[0][7:9] + '-' + words[0][9:11]
        if len(words) > 1:
            words[1] = re.sub("[+\- ()]", "", words[1])
            words[0] = f"{words[0]} доб.{words[1]}"
    return words[0]

def compare_and_join(l1, l2):
    """
    Сравнивает две записи о контактах
    Совпадающими считаются только полные тёзки
    Если нашлось совпадение, выводится сообщение и поля двух записей сливаются с учётом заполненности
    :param l1:
    :param l2:
    :return:
    """
    if l1[0] == l2[0] and l1[1] == l2[1] and l1[2] == l2[2]:
        print("Дубль:", l1[0:3])
        if l1[3] == "": l1[3] = l2[3]
        if l1[4] == "": l1[4] = l2[4]
        if l1[5] == "": l1[5] = l2[5]
        if l1[6] == "": l1[6] = l2[6]
        return True
    return False

## Читаем адресную книгу в формате CSV в список contacts_list:
with open("phonebook_raw.csv") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
pprint(contacts_list)

## 1. Выполните пункты 1-3 задания.
## Ваш код
temp_list = []
for l in contacts_list:
    # Нормализуем фамилию, имя отчество
    lname, name, sname = find_names(' '.join(l[0:3]))
    if lname:
        # Нормализуем номер телефона
        phone_num = normalize_phonenum(l[5])
        temp_list.append([lname, name, sname, l[3], l[4], phone_num, l[6]])

# Удаляем дубли
temp_list = sorted(temp_list, key=lambda d: (d[0], d[1], d[2]))
contacts_list, i = [], 0
while i < len(temp_list):
    while i + 1 < len(temp_list) and compare_and_join(temp_list[i], temp_list[i + 1]):
        del temp_list[i + 1]
    contacts_list.append(temp_list[i])
    i += 1
print("================ Результат =================")
pprint(contacts_list)

## 2. Сохраните получившиеся данные в другой файл.
## Код для записи файла в формате CSV:
with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')

    ## Вместо contacts_list подставьте свой список:
    datawriter.writerows(contacts_list)