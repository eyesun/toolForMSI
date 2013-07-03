"""
In this script, we need to extract information from Ashampoo file which contains all the files that have been installed.
Considering the shortage of Ashampoo file (lack of version information such as '**.sys'), we also need to compare the Ashampoo file with Orca file.
So, in this script, we need 2 arguments--Ashampoo file name and Orca file name. For different Ashampoo file we use different strategy to deal with,
so we use immutable name for all the files, the meaning of each file's name shows below
"""
#############################################################################
##  File Name     #           Meaning
############################################################################# 
##  freInst.txt   #   Ashampoo file generated with way of 'Fresh Installs'
##  UpInst.txt    #   Ashampoo file generated with way of 'Upgrade Installs'
##                #
##  orca.txt      #	  orca file extracted from msi
##############################################################################


import sys
import re

def main():
	ashFile = sys.argv[1]
	#orcaFile = sys.argv[2]
	ashmpToRead = open(ashFile , 'r')
	#orcToRead =open(orcaFile, 'r')
	orcToRead =open('orca.txt', 'r')
	output = open('hotfix.csv', 'a')
	extAshLog = open ('HFLog.txt', 'a') 
	#here is some variables we need
	ashFileName = ''
	ashFileLoc =''
	ashFileVers = ''
	orcFileName = ''
	orcFileVers = ''

	if ashFile == 'freInst.txt':
		for ashLine in ashmpToRead:
			if ashLine[0:3] == '[+]':
				match = re.match(r'\[\+\]\[([\s\S]*)\]', ashLine)
				if match:
					ashFileLoc = match.group(1)
			if ashLine[2:5] == '[+]':
				match = re.match(r'\s*\[\+\]\"(\S+)\"[\s\S]*(\d+\.\d+\.\d+\.\d+)', ashLine)
				if match:
					ashFileName = match.group(1)
					ashFileVers = match.group(2)
					#if ashFileVers == '0.0.0.0':
						#ashFileVers = 'verDmg'
					#read every line in the orca file to extract the fileName, fileVersion
					for orcLine in orcToRead:
						#for every file, they may have 2 kinds of different name -- inner name or public name
						#here we just need the public name
						if orcLine.find('|') != -1:##remove the inner fileName in orca file
							pat = r'([\s\S]+?)\|([\s\S]+?)[\s]+([\d\D]*)'
						else:
							pat = r'([\s\S]+?)[\s]+([\s\S]+?)[\s]+([\d\D]*)'
						match = re.match(pat, orcLine)
						if match:
							orcFileName = match.group(2)
							orcFileVers = match.group(3)
							if ashFileName == orcFileName:
								if ashFileVers != '0.0.0.0':
									output.write(ashFileName + ',' + ashFileLoc + ',' + ashFileVers + '\n')
								if ashFileVers == '0.0.0.0' and orcFileVers != '':
									##Actually, here is a bug and hasn't figure out. Because maybe there is 2 files with same name but diffrent
									##version, the code below just matching the first orca file version and omit the others(It will break when find
									##the first matching version)
									output.write(ashFileName + ',' + ashFileLoc + ',' + orcFileVers)
								if ashFileVers == '0.0.0.0' and orcFileVers == '':
									output.write(ashFileName + ',' + ashFileLoc + ',' + 'NOVERSION' + '\n')
								break
					orcToRead.seek(0)



	elif ashFile == 'UpInst.txt':
		for ashLine in ashmpToRead:
			if ashLine[0:3] == '[#]':
				match = re.match(r'\[\#\]\[([\s\S]*)\]', ashLine)
				if match:
					ashFileLoc = match.group(1)
			if ashLine[2:5] == '[+]':
				extAshLog.write(ashFileLoc + ashLine)
			if ashLine[2:5] == '[-]':
				extAshLog.write(ashFileLoc + ashLine)
			if ashLine[2:5] == '[*]':
				match = re.match(r'\s*\[\*\]\"(\S+)\"[\s\S]*(\d+\.\d+\.\d+\.\d+)', ashLine)
				if match:
					ashFileName = match.group(1)
					ashFileVers = match.group(2)
					#if ashFileVers == '0.0.0.0':
						#ashFileVers = 'verDmg'
					#read every line in the orca file to extract the fileName, fileVersion
					for orcLine in orcToRead:
						#for every file, they may have 2 kinds of different name -- inner name or public name
						#here we just need the public name
						if orcLine.find('|') != -1:##remove the inner fileName in orca file
							pat = r'([\s\S]+?)\|([\s\S]+?)[\s]+([\d\D]*)'
						else:
							pat = r'([\s\S]+?)[\s]+([\s\S]+?)[\s]+([\d\D]*)'
						match = re.match(pat, orcLine)
						if match:
							orcFileName = match.group(2)
							orcFileVers = match.group(3)
							if ashFileName == orcFileName:
								if ashFileVers != '0.0.0.0':
									output.write(ashFileName + ',' + ashFileLoc + ',' + ashFileVers + '\n')
								if ashFileVers == '0.0.0.0' and orcFileVers != '':
									##Actually, here is a bug and hasn't figure out. Because maybe there is 2 files with same name but diffrent
									##version, the code below just matching the first orca file version and omit the others(It will break when find
									##the first matching version)
									output.write(ashFileName + ',' + ashFileLoc + ',' + orcFileVers)
								if ashFileVers == '0.0.0.0' and orcFileVers == '':
									output.write(ashFileName + ',' + ashFileLoc + ',' + 'NOVERSION' + '\n')
								break
					orcToRead.seek(0)

	else:
		extAshLog.write("wrong file name")

	ashmpToRead.close
	orcToRead.close
	output.close
	extAshLog.close
if __name__ == '__main__':
	main()
