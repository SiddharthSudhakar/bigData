import sys, getopt

def apriory(inputfile, outputfile):

   #Print original file
   print "***Original File -*****************"
   try:
       file = open(inputfile)
   except:
       print 'File cannot be opened:', inputfile
       exit()

   for list in file:
      print list.split()

   file.close()

   #Solve first level
   print "***Solve First Level-*****************"
   try:
       file = open(inputfile)
   except:
       print 'File cannot be opened:', inputfile
       exit()

   counts = []
   for line in file:
       words = line.split()
       count = dict()
       for word in words:
           if word not in count:
               count[word] = 1
           else:
               count[word] += 1
       counts.append(count)
   print counts

   file.close()




#Main program will intake the input file and the output file
#According to " apriory.py -i <inputfile> -o <outputfile> " format
def main(argv):
   inputfile = ''
   outputfile = ''
   minsuccess = ''
   try:
      opts, args = getopt.getopt(argv,"i:o:m",["ifile=","ofile=", "msupport="])
   except getopt.GetoptError:
      print 'apriory.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'apriory.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
      elif opt in ("-m", "--msupport"):
         outputfile = arg
   inputfile = 'inputtext.txt'
   outputfile = 'outputtext.txt'
   minsuccess = ''
   apriory(inputfile,outputfile)
   print 'Input file is "', inputfile
   print 'Output file is "', outputfile
   print 'Min Success is "', minsuccess

if __name__ == "__main__":
   main(sys.argv[1:])