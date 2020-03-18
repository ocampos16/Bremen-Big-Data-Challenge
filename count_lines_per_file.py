# We import all the necessary libraries
import os, platform, glob


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


def file_len(fname):
	with open(fname) as f:
		for i, l in enumerate(f):
			pass
	return i + 1

# We will start by combining the training data from the emg recordings into a single csv file.
# combine_emg_files()
c_dir = os.getcwd()
# We add the new directory
# But first we determine the separator based on our OS
sep = get_os_directory_separator()
n_dir = c_dir + '' + sep + 'bbdc_2020' + sep + 'train' + sep + 'emg'
# n_dir = c_dir + '' + sep + 'bbdc_2020' + sep + 'test_combine'
# Now we proceed to change the directory
os.chdir(n_dir)

# We get the extension to the csv
extension = 'csv'
# Now we count the lines per file
all_filenames = [i for i in glob.glob('combined_csv.{}'.format(extension))]

file_dict = {}
total = 0
for filename in all_filenames:
	count = file_len(filename)
	file_dict[filename] = count
	total += count

num_files = len(all_filenames)
print('Total count: '+str(total - num_files))
print("All the line files have been counted")

# Now we write the dictionary to a csv file
with open('file_stats.csv', 'w') as f:
	for key in file_dict.keys():
		f.write("%s,%s\n" % (key,file_dict[key]))

print("The dictionary has been successfully been written")
