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

    # TODO: Update this!
    @classmethod
    def create_record(cls, row):
        try:
            cls.model.create(**row)
        except IntegrityError as err:
            query = cls.model.select().where(cls.model.product_name == row['product_name'])
            if not len(query) == 1:
                raise IntegrityError(err)
            if row.get('date_updated', True):
                row['date_updated'] = datetime.datetime.strftime(datetime.datetime.now(), '%m/%d/%Y')
            cls.model.update(**row).where(cls.model.product_name == row['product_name']).execute()

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
