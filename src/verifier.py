"""Verifier for stable matching solutions. Checks for validity and stability."""

import sys
import os

def parse_input(filename):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    n = int(lines[0])
    if n == 0:
        return 0, [], []

    hospital_prefs = [[int(x) - 1 for x in lines[i].split()] for i in range(1, n + 1)]
    student_prefs = [[int(x) - 1 for x in lines[i].split()] for i in range(n + 1, 2 * n + 1)]

    return n, hospital_prefs, student_prefs


def parse_matching(filename, n):
    hospital_to_student = {}
    student_to_hospital = {}

    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    for line in lines:
        parts = line.split()
        if len(parts) != 2:
            continue
        h = int(parts[0]) - 1
        s = int(parts[1]) - 1
        hospital_to_student[h] = s
        student_to_hospital[s] = h

    return hospital_to_student, student_to_hospital


def check_validity(n, hospital_to_student, student_to_hospital):
    errors = []

    if len(hospital_to_student) != n:
        errors.append(f"Validity Check: INVALID Expected {n} hospitals to be matched instead found {len(hospital_to_student)}")

    if len(student_to_hospital) != n:
        errors.append(f"Validity Check: INVALID Expected {n} students to be matched instead found {len(student_to_hospital)}")

    for h in range(n):
        if h not in hospital_to_student:
            errors.append(f"Validity Check: INVALID Hospital {h + 1} is not matched to any student")
    for s in range(n):
        if s not in student_to_hospital:
            errors.append(f"Validity Check: INVALID Student {s + 1} is not matched to any hospital")

    matched_students = list(hospital_to_student.values())
    if len(matched_students) != len(set(matched_students)):
        errors.append("Validity Check: INVALID students are matched to multiple hospitals")

    matched_hospitals = list(student_to_hospital.values())
    if len(matched_hospitals) != len(set(matched_hospitals)):
        errors.append("Validity Check: INVALID hospitals are matched to multiple students")
    for h, s in hospital_to_student.items():
        if h < 0 or h >= n:
            errors.append(f"Validity Check: INVALID Hospital ID {h + 1} is out of range")
        if s < 0 or s >= n:
            errors.append(f"Validity Check: INVALID Student ID {s + 1} is out of range")

    for h, s in hospital_to_student.items():
        if s in student_to_hospital and student_to_hospital[s] != h:
            errors.append(f"Validity Check: INVALID Inconsistent matching Hospital {h + 1} matched to Student {s + 1}, but Student {s + 1} matched to Hospital {student_to_hospital[s] + 1}")

    return len(errors) == 0, errors


def check_stability(n, hospital_prefs, student_prefs, hospital_to_student, student_to_hospital):
    hospital_rank = [[0] * n for _ in range(n)]
    for h in range(n):
        for rank, s in enumerate(hospital_prefs[h]):
            hospital_rank[h][s] = rank

    student_rank = [[0] * n for _ in range(n)]
    for s in range(n):
        for rank, h in enumerate(student_prefs[s]):
            student_rank[s][h] = rank

    blocking_pairs = []

    for h in range(n):
        for s in range(n):
            if hospital_to_student.get(h) == s:
                continue

            current_student = hospital_to_student.get(h)
            current_hospital = student_to_hospital.get(s)

            if current_student is None or current_hospital is None:
                continue

            hospital_prefers = hospital_rank[h][s] < hospital_rank[h][current_student]

            student_prefers = student_rank[s][h] < student_rank[s][current_hospital]

            if hospital_prefers and student_prefers:
                blocking_pairs.append((h + 1, s + 1))

    return len(blocking_pairs) == 0, blocking_pairs


def verify_matching(preferences_file, matching_file):
    n, hospital_prefs, student_prefs = parse_input(preferences_file)
    
    if n == 0:
        return True, True, ["Valid and stable matching for n = 0"]

    hospital_to_student, student_to_hospital = parse_matching(matching_file, n)

    messages = []

    is_valid, validity_errors = check_validity(n, hospital_to_student, student_to_hospital)
    
    if not is_valid:
        messages.extend(validity_errors)
        return False, False, messages
    
    messages.append("Validity Check: VALID")

    is_stable, blocking_pairs = check_stability(n, hospital_prefs, student_prefs, 
                                                  hospital_to_student, student_to_hospital)
    
    if not is_stable:
        messages.append("Stability Check: UNSTABLE")
        messages.append(f"Found blocking pairs:")
        for h, s in blocking_pairs:
            messages.append(f"  Hospital {h} and Student {s} are a blocking pair")
        return True, False, messages
    
    messages.append("Stability Check: STABLE")
    
    return True, True, messages


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "..", "data")

    preferences_file = sys.argv[1]
    matching_file = sys.argv[2]

    if not os.path.exists(preferences_file):
        potential_path = os.path.join(data_dir, preferences_file)
        if os.path.exists(potential_path):
            preferences_file = potential_path

    if not os.path.exists(matching_file):
        potential_path = os.path.join(data_dir, matching_file)
        if os.path.exists(potential_path):
            matching_file = potential_path

    try:
        is_valid, is_stable, messages = verify_matching(preferences_file, matching_file)
        
        print("\nSTABLE MATCHING CHECK (Validity and Stability):\n")
        print(f"Preferences file: {preferences_file}")
        print(f"Matching file: {matching_file}\n")
        
        for msg in messages:
            print(msg)
        
        if is_valid and is_stable:
            print("Therefore matching is VALID and STABLE\n")
            sys.exit(0)
        elif is_valid:
            print("Therefore matching is VALID but UNSTABLE\n")
            sys.exit(1)
        else:
            print("Therefore matching is INVALID\n")
            sys.exit(1)

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
