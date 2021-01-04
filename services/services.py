import csv
import datetime
from models import Journal
from peewee import IntegrityError


class BaseService:
    model = None


class JournalService(BaseService):
    model = Journal
    Journal.initialize()

    @classmethod
    def get_record_by_id(cls, journal_id):
        try:
            return cls.model.select().where(cls.model.id == journal_id).dicts().get(), False
        except cls.model.DoesNotExist:
            return None, True

    @classmethod
    def create_record(cls, row):
        try:
            record_id = cls.model.create(**row)
            if not record_id:
                return None, True
            return record_id, False
        except IntegrityError:
            return None, True

    @classmethod
    def delete_record(cls, journal_id):
        user = cls.model.get(cls.model.id == journal_id)
        if user:
            user.delete_instance()
            return True
        else:
            return False

    @classmethod
    def import_database_by_csv(cls, filepath):
        if not len(cls.model.select()) == 0:
            print("Database already contains data, Skipping csv initialization...")
            return

        print(f"Database Does not Exist, Seeding Database with {filepath}...")
        with open(filepath, newline='') as csvfile:
            journal_entries = csv.DictReader(csvfile, delimiter=',')
            for row in list(journal_entries):
                cls.create_record(row)
