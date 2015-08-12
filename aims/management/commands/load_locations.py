from django.core.management.base import BaseCommand
from management.models import Location, SubLocation
import codecs
import csv
from django.db.utils import IntegrityError



class Command(BaseCommand):
    help = 'Imports locations and sublocations from CSV. The CSV file is given as a cmd line argument'

    def add_arguments(self, parser):
        parser.add_argument('file_path')

    def handle(self, file_path, *args, **options):
        with codecs.open(file_path, "r", encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f, dialect='excel')
            locs = {}
            for row in reader:
                print(str(row))
                location = row['Locations']
                if location in locs:
                    locs[location].append(row['Sub-locations'])
                else:
                    locs[location] = []
                    locs[location].append(row['Sub-locations'])
            for i, j in iter(locs.items()):
                try:
                    l = Location(name=i)
                    l.save()
                except IntegrityError:
                    continue
                for sub in j:
                    s = SubLocation(name=sub, location=l)
                    s.save()