import sys, os, subprocess, re

maps = []
#Default languages which are searched for
languages = []

#Recursion in maps
SET_RECURSION = False
#Print the progress
SET_PRINT = False
#Only new videos without subs in that language
SET_NEW = False
#Limits of filesizes
lowLimit = -1
highLimit = -1

#Languages which has to be searched
ITERATION_LANG = False
ITERATION_LIMIT = False

BITSHIFT_BYTES = 9

#Check if input is equal to checkArg, Caps are ignored by default
def isArg(input, checkArg, caps=False):
	return input.lower() == checkArg.lower()	#if caps == False:
	#	return re.match(input, checkArg, re.IGNORECASE)
	#return re.match(input, checkArg)

#check if file is a map
def isMap(file):
	return os.path.isdir(file)

#check if file is a video
def isVideo(file):
	command = "mediainfo \""+str(file)+"\""
	process = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
	output = process.stdout.read()
	if "Video" in str(output):
		return True
	return False

#Check if the filesize is in the limits if they are set
def isInLimit(size):
	if (lowLimit != -1 & size < lowLimit):
		if SET_PRINT:
			print("File too small")
		return False
	if (highLimit != -1 & size > highLimit):
		if SET_PRINT:
			print("File too big")
		return False
	return True

#List all files in dir
def listFiles(dir):
	return os.listdir(dir)

#Find and download subs for file
def findSub(file,lang):
	command = "subliminal download -l "+ lang+" \""+file+"\""
	if SET_PRINT:
		print(command)
	process = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
	output = process.stdout.read()
	# TODO see what subs are downloaded and report nicely
	#print("FINDSUB"+str(output))

#Check if a sub already exists
def noSub(file, allFiles, lang):
	videoName = os.path.splitext(file)[0]
	for f in allFiles:
		if (videoName in f) & (str(f).endswith(str(lang)+".srt")):
			return False
	return True


#recursive functions which checks all files if they are a video, if so download subs, else go into map (if recursion is on)
def exploreMaps(dir):
	allFiles = listFiles(dir)
	for currentFile in allFiles:
		if not str(dir).endswith("/"):
			dir = str(dir) + "/"
		newFile = str(dir) + str(currentFile)
		if  isMap(newFile):
			if SET_RECURSION:
				exploreMaps(newFile)
		elif isVideo(newFile):
			for lang in languages:
				# Skip all if any sub of PREF is already there, or just any sub is there
				if ((not SET_NEW) | (SET_NEW & noSub(currentFile, allFiles, lang))) & isInLimit(os.path.getsize(newFile)):
					findSub(newFile, lang)
	return

#Calculate bytes
def byteStep(n):
	return 1024 * (n)

def get_num(x):
    return int(''.join(ele for ele in x if ele.isdigit()))

#The parse 
def parseLimit(string):
	string = string.lower()
	number = get_num(string)
	if "tb" in string:
		return parseLimit(str(byteStep(number)) + 'gb')
	elif "gb" in string:
		return parseLimit(str(byteStep(number)) + 'mb')
	elif "mb" in string:
		return parseLimit(str(byteStep(number)) + 'kb')
	elif "kb" in string:
		return parseLimit(str(byteStep(number)) + 'b')
	return number

#Set the file size limits
def setLimit(string):
	isLow = None
	lowLimit = -1
	highLimit = -1
	lowString = ""
	highString = ""
	for letter in string:
		if letter == '-':
			isLow = True
			continue;
		elif letter == '+':
			isLow = False
			continue
		elif isLow == True:
			lowString += letter
		elif isLow == False:
			highString += letter
	if lowString != "":
		lowLimit = parseLimit(lowString)
	if highString != "":
		highLimit = parseLimit(highString)
	return lowLimit, highLimit

#check if dir(s) are given
if len(sys.argv) < 2:
	sys.exit("No directory given as parameter!")

#check input arguments
for arg in sys.argv:
	if ITERATION_LANG:
		if arg == "":
			sys.exit("No correct languages given")
		languages = arg.split(",")
		ITERATION_LANG = False
	elif ITERATION_LIMIT:
		lowLimit, highLimit = setLimit(arg)
		ITERATION_LIMIT = False
	elif isArg(arg, "-r"):
		SET_RECURSION = True
	elif isArg(arg, "-limit"):
		ITERATION_LIMIT = True
	elif isArg(arg, "-l"):
		ITERATION_LANG = True
	elif isArg(arg, "-print"):
		SET_PRINT = True
	elif isArg(arg, "-new"):
		SET_NEW = True
	elif isMap(arg):
		maps.append(arg)

#Make sure the given dirs are a real dir
if maps == None or len(maps) < 1:
	sys.exit("No correct Directories given!")

if languages == []:
	sys.exit("No languages given!")

#go into recursive function
for map in maps:
	exploreMaps(map)
