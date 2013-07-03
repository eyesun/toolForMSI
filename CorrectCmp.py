import re
import sys
import time
import string

#define the comparision file
HFfilenameGlobal = 'HFfile.csv'
BLfilenameGlobal = 'Baselinefile.csv'
CompResultname = 'CompResult.csv'

BLfilename2 ='tempPartBL.txt' # storge compararion record in BL
DiffFilename = 'tempDiffBL.txt'



 



#Function is testing whether info is in BaseLine
def CompBLine(HFfilename,HFfileloc,HFfileVer):
 # print 'Func CompBLine'

  #define the variable APHelper.dll,C:\Program Files\Citrix\Group Policy\Client-Side Extension\,7.2.10009.1


  
  global BLfilenameGlobal
  global CompResultname
  global BLfilename2
  

  
  #open file
  BLfile = open(BLfilenameGlobal,'r')
  CompResultFile = open(CompResultname,'a')
  BLTemp = open(BLfilename2,'a')

  
  #define variable
  BLfileName = ''
  BLfileVer = ''
  BLfileloc = ''

  flag = 0 # define whether match filename and fileversion
  

  for line in BLfile:
  #  print line
    linelist = line.split(',')
    if linelist:
        BLfileName = linelist[0].strip()
        BLfileloc = linelist[1].strip()
        BLfileVer  = linelist[2].strip()
      #  print '%%%%%%bl:',BLfileName,BLfileloc,BLfileVer
        
        if BLfileName == HFfilename and BLfileloc == HFfileloc:
         #    print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@  +++equal++++@@@@@@@@@'
             flag = 1
             BLTemp.write(line)
           #  print HFfilename,BLfileVer,HFfileVer
             if  isVerUpgrade(BLfileVer,HFfileVer)=='Degrade':
                string = HFfilename+','+HFfileloc+','+HFfileVer+','+'Version_Degrade\n'
            #    print HFfilename+'*<<< <*******'
                CompResultFile.write(string)
                break
             elif  isVerUpgrade(BLfileVer,HFfileVer)=='Equal':
                string = HFfilename+','+HFfileloc+','+HFfileVer+','+'Version_Equal\n'
             #   print HFfilename+'*=== ==*******'
                CompResultFile.write(string)
                break
     
  if flag == 0:
        string = HFfilename+','+HFfileloc+','+HFfileVer+','+'NewFile\n'
 #       print '******add excep*******',string
        CompResultFile.write(string)
  
 
  #close file          
  BLfile.close()
  CompResultFile.close()
  BLTemp.close()
     
            
           

#Function is comparing two file diff
def FileDiff(fileAllname,filePartname,resultname):

   #open file
    fileAll = open(fileAllname,'r')
    filePart = open(filePartname,'r')
    result = open(resultname,'w')

   
   
    m1 = fileAll.readlines()
    m2 = filePart.readlines()
    
    list1 = [x for x in m1 if x not in m2]
   
    for i in range(len(list1)):
       list1[i] = list1[i].strip()+','+'DeletedFile'
    
    string = '\n'.join(list1)
    result.write(string)

    #close file
   
    fileAll.close()
    filePart.close()
    result.close()
    
   

#Function is write content from file1 to file2
def WriteFileFromAnther(ToFilename,FromFilename):
    
 
    ToFile = open(ToFilename,'a')
    FromFile = open(FromFilename ,'r')

    for i in FromFile:
      ToFile.write(i)

    ToFile.close()
    FromFile.close()
#Function is testing whether the version is correct
def isVerUpgrade(oldVer,newVer):
 #  print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
   if oldVer =='' or newVer =='' :
      return 'Upgrade'
   #print oldVer+'\n'
   #print newVer+'\n'

   oldVerlist = oldVer.split('.')
   newVerlist = newVer.split('.')
   
   #print newVerlist
  # print oldVerlist

   #define the variable
   i=0
   result = 'Equal'
  
   for old in oldVerlist:
     new = string.atoi(newVerlist[i]) 
     old = string.atoi(old)
     i=i+1
    # print "******************=====,old=%s,new=%s,result=%s"%(old,new,result)
     if new == old:
     #   print 'equal' + result
        continue
     elif new>old:
        result ='Upgrade'
      #  print '>' + result
        return result
     else :
        result = 'Degrade'
       # print newVerlist
      #  print oldVerlist
        return 'Degrade'
     
        
  # print "\n======="+result
   return result  

def ReadFile(filename):
   Rfile = open(filename,'r')
   for line in Rfile:
      print line
   Rfile.close()


def HFvsBaseLine():


  #global variable
  global HFfilenameGlobal
  global BLfilenameGlobal
  global CompResultname
  global BLfilename2
  global DiffFilename

  #open file
  HFfile = open(HFfilenameGlobal,'r')
  CompResultFile = open(CompResultname,'r')

  
  #define the variable
  HFfileName = ''
  HFfileVer = ''
  HFfileloc = ''
  i=0

  for line in HFfile:
       HFlist = line.split(',')
       i=i+1
   
       if HFlist:
         HFfileName = HFlist[0].strip()
         HFfileloc  = HFlist[1].strip()
         HFfileVer = HFlist[2].strip()
 
         # detect the record  from BL
         CompBLine(HFfileName,HFfileloc,HFfileVer)
  

 
  FileDiff(BLfilenameGlobal,BLfilename2,DiffFilename)

  WriteFileFromAnther(CompResultname,DiffFilename)

  #close file
          
  HFfile.close()           
  CompResultFile.close()
     
def getFileName():
  
   #global variable
    global HFfilenameGlobal
    global BLfilenameGlobal
    global CompResultname
    global BLfilename2
    global DiffFilename
    
    num = raw_input('''Input 1 or 2:\n
                   1: Choose to default HF file name : HFfile.csv\n
                   2: Input the HF file name yourself \n''')
    
    if num == '2':
          HFfilenameGlobal = raw_input( 'Please input the HF file name:')

    
    num = raw_input('''Input 1 or 2:\n
                   1: Choose to default Baseline file name : Baselinefile.csv\n
                   2: Input the Baseline file name yourself \n''')

    if num == '2':
          HFfilenameGlobal = raw_input( 'Please input the Baseline file name:')


    num = raw_input('''Input 1 or 2:\n
                   1: Choose to CompResult HF file name : CompResult.csv\n
                   2: Input the CompResult file name yourself \n''')


    if num == '2':
          HFfilenameGlobal = raw_input( 'Please input the CompResult file name:')
   
    
         
def inputTimestamp():

    #write time stamp in the beginning of result file
  nowTime =time.strftime('%Y-%m-%d %H: %M :%S',time.localtime(time.time()))
  print nowTime

     #open file
  CompResultFile = open(CompResultname,'w')
  
  CompResultFile.write('\n\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n')
  CompResultFile.write('Update Time:  '+nowTime+'\n')
  CompResultFile.write('VDA Verson :  5.6.300.9 \n')
  CompResultFile.write('   OS      :  Win7-SP -X86  \n \n')
  CompResultFile.write('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n\n')

    #write one record to ComResultFile as the title
  CompResultFile.write('FileName,FileLocation,FileVersion,ExceptionType\n')

  #close the file
  CompResultFile.close()

  
#delete McAfee files
def deleMcAfeeAndWinsxs():

  global CompResultname
  comp = open(CompResultname,'r')
  temp = open('tempMcAfee.csv','w')
  
  #search whether the loc has McAfee
  pat1=r'.*McAfee.*'
  pat2=r'.*winsxs.*'



  for line in comp:
    findMcAfee = re.search(pat1,line)
    findWinsxs = re.search(pat2,line)
    if findMcAfee is None and findWinsxs is None:
       temp.write(line)             
  
   #close the file
  comp.close()
  temp.close()
 
  WriteFileFromAnther(CompResultname,'tempMcAfee.csv')

  

  #close the file
  temp.close()
  comp.close()

        
  
def main():
  getFileName()
  inputTimestamp()
  HFvsBaseLine()

  deleMcAfeeAndWinsxs()

if __name__=='__main__':
   print '\n\n\n\n\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
   main()

