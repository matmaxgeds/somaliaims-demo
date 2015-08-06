from django.core.management.base import BaseCommand
from data_entry.models import Project, Organization
from management.models import Organization, Currency
import codecs
import csv
from django.contrib.auth.models import User
from _datetime import datetime
from time import strptime
from datetime import date
from collections import namedtuple


class Command(BaseCommand):
    help = 'Imports project information'

    def add_arguments(self, parser):
        parser.add_argument('file_path')

    def handle(self, file_path, *args, **options):
        with codecs.open('/Users/alphabuddha/Downloads/csv.csv', "r", encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f, dialect='excel')
            for row in reader:
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
                    currency = Currency.objects.get(abbrev=row['Project reporting currency'])
                except Currency.DoesNotExist:
                    currency = Currency(currency=row['Project reporting currency'],
                                        abbrev=row['Project reporting currency'])
                    currency.save()
                start = row['Start date'].split('-') if row['Start date'] != 'Pipeline' else date.today()
                month = strptime(start[0], '%b').tm_mon
                year = int(start[1])
                dtstr = "%s-%s" %(year, month)
                dt = datetime.strptime(dtstr, '%Y-%m')
                end = row['Start date'].split('-')
                month1 = strptime(end[0], '%b').tm_mon
                year1 = int(end[1])
                dtstr1 = "%s-%s" %(year1, month1)
                dt1 = datetime.strptime(dtstr1, '%Y-%m')
                project = Project(user=user, name=row['Project title'], description=row['Project objectives / purpose'],
                                  startDate=dt, endDate=dt1,
                                  value=int(row['Project value'].strip().replace(",", "")), currency=currency,
                                  rateToUSD=row['Amount of reporting currency per 1 USD'], ocha_fts_reported=row[
                        'Is this a humanitarian project which is also reported in the OCHA FTS database?'])
                project.save()
                for i in f:
                    project.funders.add(i)
                for j in d:
                    project.implementers.add(j)

                    # TODO Parse dicts while saving data



                    # print(str(sheet.rows))
                    # for row in sheet.iter_rows(self.PROJECT_RANGE):
                    #     user = User.objects.get(id=1)
                    #     count = 0
                    #     max_count = 23  # Count of last column to be fetched.
                    #     for cell in row:
                    #         if count > max_count:
                    #             count = 0
                    #         if count == 0:
                    #             reporter = cell.value
                    #             print(reporter)
                    #             count += 1
                    #             continue
                    #         fund = []
                    #         if count == 1:
                    #             funders = cell.value
                    #             s = funders.rpartition(': ')
                    #             n = s[2].split(', ')
                    #             for org in n:
                    #                 try:
                    #                     o = Organization.objects.get(short_name=org, name=org)
                    #                     fund.append(o)
                    #                 except Exception:
                    #                     new_save = Organization(name=org, short_name=org)
                    #                     print(str(new_save))
                    #                     new_save.save()
                    #                     fund.append(new_save)
                    #             print(funders)
                    #             count += 1
                    #             continue
                    #         plementers = []
                    #         if count == 2:
                    #             implementers = cell.value
                    #             d = implementers.rpartition(': ')
                    #             l = d[2].split(', ')
                    #             for org in l:
                    #                 try:
                    #                     o = Organization.objects.get(short_name=org, name=org)
                    #                     plementers.append(o)
                    #                 except Exception:
                    #                     new_save = Organization(name=org, short_name=org)
                    #                     new_save.save()
                    #                     plementers.append(new_save)
                    #             print(implementers)
                    #             count += 1
                    #             continue
                    #         if count == 3:
                    #             title = cell.value
                    #             print(title)
                    #             count += 1
                    #             continue
                    #         if count == 4:
                    #             description = cell.value
                    #             print(description)
                    #             count += 1
                    #             continue
                    #         if count == 5:
                    #             ocha_ots = cell.value
                    #             print(ocha_ots)
                    #             count += 1
                    #             continue
                    #         if count == 6:
                    #             sector = cell.value
                    #             count += 1
                    #             continue
                    #         if count == 7:
                    #             sector1 = cell.value
                    #             print(sector1)
                    #             if type(sector1) is not str:
                    #                 pass
                    #             else:
                    #                 sec1 = Sector(name=sector1)
                    #                 sec1.save()
                    #             count += 1
                    #             continue
                    #         if count == 8:
                    #             sector1_allocation = cell.value
                    #             # alloc1 = SectorAllocation()
                    #             print(sector1_allocation)
                    #             count += 1
                    #             continue
                    #         if count == 9:
                    #             sector2 = cell.value
                    #             print(sector2)
                    #             if type(sector2) is not str:
                    #                 pass
                    #             else:
                    #                 sec2 = Sector(name=sector2)
                    #                 sec2.save()
                    #             count += 1
                    #             continue
                    #         if count == 10:
                    #             sector2_allocation = cell.value
                    #             # alloc2 = SectorAllocation()
                    #             # print(sector2_allocation)
                    #             count += 1
                    #             continue
                    #         if count == 11:
                    #             startDate = cell.value
                    #             print(startDate)
                    #             #print(str(datetime.datetime.strptime(startDate, "%d%m%Y").date()))
                    #             count += 1
                    #             continue
                    #         if count == 12:
                    #             endDate = cell.value
                    #             print(endDate)
                    #             #print(str(datetime.datetime.strptime(endDate, "%d%m%Y").date()))
                    #             count += 1
                    #             continue
                    #         if count == 13:  # Reporting currency.
                    #             currency = cell.value
                    #             try:
                    #                 s = Currency.objects.get(currency=currency)
                    #                 c = s
                    #             except Exception:
                    #                 d = Currency(abbrev=currency, currency=currency)
                    #                 d.save()
                    #                 c = d
                    #             print(c)
                    #             count += 1
                    #             continue
                    #         if count == 14:  # Reporting currency rate per USD.
                    #             rateToUSD = cell.value
                    #             print(rateToUSD)
                    #             count += 1
                    #             continue
                    #         if count == 15:
                    #             value = cell.value
                    #             print(value)
                    #             count += 1
                    #             continue
                    #         if count == 16:
                    #             spendingLastYear = cell.value
                    #             #project['spendingLastYear'] = spendingLastYear
                    #             print(spendingLastYear)
                    #             count += 1
                    #             continue
                    #         if count == 17:
                    #             spendingToDate = cell.value
                    #             #project['spendingToDate'] = spendingToDate
                    #             print(spendingToDate)
                    #             count += 1
                    #             continue
                    #         # if count == 13:
                    #         #     spendingThisYear = cell.value
                    #         #     print(spendingThisYear)
                    #         #     count += 1
                    #         #     continue
                    #         if count == 18:
                    #             spendingNextYear = cell.value
                    #             #project['spendingNextYear'] = spendingNextYear
                    #             print(spendingNextYear)
                    #             count += 1
                    #             continue
                    #         if count == 19:
                    #             locationSpending = cell.value
                    #             localloc = LocationAllocation()
                    #             print(locationSpending)
                    #             count += 1
                    #             continue
                    #         if count == 20:
                    #             sublocations = cell.value
                    #             sub = SubLocation()
                    #             print(sublocations)
                    #             count += 1
                    #             continue
                    #         if count == 21:
                    #             documentLinks = cell.value
                    #             doc = Document(link_to_document_website=documentLinks)
                    #             print(documentLinks)
                    #             count += 1
                    #             continue
                    #         if count == 22:
                    #             sdrf_ssa = cell.value
                    #             print(sdrf_ssa)
                    #             count += 1
                    #             continue
                    #
                    #     project = Project(user=user, name=title, description=description,
                    #                       ocha_fts_reported=True if ocha_ots == 'Yes' else False, startDate=startDate, endDate=endDate, currency=c, rateToUSD=rateToUSD, value=value, sdrf_ssa=sdrf_ssa)
                    #     project.save()
                    #     for i in fund:
                    #         project.funders.add(i)
                    #     for j in plementers:
                    #         project.implementers.add(j)

                    # if count == 23:
                    #     contactName = cell.value
                    #     print(contactName)
                    #     count += 1
                    #     continue
                    # if count == 19:
                    #     contactEmail = cell.value
                    #     print(contactEmail)
                    #     count += 1
                    #     continue
                    # if count == 20:
                    #     contactPhone = cell.value
                    #     print(contactPhone)
                    #     count += 1
