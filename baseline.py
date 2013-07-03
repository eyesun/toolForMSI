import sys
import re




def main():
	ashmpToRead = open('BaselineAsh.txt', 'r')
	orcToRead = open('BaselineOrca.txt', 'r')
	baseline = open('baseline.csv', 'a')
	#here is some variables we need
	ashFileName = ''
	ashFileLoc =''
	ashFileVers = ''

	orcFileName = ''
	orcFileVers = ''


	#read every line in the Ashampoo file to extract the fileName, fileLocation, fileVersion
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
								baseline.write(ashFileName + ',' + ashFileLoc + ',' + ashFileVers + '\n')
							if ashFileVers == '0.0.0.0' and orcFileVers != '':
								##Actually, here is a bug and hasn't figure out. Because maybe there is 2 file with same name but diffrent
								##version, the code below just matching the first orca file version and omit the others(It will break when find
								##the first matching version)
								baseline.write(ashFileName + ',' + ashFileLoc + ',' + orcFileVers)
							if ashFileVers == '0.0.0.0' and orcFileVers == '':
								baseline.write(ashFileName + ',' + ashFileLoc + '\n')
							break
				orcToRead.seek(0)

	#close all files
	ashmpToRead.close
	orcToRead.close
	baseline.close
if __name__ == '__main__':
	main()
