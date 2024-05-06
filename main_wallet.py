import datetime


class Wallet:
    """Класс кошелек"""
    def __init__(self, date: datetime, category: str, amount: float, description: str) -> None:
        """Инициализация"""
        self.date: datetime = date
        self.category: str = category
        self.amount: float = amount
        self.description: str = description


def create_record(date: datetime, category: str, amount: float, description: str) -> Wallet:
    """Создание записи"""
    return Wallet(date, category, amount, description)


def save_record_to_file(record, filename) -> None:
    """Сохранение записи в фаил"""
    with open(filename, 'a') as file:
        file.write("Дата: {}\n".format(record.date))
        file.write("Категория: {}\n".format(record.category))
        file.write("Сумма: {}\n".format(record.amount))
        file.write("Описание: {}\n\n".format(record.description))


def read_records_from_file(filename) -> list[Wallet]:
    """Чтение записи из файла"""
    records = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        record_info = {}
        for line in lines:
            if line.strip() != "":
                key, value = line.split(": ")
                record_info[key] = value.strip()
            else:
                records.append(Wallet(record_info['Дата'], record_info['Категория'],
                                      int(record_info['Сумма']), record_info['Описание']))
                record_info = {}
    return records


def calculate_balance(records) -> tuple[int, int, int]:
    """Расчет баланса"""
    income: int = 0
    expenses: int = 0
    for record in records:
        if record.category == 'Доход':
            income += record.amount
        elif record.category == 'Расход':
            expenses += record.amount
    balance = income - expenses
    return income, expenses, balance


date: datetime = input("Введите дату: ")
category: str = input("Введите категорию (Доход/Расход): ")
amount: float = int(input("Введите сумму: "))
description: str = input("Введите описание: ")

new_record = create_record(date, category, amount, description)
save_record_to_file(new_record, 'records.txt')

all_records = read_records_from_file('records.txt')
income, expenses, balance = calculate_balance(all_records)
current_date = datetime.datetime.now()
current_date_only = current_date.date()


print("Текущая дата:", current_date_only)
print("Доходы: ", income)
print("Расходы: ", expenses)
print("Баланс: ", balance)
