from peewee import SqliteDatabase, PostgresqlDatabase
from peewee import Model
from peewee import CharField, DateTimeField, ForeignKeyField, TextField, IntegerField
from datetime import datetime

import secrets

db = PostgresqlDatabase(secrets.POSTGRES_DB,
        user=secrets.POSTGRES_USER,
        password=secrets.POSTGRES_PASSWORD,
        host='127.0.0.1')

class Question(Model):
    class Meta:
        database = db
        order_by = ('-timestamp',)
    text = TextField()
    timestamp = DateTimeField(default=datetime.now())
    def display_time(self):
        return self.timestamp.strftime("%H:%M on %A %d %B %Y")
    
    def latest_answer(self):
        if self.answers:
            
            k =  max([k.timestamp for k in self.answers])
            return k
        else:
            return None

    def answered(self):
        return True if self.answers else False

class Answer(Model):

    class Meta:
        database = db
        order_by = ('timestamp',)

    text = TextField()
    question = ForeignKeyField(Question, related_name = "answers", on_delete='CASCADE')
    timestamp = DateTimeField(default=datetime.now())
    likes = IntegerField(default=0)
    def display_time(self):
        return self.timestamp.strftime("%H:%M on %A %d %B %Y")

class Famq(Model):
    class Meta:
        database = db

    question = TextField()
    answer = TextField()



