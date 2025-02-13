
class Task:
    def __init__(self):
        self.__task_id = None
        self.__title = None
        self.__description = None
        self.__deadline = None
        self.__priority = None
        self.__is_done = False
        self.__user_id = None

    @property
    def task_id(self):
        return self.__task_id

    @task_id.setter
    def task_id(self, task_id):
        self.__task_id = task_id

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id):
        self.__user_id = user_id

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        if len(title) == 0:
            print('Заголовок не может быть пустым')
        elif len(title) > 16:
            print("Слишком длинный заголовок (макс. 16 символов)")
        else:
            self.__title = title

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        if len(description) == 0:
            print('Описание не может быть пустым')
        elif len(description) > 64:
            print("Слишком длинное описание (макс. 64 символа")
        else:
            self.__description = description

    @property
    def deadline(self):
        return self.__deadline

    @deadline.setter
    def deadline(self, deadline):
        # if len(deadline) == 0:
        #     print('Дедлайн не может быть пустым')
        # elif len(deadline) != 10:
        #     print("Не правильный формат даты (DD-MM-YYYY)")
        # else:
        self.__deadline = deadline

    @property
    def priority(self):
        return self.__priority

    @priority.setter
    def priority(self, priority):
        values = ["низкий", "средний", "высокий"]
        if priority not in values:
            print("Некорректное значение приоритета")
        else:
            self.__priority = priority

    @property
    def is_done(self):
        return self.__is_done

    @is_done.setter
    def is_done(self, is_done):
        # if is_done is True and self.__is_done is True:
        #     print("Задача уже выполнена!!!")
        # elif is_done is False and self.__is_done is False:
        #     print("Задача и так выполнена!!!!")
        # else:
        self.__is_done = is_done
