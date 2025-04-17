#!/usr/bin/env python3

# userinput = input('Enter any key to continue, "a" to abort: ')
if not 'userinput' in locals():
	userinput = 'y'
# print(userinput)
if userinput == 'a' or userinput == 'A':
	print("Program terminated by user.")
	exit()
# exit()

# print('Task started.')

import os
import sys
# import time
# import pyperclip

# print(sys.argv)
# print(len(sys.argv))
# print(os.getcwd())
# print('Separator')

if len(sys.argv) == 1:
	helpvar = 1

for item in sys.argv[1:]:
	if item == '-s' or item == '--subfolder':
		subfolder = True
	elif item == '-d' or item == '--dryrun':
		dryrun = True
	elif item == '-r' or item == '--run':
		run = True
	elif item == '-i':
		incrementalNaming = True
		forcerun = 1
	elif '-t=' in item:
		target = item[3:]
	elif '-p' in item:
		partitionvar = item[2:]
		forcerun = 1
	elif '-f=' in item:
		filename = item[3:]
		exitvar = 1
	elif item == '-f' or item == '--force':
		forcerun = 1
	elif item == '-h' or item == '--help':
		helpvar = 1
	elif item[2:].isdigit():
		if '-f' in item:
			fcharlen = int(item[2:])
			# lcharlen = 0
			# forcerun = 1
		if '-l' in item:
			lcharlen = int(item[2:])
			# fcharlen = 0
			# forcerun = 1
		if '-w' in item:
			wordcount = int(item[2:])
	else:
		helpvar = 1
		print('Invalid argument: {} \n'.format(item))

if not 'target' in locals():
	target = os.getcwd()
if not 'filename' in locals():
	filename = ''
if not 'subfolder' in locals():
	subfolder = False
if not 'dryrun' in locals():
	dryrun = False
if not 'incrementalNaming' in locals():
	incrementalNaming = False
if not 'fcharlen' in locals():
	fcharlen = 0
if not 'lcharlen' in locals():
	lcharlen = 0
if not 'forcerun' in locals():
	forcerun = 0
if not 'helpvar' in locals():
	helpvar = 0
if not 'exitvar' in locals():
	exitvar = 0
if not 'wordcount' in locals():
	wordcount = 0
if not 'partitionvar' in locals():
	partitionvar = ''

if partitionvar != '':
	tempvar = partitionvar.partition('+')
	partitionvar = tempvar[0]
	partitionint = tempvar[2]
	if partitionint == '':
		partitionint = 0
	partitionint = int(partitionint)
	# print(partitionvar, partitionint)

# print(target) # Comment
# print(filename) # Comment
# pyperclip.copy(target) # Comment
# time.sleep(10) # Comment
# pyperclip.copy(filename) # Comment
# exit() # Comment
# print(subfolder)
# print(target) # Comment
# exit() # Comment
# print(os.getenv("HOME"))
# print(fcharlen)
# print(lcharlen)
# exit()
if helpvar == 1:
	print('renamechars.py is a python program to bulk rename files in a folder and/or its sub-folders.')
	print('Use -r to run the program without any other arguments.')
	print("Use -h for help.")
	print('Use -s to include subfolders.')
	print('Use -i for incremental naming of all file in the folder')
	print("Use -f to force run the program on files that don't have trigger charlist.")
	print("Use -f## for first ## characters.")
	print("Use -l## for last ## characters.")
	print("Use -w# for first # words.")
	print("Use -p@@ for partition. Optionally -p@@+## to include ## words after partition.")
	print("Use -t= for specifying target folder.")
	print("Use -d for dryrun. \n")
	print("Usage example:")
	print("renamechars.py -r")
	print("renamechars.py -h")
	print("renamechars.py -pEP+1")
	print("renamechars.py -s -f -d")
	print("renamechars.py -f10")
	print("renamechars.py -l10")
	print("renamechars.py -s -f -d -t=/home/prithivi/Temp")
	exit()

if target == os.getenv("HOME"):
	print('This program is prohibited to be run in home folder. \nProgram will now exit. Modify program to override.')
	exit()

charlist = [' ', '\\', '[', ']', '(', ')', '{', '}', '\'', '!', '+', '-', '~', ':', ';']
trans1 = ''.join(charlist)
trans2 = '_' * len(charlist)
transdict = ''.maketrans(trans1, trans2)
# print(trans1)
# print(trans2)
# print(transdict)
# exit()

# print('Checkpoint 1')
iteration = 1
count = 1
while count > 0:
	print(f'Iteration {iteration}')
	for folder, subfolders, files in os.walk(target):
		# print('\nFolder is :' + folder) # Comment
		# print('Checkpoint 2') # Comment
		if folder != target and subfolder == False:
			break
			# print('Checkpoint 3') # Comment

		for item in files:
			premod = os.path.join(folder, item)
			# print(premod + '\n') # Comment
			# print(filename)
			# print(item)
			if (any(chars in item for chars in charlist) or forcerun == 1) and (filename == '' or item == filename):
				filename = ''
				# print(premod) # Comment
				tempstring = item.translate(transdict)
				templist = tempstring.split('_')
				# print(templist)
				templist = list(filter(None, templist))
				# print(templist)
				tempstring = '_'.join(templist)
				tempstring = tempstring.replace('_.','.')
				tempstring = tempstring.replace('...','.')
				tempstring = tempstring.replace('..','.')
				tempstring = tempstring.replace('___','_')
				tempstring = tempstring.replace('_+_','_')
				tempstring = tempstring.replace('_-_','_')

				countval = tempstring.count(".") - 1
				tempstring = tempstring.replace('.', '_', countval)
				tempstring = tempstring.replace('__','_')
				file_ext = tempstring.split('.')
				if len(file_ext) > 1:
					file_ext = '.' + file_ext[-1]
					tempstring = tempstring.split('.')[:-1]
				else:
					file_ext = ''
					tempstring = tempstring.split('.')[0]
				# print(file_ext)
				# exit()

				www = 0
				tempstring = ''.join(tempstring)
				# print(tempstring)
				year = len(tempstring.split('_'))
				for index,items in enumerate(tempstring.split('_')):
					if 'www' in items or 'ww' in items:
						www = index + 3
						break
				for index,items in enumerate(tempstring.split('_')):
					if 'eason' in premod or 'EASON' in premod or 'S0' in premod or 's0' in premod or 'EP' in premod:
						# print(premod)
						# exit()
						break
					if items.isdigit() and index > www and len(items) == 4:
						year = index + 1
						break
				tempstring = tempstring.split('_')[www:year]
				if wordcount == 0:
					tempstring = '_'.join(tempstring)
				else:
					tempstring = '_'.join(tempstring[0:wordcount])
				# print(tempstring)
				tempstring1 = ''
				tempstring2 = ''
				if fcharlen != 0 and fcharlen <= len(tempstring):
					tempstring1 = tempstring[0:fcharlen]
				if lcharlen != 0 and lcharlen <= len(tempstring):
					tempstring2 = tempstring[-lcharlen:]
				if tempstring1 != '' or tempstring2 != '':
					tempstring = tempstring1 + tempstring2

				if partitionvar != '':
					tempstring1 = tempstring.split('_')
					tempstring = tempstring.partition(partitionvar)
					# print(tempstring)
					if tempstring[1] == '':
						continue
					tempvar = len(tempstring[0].split('_')) + partitionint
					if tempvar >= len(tempstring1):
						tempvar = len(tempstring1)
					# print(tempstring, tempvar, tempstring1, partitionvar, partitionint) # Comment
					tempstring1 = tempstring1[:tempvar]
					tempstring = '_'.join(tempstring1)

				if incrementalNaming == True:
					incrementalVar = 1
					tempstring = str(incrementalVar)
					postmod = os.path.join(folder, tempstring + file_ext)
					while os.path.isfile(postmod):
						tempstring = str(incrementalVar)
						incrementalVar = incrementalVar + 1
						postmod = os.path.join(folder, tempstring + file_ext)
				# exit() # Comment

				tempstring = tempstring + file_ext
				# print(tempstring)
				# exit()


				postmod = os.path.join(folder, tempstring)
				# print(postmod)
				if postmod != premod:
					cmd = 'mv -n "' + premod + '" "' + postmod + '"'
					print(premod + ' --> ' + postmod)
					# print('\n' + cmd + '\n')
					if dryrun == False:
						os.system(cmd)
						# print(exitvar) # Comment
						if exitvar == 1:
							exit()
				if incrementalNaming == True:
					if incrementalVar == 2:
						cmd = "echo file " + postmod + " > filelist.txt"
						os.system(cmd)
					elif incrementalVar > 2:
						cmd = "echo file " + postmod + " >> filelist.txt"
						os.system(cmd)

		# exit() # Comment
		for item in subfolders:
			premod = os.path.join(folder, item)
			# print(premod + '\n') # Comment
			if filename == '':
				filename = item
			if (any(chars in item for chars in charlist) or forcerun == 1) and item == filename:
				filename = ''
				# print(premod) # Comment
				tempstring = item.translate(transdict)
				templist = tempstring.split('_')
				# print(templist)
				templist = list(filter(None, templist))
				# print(templist)
				tempstring = '_'.join(templist)
				tempstring = tempstring.replace('_.','.')
				tempstring = tempstring.replace('...','.')
				tempstring = tempstring.replace('..','.')
				tempstring = tempstring.replace('___','_')
				tempstring = tempstring.replace('_+_','_')
				tempstring = tempstring.replace('_-_','_')
				tempstring = tempstring.replace('.','_')
				tempstring = tempstring.replace('__','_')


				www = 0
				tempstring = ''.join(tempstring)
				# print(tempstring)
				year = len(tempstring.split('_'))
				for index,items in enumerate(tempstring.split('_')):
					if 'www' in items:
						www = index + 3
						break
				for index,items in enumerate(tempstring.split('_')):
					if 'eason' in premod or 'EASON' in premod or 'S0' in premod or 's0' in premod or 'EP' in premod:
						# print(premod)
						# exit()
						break
					if items.isdigit() and index > www and len(items) == 4:
						year = index + 1
						break
				tempstring = tempstring.split('_')[www:year]
				if wordcount == 0:
					tempstring = '_'.join(tempstring)
				else:
					tempstring = '_'.join(tempstring[0:wordcount])
				# print(tempstring)
				tempstring1 = ''
				tempstring2 = ''
				if fcharlen != 0 and fcharlen <= len(tempstring):
					tempstring1 = tempstring[0:fcharlen]
				if lcharlen != 0 and lcharlen <= len(tempstring):
					tempstring2 = tempstring[-lcharlen:]
				if tempstring1 != '' or tempstring2 != '':
					tempstring = tempstring1 + tempstring2

				if partitionvar != '':
					tempstring1 = tempstring.split('_')
					tempstring = tempstring.partition(partitionvar)
					if tempstring[1] == '':
						continue
					tempvar = len(tempstring[0].split('_')) + partitionint
					if tempvar >= len(tempstring1):
						tempvar = len(tempstring1)
					tempstring1 = tempstring1[:tempvar]
					tempstring = '_'.join(tempstring1)

				# print(tempstring)
				# exit()

				postmod = os.path.join(folder, tempstring)
				# print(postmod)
				if postmod != premod:
					cmd = 'mv -n "' + premod + '" "' + postmod + '"'
					print(premod + ' --> ' + postmod)
					# print('\n' + cmd + '\n')
					if dryrun == False:
						os.system(cmd)
						count += 1
						if exitvar == 1:
							exit()
	count -= 1
	# print(count)
	iteration += 1
	if iteration > 50:
		count = 0

# print('Task completed.')
