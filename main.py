# Задача:
# Название - title
# Описание - description
# Срок выполнения - deadline
# Приоритет - priority (низкий, средний, высокий)
# Статус - is_done

from console_application import ConsoleApplication


try:
    c = ConsoleApplication()
    c.start()
except Exception as e:
    print("Произошла ошибка: ", e)
    exit(1)

