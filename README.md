
### Замечание

В заготовке, которую нам предложили, уже было чтение **SCV** файла, и оно было реализовано методом **csv.reader**:
```
with open("phonebook_raw.csv") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
pprint(contacts_list)
```
