import sys, getopt

#takes in two sets, orders them and returns complement items
def getcomplement(seta, setb):
    lia = list(seta)
    lib= list(setb)
    complement= []
    if len(lia) < len(lib):
        l1= lib
        l2= lia
    else:
        l1= lia
        l2= lib
    for x in l1:
        if x not in l2:
            complement.append(x)
    if len(complement)==1:
        return complement[0]
    elif len(complement)>1:
        #print 'seta, setb, complement:',seta,setb,complement
        return complement
    else:
        return #never going to come to this case

#To display associations
def assocprint(assoc):
    key_pair = assoc.keys()
    for key in key_pair:
        print "\n ",key[0]," => ",key[1]," = ",assoc[key]

def assocopwrite(outputfile, label, assoc):
    # Print original file
    print "***Output File written -*****************"
    try:
        file = open(outputfile, 'a')
    except:
        print 'File cannot be opened:', outputfile
        exit()
    file.write("\n **********" + label + "***********\n")
    key_pair = assoc.keys()
    for key in key_pair:
        file.write("\n "+ str(key[0])+ " => "+ str(key[1]) + " = "+ str(assoc[key]))

    file.close()

def opwrite(outputfile, label, data):
    # Print original file
    print "***Output File written -*****************"
    try:
        file = open(outputfile, 'a')
    except:
        print 'File cannot be opened:', outputfile
        exit()

    file.write("\n **********"+label+"***********\n")
    keylist = data.keys()
    for key in keylist:
        file.write("\'"+str(key)+"\': "+ str(data[key])+", ")
    file.write("\n")

    file.close()

def apriory(inputfile, outputfile, minsup, minconf):

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

   try:
       file = open(outputfile, 'w')
   except:
       print 'File cannot be opened:', outputfile
       exit()

   file.close()

   #Solve first level
   print "*** Pre Process the data -*****************"
   try:
       file = open(inputfile)
   except:
       print 'File cannot be opened:', inputfile
       exit()

   ogdata_list = []
   datalist= []
   for line in file:
       words = line.split()
       ogdata_list.append(words)
       for word in words:
           datalist.append(word)
   print 'Original datalines:', ogdata_list

   # Close file after use
   file.close()

   print 'Datalist', datalist

   #Pick one data at a time- One itemset data frequency
   print "*** Creating One Item Set -*****************"
   datadict = dict()
   for i in datalist:
       if i not in datadict:
           datadict[i] = 1.0
       else:
           datadict[i] += 1.0
   print 'Datadict: ',datadict

   #Filter based on minsup - one item set
   keys_list = datadict.keys()
   for key in keys_list:
       if datadict[key] < minsup * len(ogdata_list):
           del datadict[key]

   print 'Filtered One Data Set with minsup: ', datadict
   opwrite(outputfile, 'One Item Set', datadict)
   #new datadict

   #Pick two data at a time from this set
   print "*** Creating Two Item Set -*****************"
   keys_list = datadict.keys()
   datadict2 = {}
   for key1 in keys_list:
       keys_list.pop(keys_list.index(key1))
       for key2 in keys_list:
           if key1 != key2 :
               #print 'keys:', key1, key2
               if (key1, key2) not in datadict2.keys():
                   datadict2[(key1, key2)] = 0.0 #key added
               for x in ogdata_list:
                   if (key1 in x) and (key2 in x):
                       datadict2[(key1, key2)] += 1.0
                       #print 'added!', key1, key2
   print 'Datadict2', datadict2

   #Filter based on minsup - Two item set
   keys_list = datadict2.keys()
   for key in keys_list:
       if datadict2[key] < minsup * len(ogdata_list):
           del datadict2[key]

   print 'Filtered Two Data Set with minsup: ', datadict2
   opwrite(outputfile, 'Two Item Set', datadict2)
   # new datadict2

   #Pick Three item set
   print "*** Creating Three Item Set -*****************"
   datadict3 ={}
   keys_list = datadict2.keys()
   for (x,y) in keys_list:
       keys_list.pop(keys_list.index((x,y)))
       for (p,q) in keys_list:
           if x == p or y == p:
               if (x,y,q) not in datadict3.keys():
                   datadict3[(x, y, q)] = 0.0
               else:
                   datadict3[(x,y,q)] += 1.0
           if x == q or y == q:
               if (x, y, p) not in datadict3.keys():
                   datadict3[(x, y, p)] = 0.0
               else:
                   datadict3[(x, y, p)] += 1.0
   print 'Datadict3: ',datadict3

   # Filter based on minsup - Three item set
   keys_list = datadict3.keys()
   for key in keys_list:
       if datadict3[key] < minsup * len(ogdata_list):
           del datadict3[key]

   print 'Filtered Three Data Set with minsup: ', datadict3
   opwrite(outputfile, 'Three Item Set', datadict3)
   # new datadict3

   #associations
   key_list3 = datadict3.keys()
   #print 'keylist3:', key_list3
   key_list2 = datadict2.keys()
   #print 'keylist2:', key_list2
   key_list = datadict.keys()
   #print 'keylist:', key_list
   allassoc = {} # will be ((x,y),z): [p,q]= (x,y)-> z , confidence p, lift q
   #confidence is calculated by using (x,y,z)/ (x,y)
   #lift is calculated by using (x,y,z)/ (x)*(y)
   mainassoc = {} # will be ((x,y),z): [p,q]= (x,y)-> z , confidence p, lift q
   fullconfassoc = {} # will be ((x,y),z): [p,q]= (x,y)-> z , confidence p, lift q

   for key3 in key_list3:
       #print 'key3:', key3
       key_list3.pop(key_list3.index(key3))
       for key2 in key_list2:
           comp = getcomplement(key3, key2)
           if isinstance(comp, str):
               complement = tuple((comp,))
           else:
               complement = tuple(comp)
           #Taking in normal order
           if (key2, complement) not in allassoc.keys():
               conf = (datadict3[key3]/ len(ogdata_list))/ (datadict2[key2]/ len(ogdata_list))
               lift = 0.0
               #lift = (datadict3[key3]/ len(ogdata_list))/ (((datadict2[key2]/len(ogdata_list)))*((datadict1[key3]/len(ogdata_list))))
               allassoc[(key2, complement)] = [conf, lift]
               if (conf >= minconf):
                   mainassoc[(key2, complement)] = [conf, lift]
                   if (conf == 1.0):
                       fullconfassoc[(key2, complement)] = [conf, lift]
           elif (complement, key) not in allassoc.keys(): #taking in reverse order
               conf = (datadict3[key3] / len(ogdata_list)) / (datadict[complement] / len(ogdata_list))
               lift = 0.0
               # lift = (datadict3[key3]/ len(ogdata_list))/ (((datadict2[key2]/len(ogdata_list)))*((datadict1[key3]/len(ogdata_list))))
               allassoc[(complement, key2)] = [conf, lift]
               if (conf >= minconf):
                   mainassoc[(complement, key2)] = [conf, lift]
                   if (conf == 1.0):
                       fullconfassoc[(complement, key2)] = [conf, lift]
       for key in tuple(key_list):
           key1 = [key]
           comp = getcomplement(key3, tuple(key1))
           complement = tuple(comp)
           # Taking in normal order
           if (tuple(key1), complement) not in allassoc.keys():
               conf = (datadict3[key3] / len(ogdata_list)) / (datadict[key] / len(ogdata_list))
               lift = 0.0
               allassoc[(tuple(key1), complement)] = [conf, lift]
               if (conf >= minconf):
                   mainassoc[(tuple(key1), complement)] = [conf, lift]
                   if(conf == 1.0):
                       fullconfassoc[(tuple(key1), complement)] = [conf, lift]
           elif (complement, tuple(key)) not in allassoc.keys():  # taking in reverse order
               conf = (datadict3[key3] / len(ogdata_list)) / (datadict[complement] / len(ogdata_list))
               lift = 0.0
               allassoc[(complement, tuple(key1))] = [conf, lift]
               if (conf >= minconf):
                   mainassoc[(complement, tuple(key1))] = [conf, lift]
                   if (conf == 1.0):
                       fullconfassoc[(complement, tuple(key1))] = [conf, lift]
   print 'Main Assoc: ', mainassoc
   assocprint(mainassoc)
   assocopwrite( outputfile , 'Main Assoc: ', mainassoc)
   print 'All Assoc: ', allassoc
   print 'Full Assoc: ', fullconfassoc
   assocprint(fullconfassoc)
   assocopwrite(outputfile, 'Full Assoc: ', fullconfassoc)











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
      elif opt in ("-s", "--support"):
          minsupport = float(arg)
      elif opt in ("-c", "--confidence"):
          minconfidence = float(arg)
   '''# Enable for static testing only
   inputfile = 'inputtext.txt'
   outputfile = 'outputtext.txt'
   minconfidence = 0.5
   minsupport = 0.1
   '''


   apriory(inputfile,outputfile, minsupport, minconfidence)
   print 'Input file is ', inputfile
   print 'Output file is ', outputfile
   print 'Min Support is ', minsupport
   print 'Min Confidence is ', minconfidence

if __name__ == "__main__":
   main(sys.argv[1:])