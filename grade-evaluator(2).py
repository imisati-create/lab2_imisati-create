import csv
import sys
import os

REQUIRED_COLUMNS = ["assignment", "group", "score", "weight"]


def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists,
    and extracts all fields into a list of dictionaries.
    Empty rows and rows with bad data are skipped and counted.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ").strip()

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    if os.path.getsize(filename) == 0:
        print(f"Error: The file '{filename}' is empty.")
        sys.exit(1)

    assignments = []
    bad_rows = 0

    try:
        with open(filename, mode='r', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file)

            # Check that the required columns exist
            headers = [h.strip().lower() for h in (reader.fieldnames or [])]
            missing = [c for c in REQUIRED_COLUMNS if c not in headers]
            if missing:
                print(f"Error: Missing required column(s): {', '.join(missing)}")
                sys.exit(1)

            for line_no, raw in enumerate(reader, start=2):
                row = {(k or "").strip().lower(): (v or "").strip() for k, v in raw.items()}

                # Skip completely empty rows
                if not any(row.values()):
                    continue

                try:
                    group = row['group'].capitalize()
                    if not row['assignment'] or group not in ("Formative", "Summative"):
                        raise ValueError("bad name or group")
                    assignments.append({
                        'assignment': row['assignment'],
                        'group': group,
                        'score': float(row['score']),
                        'weight': float(row['weight'])
                    })
                except (ValueError, KeyError):
                    bad_rows += 1
                    print(f"Warning: line {line_no} skipped (missing or invalid data).")

    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

    if bad_rows:
        print(f"Total invalid rows skipped: {bad_rows}")

    if not assignments:
        print("Error: No valid assignment records were found in the file.")
        sys.exit(1)

    return assignments


def evaluate_grades(data):
    """
    'data' is a list of dictionaries containing the assignment records.
    """
    print("\n--- Processing Grades ---")

    # a) Check that all scores are percentages (0-100)
    out_of_range = [d for d in data if not (0 <= d['score'] <= 100)]
    if out_of_range:
        print("Error: Scores must be between 0 and 100. Invalid entries:")
        for d in out_of_range:
            print(f"  - {d['assignment']}: {d['score']}")
        return

    # b) Validate weights (Total=100, Formative=60, Summative=40)
    formative = [d for d in data if d['group'] == "Formative"]
    summative = [d for d in data if d['group'] == "Summative"]
    f_weight = sum(d['weight'] for d in formative)
    s_weight = sum(d['weight'] for d in summative)
    total_weight = f_weight + s_weight

    if abs(total_weight - 100) > 1e-9 or abs(f_weight - 60) > 1e-9 or abs(s_weight - 40) > 1e-9:
        print("Error: Invalid weights.")
        print(f"  Total: {total_weight} (must be 100)")
        print(f"  Formative: {f_weight} (must be 60)")
        print(f"  Summative: {s_weight} (must be 40)")
        return

    # c) Final grade and GPA
    f_earned = sum(d['score'] * d['weight'] / 100 for d in formative)
    s_earned = sum(d['score'] * d['weight'] / 100 for d in summative)
    total_grade = f_earned + s_earned
    gpa = (total_grade / 100) * 5.0

    # d) Pass/Fail: at least 50% in BOTH categories
    f_pct = f_earned / f_weight * 100
    s_pct = s_earned / s_weight * 100
    passed = f_pct >= 50 and s_pct >= 50

    print(f"Formative:  {f_earned:.2f}/{f_weight:.0f}  ({f_pct:.1f}%)")
    print(f"Summative:  {s_earned:.2f}/{s_weight:.0f}  ({s_pct:.1f}%)")
    print(f"Total Grade: {total_grade:.2f}/100")
    print(f"GPA: {gpa:.2f}")

    # e) Failed formative assignments (< 50%), highest weight(s) only
    failed = [d for d in formative if d['score'] < 50]

    # f) Final decision and resubmission options
    print(f"\nFinal Status: {'PASSED' if passed else 'FAILED'}")

    if failed:
        top_weight = failed[0]['weight']
        for d in failed:          # manual max, no max() needed
            if d['weight'] > top_weight:
                top_weight = d['weight']
        print("Eligible for resubmission:")
        for d in failed:
            if d['weight'] == top_weight:
                print(f"  - {d['assignment']} (weight {d['weight']:g}, score {d['score']:g})")
    else:
        print("No failed formative assignments. No resubmission needed.")


if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()

    # 2. Process the features
    evaluate_grades(course_data)
