#!/usr/bin/env python3.8
import statistics
import re
import subprocess
import sys

PERF_INVOKATIONS = 50
PERF_REPETITION = 50

PERF_MATCH = br" +(\d+.\d+) seconds time elapsed"


def run(command):
    perf_output = subprocess.check_output([
            "perf", "stat", "-r", str(PERF_INVOKATIONS),
            sys.executable, "-c", command,
        ],
        stderr=subprocess.STDOUT,
    )
    last_line = list(filter(None, perf_output.splitlines()))[-1]
    return float(re.match(PERF_MATCH, last_line).group(1))


def main():
    python = "./python"
    #print(f"Getting {PERF_INVOKATIONS} samples")
    values = []
    for i in range(PERF_INVOKATIONS):
        value = run("pass")
        value_str = int(value * 1_000_000)
        #print(f"{i:02d}", " - ", f"{value_str}us")
        values.append(value)
    mean = statistics.geometric_mean(values)
    #print(f"geometric mean {int(mean * 1_000_000)}us")
    print(int(mean * 1_000_000)) # us


if __name__ == '__main__':
    main()
