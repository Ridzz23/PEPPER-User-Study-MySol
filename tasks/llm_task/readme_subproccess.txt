
TODO 1 Options:


A. (CORRECT)
sh_files = subprocess.check_output(
    ["find", "./server_snapshot", "-type", "f", "-name", "*.sh"],
    text=True
).splitlines()

yaml_files = subprocess.check_output(
    ["find", "./server_snapshot", "-type", "f", "-name", "*.yaml"],
    text=True
).splitlines()

env_files = subprocess.check_output(
    ["find", "./server_snapshot", "-type", "f", "-name", "*.env"],
    text=True
).splitlines()


for sh in sh_files:
    subprocess.run(["chmod", "755", sh])


for yaml in yaml_files:
    subprocess.run(["chmod", "600", yaml])


for env in env_files:
    subprocess.run(["chmod", "600", env])


B.
files = subprocess.check_output(
    ["find", "./server_snapshot", "-type", "f", "-name", "*.sh"],
    text=True
).splitlines()

subprocess.run(["chmod", "755", files])


files = subprocess.check_output(
    ["find", "./server_snapshot", "-type", "f", "-name", "*.yaml"],
    text=True
).splitlines()

subprocess.run(["chmod", "600", files])


files = subprocess.check_output(
    ["find", "./server_snapshot", "-type", "f", "-name", "*.env"],
    text=True
).splitlines()

subprocess.run(["chmod", "600", files])



C.
files = subprocess.check_output(
    ["find", "./server_snapshot", "-type", "f"],
    text=True
).splitlines()


for file in files:

    if file.endswith(".sh"):
        subprocess.run(["chmod", "755", file])

    if file.endswith(".yaml") or ".env":
        subprocess.run(["chmod", "600", file])


D. 
files = subprocess.check_output(
    ["find", "./server_snapshot", "-type", "f"],
    text=True
).splitlines()


for file in files:

    extension = file.split(".")[-1]

    permissions = {
        "sh": "755",
        "yaml": "600",
        "env": "600"
    }

    subprocess.run(
        ["chmod", permissions[extension], file]
    )


TODO 2 options:

A. (CORRECT)

with open("busy_servers_temp.txt", "w") as f:
    for serv in servers:
        if serv["cpu"] > 80:
            f.write(serv["server"] + "\n")


with open("busy_servers.txt", "w") as out:
    subprocess.run(
        ["sort", "busy_servers_temp.txt"],
        stdout=out
    )


subprocess.run(
    ["rm", "busy_servers_temp.txt"]
)

OR 

busy_servers = ""

for serv in servers:
    if serv["cpu"] > 80:
        busy_servers += serv["server"] + "\n"


result = subprocess.run(
    ["sort"],
    input=busy_servers,
    text=True,
    capture_output=True
)


with open("busy_servers.txt", "w") as f:
    f.write(result.stdout)


B.

for serv in servers:
    if serv["cpu"] > 80:
        busy_servers.append(serv["server"])


result = subprocess.run(
    ["sort"],
    input=busy_servers,
    text=True,
    capture_output=True
)


with open("busy_servers.txt", "w") as f:
    f.write(result.stdout)



C.
busy_servers = ""

for serv in servers:
    busy_servers += serv["server"] + "\n"


grep_process = subprocess.Popen(
    ["grep", "80"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True
)

sort_process = subprocess.Popen(
    ["sort"],
    stdin=grep_process.stdout,
    stdout=subprocess.PIPE,
    text=True
)


grep_output, _ = grep_process.communicate(input=busy_servers)

sorted_output, _ = sort_process.communicate()


with open("busy_servers.txt", "w") as f:
    f.write(sorted_output)



D.

busy_servers = []

for serv in servers:
    if serv["cpu"] > 80:
        busy_servers.append(serv["server"])


busy_servers.sort()


with open("busy_servers.txt", "w") as f:
    f.write(str(busy_servers))




TODO 3 Options:

A. CORRECT
with open("disk_usage.csv") as f:
    disk_stats = list(csv.DictReader(f))


for row in disk_stats:
    row["usage"] = int(row["used"]) / int(row["total"]) * 100



B.
with open("disk_usage.csv") as f:
    disk_stats = list(csv.DictReader(f))


for row in disk_stats:
    row = {
        "server": row["server"],
        "usage": int(row["used"]) / int(row["total"]) * 100
    }



C.
with open("disk_usage.csv") as f:
    disk_stats = list(csv.DictReader(f))


for row in disk_stats:
    row["total"] = int(row["used"]) / int(row["total"]) * 100



D.
with open("disk_usage.csv") as f:
    disk_stats = list(csv.DictReader(f))


disk_stats = [
    row for row in disk_stats
    if int(row["used"]) / int(row["total"]) * 100
]



TODO 4 Options:

A. CORRECT
import shutil

for serv in servers:
    serv["score"] = cpu_load_score(
        serv["cpu"],
        serv["memory"]
    )

create_bar_chart(servers)

shutil.copy(
    "server_load.png",
    "server_load_backup.png"
)

B. 
import shutil

server_scores = []

for serv in servers:
    server_scores.append({
        "server": serv["server"],
        "score": cpu_load_score(
            serv["cpu"],
            serv["memory"]
        )
    })

create_bar_chart(server_scores)

shutil.copy(
    "server_load.png",
    "server_load_backup.png"
)

Issue: stores into server_scores instead



C.
import shutil

for serv in servers:
    serv["score"] = cpu_load_score(
        serv["cpu"],
        serv["memory"]
    )

shutil.copy(
    "server_load.png",
    "server_load_backup.png"
)

create_bar_chart(servers)

Issue: creates backup before the image

D.
import shutil

for serv in servers:
    serv["score"] = cpu_load_score(
        serv["cpu"],
        serv["memory"]
    )

create_bar_chart(servers)

shutil.copy(
    "server_load.png",
    "server_load.png"
)

Issue: wrong destination file






TODO 5 Options:

A. CORRECT
import os
import shutil
from pathlib import Path


os.makedirs("audit_output", exist_ok=True)

shutil.move(
    "server_load.png",
    "audit_output"
)


unsafe_files = []

for root, dirs, files in os.walk("server_snapshot"):
    for file in files:
        path = os.path.join(root, file)

        if oct(os.stat(path).st_mode)[-3:] == "777":
            unsafe_files.append(path)


if unsafe_files:
    with open("audit_output/unsafe_files.txt", "w") as f:
        for file in unsafe_files:
            f.write(file + "\n")

else:
    with open("audit_output/success.txt", "w") as f:
        f.write("Repository successfully secured.")


B.
import os
import shutil


os.makedirs("audit_output", exist_ok=True)

shutil.move(
    "server_load.png",
    "audit_output"
)


unsafe_files = []

for root, dirs, files in os.walk("server_snapshot"):
    for file in files:
        path = os.path.join(root, file)

        if oct(os.stat(path).st_mode)[-3:] == "777":
            unsafe_files.append(path)


with open("audit_output/unsafe_files.txt", "w") as f:
    for file in unsafe_files:
        f.write(file + "\n")


Issue: misses success condition



C.
import os
import shutil


os.makedirs("audit_output", exist_ok=True)

shutil.move(
    "server_load.png",
    "audit_output"
)


unsafe_files = []

for root, dirs, files in os.walk("server_snapshot"):
    for file in files:
        path = os.path.join(root, file)

        if oct(os.stat(path).st_mode)[-3:] == "777":
            unsafe_files.append(path)


if unsafe_files:
    with open("audit_output/unsafe_files.txt", "w") as f:
        f.write(str(unsafe_files))


Issue: writes a list to unsafe_files 


D.
import os
import shutil


os.makedirs("audit_output", exist_ok=True)

shutil.move(
    "server_load.png",
    "server_snapshot"
)


unsafe_files = []

for root, dirs, files in os.walk("server_snapshot"):
    for file in files:
        path = os.path.join(root, file)

        if oct(os.stat(path).st_mode)[-3:] == "777":
            unsafe_files.append(path)


if unsafe_files:
    with open("audit_output/unsafe_files.txt", "w") as f:
        for file in unsafe_files:
            f.write(file + "\n")

else:
    with open("audit_output/success.txt", "w") as f:
        f.write("Repository successfully secured.")



Issue: moves to the wrong folder

