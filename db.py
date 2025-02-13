import datetime

from task import Task
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, TIMESTAMP

engine = create_engine("postgresql://postgres:memuna19641970@localhost:5432/python_db")

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now())

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    description = Column(String)
    deadline = Column(TIMESTAMP)
    priority = Column(String)
    is_done = Column(Boolean, default=False)
    deleted_at = Column(TIMESTAMP)

try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print("Ошибка во время миграции")


# C - create
def create_task(task):
    try:
        transformed_deadline = datetime.datetime.strptime(task.deadline, "%d-%m-%Y").date()
    except ValueError:
        print("Ошибка: неверный формат даты!")

    try:
        with Session(autoflush=False, bind=engine) as db:
            t = Task(
                user_id=task.user_id,
                title=task.title,
                description=task.description,
                deadline=transformed_deadline,
                priority=task.priority
            )
            db.add(t)
            db.commit()
            return t.id
    except Exception as e:
        print(f"Ошибка во сохранения задачи в бд: {e}")
        return None


def get_task_by_id(task_id, user_id):
    with Session(autoflush=False, bind=engine) as db:
        task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id, Task.deleted_at == None).first()
        
    if task is None:
        return None
    else:
        return task
    

def get_all_tasks(user_id):
    with Session(autoflush=False, bind=engine) as db:
        tasks = db.query(Task).filter(Task.user_id == user_id, Task.deleted_at == None).all()
        return tasks


def edit_task(task, user_id):
    try:
        transformed_deadline = datetime.datetime.strptime(task.deadline, "%d-%m-%Y").date()
    except ValueError:
        print("Ошибка: неверный формат даты!")


    with Session(autoflush=False, bind=engine) as db:
        task_db = db.query(Task).filter(Task.id == task.id, Task.user_id == user_id).first()

        if task_db is not None:
            task_db.title = task.title
            task_db.description = task.description
            task_db.deadline = transformed_deadline
            task_db.priority = task.priority
            db.commit()
            print("Task edit successfully")
        else:
            return None
        

def soft_delete_task(task_id, user_id):
    with Session(autoflush=False, bind=engine) as db:
        task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
        if task is not None:
            task.deleted_at = datetime.datetime.now()
            db.commit()
        else:
            print("Задача не найдена")


def hard_delete_task(task_id, user_id):
    with Session(autoflush=False, bind=engine) as db:
        task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
        if task is not None:
            db.delete(task)
            db.commit()
        else:
            print("Task is not found!!!")


def change_task_status(task_id, status, user_id):
    with Session(autoflush=False, bind=engine) as db:
        task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
        task.is_done = status
        db.commit()


def get_user_by_username_and_password(username, password):
    with Session(autoflush=False, bind=engine) as db:
        user = db.query(User).filter(User.username == username, User.password == password).first()
        return user


def get_user_by_username(username):
    with Session(autoflush=False, bind=engine) as db:
        user = db.query(User).filter(User.username == username).first()
        return user


def add_user(username, full_name, password):
    try:
        with Session(autoflush=False, bind=engine) as db:
            user = User(username = username, full_name = full_name, password = password )
            db.add(user)
            db.commit()
            
            return user.id
    except Exception as e:
        print("Ошибка при добавлении нового пользователя в бд:", e)
        return None


def get_deleted_tasks(user_id):
    with Session(autoflush=False, bind=engine) as db:
        tasks = db.query(Task).filter(Task.user_id == user_id, Task.deleted_at != None).all()

        if len(tasks)  == 0:

            print("У юзера нет удаленных задач")
        
            return None
        
        return tasks