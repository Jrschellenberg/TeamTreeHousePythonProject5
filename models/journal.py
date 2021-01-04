import datetime
from peewee import *


db = SqliteDatabase('storage/data.db')


class Journal(Model):
    id = IntegerField(primary_key=True, unique=True)
    title = CharField(max_length=255, unique=True)
    time_spent = CharField(max_length=40)
    what_was_learned = CharField(max_length=1023)
    resources_to_remember = CharField(max_length=1023)
    date_updated = DateField(default=datetime.datetime.now, formats=['%m/%d/%Y'])

    @classmethod
    def initialize(cls):
        db.connect()
        db.create_tables([Journal], safe=True)

    class Meta:
        database = db
