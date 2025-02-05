import datetime

import psycopg2
from task import Task

conn = psycopg2.connect(dbname="python_db", host="localhost", user="postgres", password="memuna19641970", port=5432)

conn.autocommit = True
cursor = conn.cursor()


def migrate_tables():
    try:
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users
            (
                id         SERIAL PRIMARY KEY,
                full_name  VARCHAR,
                username   VARCHAR UNIQUE NOT NULL,
                password   VARCHAR        NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );""")
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tasks
                    (
                        id          SERIAL PRIMARY KEY,
                        user_id     INT NOT NULL,
                        title       VARCHAR,
                        description TEXT,
                        deadline    TIMESTAMP,
                        priority    VARCHAR,
                        is_done     BOOLEAN DEFAULT false,
                        deleted_at  TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    );""")
    except Exception as e:
        print(f"Ошибка во время миграции: {e}")


def close_db_conn():
    cursor.close()
    conn.close()


# C - create
def create_task(task):
    try:
        transformed_deadline = datetime.datetime.strptime(task.deadline, "%d-%m-%Y").date()
    except ValueError:
        print("Ошибка: неверный формат даты!")

    try:
        sql_query = """
        INSERT INTO tasks (user_id, title, description, deadline, priority)
        VALUES (%s, %s, %s, %s, %s) RETURNING id;"""
        cursor.execute(sql_query, (
            task.user_id,
            task.title,
            task.description,
            transformed_deadline,
            task.priority
        ))
        id_tuple = cursor.fetchone()
        return id_tuple[0]
    except Exception as e:
        print(f"Ошибка во сохранения задачи в бд: {e}")
        return None


def get_task_by_id(task_id, user_id):
    sql_query = """SELECT id, title, description, deadline, priority, is_done
        FROM tasks WHERE id = %s AND deleted_at IS NULL and user_id = %s;"""

    cursor.execute(sql_query, (task_id, user_id))
    task_tuple = cursor.fetchone()

    if task_tuple is None:
        return None
    else:
        t = Task()
        t.task_id = task_tuple[0]
        t.title = task_tuple[1]
        t.description = task_tuple[2]
        t.deadline = task_tuple[3]
        t.priority = task_tuple[4]
        t.is_done = task_tuple[5]
        return t


def get_all_tasks(user_id):
    sql_query = """SELECT id, title, description, deadline, priority, is_done
        FROM tasks WHERE deleted_at IS NULL AND user_id = %s ORDER BY id;"""

    cursor.execute(sql_query, (user_id,))

    tasks_tuple = cursor.fetchall()
    # (
    #   (1, "Task1", "Desc1", "10-10-2025", "низкий", True ),
    #   (2, "Task2", "Desc2", "11-10-2025", "низкий",  False )
    # )

    tasks = list()
    for task_tuple in tasks_tuple:
        t = Task()
        t.task_id = task_tuple[0]
        t.title = task_tuple[1]
        t.description = task_tuple[2]
        t.deadline = task_tuple[3]
        t.priority = task_tuple[4]
        t.is_done = task_tuple[5]
        tasks.append(t)

    return tasks


def edit_task(task, user_id):
    try:
        transformed_deadline = datetime.datetime.strptime(task.deadline, "%d-%m-%Y").date()
    except ValueError:
        print("Ошибка: неверный формат даты!")

    sql_query = """UPDATE tasks
        SET title       = %s,
            description = %s,
            deadline    = %s,
            priority    = %s
        WHERE id = %s 
        AND user_id = %s;"""

    cursor.execute(sql_query, (
        task.title,
        task.description,
        transformed_deadline,
        task.priority,
        task.task_id,
        user_id)
         )

    # try:
    #     conn = self.connect()
    #     if conn is None:
    #         return
    #     cursor = conn.cursor()
    #     query = "SELECT * FROM tasks WHERE task_id = %s;"
    #     cursor.execute(query, (task_id,))
    #     result = cursor.fetchone()
    #     if result is None:
    #         print(f"Задача с ID {task_id} не найдена")
    #     else:
    #         task = Task(result[0])
    #         task.title = result[1]
    #         task.description = result[2]
    #         task.deadline = result[3]
    #         task.priority = result[4]
    #         task.is_done = result[5]
    #         cursor.close()
    #         conn.close()
    #         return task
    # except psycopg2.Error as e:
    #     print(f"Ошибка при получении задачи: {e}")
    # finally:
    #     if conn:
    #         conn.close()


def soft_delete_task(task_id, user_id):
    sql_query = """UPDATE tasks
        SET deleted_at = CURRENT_TIMESTAMP
        WHERE id = %s AND user_id = %s;"""

    cursor.execute(sql_query, (task_id, user_id))


def hard_delete_task(task_id, user_id):
    sql_query = """DELETE FROM tasks WHERE id = %s AND user_id = %s;"""

    cursor.execute(sql_query, (task_id,))


def change_task_status(task_id, status, user_id):
    sql_query = """UPDATE tasks SET is_done = %s WHERE id = %s AND user_id = %s;"""

    cursor.execute(sql_query, (status, task_id, user_id))


def get_user_by_username_and_password(username, password):
    sql_query = """SELECT id, full_name FROM users WHERE username = %s AND password = %s;"""
    cursor.execute(sql_query, (username, password))

    return cursor.fetchone()


def get_user_by_username(username):
    sql_query = """SELECT id, full_name FROM users WHERE username = %s;"""
    cursor.execute(sql_query, (username,))

    return cursor.fetchone()


def add_user(username, full_name, password):
    try:
        sql_query = """
        INSERT INTO users (username, full_name, password) 
        VALUES (%s, %s, %s) RETURNING id;"""
        cursor.execute(sql_query, (username, full_name, password))

        id_tuple = cursor.fetchone()
        return id_tuple[0]
    except Exception as e:
        print("Ошибка при добавлении нового пользователя в бд:", e)
        return None


def get_deleted_tasks(user_id):
    sql_query = """SELECT id, title, description, deadline, priority, is_done
        FROM tasks WHERE deleted_at IS NOT NULL AND user_id = %s ORDER BY id;"""

    cursor.execute(sql_query, (user_id,))

    tasks_tuple = cursor.fetchall()

    if len(tasks_tuple)  == 0:
        
        print("Удаленных задач нет")
        
        return None
    else:
        
        tasks = list()
        for task_tuple in tasks_tuple:
            t = Task()
            t.task_id = task_tuple[0]
            t.title = task_tuple[1]
            t.description = task_tuple[2]
            t.deadline = task_tuple[3]
            t.priority = task_tuple[4]
            t.is_done = task_tuple[5]
            tasks.append(t)

        return tasks