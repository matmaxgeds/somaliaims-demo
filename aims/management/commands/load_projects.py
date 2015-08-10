from django.core.management.base import BaseCommand
from data_entry.models import Project, Spending, Contact, Document, SectorAllocation
from management.models import Organization, Currency, Sector
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
        with codecs.open(file_path, "r", encoding='utf-8', errors='ignore') as f:
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
                end = row['End date'].split('-')
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

                try:
                    to_date = int(row['Amount spent to date'].strip().replace(",", ""))
                except Exception:
                    to_date = 0.0

                try:
                    last_year = int(row['Amount spent to end 2014'].strip().replace(",", ""))
                except Exception:
                    last_year = 0.0

                try:
                    next_year = int(row['Amount spent to end 2014'].strip().replace(",", ""))
                except Exception:
                    next_year = 0.0

                spending = Spending(project=project, spendingToDate=to_date,
                                    lastYearSpending=last_year, thisYearSpending=0,
                                    nextYearSpending=next_year)
                spending.save()

                try:
                    link = row['Link to project documents website']
                except Exception:
                    link = ''
                doc = Document(project=project, link_to_document_website=link)
                doc.save()

                try:
                    name = row['Project contact name']
                except Exception:
                    name = ''
                try:
                    email = row['Project contact email']
                except Exception:
                    email = ''

                try:
                    phone = row['Project contact phone']
                except Exception:
                    phone = ''

                con = Contact(project=project, name=name, number=phone,
                              email=email)  # Organization has not been included
                con.save()

                sec1 = row['Primary Sector'].rpartition(': ')[2]
                try:
                    sector1 = Sector.objects.get(name=sec1)
                except Sector.DoesNotExist:
                    sector1 = Sector(name=sec1)
                    sector1.save()
                try:
                    sec1_percentage = float(row['Primary Sector %'].strip('%'))
                except Exception:
                    sec1_percentage = 0
                if sec1 and sec1_percentage != 0:
                    sec_alloc1 = SectorAllocation(project=project, sector=sector1, allocatedPercentage=sec1_percentage)
                    sec_alloc1.save()

                sec2 = row['Secondary Sector'].rpartition(': ')[2]
                try:
                    sector2 = Sector.objects.get(name=sec1)
                except Sector.DoesNotExist:
                    sector2 = Sector(name=sec2)
                    sector2.save()
                try:
                    sec2_percentage = float(row['Secondary Sector %'].strip('%'))
                except Exception:
                    sec2_percentage = 0
                if sec2 and sec2_percentage != 0:
                    sec_alloc2 = SectorAllocation(project=project, sector=sector2, allocatedPercentage=sec2_percentage)
                    sec_alloc2.save()

                # TODO Parse dicts while saving data
