__author__ = 'bread'

from django.http import HttpResponse, QueryDict
from django.db.models import Q
from django.shortcuts import render

import json
import urllib2

from traffic.models import * #Meter, Parking, Street, Streetparking, TMC, TMC_data, Incidents, Weather
from datetime import date


def parking(request):
    return render(request, 'traffic/parking.html', {'n': range(1, 32)})


def street_parking_geojson_prediction(request):
    stpdate = date(2013, 1, 1)
    edpdate = date(2014, 8, 30)
    intervals = 144
    py = request.GET['py']
    pm = request.GET['pm']
    pd = request.GET['pd']
    pdate = date(int(py), int(pm)+1, int(pd))
    ##########
    py1 = request.GET['py1']
    pm1 = request.GET['pm1']
    pd1 = request.GET['pd1']
    pdate1 = date(int(py1), int(pm1)+1, int(pd1))
    ###############
    weekday = (pdate.weekday()+1) % 7 + 1
    wkdys = request.GET.getlist('wkdys[]')
    cr = []
    for i in range(7):
        cr.append(0)
    for i in range(7):
        if int(wkdys[i]) != 0:
            cr[i] = Q(date__week_day=(i+1))
        else:
            cr[i] = Q(date__week_day=0)
    #################
    print "New Request"
    result = '''{"type":"FeatureCollection","features":['''
    for t in Street.objects.all():
        p = 0
        r = 0
        if not (pdate > edpdate or pdate1 < stpdate):  # use historical data
            p = t.streetparking_set.filter(date__range=(pdate, pdate1))
            r = t.streetrate_set.filter(date__range=(pdate, pdate1))
            if pdate != pdate1:   # historical date range
                p = p.filter(cr[0] | cr[1] | cr[2] | cr[3] | cr[4] | cr[5] | cr[6])
                r = r.filter(cr[0] | cr[1] | cr[2] | cr[3] | cr[4] | cr[5] | cr[6])
        if (not p) or (p == 0):   # No historical data, use prediction
            if pdate1 == pdate:   # same day
                p = t.streetpre_set.filter(date__week_day=weekday)
                r = t.streetratepre_set.filter(date__week_day=weekday)
            else:                 # Day ranges
                p = t.streetpre_set.filter(cr[0] | cr[1] | cr[2] | cr[3] | cr[4] | cr[5] | cr[6])
                r = t.streetratepre_set.filter(cr[0] | cr[1] | cr[2] | cr[3] | cr[4] | cr[5] | cr[6])
        if p:
            n = p.count()
            c = [0]*intervals
            for day in p:
                dc = day.occupancy.split(',')
                for i in range(intervals):
                    c[i] += float(dc[i])/n
            cr = [0]*48
            for day in r:
                dc = day.rate.split(',')
                for i in range(48):
                    cr[i] = dc[i]
            if (len(t.coordinate.replace(" ", "").split("],["))==1):
                result += '''{"type":"Feature","properties":{"streetID":"''' + t.sid + '''","street":"''' + t.street_name + '''","rate":[''' + ",".join(str(ic) for ic in cr) + '''],"occupancy":[''' + ",".join(str(ic) for ic in c) + ''']},"geometry":{"type":"Point","coordinates":''' + t.coordinate + "}},"
            else:
                result += '''{"type":"Feature","properties":{"streetID":"''' + t.sid + '''","street":"''' + t.street_name + '''","rate":[''' + ",".join(str(ic) for ic in cr) + '''],"occupancy":[''' + ",".join(str(ic) for ic in c) + ''']},"geometry":{"type":"LineString","coordinates":''' + t.coordinate + "}},"
    result = result.rstrip(',')
    result += "]}"
    response = json.dumps(result)
    return HttpResponse(response, content_type='application/json')


def parking_lots(request):
    lots = {"type" : "FeatureCollection", "features": []}
    for i in range(2, 43):
        url = 'http://parkpgh.org/index.php/api/getLotById?lotId=' + str(i)
        p = urllib2.urlopen(url)
        info = p.read()
        info = json.loads(info)
        this_lot = {"type": "Feature", "geometry": {"type": "Point", "coordinates": []}, "properties": {}}
        if 'id' in info:
            this_lot['geometry']['coordinates'] = [info['lon'] , info['lat']]
            this_lot['properties'] = info
            lots['features'].append(this_lot)
    response = json.dumps(lots)
    return HttpResponse(response, content_type='application/json')

