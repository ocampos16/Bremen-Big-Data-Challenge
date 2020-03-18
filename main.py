# We import all the necessary libraries
import os
from os import path
import glob
import pandas as pd
import platform
# Imports for managing file
from csv import writer
from csv import reader
# We import our file
from PreProcessing import PreProcessing

# We add a column to a csv file
def add_column_in_csv(input_file, output_file, transform_row):
	""" Append a column in existing csv using csv.reader / csv.writer classes"""
	# Open the input_file in read mode and output_file in write mode
	with open(input_file, 'r') as read_obj, \
			open(output_file, 'w', newline='') as write_obj:
		# Create a csv.reader object from the input file object
		csv_reader = reader(read_obj)
		# Create a csv.writer object from the output file object
		csv_writer = writer(write_obj)
		# Read each row of the input csv file as list
		for row in csv_reader:
			# Pass the list / row in the transform function to add column text for this row
			transform_row(row, csv_reader.line_num)

			# Write the updated row / list to the output file
			csv_writer.writerow(row)


# This method will add a column to the emg file with the names of the subjects that were used.
def add_test_subject_column():
	# We get the extension to the csv
	extension = 'csv'
	# We get all the file names into a list
	all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

	# Now we loop through all the file and append the
	for filename in all_filenames:
		print('Filename ='+filename)

		# We specify the output folder where the merge data will go
		output_file = 'output_'+filename
		# We add the header of the new column
		header_of_new_col = 'src_file'
		# We split the filename on '.' in order to only add the name of the file
		default_text = filename.split('.')[0]

		# Add the column in csv file with header
		add_column_in_csv(filename, output_file, lambda row, line_num: row.insert(0,header_of_new_col) if line_num == 1 else row.insert(0, default_text))

		# Add a column to a csv file; source: https://thispointer.com/python-add-a-column-to-an-existing-csv-file/
		# add_column_in_csv(filename, output_file, lambda row, line_num: row.insert(0, split_filename[0]))

		print('Column '+header_of_new_col+' with all rows successfully added to '+filename+"!")


# the switcher method returns the separator based on the OS.
def switcher(argument):
    switch = {
        "Windows": "\\",
        "Linux": "/",
        "Mac": "/",
    }  # End switch

    return switch.get(argument, "nothing")


# We get the directory separator based on the OS platform that user is in.
def get_os_directory_separator():
	# We get the system name from the platform that we are using
	plt = platform.system()
	return switcher(plt)


# First we will combine all the training data from the emg recordings into a single csv file.
def combine_emg_files():
	# We surround the operation in a try/catch block to keep track of the possible errors that might come out.
	try:
		# https://www.freecodecamp.org/news/how-to-combine-multiple-csv-files-with-8-lines-of-code-265183e0854/
		extension = 'csv'
		# all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
		# We get all the file_names with the prefix output
		all_filenames = [i for i in glob.glob('output_*.{}'.format(extension))]
		# combine all file in the list
		combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
		# export to csv
		combined_csv.to_csv("combined_csv.csv", index=False, encoding='utf-8-sig')

		# If we get here then the file were combined correctly.
		print('Files were combined successfully')
	except:
		# If we get here then there was an error when combining the file
		print('There was an error while combining the file')


# We execute the main function
if __name__ == '__main__':

	# We will start by locating the data
	# And then combining the training data from the emg recordings into a single csv file.
	c_dir = os.getcwd()
	# We add the new directory
	# But first we determine the separator based on our OS
	sep = get_os_directory_separator()

	# We set the two working directories for the data
	emg_dir = c_dir + '' + sep + 'bbdc_2020' + sep + 'train' + sep + 'emg'
	mocap_dir = c_dir + '' + sep + 'bbdc_2020' + sep + 'train' + sep + 'mocap'

	# Combined file string
	end_combined_file = sep + 'combined_csv.csv'

	# We create a list of the combined_csv file
	combined_files_list = {emg_dir+end_combined_file, mocap_dir+end_combined_file}

	# We will iterate through the combined_files_list and check if 'combined_csv' exists on both folders.
	print("Checking combined files...")
	for file in combined_files_list:
		# We will first check if there's no 'combined_csv' file in 'bbdc_2020\train\emg'
		if not path.exists(file):
			# If the file doesn't exist then we will create it.
			# If files don't exist we create them
			print("File: "+file+" doesn't exist.")
			print("Creating "+file+"...")
			# We create the file
			# Now we proceed to change the directory
			temp_dir = file.rsplit('\\', 1)[0]
			os.chdir(temp_dir)

			# We add the filename as a column to each file
			add_test_subject_column()

			# Once we change the directory we will proceed to combine the csv file into one single file for easier
			# handling.
			combine_emg_files()

			# If we get here then the file was created successfully
			print("File: " + file + " has been created successfully.")
		else:
			print("File: " + file + " exists!")

	# If we have reached this point then we will proceed to run pre-processing on both files.
	# We will first create an instance of PreProcessing.py
	pre = PreProcessing()
	pre.pre_process_data_frame()

	# We finish the execution of the program
	print("Finished execution!")
