"""
Напишите модуль find_athlete.py поиска ближайшего к пользователю атлета. Логика работы модуля такова:

запросить идентификатор пользователя;
если пользователь с таким идентификатором существует в таблице user, то вывести на экран двух атлетов: ближайшего по дате рождения к данному пользователю и ближайшего по росту к данному пользователю;
если пользователя с таким идентификатором нет, вывести соответствующее сообщение.
"""
#Импортируем из модуля users уже готовый класс User и функцию создания соединения connect_db
from users import User, connect_db
# импортируем библиотеку sqlalchemy и некоторые функции из нее
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

# базовый класс моделей таблиц
Base = declarative_base()

class Athelete(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'athelete'
    # идентификатор атлета, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True)
    # Возраст
    age = sa.Column(sa.Integer)
    # Дата рождения
    birthdate = sa.Column(sa.Text)
    # Пол
    gender = sa.Column(sa.Text)
    # Рост
    height = sa.Column(sa.Float)
    # Имя атлета
    name = sa.Column(sa.Text)
    # Вес
    weight = sa.Column(sa.Integer)
    # Золотых медалей
    gold_medals = sa.Column(sa.Integer)
    # Серебрянных медалей
    silver_medals = sa.Column(sa.Integer)
    # Бронзовых медалей
    bronze_medals = sa.Column(sa.Integer)
    # Сумма медалей
    total_medals = sa.Column(sa.Integer)
    # Вид спорта
    sport = sa.Column(sa.Text)
    # Страна
    country = sa.Column(sa.Text)

def findUser(id_user, session):
    """
    Производит поиск пользователя в таблице user по заданному имени name
    и поиск ближайших спортсменов в таблице athelete
    """
    # находим user в таблице User, у которого поле User.id совпадает с параметром id_user
    query = session.query(User).filter(User.id == id_user).first()
    return query

def findAthelete(user_birthdate, user_height, session):
    """
    Производит поиск ближайших атлетов в таблице user по переданным user_birthdate, user_height
    """
    # Вычисление нижней и верхней границы диапазона даты рождения
    low_lim  = session.query(func.max(Athelete.birthdate)).filter(Athelete.birthdate <= user_birthdate).first()[0]
    upp_lim  = session.query(func.min(Athelete.birthdate)).filter(Athelete.birthdate >= user_birthdate).first()[0]
    # Определение ближайшей границы
    if low_lim is None :
        user_birthdate = upp_lim
    elif upp_lim is None :
        user_birthdate = low_lim
    else:
        tmpLow = int(low_lim.replace("-", ""))
        tmpUpp = int(upp_lim.replace("-", ""))
        tmpBth = int(user_birthdate.replace("-", ""))
        if abs(tmpBth-tmpLow) <= abs(tmpBth-tmpUpp) :
            user_birthdate = low_lim
        else:
            user_birthdate = upp_lim
    # Вычисление нижней и верхней границы диапазона роста
    low_lim = session.query(func.max(Athelete.height)).filter(Athelete.height <= user_height, Athelete.height.isnot(None)).first()[0]
    upp_lim = session.query(func.min(Athelete.height)).filter(Athelete.height >= user_height, Athelete.height.isnot(None)).first()[0]
    # Определение ближайшей границы
    if low_lim is None :
        user_height = upp_lim
    elif upp_lim is None :
        user_height = low_lim
    else:
        if abs(user_height-low_lim) <= abs(user_height-upp_lim) :
            user_height = low_lim
        else:
            user_height = upp_lim

    # Получение первого ближайшего атлета по дате рождения
    user_birthdate = session.query(Athelete).filter(Athelete.birthdate == user_birthdate).first()
    user_birthdate = user_birthdate.__dict__

    # Получение первого ближайшего атлета по росту
    user_height = session.query(Athelete).filter(Athelete.height == user_height).first()
    user_height = user_height.__dict__

    return (user_birthdate, user_height)

def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    id_user = input("Введите идентификатор пользователя: ")
    user = findUser(id_user, session)
    if user :
        user_birthdate, user_height = findAthelete(user.birthdate, user.height, session)
        print("Первый ближайший по дате рождения атлет - id:%(id)s ФИО:%(name)s ДР:%(birthdate)s Рост:%(height)s " % user_birthdate)
        print("Первый ближайший по росту атлет - id:%(id)s ФИО:%(name)s ДР:%(birthdate)s Рост:%(height)s " % user_height)
    else: print("Пользователя с таким ID не найдено.")

if __name__ == "__main__" :
    main()