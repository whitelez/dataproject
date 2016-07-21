# get real time travel time of tomtom

#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib2, xml.etree.ElementTree as ET, MySQLdb
from datetime import datetime
import time
from pytz import timezone

# database connection
# db = MySQLdb.connect("localhost","root","dataproject","Travel_Time_Data" ) # (port, user, password, database)
# cursor = db.cursor()

tmcdic = {}
tmclist = open("TMC_list.txt", "r")
line = tmclist.readline()
while line:
    tmcdic[str(line)] = 1
    line = tmclist.readline()
tmclist.close()


while True:
    # read TomTom real time travel time data in XML format
    try:
        url = "http://traffic.tomtom.com/tsq/hdf/USA-HDF-TMC/2f398080-3324-45aa-b102-e2a13f999d04/content.xml?flowType=all"
        req = urllib2.urlopen(url)
        CHUNK = 16 * 1024
        with open("non_freeflow.xml", "w") as fp:
            while True:
                chunk = req.read(CHUNK)
                if not chunk:
                    break
                fp.write(chunk)
    except Exception, e:
        print e
        continue

    # find data in response XML
    # parsing xml with namespace: https://docs.python.org/2/library/xml.etree.elementtree.html#parsing-xml-with-namespaces
    ns = {'standard':'http://datex2.eu/schema/1_0/1_0'}

    tree = ET.parse("non_freeflow.xml")
    root = tree.getroot()
    payload = root.find("standard:payloadPublication", ns)

    timestamp = payload.find("standard:publicationTime", ns).text
    timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    timestamp = timestamp.replace(tzinfo=timezone('UTC')).astimezone(timezone('US/Eastern')).strftime("%Y-%m-%d %H:%M:%S") # convert timestamp in UTC format to format of MySQL database
    print timestamp
    result = "time," + timestamp + ",,\n" #keep csv format, first line of each query is timestamp

    for data in payload.findall("standard:elaboratedData", ns):
        # tmc
        tmc = data.attrib["id"]
        tmc = tmc[1:]
        if tmc not in tmcdic:
            continue
        print tmc
        dataValue = data.find("standard:basicDataValue",ns)
        # data quality
        quality = float(dataValue.find("standard:supplierCalculatedDataQuality",ns).text)
        # travel time
        tt = float(dataValue.find("standard:travelTime", ns).text) # in seconds
        speed = float(dataValue.find("standard:travelTimeValueExtension",ns).find("standard:averageSpeed",ns).text) # in km/h
        values = [str(tmc), str(tt), str(speed), str(quality)]
        result += values.join(",") + "\n"
        # print tmc, tt, speed, timestamp
        # try:
        #     cursor.execute("INSERT INTO tomtom_travel_time VALUES (%s,%s,%s,%s,%s)", values)
        #     db.commit()
        # except:
        #     db.rollback()
    with open("non_ff_traveltimes.csv", "a") as myfile:
        myfile.write(result)
    time.sleep(30)

# will not reach here if operating correctly
# db.close()
