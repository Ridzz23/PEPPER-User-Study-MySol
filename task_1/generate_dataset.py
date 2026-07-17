from pathlib import Path
import random
import shutil

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

random.seed(42)

ROOT = Path("experiment_results")

CLUSTERS = ["cluster_A", "cluster_B", "cluster_C"]
NODES_PER_CLUSTER = 4

MIN_METRICS = 15
MAX_METRICS = 20

WARNING_PROB = 0.10
MALFORMED_PROB = 0.05

# Number of experiment.log files that will be intentionally omitted
MISSING_LOGS = 2

# ---------------------------------------------------------------------
# Fresh start
# ---------------------------------------------------------------------

if ROOT.exists():
    shutil.rmtree(ROOT)

ROOT.mkdir(parents=True)

# ---------------------------------------------------------------------
# Randomly choose which logs will be missing
# ---------------------------------------------------------------------

all_nodes = []

for cluster in CLUSTERS:
    for node in range(1, NODES_PER_CLUSTER + 1):
        all_nodes.append((cluster, f"node_{node:02d}"))

missing_logs = set(random.sample(all_nodes, MISSING_LOGS))

# ---------------------------------------------------------------------
# Generate dataset
# ---------------------------------------------------------------------

for cluster in CLUSTERS:

    for node in range(1, NODES_PER_CLUSTER + 1):

        node_name = f"node_{node:02d}"

        log_dir = ROOT / cluster / node_name / "run_logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        if (cluster, node_name) in missing_logs:
            # Directory exists but experiment.log is intentionally absent.
            continue

        log_file = log_dir / "experiment.log"

        with open(log_file, "w") as f:

            run_id = f"{cluster}_{node_name}"

            f.write(f"[INFO] run_id={run_id}\n")
            f.write("[INFO] benchmark=SchedulerBench\n")
            f.write("[INFO] kernel=6.8.0\n")
            f.write("[INFO] starting benchmark\n\n")

            num_metrics = random.randint(MIN_METRICS, MAX_METRICS)

            for _ in range(num_metrics):

                # Occasionally insert a warning
                if random.random() < WARNING_PROB:
                    f.write("[WARN] CPU frequency scaling detected\n")

                latency = round(random.uniform(6.0, 18.0), 2)
                throughput = random.randint(350, 500)
                qps = random.randint(1000, 1500)

                # Occasionally generate malformed data
                if random.random() < MALFORMED_PROB:

                    malformed = random.choice([
                        f"[METRIC] latency_ms=BAD throughput={throughput} qps={qps}",
                        f"[METRIC] throughput={throughput} qps={qps}",
                        "[METRIC]",
                        "THIS IS NOT A VALID LOG ENTRY",
                    ])

                    f.write(malformed + "\n")

                else:

                    f.write(
                        f"[METRIC] latency_ms={latency} "
                        f"throughput={throughput} "
                        f"qps={qps}\n"
                    )

            f.write("\n")
            f.write("[INFO] benchmark complete\n")

print("Dataset generated successfully!\n")

print("Missing experiment.log files:")

for cluster, node in sorted(missing_logs):
    print(f"  {cluster}/{node}")