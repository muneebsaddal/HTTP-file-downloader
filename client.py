import sys, getopt

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

argsInput(sys.argv[1:])
