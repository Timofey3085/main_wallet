from wallet import Wallet, create_record, save_record_to_file, read_records_from_file, edit_record, calculate_balance, search_records
import datetime


def choose_action():
    """Выбор редактировать или создать новую запись"""
    all_records = read_records_from_file('records.txt')
    action = input("Выберите действие (1 - Редактировать запись, 2 - Добавить новую запись): ")
    if action == '1':
        # Редактирование записи
        date_to_edit: datetime = datetime.datetime.strptime(input("Введите дату для редактирования: "), '%d.%m.%Y')
        category_to_edit: str = input("Введите категорию для редактирования (Доход/Расход): ")
        amount_to_edit: int = int(input("Введите сумму для редактирования: "))
        description_to_edit: str = input("Введите описание для редактирования: ")

        if edit_record(all_records, date_to_edit, category_to_edit, amount_to_edit, description_to_edit):
            with open('records.txt', 'w') as file:
                for record in all_records:
                    file.write("Дата: {}\n".format(record.date.strftime('%d.%m.%Y')))
                    file.write("Категория: {}\n".format(record.category))
                    file.write("Сумма: {}\n".format(record.amount))
                    file.write("Описание: {}\n".format(record.description))
            print("Редактирование выполнено.")
        else:
            print("Запись для редактирования не найдена.")
    elif action == '2':
        # Добавление новой записи
        date: datetime = datetime.datetime.strptime(input("Введите дату: "), '%d.%m.%Y')
        category: str = input("Введите категорию (Доход/Расход): ")
        amount: int = int(input("Введите сумму: "))
        description: str = input("Введите описание: ")

        new_record = create_record(date, category, amount, description)
        save_record_to_file(new_record, 'records.txt')
        print("Новая запись добавлена.")
    else:
        print("Неверный выбор. Попробуйте еще раз.")


if __name__ == "__main__":
    choose_action()
