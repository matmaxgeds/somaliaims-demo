from django.core.management.base import BaseCommand
from data_entry.models import Project
from management.models import Organization, Currency
import codecs
import csv
from django.contrib.auth.models import User
from _datetime import datetime
from time import strptime
from datetime import date


class Command(BaseCommand):
    help = 'Imports project information'

    def add_arguments(self, parser):
        parser.add_argument('file_path')

    def handle(self, file_path, *args, **options):
        with codecs.open('/Users/alphabuddha/Downloads/csv.csv', "r", encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f, dialect='excel')
            for row in reader:
                if row['Project title'] == '':
                    continue
                f = []
                funders = row['Funder(s)']
                for funder in funders.rpartition(': ')[2].split(', '):
                    try:
                        a = Organization.objects.get(name=funder)
                        f.append(a)
                    except Organization.DoesNotExist:
                        if funder:
                            print(funder)
                            n = Organization(name=funder, short_name=funder)
                            n.save()
                            f.append(n)
                implementers = row['Implementer(s)']
                d = []
                for implementer in implementers.rpartition(': ')[2].split(', '):
                    try:
                        v = Organization.objects.get(name=implementer)
                        d.append(v)
                    except Organization.DoesNotExist:
                        if implementer:
                            print(implementer)
                            k = Organization(name=implementer, short_name=implementer)
                            k.save()
                            d.append(k)
                user = User.objects.get(id=1)
                try:
                    currency = Currency.objects.get(currency=row['Project reporting currency'].strip())
                except Currency.DoesNotExist:
                    currency = Currency(currency=row['Project reporting currency'],
                                        abbrev=row['Project reporting currency'])
                    currency.save()
                start = row['Start date'].split('-') if row['Start date'] != 'Pipeline' else date.today()
                try:
                    month = strptime(start[0], '%b').tm_mon
                except TypeError:
                    month = 1
                except ValueError:
                    month = 1

                try:
                    year = int(start[1])
                except Exception:
                    year = 1900
                dtstr = "%s-%s" % (year, month)
                dt = datetime.strptime(dtstr, '%Y-%m')
                end = row['Start date'].split('-')
                try:
                    month1 = strptime(start[0], '%b').tm_mon
                except TypeError:
                    month1 = 1
                except ValueError:
                    month1 = 1
                try:
                    year1 = int(end[1])
                except Exception:
                    year1 = 2020
                dtstr1 = "%s-%s" % (year1, month1)
                dt1 = datetime.strptime(dtstr1, '%Y-%m')
                try:
                    value = int(row['Project value'].strip().replace(",", ""))
                except Exception:
                    value = 0.0

                try:
                    rate = row['Amount of reporting currency per 1 USD']
                    if not rate:
                        rate = 0.0
                except Exception:
                    rate = 0.0

                print("*************")
                print(row['Project title'])
                print(value)
                print(rate)
                project = Project(user=user, name=row['Project title'], description=row['Project objectives / purpose'],
                                  startDate=dt, endDate=dt1,
                                  value=value, currency=currency,
                                  rateToUSD=rate, ocha_fts_reported=row[
                        'Is this a humanitarian project which is also reported in the OCHA FTS database?'])
                project.save()
                for i in f:
                    project.funders.add(i)
                for j in d:
                    project.implementers.add(j)

                

                # TODO Parse dicts while saving data
