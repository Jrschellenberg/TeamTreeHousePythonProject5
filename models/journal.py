import csv
import datetime
from peewee import *


db = SqliteDatabase('storage/data.db')


class Journal(Model):
    id = IntegerField(primary_key=True, unique=True)
    title = CharField(max_length=255, null=False)
    time_spent = IntegerField()
    what_i_learned = CharField(max_length=1023)
    resources_to_remember = CharField(max_length=1023)
    date = DateField(default=datetime.datetime.now,
                     formats=['%m/%d/%Y'], null=False)

    class Meta:
        database = db
        order_by = ('-date',)

    @classmethod
    def initialize(cls):
        db.connect()
        db.create_tables([Journal], safe=True)

    @classmethod
    def connect(cls):
        db.connect()

    @classmethod
    def close(cls):
        db.close()

    @classmethod
    def get_all_records(cls):
        try:
            return cls.select()
        except cls.DoesNotExist:
            return []

    @classmethod
    def get_record_by_id(cls, journal_id):
        try:
            return cls.select()\
                       .where(cls.id == journal_id).dicts().get(), False
        except cls.DoesNotExist:
            return None, True

    @classmethod
    def update_record(cls, row_id, row):
        try:
            cls.update(**row).where(cls.id == row_id).execute()
            return None, False
        except IntegrityError as e:
            return e, True

    @classmethod
    def create_record(cls, row):
        try:
            record_id = cls.create(**row)
            if not record_id:
                return None, True
            return record_id, False
        except IntegrityError:
            return None, True

    @classmethod
    def delete_record(cls, journal_id):
        user = cls.get(cls.id == journal_id)
        if user:
            user.delete_instance()
            return True
        else:
            return False

    @classmethod
    def import_database_by_csv(cls, filepath):
        if not len(cls.select()) == 0:
            print("Database already contains data,"
                  " Skipping csv initialization...")
            return

        print(f"Database Does not Exist, Seeding Database with {filepath}...")
        with open(filepath, newline='') as csvfile:
            journal_entries = csv.DictReader(csvfile, delimiter=',')
            for row in list(journal_entries):
                cls.create_record(row)
