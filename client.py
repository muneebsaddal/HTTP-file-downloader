import sys, getopt, requests, threading 

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
   for opt,arg in opts:
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

   if (numConnection is '' or metricInterval is '' or connectionType is '' or fileLocation is '' or outputLocation is ''):
      print '--Input Argument error--\nEnter all the required arguments'
      sys.exit()

   print 'r', resumeFlag
   print 'n', numConnection
   print 'i', metricInterval
   print 'c', connectionType
   print 'f', fileLocation
   print 'o', outputLocation

lock = threading.Lock()
fileLocation = "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
file_name = fileLocation.split('/')[-1]
global file_size
numConnection = 4
totalDownloaded = 0

def handlerURL(start, end, url, filename): 
   global totalDownloaded
   headers = {'Range': 'bytes=%d-%d' % (start, end)} 
   r = requests.get(url, headers=headers, stream=True) 
   with open(filename, "r+b") as fp:
      threadedSize = end - start
      threadedDown = 0
      fp.seek(start) 
      var = fp.tell()
      buffer = r.content
      threadedDown += len(buffer)
      fp.write(buffer)
      totalDownloaded += threadedDown
      status = r"%10d  [%3.f%%]" % (threadedDown, threadedDown * 100. / threadedSize)
      #status = status + chr(8)*(len(status)+1)
      print status
 
def downloadFileURL(): 
   r = requests.head(fileLocation) 
   statusCode = r.status_code 
   print statusCode
   if statusCode == 404:
      print 'File not found'
      sys.exit()
   elif statusCode == 200:
      numConnection = 3
   try: 
      file_size = int(r.headers['content-length']) 
   except: 
      print "Invalid URL"
      return
   part = int(file_size) / numConnection 
   fp = open(file_name, "wb") 
   fp.write('\0' * file_size) 
   fp.close() 
   for i in range(numConnection): 
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


#argsInput(sys.argv[1:])
downloadFileURL()
print totalDownloaded