import csv
import sqlite3
from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandParser

connection = sqlite3.connect('db.sqlite3')
cursor = connection.cursor()


class Command(BaseCommand):
    help = 'Loads data from external csv to database'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('files', nargs='+', type=str)
        parser.add_argument('--database', type=str, help='Database name')

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        for file in options['files']:
            self.stdout.write('Arg %s\n' % file)
            self.stdout.write('Arg type %s\n' % type(file))

        # for option in options:
        #     self.stdout.write('Option %s\n' % option)
        #     self.stdout.write('Option type %s\n' % type(option))

        if options['database']:
            # self.stdout.write('Database: %s' % options['database'])
            # connection = sqlite3.connect(options['database'])
            # self.stdout.write('Have --database arg')
            ...
        for file in options['files']:
            with open(file, 'r') as fin:
                table_name = file[:-4]
                dr = csv.DictReader(fin)
                fieldnames = (dr.fieldnames)
                cursor.execute(
                    f"CREATE TABLE {table_name} ({fieldnames});")
                ...

        self.stdout.write('Handle works!!!')
