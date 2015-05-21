import psycopg2
import logging
import urllib.request
import json



try:
    conn = psycopg2.connect("dbname='somaliaims' user='somaliaims' host='localhost' password='aims.somali'")
except Exception:
    conn = psycopg2.connect(
        "host='somaliaims-43.postgres.pythonanywhere-services.com' password='aims.somali' port='10043' dbname='somaliaims' user='somaliaims'")
except:
    logfile = 'db.log'
    logging.basicConfig(filename=logfile, level=logging.DEBUG)
    # Make it send email to maintainer
    logging.debug('Error connecting to db')

if conn:
    cur = conn.cursor()
    cur.execute("""SELECT * from locations""")
    locations = cur.fetchall()
    car = conn.cursor()
    for location in locations:
        final_loc = location[1].replace(" ", "+") + "+" + "somalia"
        try:
            address=final_loc
            url="https://maps.googleapis.com/maps/api/geocode/json?address=%s" % address
            t = urllib.request.Request(url)
            response = urllib.request.urlopen(t).read()
            jsongeocode = json.loads(response.decode('utf8'))
            lng = jsongeocode['results'][0]['geometry']['location']['lng']
            lat = jsongeocode['results'][0]['geometry']['location']['lat']
        except Exception:
            pass
        try:
            if lat and lng:
                g = """UPDATE locations set lng='{0}', lat='{1}' where id='{2}';""".format(lng, lat, location[0])
                cur.execute(g)
        except NameError:
            continue

        s = """SELECT * from sublocations where location_id='{0}'""".format(location[0])

        car.execute(s)
        sublocations = car.fetchall()
        for sublocation in sublocations:
            complete = sublocation[1].replace(" ", "+") + "+" + location[1].replace(" ", "+") + "+" + "somalia"
            try:
                address = complete
                url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s" % address
                t = urllib.request.Request(url)
                response = urllib.request.urlopen(t).read()
                print(str(dir(response)))
                jsongeocode = json.loads(response.decode('utf8'))
                lng1 = jsongeocode['results'][0]['geometry']['location']['lng']
                lat1 = jsongeocode['results'][0]['geometry']['location']['lat']
            except Exception:
                pass
            try:
                if lat1 and lng1:
                    j = """UPDATE sublocations set lng='{0}', lat='{1}' where id='{2}'""".format(lng1, lat1, sublocation[0])
                    print(j)
                    car.execute(j)
                    conn.commit()
            except NameError:
                continue