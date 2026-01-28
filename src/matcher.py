"""Gale-Shapley hospital-proposing stable matching algorithm."""

import sys

def parse_input(filename):
    """Parse input file and return n, hospital_prefs, student_prefs (0-indexed)."""
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    n = int(lines[0])
    if n == 0:
        return 0, [], []

    hospital_prefs = [[int(x) - 1 for x in lines[i].split()] for i in range(1, n + 1)]
    student_prefs = [[int(x) - 1 for x in lines[i].split()] for i in range(n + 1, 2 * n + 1)]

    return n, hospital_prefs, student_prefs


def gale_shapley(n, hospital_prefs, student_prefs):
    """
    Run hospital-proposing Gale-Shapley algorithm.
    Returns: (matching dict, proposal_count)
    """
    if n == 0:
        return {}, 0

    # Build student ranking lookup: student_rank[s][h] = rank of hospital h for student s
    student_rank = [[0] * n for _ in range(n)]
    for s in range(n):
        for rank, h in enumerate(student_prefs[s]):
            student_rank[s][h] = rank

    # Track state
    hospital_next = [0] * n  # Next student to propose to for each hospital
    student_match = [None] * n  # Current match for each student
    unmatched = list(range(n))  # Unmatched hospitals
    proposals = 0

    while unmatched:
        h = unmatched.pop(0)

        if hospital_next[h] >= n:
            continue

        s = hospital_prefs[h][hospital_next[h]]
        hospital_next[h] += 1
        proposals += 1


        if student_match[s] is None:
            student_match[s] = h
        elif student_rank[s][h] < student_rank[s][student_match[s]]:
            unmatched.append(student_match[s])
            student_match[s] = h
        else:
            unmatched.append(h)
        
        print(f"Hospital {h + 1} proposes to Student {s + 1}. Student's current match: {student_match[s] + 1 if student_match[s] is not None else 'None'}")

    # Convert to hospital -> student matching
    matching = {}
    for s, h in enumerate(student_match):
        if h is not None:
            matching[h] = s

    return matching, proposals


def main():
    if len(sys.argv) < 2:
        print("Usage: python matcher.py <input_file>")
        sys.exit(1)

    n, hospital_prefs, student_prefs = parse_input(sys.argv[1])
    matching, proposals = gale_shapley(n, hospital_prefs, student_prefs)

    for h in range(n):
        print(f"{h + 1} {matching[h] + 1}")


if __name__ == "__main__":
    main()
