# to run: pyExt <file_name>

import os


CONFIG_EXTENSIONS = {
    ".yaml",
    ".env"
}

SCRIPT_EXTENSIONS = {
    ".sh"
}



def get_permissions(path):
    return oct(os.stat(path).st_mode & 0o777)



#------------------------------ START CODING FROM HERE; DO NOT CHANGE THE CODE ABOVE THIS LINE ------------------------------


# TODO 1:
# Find every file inside the project directory that currently has
# permissions 777.
#
# Store their filenames in a Python list called corrupted_files.
#
# (FS -> DATA)


corrupted_files = []



# TODO 2:
# Iterate through files and restore permissions for every corrupted file:
#
# .sh files      -> 755
# .yaml/.env     -> 600
# everything else -> 644
#
# (DATA + FS)



# TODO 3:
# Remove all temporary files from the project directory.
#
# Delete:
#   - files ending in ".cache"
#   - the entire "logs/" directory
#
# (FS)



# TODO 4:
# Create a directory called "bin".
#
# Find all shell scripts (.sh) inside the project directory
# and move them into the bin directory.
#
# (FS)



# TODO 5:
# Verify that no files still have permissions 777.
# if there are then write the file name to a file called unsafe_file.txt
#
# (FS -> DATA)

