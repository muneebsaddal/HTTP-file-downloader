import getopt
import os
import requests
import sys
import threading
import urllib
import urllib2

def argsInput(argv):
    numConnection = ''
    metricInterval = ''
    connectionType = ''
    fileLocation = ''
    outputLocation = ''
    resumeFlag = 'false'

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

    print 'r', resumeFlag
    print 'n', numConnection
    print 'i', metricInterval
    print 'c', connectionType
    print 'f', fileLocation
    print 'o', outputLocation


#fileLocation = "https://sample-videos.com/audio/mp3/wave.mp3"
fileLocation = 'file:' + urllib.pathname2url(r'c:\xampp\htdocs\downloadables\Ep-18.The.Apartment.mp4')
if fileLocation[0] == 'h':
   localFlag = False
elif fileLocation[0] == 'f':
   localFlag = True
file_name = fileLocation.split('/')[-1]
#file_name = "test.txt"
global file_size
numConnection = 1
totalDownloaded = 0
print localFlag

def handlerURL(start, end, url, filename):
    global totalDownloaded
    headers = {'Range': 'bytes=%d-%d' % (start, end)}
    if localFlag:
      request = urllib2.Request(url, headers=headers)
      r = urllib2.urlopen(request)
    else:
      r = requests.get(url, headers=headers, stream=True)
    with open(filename, "r+b") as fp:
        threadedSize = end - start
        threadedDown = 0
        fp.seek(start)
        var = fp.tell()
        if localFlag:
           buffer = r.read()
        else:
           buffer = r.content
        threadedDown += len(buffer)
        fp.write(buffer)
        totalDownloaded += threadedDown
        status = r"%10d  [%3.f%%]" % (threadedDown, threadedDown * 100. / threadedSize)
        # status = status + chr(8)*(len(status)+1)
        print status


def downloadFileURL():
    global numConnection
    if localFlag:
       request = urllib2.Request(fileLocation)
       response = urllib2.urlopen(request)
       r = response.info()
    else:
       r = requests.head(fileLocation)
       statusCode = r.status_code
       print "Status Code --> ", statusCode
       if statusCode == 404:
           print 'File not found'
           sys.exit()
       elif statusCode == 200:
           numConnection = 1
    try:
        if localFlag:
           file_size = int(r['Content-length'])
        else:
           file_size = int(r.headers['content-length'])
    except:
        print "Invalid URL"
        return
    if os.path.exists(file_name):
        outputFile = open(file_name, "ab")
        fileExistSize = os.path.getsize(file_name)
        print "already download file size", fileExistSize
        if fileExistSize == file_size:
            print "File already downloaded!"
            sys.exit()
        start = fileExistSize + 1
        file_size = file_size - fileExistSize
    else:
        start = 0
    part = int(file_size) / numConnection
    fp = open(file_name, "wb")
    fp.write('\0' * file_size)
    fp.close()
    for i in range(numConnection):
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
    print '%s downloaded' % file_name


# argsInput(sys.argv[1:])
downloadFileURL()
print "Total downloaded --> ", totalDownloaded
