import os
import gzip
import glob

def gunzip(fin, fout):
	""" Gunzip a file. """
	with gzip.open(fin, 'rb') as fgz:
		with open(fout, 'wb') as f:
			for line in fgz:
				f.write(line)
		f.close()
	fgz.close()

def removeGz():
	""" Remove all .gz files in the current directory. """
	for file in glob.iglob(fr'{directory}*.gz'):
		os.remove(file)

def gunzipDir():
	"""  
	Reads current directory for files ending in .gz to make a list of files.
	Writes unzipped contents to file with same name without .gz extension.
	"""
	for filepath in glob.iglob(fr'{directory}*.gz'):
		new_name = os.path.splitext(filepath)[0]
		print(f"Unzipping {new_name}...")
		gunzip(filepath, new_name)

def grepOut(pattern, output_file):
	""" 
	Reads current directory for files ending in .log to make a list of input_files.
	Opens input files for reading and creates an output file for writing.
	For each line in input_files, a matching pattern will write that line to the output file.
	"""
	# try:


	for input_file in glob.iglob(fr'{directory}*.log'):
		print(f"Processing {input_file} for {pattern} in {directory}...")
		with open(input_file, 'r', encoding="utf-8") as fin:
			with open(output_file, 'a', encoding="utf-8") as fout:
				for line in fin:
					if pattern in line:
						fout.write(f"\n{line.strip()}")

	# except UnicodeDecodeError:
	# 	pass

def removeLog():
	""" Remove all .log files in the current directory. """
	for file in glob.iglob(r'*.log'):
		os.remove(file)

directory = input("""
This script is intended for handling the decompression and analysis of USM Anywhere archived log data.

Once the compressed log folder has been downloaded and unzipped, this script will gunzip each individual
log file within that specified directory, remove the .gz files, analyze the logs for a specific pattern
and output the matching logs to the specified output file. Once complete, if uncommented , it will 
remove the .log files leaving only the extracted, matching log files.

### Please ensure you have sufficient storage for all of the unzipped log files!! ###

What directory would you like to run within? (Include the ending '\\')
Hit enter to run in the current directory.	""")

pattern = input("""
What is the pattern you would like to analyze the logs for?
If you'd like to analyze for more than one pattern, please modify the script directly. """)

""" Gunzip all .log.gz files to standard log files then delete the .gz files. """
gunzipDir()
removeGz()

""" Define the pattern to match and the full path and name of the output file. """
#grepOut('PATTERN', f'{directory}PATTERN.txt')
#grepOut('PATTERN', f'{directory}PATTERN.txt')
#grepOut('PATTERN', f'{directory}PATTERN.txt')
grepOut(f'{pattern}', f'{directory}{pattern}.txt')

""" Delete remaining log files. """
#removeLog()
