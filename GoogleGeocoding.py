import urllib
import csv
import json, io, os, base64
import time

def req_loc(stri):
    #addr = stri.split(' ')
    #trans_addr = ''
    #for item in addr:
    #    trans_addr = trans_addr+'+'+item
    #trans_addr = trans_addr[1:]
    # trans_addr = stri
    # print trans_addr

    resquest = urllib.urlopen('http://maps.googleapis.com/maps/api/geocode/json?address='+stri+'&sensor=false')
    data = resquest.read().decode('utf-8')
    jsonData = json.loads(data)
    results = jsonData['results']

    if results==[]:
        return ['', '']
    lat_lng = results[0]['geometry']['location']
    # print results[0]['types']
    return [lat_lng['lat'], lat_lng['lng']]


def parsetime(stri):
    stri = stri.lower()
    if stri == 'any' or stri == 'continuous':
        print stri
        tt = [str(0), str(23)]
    elif stri == 'n/a' or stri == '':
        tt = [str(24), str(24)]
    else:
        times = stri.split(';')
        tt = []
        t = times[0].split(' to ')
        print t

        if t[0].endswith('pm'):
            t1 = float(t[0].split('pm')[0])+12
        else:
            t1 = float(t[0].split('am')[0])
        if t[1].endswith('pm'):
            t2 = float(t[1].split('pm')[0])+12
        else:
            t2 = float(t[1].split('am')[0])
        if t1 < t2:
            tt.extend([str(t1), str(t2)])
        else:
            tt.extend([str(0), str(t2), str(t1), str(23)])

        if len(times) == 2:  # there is two time slot
            t = times[1].split(' to ')
            if t[0].endswith('pm'):
                t1 = float(t[0].split('pm')[0])+12
            else:
                t1 = float(t[0].split('am')[0])
            if t[1].endswith('pm'):
                t2 = float(t[1].split('pm')[0])+12
            else:
                t2 = float(t[1].split('am')[0])
            if t1 < t2:
                tt.extend([str(t1), str(t2)])
            else:
                tt.extend([str(0), str(t2), str(t1), str(23)])
    return tt
            #float(time)




datareader = file('/Users/bread/Downloads/Road_closure_data/2013.csv', 'rU')
mycsv = file('/Users/bread/Downloads/Road_closure_data/2013time.csv', 'wb')
reader = csv.reader(datareader)
writer = csv.writer(mycsv)
writer.writerow(['Permit No', 'location', 'lat', 'lng', 'note', 'start_date', 'end_date', 'wkday_hour', 'wkend_hour'])
#n = 0

#add replace "," trim
for line in reader:
         location = line[0]
         neighbor = line[1]
         note = line[3]
         if (location != '' and neighbor != '' and line[4] != '' and line[5] != ''): #  nothing missing
            st_date = line[4].split(' ')[0]
            ed_data = line[4].split(' ')[2]
            wkd = '-'.join(parsetime(line[5]))
            wke = '-'.join(parsetime(line[6]))
            writer.writerow([location, neighbor, line[7], line[8], note, st_date, ed_data, wkd, wke])

#cnt = 0
#contin = 0
#for line in reader:
#
#   #if line[0] == '9':
#       # n += 1
#       location = line[1]
#       neighbor = line[2]
#       reason = line[3]
#       str = ''
#       if location != '':
#           str += location
#       if neighbor != '':
#           str += ' '+neighbor
#       if location != '' and neighbor != '':
#           latitude, longitude = req_loc(str + ' Pennsylvania')
#           print latitude, longitude
#           writer.writerow([location, neighbor, latitude, longitude, reason])
#           cnt += 1
#           if cnt == 10:
#               time.sleep(5)
#               cnt = 0
#