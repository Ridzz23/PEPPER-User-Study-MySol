# to run: pyExt <file_name>

import os
import subprocess


CONFIG_EXTENSIONS = {
    ".yaml",
    ".env"
}

SCRIPT_EXTENSIONS = {
    ".sh"
}


def run_shell(cmd):
    return subprocess.check_output(cmd, shell=True, text=True)



def get_permissions(path):
    return oct(os.stat(path).st_mode & 0o777)



#------------------------------ START CODING FROM HERE; DO NOT CHANGE THE CODE ABOVE THIS LINE ------------------------------


project_dir = "./project"



# TODO 1:
# Find every file inside the project directory that currently has
# permissions 777.
#
# Store their filenames in a Python list called corrupted_files.
#
# (FS -> DATA)


corrupted_files = run_shell(
    f"find {project_dir} -type f -perm 777"
).splitlines()



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
        subprocess.run(
            f"chmod 755 {file}",
            shell=True
        )

    elif file.endswith(".yaml") or file.endswith(".env"):
        subprocess.run(
            f"chmod 600 {file}",
            shell=True
        )

    else:
        subprocess.run(
            f"chmod 644 {file}",
            shell=True
        )



# TODO 3:
# Remove all temporary files from the project directory.
#
# Delete:
#   - files ending in ".cache"
#   - the entire "logs/" directory
#
# (FS)


cache_files = run_shell(
    f"find {project_dir} -type f -name '*.cache'"
).splitlines()

for file in cache_files:
    subprocess.run(
        f"rm {file}",
        shell=True
    )


subprocess.run(
    f"rm -rf {project_dir}/logs",
    shell=True
)



# TODO 4:
# Create a directory called "bin".
#
# Find all shell scripts (.sh) inside the project directory
# and move them into the bin directory.
#
# (FS)


subprocess.run(
    "mkdir -p bin",
    shell=True
)


scripts = run_shell(
    f"find {project_dir} -type f -name '*.sh'"
).splitlines()


for script in scripts:
    subprocess.run(
        f"mv {script} bin/",
        shell=True
    )



# TODO 5:
# Verify that no files still have permissions 777.
# if there are then write the file name to a file called unsafe_file.txt
#
# (FS -> DATA)


remaining_unsafe = run_shell(
    f"find {project_dir} -type f -perm 777"
).splitlines()


if len(remaining_unsafe) > 0:
    with open("unsafe_file.txt", "w") as f:
        for file in remaining_unsafe:
            f.write(file + "\n")