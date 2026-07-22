import re

LATENCY_PATTERN = re.compile(r"latency_ms=([0-9.]+)")

def avg_latency_calc(latency_list):
    return sum(latency_list) / len(latency_list)

def extract_latencies(lines):
    latencies = []

    for line in lines:
        match = LATENCY_PATTERN.search(line)
        if match:
            latencies.append(float(match.group(1)))

    return latencies



log_files = find "experiment_results" -name "experiment.log"
print(log_files)

#mkdir -p analysis/stable_runs

for log_file in log_files.splitlines():
    log_content = cat log_file
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
    if (avg_latency < 10 and (not warn_flag)):
        print("stable")
        #write to file
    else:
        print("unstable")

