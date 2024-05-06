import datetime
import unittest


class TestWallet(unittest.TestCase):

    def test_create_record(self):
        """Тестирование создания записи."""
        date = datetime.datetime.strptime('02.02.2000', '%d.%m.%Y')
        record = create_record(date, 'Доход', 1000, 'Зарплата')
        self.assertIsInstance(record, Wallet)
        self.assertEqual(record.date, date)
        self.assertEqual(record.category, 'Доход')


class Wallet:
    """Класс кошелек"""
    def __init__(self, date: datetime, category: str, amount: int, description: str) -> None:
        """Инициализация"""
        self.date: datetime = date
        self.category: str = category
        self.amount: float = amount
        self.description: str = description


def create_record(date: datetime, category: str, amount: int, description: str) -> Wallet:
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


def edit_record(records, date: datetime, category: str, amount: int, description: str) -> bool:
    """Редактирование записи"""
    for record in records:
        if (record.date == date and record.category == category and
                record.amount == amount and record.description == description):
            print("Запись найдена. Введите новые данные.")
            new_date: datetime = input("Введите новую дату: ")
            new_category: str = input("Введите новую категорию (Доход/Расход): ")
            new_amount: int = int(input("Введите новую сумму: "))
            new_description: str = input("Введите новое описание: ")
            record.date: datetime = new_date
            record.category: str = new_category
            record.amount: int = new_amount
            record.description: str = new_description
            print("Запись обновлена.")
            return True
    print("Запись не найдена.")
    return False


# Переменные для редактирования записи
date_to_edit = datetime.datetime.strptime(input("Введите дату для редактирования: "), '%d.%m.%Y')
category_to_edit: str = input("Введите категорию для редактирования (Доход/Расход): ")
amount_to_edit: int = int(input("Введите сумму для редактирования: "))
description_to_edit: str = input("Введите описание для редактирования: ")

# Создание новой записи
date: datetime = datetime.datetime.strptime(input("Введите дату: "), '%d.%m.%Y')
category: str = input("Введите категорию (Доход/Расход): ")
amount: int = int(input("Введите сумму: "))
description: str = input("Введите описание: ")

new_record = create_record(date, category, amount, description)
save_record_to_file(new_record, 'records.txt')

# Чтение всех записей из файла
all_records = read_records_from_file('records.txt')

# Редактирование записи
if edit_record(all_records, date_to_edit, category_to_edit, amount_to_edit, description_to_edit):
    # Сохраняем обновленные записи обратно в файл
    with open('records.txt', 'w') as file:
        for record in all_records:
            file.write("Дата: {}\n".format(record.date))
            file.write("Категория: {}\n".format(record.category))
            file.write("Сумма: {}\n".format(record.amount))
            file.write("Описание: {}\n\n".format(record.description))
else:
    print("Редактирование не выполнено.")


    def search_records(records, search_term: str, search_type: str) -> list[Wallet]:
        """Поиск записей по категории, дате или сумме."""
        search_results = []
        for record in records:
            if search_type == 'категория' and search_term.lower() in record.category.lower():
                search_results.append(record)
            elif search_type == 'дата' and search_term == record.date.strftime('%d.%m.%Y'):
                search_results.append(record)
            elif search_type == 'сумма' and search_term == str(record.amount):
                search_results.append(record)
        return search_results


    # Пример использования функции поиска
    search_type = input("Введите тип поиска (категория/дата/сумма): ").lower()
    search_term = input("Введите искомое значение: ")

    found_records = search_records(all_records, search_term, search_type)
    for record in found_records:
        print(
            f"Дата: {record.date.strftime('%d.%m.%Y')}, "
            f"Категория: {record.category}, "
            f"Сумма: {record.amount}, Описание: {record.description}")

# Расчет баланса
income, expenses, balance = calculate_balance(all_records)
current_date = datetime.datetime.now()
current_date_only = current_date.date()

print("Текущая дата:", current_date_only)
print("Доходы: ", income)
print("Расходы: ", expenses)
print("Баланс: ", balance)
