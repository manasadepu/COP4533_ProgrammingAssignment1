# COP4533 Programming Assignment 1: Stable Matching

## Team Members
- Taebok Joseph Kim
- Manas Adepu

## Overview
Implementation of the Gale-Shapley algorithm for the hospital-student stable matching problem.

## Project Structure
```
src/       - Source code (matcher, verifier)
data/      - Example input/output files (example.in example.out matching is valid and stable)
results/   - Benchmark results and graphs
```

## Requirements
- Python 3.7+

### Running the Matcher
The matcher implements the hospital-proposing Gale-Shapley algorithm.

From the `src/` directory:
```bash
python matcher.py example.in
```

**You do not need to provide the full path for an input file, matcher.py automatically assumes the data directory!**

### Running the Verifier
The verifier checks if a matching is valid and stable.

From the `src/` directory:
```bash
python verifier.py example.in example.out
```

**You do not need to provide the full path for an input/output file, verifier.py automatically assumes the data directory!**
