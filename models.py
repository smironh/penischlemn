from peewee import *
import sqlite3

db = SqliteDatabase('referals.db')


class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):
    user_id = IntegerField(unique=True)
    ref = IntegerField(default=0)

    @classmethod
    def get_user(cls, user_id):
        return cls.get(user_id == user_id)

    @classmethod
    def get_ref_count(cls, user_id):
        return cls.get(Users.user_id == user_id).ref

    @classmethod
    def increase_ref_count(cls, user_id):
        user = cls.get_user(user_id)
        user.ref += 1
        user.save()
        with sqlite3.connect('db.db') as db:
            cursor = db.cursor()

            cursor.execute('UPDATE user SET balance = balance + 5 WHERE ID = ?', (user_id, ))
            print('1')
            bot.send_database(user_id, '1 реферал перешел по вашей ссылке! +5 Монет')

    @classmethod
    def user_exists(cls, user_id):
        query = cls().select().where(cls.user_id == user_id)
        return query.exists()

    @classmethod
    def create_user(cls, user_id):
        user, created = cls.get_or_create(user_id=user_id)

db.create_tables([Users]) #Создание таблицы