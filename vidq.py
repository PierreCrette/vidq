#!/usr/bin/env python3

import sys
import os
import subprocess
import fnmatch
import shutil
from os.path import join, getsize
import hashlib
import sqlite3
#import psycopg2
from pprint import pprint

#Declarations
debug = 0
level = 0
findimagedupes = 0
foldervideo= '.'

#Generate jpg images files for one source video file
def OneFile(folderv,file,level):
	#Initialization
	fvideo = folderv + file
	if debug>3: print ('OneFile(' + folderv +', ' + ', ' + file + ')')
	
	s = ''
	for i in range(level): s = s + '  '
	s = s + "mediainfo '" + fvideo + "'"

	#Call mediainfo
	print (s)
	p=subprocess.Popen(s, stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()  
	#print (output)
	p_status = p.wait()

	height = ''
	width = ''
	duration = ''
	bitrate = ''
	s = output.decode(encoding="utf-8", errors="strict")
	#print (str(len(s)))

	for i in range(len(s)):
		if s[i:i+6] == 'Height':
			j = i+7
			while s[j] != ':': j = j+1
			k = j+2
			while s[k] != 'p': k = k+1
			height = s[j+2:k]
			if debug>1: print('height = ' + height)
		if s[i:i+5] == 'Width':
			j = i+6
			while s[j] != ':': j = j+1
			k = j+2
			while s[k] != 'p': k = k+1
			width = s[j+2:k]
			if debug>1: print('width = ' + width)
	for i in range(len(s)):
		if s[i:i+8] == 'Duration':
			j = i+9
			while s[j] != ':': j = j+1
			k = j+2
			while s[k] != '\n': k = k+1
			duration = s[j+2:k]
			if debug>1: print('duration = ' + duration)
	for i in range(len(s)):
		if s[i:i+16] == 'Overall bit rate':
			j = i+17
			while s[j] != ':': j = j+1
			k = j+2
			while s[k] != '\n': k = k+1
			bitrate = s[j+2:k]
			if debug>1: print('bitrate = ' + bitrate)
							
	ftarget.write(fvideo + ';' + height + ';' + width + ';' + duration + ';' + bitrate + '\n')



# Parse a single folder to call OneFile for source video files and BoucleFichier recursively if it'a a subfolder
def BoucleFichiers(folderv='.',level=1):
	level = level + 1
	spacer = ''
	if debug>0: 
		for i in range(level): spacer=spacer+'  '
		print(spacer + '[ ' + folderv)
	if os.path.isdir(folderv):
		if folderv[-1] != "/": folderv = folderv + "/"
		for file in os.listdir(folderv):
			ext = os.path.splitext(file)[1]
			if os.path.isdir(folderv+file):
				BoucleFichiers(folderv+file,level)
			elif (ext.upper() == '.MP4') or (ext.upper() == '.AVI') or (ext.upper() == '.MOV') or (ext.upper() == '.M4V') \
				or (ext.upper() == '.VOB') or (ext.upper() == '.MPG') or (ext.upper() == '.MPEG') or (ext.upper() == '.MKV') \
				or (ext.upper() == '.WMV') or (ext.upper() == '.ASF') or (ext.upper() == '.FLV') \
				or (ext.upper() == '.RM') or (ext.upper() == '.OGM') or (ext.upper() == '.M2TS') or (ext.upper() == '.RMVB'):
				OneFile(folderv, file, level)
			elif not(ext.upper() == '.JPG' or ext.upper() == '.TXT'):
				print (spacer + '  Not match : ' + folderv + file)
	if debug>0: 
		spacer = ''
		for i in range(level): spacer=spacer+'  '
		print (spacer + folderv +  ' ]')
	level = level - 1

#main
#Step0: Read arguments and initialize variables
if debug>3: print(sys.argv)
if len(sys.argv)<2:
	print('SYNTAX ERROR: vidq foldervideo targetcsv')
	halt
else:
	foldervideo = os.path.normpath(sys.argv[1])
	if foldervideo[-1] != "/": foldervideo = foldervideo + "/"
	target = os.path.normpath(sys.argv[2])
	ftarget = open(target,'w')
	ftarget.write('filename;height;width;duration;bitrate\n')

	print('************************************************************************************')
	print('* vidq.py ' + foldervideo + ' ' + target)
	print('Vidq : video quality based on size and bitrate.')
	print('Beware: video quality is a complex subject and the simple approach used in this program is not accurate.')
	print('eg. a Mpeg2 encoded file may wrongly appears better than a .mp4.')
	print('Copyright (C) 2018  Pierre Crette')
	print('')
	print('This program is free software: you can redistribute it and/or modify')
	print('it under the terms of the GNU General Public License as published by')
	print('the Free Software Foundation, either version 3 of the License, or')
	print('(at your option) any later version.')
	print('')
	print('This program is distributed in the hope that it will be useful,')
	print('but WITHOUT ANY WARRANTY; without even the implied warranty of')
	print('MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the')
	print('GNU General Public License for more details.')
	print('')
	print('You should have received a copy of the GNU General Public License')
	print('along with this program.  If not, see <http://www.gnu.org/licenses/>.')
	print('')

	if debug>1: print ('foldervideo : ', foldervideo)
	
	BoucleFichiers(foldervideo, level)

	ftarget.close
	
print('************************************************************************************')
print('* vidq ' + foldervideo + ' ' + target + ' DONE')
print('************************************************************************************')

