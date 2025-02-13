from task import Task
from db import create_task, get_all_tasks, get_task_by_id, edit_task, soft_delete_task, change_task_status, \
    get_user_by_username_and_password, get_user_by_username, add_user, get_deleted_tasks


class ConsoleApplication:
    def __init__(self):
        self.authorized_user_id = None

    def add_task(self):
        print("--------------Добавление задачи--------------")
        t = Task()
        t.user_id = self.authorized_user_id

        title = input("Введи название задачи: ")
        t.title = title

        description = input("Введи описание задачи: ")
        t.description = description

        deadline = input("Введи дедлайн задачи: ")
        t.deadline = deadline

        priority_id = int(input("Введи приоритет задачи (низкий(1), средний(2), высокий(3)): "))
        priorities = ["низкий", "средний", "высокий"]
        if 1 > priority_id or priority_id > 3:
            print("Вы ввели неправильный ID приоритета!")
            return
        t.priority = priorities[priority_id - 1]

        # self.tasks.append(t)
        task_id = create_task(t)
        if task_id is None:
            print("Ошибка во время создания задачи!")
            return
        print(f"--------------Задача {task_id} успешно  добавлена--------------")
        # self.current_id += 1

    def print_tasks(self):
        user_id = self.authorized_user_id
        tasks = get_all_tasks(user_id)
        if len(tasks) == 0:
            print("У вас нет задач!")
            return
        
        print("--------------Список ваших задач:--------------")
        for task in tasks:
            print(f"{task.id}. {task.title}")
        print("-----------------------------------------------")

    def edit_task(self):
        user_id = self.authorized_user_id
        target_task_id = int(input("Введи ID задачи которую хотите изменить: "))

        task = get_task_by_id(target_task_id, user_id)
        if task is None:
            print(f"Нет задачи с ID = {target_task_id}")
            return

        title = input("Введи название задачи: ")
        task.title = title

        description = input("Введи описание задачи: ")
        task.description = description

        deadline = input("Введи дедлайн задачи: ")
        task.deadline = deadline

        priority = input("Введи приоритет задачи (низкий, средний, высокий): ")
        task.priority = priority

        edit_task(task, self.authorized_user_id)

    def print_task_by_id(self):
        target_task_id = int(input("Введи ID задачи: "))
        user_id = self.authorized_user_id

        task = get_task_by_id(target_task_id, user_id)
        if task is None:
            print(f"Нет задачи с ID = {target_task_id}")
        else:
            print(f"--------------Задача с ID = {target_task_id}--------------")
            print(f"Название: {task.title}")
            print(f"Описание: {task.description}")
            print(f"Дедлайн: {task.deadline}")
            print(f"Приоритет: {task.priority}")
            if task.is_done:
                print(f"Статус: Выполнено")
            else:
                print(f"Статус: Не выполнено")

    def delete_task(self):
        target_task_id = int(input("Введи ID задачи: "))
        user_id = self.authorized_user_id

        task = get_task_by_id(target_task_id, user_id)
        if task is None:
            print(f"Нет задачи с ID = {target_task_id}")
            return

        soft_delete_task(target_task_id, user_id)
        print(f"----Задача с ID = {target_task_id} успешно удалена!")

    def change_task_status(self):
        target_task_id = int(input("Введи ID задачи: "))
        user_id = self.authorized_user_id

        task = get_task_by_id(target_task_id, user_id)
        if task is None:
            print(f"Нет задачи с ID = {target_task_id}")
            return

        status_id = int(input("Введите новый статус задачи (1 - Выполнено / 0 - не выполнено): "))
        if status_id == 0:
            change_task_status(target_task_id, False, self.authorized_user_id)
        elif status_id == 1:
            change_task_status(target_task_id, True, self.authorized_user_id)
        else:
            print("Вы ввели несуществующий статус!")


    def print_deleted_tasks(self):
        user_id = self.authorized_user_id
        tasks = get_deleted_tasks(user_id)
        if tasks is None:
            return
        print("--------------Список удаленных задач:--------------")
        for task in tasks:
            print(f"{task.id}. {task.title} : {task.description}")
        print("-----------------------------------------------")


    def main_menu(self):
        print("Добро пожаловать в Todo-List-App!")
        while True:
            print("-----------------------------------------------")
            print("Главное меню:")
            print("1. Добавить новую задачу")
            print("2. Вывести список задач")
            print("3. Редактировать задачу")
            print("4. Вывести задачу по ID")
            print("5. Удалить задачу по ID")
            print("6. Пометить задачу Выполнено / Не выполнено")
            print("7. Корзина (вывод удаленных задач)")
            print("0. Выход")
            cmd = int(input("Выберите нужную команду: "))

            if cmd == 0:
                self.authorized_user_id = None
                print("До скорой встречи!)")
                break
            elif cmd == 1:
                self.add_task()
            elif cmd == 2:
                self.print_tasks()
            elif cmd == 3:
                self.edit_task()
            elif cmd == 4:
                self.print_task_by_id()
            elif cmd == 5:
                self.delete_task()
            elif cmd == 6:
                self.change_task_status()
            elif cmd == 7:
                self.print_deleted_tasks()
            else:
                print("Вы ввели несуществующую команду!!!")
            print("-----------------------------------------------")

    def sign_in(self):
        username = input("Введите свой логин: ")
        password = input("Введите свой пароль: ")

        user = get_user_by_username_and_password(username, password)
        if user is None:
            print("Неправильный логин или пароль!")
            return
        else:
            user_id, full_name = user.id, user.full_name
            self.authorized_user_id = user_id
            print(f"С возвращением {full_name}")
            self.main_menu()

    def sign_up(self):
        # 1. Получить логин который хочет пользователь
        username = input("Введите свой логин: ")
        if len(username) == 0:
            print("Поле логин не может быть пустым!")
            return
        # 2. Проверить свободен ли этот логин
        user = get_user_by_username(username)
        if user is not None:
            print("Пользователь с таким логином уже существует")
            return

        # 3. Проверить не пустой ли пароль
        password = input("Введите пароль: ")
        if len(password) < 8:
            print("Пароль должен состоять минимум из 8-и символов")
            return

        # 4. Проверить не пустое ли ФИО
        full_name = input("Введите свое ФИО: ")
        if len(full_name) == 0:
            print("Поле ФИО не может быть пустым")
            return

        # 5. Создать пользователя
        user_id = add_user(username, full_name, password)
        if user_id is None:
            print("Что-то пошло не так!")
        else:
            print("Вы успешно зарегистрированы!")

    def start(self):
        while True:
            print("-----------------------------------------------")
            print("1. Вход")
            print("2. Регистрация")
            print("0. Выход")
            cmd = int(input("Выберите нужную команду: "))
            if cmd == 0:
                print("До встречи!")
                break
            elif cmd == 1:
                self.sign_in()
            elif cmd == 2:
                self.sign_up()
            else:
                print("Вы ввели несуществующую команду!")
                break
