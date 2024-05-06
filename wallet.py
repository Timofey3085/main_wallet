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
    """Сохранение записи в файл"""
    with open(filename, 'a') as file:
        file.write("Дата: {}\n".format(record.date.strftime('%d.%m.%Y')))
        file.write("Категория: {}\n".format(record.category))
        file.write("Сумма: {}\n".format(record.amount))
        file.write("Описание: {}\n\n".format(record.description))


def read_records_from_file(filename) -> list[Wallet]:
    """Чтение записей из файла"""
    records = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        record_info = {}
        for line in lines:
            if line.strip() != "":
                key, value = line.split(": ")
                record_info[key] = value.strip()
            else:
                if 'Дата' in record_info and 'Категория' in record_info and 'Сумма' in record_info and 'Описание' in record_info:
                    records.append(
                        Wallet(datetime.datetime.strptime(record_info['Дата'], '%d.%m.%Y'), record_info['Категория'],
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
        if record.date == date and record.category == category and record.amount == amount and record.description == description:
            print("Запись найдена. Введите новые данные.")
            new_date_str = input("Введите новую дату в формате (дд.мм.гггг): ")
            new_date = datetime.datetime.strptime(new_date_str, '%d.%m.%Y')
            new_category = input("Введите новую категорию (Доход/Расход): ")
            new_amount = int(input("Введите новую сумму: "))
            new_description = input("Введите новое описание: ")
            record.date = new_date
            record.category = new_category
            record.amount = new_amount
            record.description = new_description
            print("Запись обновлена.")
            return True
    print("Запись не найдена.")
    return False


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


all_records = read_records_from_file('records.txt')

print("Что вы хотите сделать?")
print("1. Добавить новую запись")
print("2. Редактировать запись")
print("3. Поиск записи")
choice = int(input("Введите номер действия: "))

if choice == 1:
    date_str = input("Введите дату записи в формате (дд.мм.гггг): ")
    date = datetime.datetime.strptime(date_str, '%d.%m.%Y')
    category = input("Введите категорию (Доход/Расход): ")
    amount = int(input("Введите сумму: "))
    description = input("Введите описание: ")
    new_record = create_record(date, category, amount, description)
    save_record_to_file(new_record, 'records.txt')

elif choice == 2:
    date_to_edit_str = input("Введите дату записи для редактирования в формате (дд.мм.гггг): ")
    date_to_edit = datetime.datetime.strptime(date_to_edit_str, '%d.%m.%Y')
    category_to_edit = input("Введите категорию для редактирования (Доход/Расход): ")
    amount_to_edit = int(input("Введите сумму для редактирования: "))
    description_to_edit = input("Введите описание для редактирования: ")
    edit_record(all_records, date_to_edit, category_to_edit, amount_to_edit, description_to_edit)

elif choice == 3:
    search_type = input("Введите тип поиска (категория/дата/сумма): ").lower()
    search_term = input("Введите искомое значение: ")
    found_records = search_records(all_records, search_term, search_type)
    for record in found_records:
        print(
            f"Дата: {record.date.strftime('%d.%m.%Y')}, Категория: {record.category}, Сумма: {record.amount}, Описание: {record.description}")

income, expenses, balance = calculate_balance(all_records)
current_date = datetime.datetime.now()
current_date_only = current_date.date()

print("Текущая дата:", current_date_only)
print("Доходы: ", income)
print("Расходы: ", expenses)
print("Баланс: ", balance)