import re
import subprocess

LATENCY_PATTERN = re.compile(r"latency_ms=([0-9.]+)")

def avg_latency_calc(latency_list):
    return sum(latency_list) / len(latency_list)

def extract_log_files():
    # equivalent of: find experiment_results -name "experiment.log"
    result = subprocess.run(
        ["find", "experiment_results", "-name", "experiment.log"],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip().splitlines()


def read_file(path):
    # equivalent of: cat file
    result = subprocess.run(
        ["cat", path],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout


log_files = extract_log_files()
print(log_files)


for log_file in log_files:
    log_content = read_file(log_file)

    warn_flag = False
    latencies = []

    if "[WARN]" in log_content:
        warn_flag = True

    print(log_content)
    print(warn_flag)

    for line in log_content.splitlines():
        match = LATENCY_PATTERN.search(line)
        if match:
            latencies.append(float(match.group(1)))

    avg_latency = avg_latency_calc(latencies)
    print(avg_latency)

    if latencies and avg_latency < 10 and not warn_flag:
        print("stable")
        # write to file (example)
    else:
        print("unstable")