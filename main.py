# We import all the necessary libraries
import os
import glob
import pandas as pd
import platform


# This method will add a column to the emg files with the names of the subjects that were used.
def add_test_subject_column():
	# We get the extension to the csv
	extension = 'csv'
	# We get all the file names into a list
	all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

	# Now we loop through all the files and append the
	for filename in all_filenames:
		print('Filename ='+filename)

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
		all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
		# combine all files in the list
		combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
		# export to csv
		combined_csv.to_csv("combined_csv.csv", index=False, encoding='utf-8-sig')

		# If we get here then the files were combined correctly.
		print('Files were combined successfully')
	except:
		# If we get here then there was an error when combining the files
		print('There was an error while combining the files')


# We execute the main function
if __name__ == '__main__':
	# We will start by combining the training data from the emg recordings into a single csv file.
	# combine_emg_files()
	c_dir = os.getcwd()
	# We add the new directory
	# But first we determine the separator based on our OS
	sep = get_os_directory_separator()
	n_dir = c_dir + '' + sep + 'bbdc_2020' + sep + 'test_combine'
	# Now we proceed to change the directory
	os.chdir(n_dir)

	# We add the filename as a column
	add_test_subject_column()


	# Once we change the directory we will proceed to combine the csv files into one single file for easier
	# handling.
	combine_emg_files()
	# We finish the executionm of the program
	print("Finished execution!")
