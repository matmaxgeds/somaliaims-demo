from management.models import Location, SubLocation
import urllib.request
import json
from django.core.management.base import BaseCommand


def action():
    locations = Location.objects.all()
    for location in locations:
        search_term = location.name.replace(" ", "+") + "+" + "somalia"
        try:
            url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s" % search_term
            req = urllib.request.Request(url)
            response = urllib.request.urlopen(req).read()
            jsongeocode = json.loads(response.decode('utf8'))
            lng = jsongeocode['results'][0]['geometry']['location']['lng']
            lat = jsongeocode['results'][0]['geometry']['location']['lat']
        except Exception:
            pass
        try:
            if lat and lng:
                location.lat, location.lng = (lat, lng)
                location.save()
        except NameError:
            continue
        sublocations = SubLocation.objects.filter(location=location)
        for sublocation in sublocations:
            search_term = sublocation.name.replace(" ", "+") + "+" + location.name.replace(" ", "+") + "+" + "somalia"
            try:
                url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s" % search_term
                req = urllib.request.Request(url)
                response = urllib.request.urlopen(req).read()
                jsongeocode = json.loads(response.decode('utf8'))
                lng1 = jsongeocode['results'][0]['geometry']['location']['lng']
                lat1 = jsongeocode['results'][0]['geometry']['location']['lat']
            except Exception:
                pass
            try:
                if lat1 and lng1:
                    sublocation.lat, sublocation.lng = (lat1, lng1)
                    sublocation.save()
            except NameError:
                continue


class Command(BaseCommand):
    help = "Fetched the co-ordinates for locations and sublocations"

    def handle(self, *args, **options):
        action()

