import os
import sys
import getopt
import urllib2
import threading

#Getting input arguments and storing in variables
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

#If input argument format not correct, show error and exit
if numConnection is '' or metricInterval is '' or connectionType is '' or fileLocation is '' or outputLocation is '':
    print '--Input Argument error--\nEnter all the required arguments'
    sys.exit()

#Formating file name and initializing global variables
file_name = fileLocation.split('/')[-1]
file_name = outputLocation + file_name
totalDownloaded = 0
file_size = 0

#Thread function, downloads and writes respective part of file
def handlerURL(start, end, url, filename):
    global totalDownloaded
    global file_size
    headers = {'Range': 'bytes=%d-%d' % (start, end)}   #Define range of part of file to download
    request = urllib2.Request(url, headers=headers)
    r = urllib2.urlopen(request)    #Get request to the server
    file_size = int(r.headers['content-length'])    #Get file size
    with open(filename, "r+b") as fp:  #Create/Open the file to write
      threadedSize = end - start
      threadedDown = 0
      fp.seek(start)    #start writing from the position assigned to the thread
      buffer = r.read() #write the data into buffer
      threadedDown += len(buffer)   #update downloaded file length
      fp.write(buffer)  #write into file 
      totalDownloaded += threadedDown   #update total data downloaded
      per = (threadedDown / file_size) * 100    #percentage of downloaded by thread
      status = "Bytes of data downloaded --> %d  Percentage of total file downloaded --> [%.2f]" % (totalDownloaded, per)
      print "\n\nCurrent Thread in working:"
      print threading.current_thread()  #print the current thread in working
      print status

def downloadFileURL():
    global numConnection
    request = urllib2.Request(fileLocation)
    response = urllib2.urlopen(request)
    r = response.info()     #get header data
    try:
        file_size = int(r['Content-length'])    #get file length
    except:
        print "Invalid URL"
        sys.exit()
    if os.path.exists(file_name):
        outputFile = open(file_name, "r")
        fileExistSize = os.path.getsize(file_name)
        # If file already downloaded, end program
        if fileExistSize == file_size:
            print "\n\n*******************File already downloaded*******************\n"
            sys.exit()
        # If partially downloaded, resume
        start = fileExistSize + 1
        file_size = file_size - fileExistSize
    else:
        start = 0
    part = int(file_size) / int(numConnection)
    fp = open(file_name, "wb")
    fp.write('\0' * file_size)
    fp.close()
    # Make threads for each connection
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
    # Join threads to synchronise
    for t in threading.enumerate():
        if t is main_thread:
            continue
        t.join()

#Call to the downlaod file function
downloadFileURL()

#Showing Final output message
if totalDownloaded >= file_size:
	print "\n\n*******************Download Complete*******************\nTotal MBs downloaded --> ", totalDownloaded
else:
	print "\n\n*******************Download failed*******************\n"