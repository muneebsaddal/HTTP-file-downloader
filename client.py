import os
import sys
import getopt
import urllib2
import threading

globalnumConnection = ''
metricInterval = ''
connectionType = ''
fileLocation = ''
outputLocation = ''
resumeFlag = 'false'
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "rn:i:c:f:o:", ["nConn=", "tInter=", "cType=", "iFile=", "oFile="])
except getopt.GetoptError:
    print 'Input arguments error'
    sys.exit()
for opt, arg in opts:
    if opt == '-r':
        resumeFlag = 'true'
    elif opt in ("-n", "--nConn"):
        numConnection = arg
    elif opt in ("-i", "--tInter"):
        metricInterval = arg
    elif opt in ("-c", "--cType"):
        connectionType = arg
    elif opt in ("-f", "--iFile"):
        fileLocation = arg
    elif opt in ("-o", "--oFile"):
        outputLocation = arg

if numConnection is '' or metricInterval is '' or connectionType is '' or fileLocation is '' or outputLocation is '':
    print '--Input Argument error--\nEnter all the required arguments'
    sys.exit()

file_name = fileLocation.split('/')[-1]
file_name = outputLocation + file_name
file_size = 0
totalDownloaded = 0


def handlerURL(start, end, url, filename):
    global totalDownloaded
    global file_size
    headers = {'Range': 'bytes=%d-%d' % (start, end)}
    request = urllib2.Request(url, headers=headers)
    r = urllib2.urlopen(request)
    file_size = int(r.headers['content-length'])
    with open(filename, "r+b") as fp:  
      threadedSize = end - start
      threadedDown = 0
      fp.seek(start)
      var = fp.tell()
      buffer = r.read()
      threadedDown += len(buffer)
      fp.write(buffer)
      totalDownloaded += threadedDown
      per = (threadedDown / file_size) * 100
      status = "Bytes of data downloaded --> %d  Percentage of total file downloaded --> [%.2f]" % (totalDownloaded, per)
      print "\n\nCurrent Thread in working:"
      print threading.current_thread()
      print status

def downloadFileURL():
    global numConnection
    request = urllib2.Request(fileLocation)
    response = urllib2.urlopen(request)
    r = response.info()
    try:
        file_size = int(r['Content-length'])
    except:
        print "Invalid URL"
        return
    if os.path.exists(file_name):
        outputFile = open(file_name, "ab")
        fileExistSize = os.path.getsize(file_name)
        if fileExistSize == file_size:
            print "\n\n*******************File already downloaded*******************\n"
            sys.exit()
        start = fileExistSize + 1
        file_size = file_size - fileExistSize
    else:
        start = 0
    part = int(file_size) / int(numConnection)
    fp = open(file_name, "wb")
    fp.write('\0' * file_size)
    fp.close()
    for i in range(int(numConnection)):
        if i == 0:
            start += part * i
        else:
            start = part * i
        end = start + part
        t = threading.Thread(target=handlerURL, kwargs={'start': start, 'end': end, 'url': fileLocation, 'filename': file_name})
        t.setDaemon(True)
        t.start()
    main_thread = threading.current_thread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        t.join()

downloadFileURL()
totalDownloaded = totalDownloaded/1000000
if totalDownloaded >= file_size:
	print "\n\n*******************Download Complete*******************\nTotal MBs downloaded --> ", totalDownloaded
else:
	print "\n\n*******************Download failed*******************\n"