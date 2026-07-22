# to run: pyExt <file_name>
# You are maintaining a software repository. The repository has incorrect permissions, misplaced files, configuration issues, and temporary artifacts. Build an automated cleanup and security report tool.


CONFIG_EXTENSIONS = {
    ".yaml",
    ".env"
}

SCRIPT_EXTENSIONS = {
    ".sh"
}



def get_extension(filename):
    return filename.split(".")[-1]



#------------------------------ START CODING FROM HERE; DO NOT CHANGE THE CODE ABOVE THIS LINE ------------------------------


project_dir = "./project"



# TODO 1:
# Find every file inside the project directory that currently has
# permissions 777.
#
# Store their filenames in a Python list called corrupted_files.
#
# (FS -> DATA)


corrupted_files = find "project_dir" -type "f" -perm "777"



# TODO 2:
# Iterate through files and restore permissions for every corrupted file:
#
# .sh files      -> 755
# .yaml/.env     -> 600
# everything else -> 644
#
# (DATA + FS)


for file in corrupted_files:

    if file.endswith(".sh"):
        chmod "755" file

    elif file.endswith(".yaml") or file.endswith(".env"):
        chmod "600" file

    else:
        chmod "644" file



# TODO 3:
# Remove all temporary files from the project directory.
#
# Delete:
#   - files ending in ".cache"
#   - the entire "logs/" directory
#
# (FS)


cache_files = find "project_dir" -type "f" -name "*.cache"

for file in cache_files:
    rm file


rm -r "project_dir/logs"



# TODO 4:
# Create a directory called "bin".
#
# Find all shell scripts (.sh) inside the project directory
# and move them into the bin directory.
#
# (FS)


mkdir -p "bin"

scripts = find "project_dir" -type "f" -name "*.sh"

for script in scripts:
    mv script "bin/"



# TODO 5:
# Verify that no files still have permissions 777.
# if there are then write the file name to a file called unsafe_file.txt
#
# (FS -> DATA)


remaining_unsafe_files = find "project_dir" -type "f" -perm "777"


if remaining_unsafe_files:
    remaining_unsafe_files $> "unsafe_file.txt"