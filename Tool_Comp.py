import re
import sys
import time
import string
import os
import shutil


os.mkdir('temp')

#define the comparision file
HFfilenameGlobal = 'HFfile.csv'
BLfilenameGlobal = 'Baselinefile.csv'
CompResultname = 'CompResult.csv'

BLfilename2 =os.path.normpath('temp/tempPartBL.txt') # storge compararion record in BL
DiffFilename = os.path.normpath('temp/tempDiffBL.txt')



 



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
#   print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
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
          BLfilenameGlobal = raw_input( 'Please input the Baseline file name:')


    num = raw_input('''Input 1 or 2:\n
                   1: Choose to CompResult HF file name : CompResult.csv\n
                   2: Input the CompResult file name yourself \n''')


    if num == '2':
          CompResultname = raw_input( 'Please input the CompResult file name:')
   
    
 # add timestamp in the front of the comp file        
def inputTimestamp(CompResultname):

    #write time stamp in the beginning of result file
  nowTime =time.strftime('%Y-%m-%d %H: %M :%S',time.localtime(time.time()))
 # print nowTime

     #open file
  CompResultFile = open(CompResultname,'w')
  
  CompResultFile.write('\n\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n')
  CompResultFile.write('  Update   Time  :  '+nowTime+'\n')
  CompResultFile.write('Baseline Version :  5.6.200.9 \n')
  CompResultFile.write('   HF    Version :  5.6.300.8 \n')
  CompResultFile.write('   OS      :  Win7-SP -X86  \n \n')
  CompResultFile.write('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n\n')

    #write one record to ComResultFile as the title
#  CompResultFile.write('FileName,FileLocation,FileVersion,ExceptionType\n')

  #close the file
  CompResultFile.close()

# copy the content of file1 to file2
def copyFile(fName1,fName2):
  file1 = open(fName1,'r')
  file2 = open(fName2,'w')
  
  for line in file1:
    file2.write(line)
  
  file1.close()
  file2.close()
  
  
#delete McAfee files
def deleMcAfeeAndWinsxs():

  global CompResultname
  comp = open(CompResultname,'r')
  temp = open(os.path.normpath('temp/tempMcAfee.txt'),'w')
  
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
 
  #write into comp from temp
  copyFile(os.path.normpath('temp/tempMcAfee.txt'),CompResultname)
  
        
#count the times of driver files whether  it includes four records 
def CountDriverFileTimes(filename):
   
    #open file
    Readfile = open(filename,'r')
    Tempfile = open(os.path.normpath('temp/TempAppearFour.txt'),'w')
    
    #read file into a list   
    RecordList = Readfile.readlines()
 
    # a directory to save the time of every record
    RecordTimesDir = {}
    for line in RecordList:
       Filename = line.split(',')[0]
       RecordTimesDir[Filename] = 0

    for line in RecordList:
       Filename = line.split(',')[0]
       RecordTimesDir[Filename] = RecordTimesDir[Filename]+1
      
    # put filename Appearing four times into file TempAppearFour
    for i in RecordTimesDir:
       if RecordTimesDir[i] == 4 :
          Tempfile.write(i+'\n')

          

    #close file
   
    Readfile.close()
    Tempfile.close()

# 
def findAppearFourFiles(filename):
   #open file
  Readfile =  open(filename,'r')
  tempfile = open(os.path.normpath('temp/TempAppearFour.txt'),'r')
  writefile = open(os.path.normpath('temp/TempAppearRecord.txt'),'w')   
  
  tempfileList = tempfile.readlines()
  templist =[]
  # delete \n
  for i in tempfileList:
     templist.append(i.split()[0]) #split fun will return a  list
  #print templist


  for line in Readfile:
    filename = line.split(',')[0]
   
    if filename in templist:
       writefile.write(line)

  #close flle
  Readfile.close()
  tempfile.close()
  writefile.close()

#get the copy of a file  exception of the timestamp
def GetFileDataCopy(filename,filecopyname):
   file1 = open(filename,'r')
   file2 = open(filecopyname,'w')
   
   for line in file1:
      if len(line.split(',')) == 4:
        file2.write(line)

   file1.close()
   file2.close()


def IsDeleDriverAppearFour(filename):
    
    GetFileDataCopy(filename,os.path.normpath('temp/copyfile.txt'))
    ApearFourFile1 = open(filename,'r')
    ApearFourFile2 = open(os.path.normpath('temp/copyfile.txt'),'r')

    
    for line1 in  ApearFourFile1:
      fName1 = line1.split(',')[0]
      fVer1 = line1.split(',')[1]
      fType1 = line1.split(',')[3]
      if fType == 'NewFile':
        for line2 in  ApearFourFile2:
            fName2 = line2.split(',')[0]
            fVer2 = line2.split(',')[1]
            fType2 = line2.split(',')[3]
 #           if fType2 == 'DeletedFile' and fName1 == fName2 
 


               
 # to judge whether two locations is the same exception of the last one
 # exp.  c:/programfile/citrix/
 #       c:/programfile/window/  return true
def isLocSimilar(loc1,loc2):
   result = False
   loc1 = loc1.strip()
   loc2 = loc2.strip()
   # define two list to save two loc
   list1 = loc1.split('\\') 
   list2 = loc2.split('\\')
#   print '###########'
#   print list1,list2
   len1 = len(list1)
   len2 = len(list2)

   if len1 != len2:
      return result
   for i in range(len1-2):
     if list1[i] != list2[i]:
        return result
   result = True
 #  print result
   return result


#append the content of a file
def AppendData(fileAppendName,fileContentName):
   f1 =open(fileAppendName,'a')
   f2 = open(fileContentName,'r')
   
   for line in f2:
     f1.write(line)
     
   f1.close()
   f2.close()
  
 

#Function is comparing two file diff
def GetRemain_After_Dele(fileAllname,filePartname,resultname):

   #open file
    fileAll = open(fileAllname,'r')
    filePart = open(filePartname,'r')
    result = open(resultname,'w')

   
   
    m1 = fileAll.readlines()
    m2 = filePart.readlines()
    
    list1 = [x for x in m1 if x not in m2]
   
    for i in range(len(list1)):
       list1[i] = list1[i].strip()
    
    string = '\n'.join(list1)
    result.write(string)

    #close file
   
    fileAll.close()
    filePart.close()
    result.close()  
# delete a pair of new and delete file which have the similar loc and upgrade version   
def Delete_NewDelete_Pair(filename):
  
    GetFileDataCopy(filename,os.path.normpath('temp/copyfile.txt'))
    compFile = open(filename,'r')
    copyFile = open(os.path.normpath('temp/copyfile.txt'),'r')
    tempFile = open(os.path.normpath('temp/New_Delete_Pair.txt'),'w')
    resultFile = open(os.path.normpath('temp/Post_dele_ND_Pair.txt'),'w')
    
 
    
    for line1 in  compFile:
      lineList1 = line1.split(',')
      if len(lineList1)==4:
        fName1 =  lineList1[0]
        fLoc1 =  lineList1[1]
        fVer1 =  lineList1[2]       
        fType1 =  lineList1[3].strip()
     #   print '@@@@@@@@@@@@@@@@@@@@@@@',line1,' type==',fType1
        if fType1 == 'NewFile':
        #  print 'enter\n\n'
	  for line2 in  copyFile:
            lineList2 = line2.split(',')
            if len(lineList2)==4:
              fName2 =  lineList2[0]
              fLoc2 =  lineList2[1]
              fVer2 =  lineList2[2]
              fType2 = lineList2[3].strip()
              if fType2 == 'DeletedFile' :
          #       print 'no enter panduan:====',fName1,'  ',fName2,'\n\n'
            #     print 'Dele@@@ fName1=%s, fName2=%s\n\n'%(fName1,fName2)
                 if fName1 == fName2 and isLocSimilar(fLoc1,fLoc2) and isVerUpgrade(fVer2,fVer1)== 'Upgrade':
            #        print line1
             #       print line2,'\n\n'
                    tempFile.write(line1)
                    tempFile.write(line2)
                    break
          copyFile.seek(0)     
    
    
     #close files
    compFile.close()
    copyFile.close()
    tempFile.close() 

    #delete new_Delete_Pair 
    GetRemain_After_Dele(os.path.normpath('temp/copyfile.txt'),os.path.normpath('temp/New_Delete_Pair.txt'),os.path.normpath('temp/Post_dele_ND_Pair.txt'))
    inputTimestamp(CompResultname)
    #copy the content of resultFile to compfile
   # copyFile('Post_dele_ND_Pair.txt',filename)
    AppendData(CompResultname,os.path.normpath('temp/Post_dele_ND_Pair.txt'))
    
   

def main():
  
  global CompResultname
 
  getFileName()
  inputTimestamp(CompResultname)
  HFvsBaseLine()

  deleMcAfeeAndWinsxs()
  
  Delete_NewDelete_Pair(CompResultname)
  CountDriverFileTimes(CompResultname)
  findAppearFourFiles(CompResultname)
  shutil.rmtree(os.path.normpath('temp/'))
if __name__=='__main__':
   print '\n\n\n\n\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
   main()

