# Задача:
# Название - title
# Описание - description
# Срок выполнения - deadline
# Приоритет - priority (низкий, средний, высокий)
# Статус - is_done

from console_application import ConsoleApplication
from db import migrate_tables, close_db_conn

try:
    migrate_tables()

    c = ConsoleApplication()
    c.start()
    close_db_conn()
except Exception as e:
    print("Произошла ошибка: ", e)
    exit(1)

