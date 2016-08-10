# -*- coding: utf-8 -*-

import struct

__author__ = 'ludek'

import sys
import serial

class UbxMessage():
    #U32 iTOW;
    # U16 year;
    # U8  month;
    # U8  day;
    # U8  hour;
    # U8  min;
    # U8  sec;
    # U8  valid;
    # U32 tAcc;
    # I32 nano;
    # /* Brief Fixtype: - 0x00 = No Fix
    #  * 		- 0x01 = Dead Reckoning only
    #  * 		- 0x02 = 2D-Fix
    #  * 		- 0x03 = 3D-Fix
    #  * 		- 0x04 = GNSS + dead reckoning combined
    #  * 		- 0x05 = Time only fix  */
    # U8  fixType;
    # U8  flags;
    # U8  reserved1;
    # U8  numSV;
    # I32 lon;
    # I32 lat;
    # I32 height;
    # I32 hMSL;
    # U32 hAcc;
    # U32 vAcc;
    # I32 velN;
    # I32 velE;
    # I32 velD;
    # I32 gSpeed;
    # I32 headMot;
    # U32 sAcc;
    # U32 headAcc;
    # U16 pDOP;
    # U16 reserved2a;
    # U32 reserved2b;
    # I32 HeadVeh;
    # U32 reseverd3;
    def __init__(self, bytes):
        ofs = 0  # for debuggging
        self.iTOW = struct.unpack('I', bytes[ofs:ofs+4])[0]
        self.year = struct.unpack('H', bytes[ofs+4:ofs+6])[0]
        self.month = struct.unpack('B', bytes[ofs+6:ofs+7])[0]
        self.day = struct.unpack('B', bytes[ofs+7:ofs+8])[0]
        self.hour = struct.unpack('B', bytes[ofs+8:ofs+9])[0]

        self.min = struct.unpack('B', bytes[ofs+9:ofs+10])[0]
        self.sec = struct.unpack('B', bytes[ofs+10:ofs+11])[0]
        self.valid = struct.unpack('B', bytes[ofs+11:ofs+12])[0]

        self.fixType = struct.unpack('B', bytes[ofs+20:ofs+21])[0]

        self.lon = struct.unpack('I', bytes[ofs+24:ofs+28])[0]/10000000.0
        self.lat = struct.unpack('I', bytes[ofs+28:ofs+32])[0]/10000000.0

        self.height = struct.unpack('I', bytes[ofs+32:ofs+36])[0]
        self.hMSL = struct.unpack('I', bytes[ofs+32:ofs+36])[0]

        self.lon_deg = int(self.lon)
        self.lon_min = int((self.lon - self.lon_deg) * 60)
        self.lon_sec = (self.lon - self.lon_deg - self.lon_min/60.0) * 3600



        self.lat_deg = int(self.lat)
        self.lat_min = int((self.lat - self.lat_deg) * 60)
        self.lat_sec = (self.lat - self.lat_deg - self.lat_min/60.0) * 3600

class UbxMessageShort():
    # U16 year;
    # U8  month;
    # U8  day;
    # U8  hour;
    # U8  min;
    # U8  sec;
    # U8  valid;
    # /* Brief Fixtype: - 0x00 = No Fix
    #  * 		- 0x01 = Dead Reckoning only
    #  * 		- 0x02 = 2D-Fix
    #  * 		- 0x03 = 3D-Fix
    #  * 		- 0x04 = GNSS + dead reckoning combined
    #  * 		- 0x05 = Time only fix  */
    # U8  fixType;
    # U8  flags;
    # U8  numSV;
    # I32 lon;
    # I32 lat;
    # I32 height;
    # I32 gSpeed;
    # U32 reseverd3;
    def __init__(self, bytes):
        ofs = 0  # for debuggging
        self.year = struct.unpack('H', bytes[ofs:ofs+2])[0]
        self.month = struct.unpack('B', bytes[ofs+2:ofs+3])[0]
        self.day = struct.unpack('B', bytes[ofs+3:ofs+4])[0]
        self.hour = struct.unpack('B', bytes[ofs+4:ofs+5])[0]

        self.min = struct.unpack('B', bytes[ofs+5:ofs+6])[0]
        self.sec = struct.unpack('B', bytes[ofs+6:ofs+7])[0]
        self.valid = struct.unpack('B', bytes[ofs+7:ofs+8])[0]

        self.fixType = struct.unpack('B', bytes[ofs+8:ofs+9])[0]
        self.flags = struct.unpack('B', bytes[ofs+9:ofs+10])[0]
        self.numSV = struct.unpack('B', bytes[ofs+10:ofs+11])[0]

        self.lon = struct.unpack('I', bytes[ofs+11:ofs+15])[0]/10000000.0
        self.lat = struct.unpack('I', bytes[ofs+15:ofs+19])[0]/10000000.0

        self.height = struct.unpack('I', bytes[ofs+19:ofs+23])[0]
        self.speed = struct.unpack('I', bytes[ofs+23:ofs+27])[0]
        self.battery1 = struct.unpack('H', bytes[ofs+27:ofs+29])[0]
        self.battery2 = struct.unpack('H', bytes[ofs+29:ofs+31])[0]


        self.lon_deg = int(self.lon)
        self.lon_min = int((self.lon - self.lon_deg) * 60)
        self.lon_sec = (self.lon - self.lon_deg - self.lon_min/60.0) * 3600



        self.lat_deg = int(self.lat)
        self.lat_min = int((self.lat - self.lat_deg) * 60)
        self.lat_sec = (self.lat - self.lat_deg - self.lat_min/60.0) * 3600




class Priklad():

    pages = 0

    def __init__(self):

        self.dev = False

        self.ubxlist = []

        try:
            self.dev = serial.Serial('/dev/ttyUSB0', baudrate=19200, timeout=3.0)
            print 'UART opened'
        except:
            print 'Could not open device!'

        #self.close()

    def lostatClicked(self):
        #flush previous characters:
        rx = self.dev.read(1000)
        print 'flushing chars: ',
        print len(rx)
        print 'send \'s\' for status...',
        self.dev.write('s')
        rx = self.dev.read(10)
        print 'Chars loaded: ',
        print len(rx)
        if len(rx) > 2:
            for char in rx:
                print "{:02x}".format(ord(char)),
            print ''
            self.pages = struct.unpack('>H', rx[0:2])[0]
            print 'Pocet stranek: {:d}'.format(self.pages)

    def clrMemClicked(self):
        self.dev.write('r')

    def dumpClicked(self):
        # create file:
        file_name = 'taGpsUbxs.bin'
        wFile = open (file_name, "wb")

        self.dev.write('d')
        actual_page = 0
        pglength = 264
        addressbytes = 4  # flash read address bytes
        dummybytes = 4  # flash read dummy bytes
        bytes_to_read = addressbytes+dummybytes+pglength
        while True:
            actual_page += 1
            rx = self.dev.read(bytes_to_read)
            print 'Chars loaded: ',
            print len(rx),
            print '... reading page {:d} from {:d}'.format(actual_page, self.pages)
            print 'numbers: ',
            for char in rx:
                print "{:02x}".format(ord(char)),
            print ''
            ubxsperpage = 8
            startOffset=addressbytes+dummybytes
            bytesPerUbxMessage=33

            if len(rx) == bytes_to_read:
                rx = rx[startOffset:]
                for ubxnum in range(0, ubxsperpage):
                    self.ubxlist.append(UbxMessageShort(rx[ubxnum*bytesPerUbxMessage:(ubxnum+1)*bytesPerUbxMessage]))
                #store bytes to a file
                wFile.write(rx)
            if len(rx) == 0:
                break
            # flush stuffing???
            # rx = self.dev.read(8)

        wFile.close()

    def loadFileClicked(self):
        # create file:
        file_name = 'taGpsUbxs.bin'
        rFile = open(file_name, "rb")
        actual_page = 0
        pglength = 264
        addressbytes = 4  # flash read address bytes
        dummybytes = 4  # flash read dummy bytes
        #we are not storing the "offset bytes" in the file....
        startOffset=addressbytes+dummybytes
        bytes_to_read = addressbytes+dummybytes+pglength-startOffset
        while True:
            actual_page += 1
            rx = rFile.read(bytes_to_read)
            print 'Page {:d}, '.format(actual_page),
            print 'chars loaded: ',
            print len(rx)
            print 'numbers: ',
            for char in rx:
                print "{:02x}".format(ord(char)),
            print ''

            ubxsperpage = 8
            bytesPerUbxMessage=33

            if len(rx) == bytes_to_read:
                #rx = rx[startOffset:]
                for ubxnum in range(0, ubxsperpage):
                    self.ubxlist.append(UbxMessageShort(rx[ubxnum*bytesPerUbxMessage:(ubxnum+1)*bytesPerUbxMessage]))
            if len(rx) == 0:
                break

        rFile.close()

    def exitClicked(self):
        if self.dev:
            print 'UART dev has been opened, close it'
            self.dev.close()

    def ubxlistToGpx(self):
        fw = open('trasa.gpx', "w")
        lines = []
        lines.append('<?xml version="1.0" encoding="UTF-8" standalone="no"?>')
        lines.append('<gpx xmlns="http://www.topografix.com/GPX/1/1" xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" creator="Sports Tracker" version="1.1" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd">')
        lines.append('  <metadata>')
        lines.append('    <name>07/07/2016 09:05</name>')
        lines.append('    <author>')
        lines.append('      <name>Ludek Uhlir</name>')
        lines.append('    </author>')
        lines.append('    <link href="www.sports-tracker.com">')
        lines.append('      <text>Sports Tracker</text>')
        lines.append('    </link>')
        lines.append('  </metadata>')
        lines.append('  <trk>')
        lines.append('    <trkseg>')

        for ubx in app.ubxlist:
            if ubx.fixType == 0x3 or ubx.fixType == 0x2: #3D or 2D fix
                lines.append('      <trkpt lat="' + str(ubx.lat) + '"' + ' lon="' + str(ubx.lon) + '"' + '>')
                lines.append('        <ele>' + "{:.1f}".format(ubx.height/1000.0) + '</ele>')
                tmstr = "{:d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(ubx.year, ubx.month, ubx.day, ubx.hour, ubx.min, ubx.sec)
                lines.append('        <time>' + tmstr + '</time>')
                lines.append('      </trkpt>')

        lines.append('    </trkseg>')
        lines.append('  </trk>')
        lines.append('</gpx>')
        fw.write('\n'.join(lines) + '\n')
        fw.close()

if __name__ == '__main__':

    app = Priklad()
    app.lostatClicked()
    #Xapp.dumpClicked()
    #app.dumpClicked()
    #app.clrMemClicked()
    #app.loadFileClicked()
    #app.exitclicked()
    if len(app.ubxlist) > 0:
        print 'Number of ubx messages: {:d}'.format(len(app.ubxlist))
        print 'Rok, mesic, den, hodin, min, sec, valid, lon, lat'
        for ubx in app.ubxlist:
            print 'UBX message: ',
            print ubx.year,
            print ubx.month,
            print ubx.day,
            print ubx.hour,
            print ubx.min,
            print ubx.sec,
        #     print ubx.valid,
        #     print ubx.lat,
        #     print ubx.lon,
        #     print str(ubx.lat_deg) + '°',
        #     print str(ubx.lat_min) + '\'',
        #     print str(ubx.lat_sec) + '\"',
        #     print str(ubx.lon_deg) + '°',
        #     print str(ubx.lon_min) + '\'',
        #     print str(ubx.lon_sec) + '\"',
            print ' fix type: 0x{:02x}'.format(ubx.fixType),
            print 'flags: 0x{:02x}'.format(ubx.flags),
            print 'numSV: 0x{:02x}'.format(ubx.numSV),
            print 'battery1: 0x{:04x}'.format(ubx.battery1),
            print 'battery2: 0x{:04x}'.format(ubx.battery2)
        app.ubxlistToGpx()


