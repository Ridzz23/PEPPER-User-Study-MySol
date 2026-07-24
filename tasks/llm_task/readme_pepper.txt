

TODO 1 Options:
- provide chmod, find documentation to them here. 
- and remind them find returns a list on pepper ? 

A. (CORRECT)

sh_files = find "./server_snapshot" -type "f" -name "*.sh"
yaml_files = find "./server_snapshot" -type "f" -name "*.yaml"
env_files = find "./server_snapshot" -type "f" -name "*.env"

for sh in sh_files:
    chmod "755" sh

for yaml in yaml_files:
    chmod "600" yaml

for env in env_files:
    chmod "600" env



B. (WRONG) - tough one

files = find "./server_snapshot" -type "f" -name "*.sh"

chmod "755" files

files = find "./server_snapshot" -type "f" -name "*.yaml"

chmod "600" files

files = find "./server_snapshot" -type "f" -name "*.env"

chmod "600" files

Issue: chmod cant accept a set of file names, can only take one at a time. also files is a list


C. 
files = find "./server_snapshot" -type "f"

for file in files:

    if file.endswith(".sh"):
        chmod "755" file

    if file.endswith(".yaml") or ".env":
        chmod "600" file


ISSUE: ".env" is always true


D. 
files = find "./server_snapshot" -type "f"

for file in files:

    extension = file.split(".")[-1]

    permissions = {
        "sh": "755",
        "yaml": "600",
        "env": "600"
    }

    chmod permissions[extension] file

ISSUE: If there is any file without one of these extensions, then this throws a key error. 





dont think we should include: 
E. (WRONG) - tough one; only people who know shell can say this is wrong

find "./server_snapshot" -type "f" -name "*.sh" $| chmod "755"

find "./server_snapshot" -type "f" -name "*.yaml" $| chmod "600"

find "./server_snapshot" -type "f" -name "*.env" $| chmod "600"

Correct version:

find "./server_snapshot" -type "f" -name "*.sh" $| xargs "chmod" "755"

find "./server_snapshot" -type "f" -name "*.yaml" $| xargs "chmod" "600"

find "./server_snapshot" -type "f" -name "*.env" $| xargs "chmod" "600"


TODO 2 Options:

A. (CORRECT)
for serv in servers:
    if serv["cpu"] > 80:
        server_name = serv["server"]
        echo server_name $>> "busy_servers_temp.txt"

cat "busy_servers_temp.txt" $| sort $> "busy_servers.txt"

rm "busy_servers_temp.txt"

OR

busy_servers = ""

for serv in servers:
    if serv["cpu"] > 80:
        busy_servers += serv["server"] + "\n"

busy_servers $| sort $> "busy_servers.txt"


B.
busy_servers = []

for serv in servers:
    if serv["cpu"] > 80:
        busy_servers.append(serv["server"])

busy_servers $| sort $> "busy_servers.txt"

Issue: sort cant sort the list. User shud be able to understand the flow of types at python to shell boundary


C.
busy_servers = ""

for serv in servers:
    busy_servers += serv["server"] + "\n"


busy_servers $| grep "80" $| sort $> "busy_servers.txt"

Issue: filtering too late once data has been lost.

D.
busy_servers = []

for serv in servers:
    if serv["cpu"] > 80:
        busy_servers.append(serv["server"])

busy_servers.sort()

busy_servers $> "busy_servers.txt"

Issue: once again should realise the type issue when data is flowing from python to shell.
Here a list like ["db1", "web1"] would convert to a string like ['db1', 'web1'].


TODO 3:
remind them of the type csv returns with an example

A. CORRECT
disk_stats = cat "disk_usage.csv"

for row in disk_stats:
    row['usage'] = int(row['used']) / int(row['total']) * 100

B.
disk_stats = cat "disk_usage.csv"


for row in disk_stats:
    row = {
        "server": row["server"],
        "usage": int(row["used"]) / int(row["total"]) * 100
    }

Issue: overwrites existing fields in a row

C.
disk_stats = cat "disk_usage.csv"

for row in disk_stats:
    row["total"] = int(row["used"]) / int(row["total"]) * 100

Issue: modifies the wrong field

D.
disk_stats = cat "disk_usage.csv"

disk_stats = [
    row for row in disk_stats
    if int(row["used"]) / int(row["total"]) * 100
]

Issue: code computes usage but never stores it


TODO 4 Options:

A. CORRECT
for serv in servers:
    serv["score"] = cpu_load_score(
        serv["cpu"],
        serv["memory"]
    )

create_bar_chart(servers)

cp "./server_load.png" "./server_load_backup.png"

B.
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

cp "./server_load.png" "./server_load_backup.png"

Issue: stores results into a new list, instead of updating the original one

C.
for serv in servers:
    serv["score"] = cpu_load_score(
        serv["cpu"],
        serv["memory"]
    )

cp "./server_load.png" "./server_load_backup.png"

create_bar_chart(servers)

Issue: creates backup before the image

D.
for serv in servers:
    serv["score"] = cpu_load_score(
        serv["cpu"],
        serv["memory"]
    )

create_bar_chart(servers)

cp "./server_load.png" "./server_load.png"

Issue: wrong desitnation file



TODO 5 Options:
- remind users that find returns a python list

A. CORRECT
mkdir "./audit_output"

mv "./server_load.png" "./audit_output"

unsafe_files = find "./server_snapshot" -type "f" -perm "777"

if unsafe_files:
    for file in unsafe_files:
        echo file $> "audit_output/unsafe_files.txt"

else:
    echo "Repository successfully secured." $> "audit_output/success.txt"




B.
mkdir "./audit_output"

mv "./server_load.png" "./audit_output"

unsafe_files = find "./server_snapshot" -type "f" -perm "777"

unsafe_files $> "audit_output/unsafe_files.txt"



Issue: misses the success condition



C.
mkdir "./audit_output"

mv "./server_load.png" "./audit_output"

unsafe_files = find "./server_snapshot" -type "f" -perm "777"

if unsafe_files:
    echo unsafe_files $> "audit_output/unsafe_files.txt"

else:
    echo "Repository successfully secured." $> "audit_output/success.txt"




Issue: find returns a python list



D.
mkdir "./audit_output"

mv "./server_load.png" "./server_snapshot"

unsafe_files = find "./server_snapshot" -type "f" -perm "777"

if unsafe_files:
    for file in unsafe_files:
        echo file $> "audit_output/unsafe_files.txt"

else:
    echo "Repository successfully secured." $> "audit_output/success.txt"



Issue: moves the png to the wrong folder