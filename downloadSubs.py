import sys, os, subprocess, re

maps = []
languages = ["nl","en"]

#Recursion in maps
SET_RECURSION = False
#Languages which has to be searched
ITERATION_LANG = False

#Check if input is equal to checkArg, Caps are ignored by default
def isArg(input, checkArg, caps=False):
	if caps == False:
		return re.match(input, checkArg, re.IGNORECASE)
	return re.match(input, checkArg)

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

#List all files in dir
def listFiles(dir):
	return os.listdir(dir)

#Find and download subs for file
def findSub(file):
	for lang in languages:
		command = "subliminal download -l "+ lang+" \""+file+"\""
		print(command)
		process = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
		output = process.stdout.read()
		#print("FINDSUB"+str(output))

#recursive functions which checks all files if they are a video, if so download subs, else go into map (if recursion is on)
def exploreMaps(dir):
	allFiles = listFiles(dir)
	for currentFile in allFiles:
		newFile = str(dir) + "/"  + str(currentFile)
		if SET_RECURSION & isMap(newFile):
			exploreMaps(newFile)
		elif isVideo(newFile):
			findSub(newFile)
	return

#check if dir(s) are given
if len(sys.argv) < 2:
	sys.exit("No directory given as parameter!")

#check input arguments
for arg in sys.argv:
	if ITERATION_LANG:
		languages = arg.split(",")
		ITERATION_LANG = False
	if isArg(arg, "-r"):
		SET_RECURSION = True
	if isArg(arg, "-l"):
		print("OOVERWRITING DEFAULT LANGAUGE SETTINGS" ,stderr)
		ITERATION_LANG = True
	if isMap(arg):
		maps.append(arg)

#Make sure the given dirs are a real dir
if maps == None or len(maps) < 1:
	sys.exit("No correct Directories given!")

#go into recursive function
for map in maps:
	exploreMaps(map)
