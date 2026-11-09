# Lab 2: ALU Transcript Generator

A Python application that calculates a student's final academic standing from a CSV file of grades, plus a Bash script that archives the CSV and logs the action.

## Files

| File | Purpose |
|---|---|
| `grade-evaluator.py` | Validates grades and weights, calculates GPA, decides PASSED/FAILED, and lists assignments eligible for resubmission |
| `organizer.sh` | Archives `grades.csv` with a timestamp, creates a fresh empty `grades.csv`, and logs the operation |
| `grades.csv` | Sample course data |
| `Readme.md` | This file |

No external libraries are used, only Python's built-in `csv`, `sys` and `os` modules.

## CSV format

```
assignment,group,score,weight
Quiz,Formative,85,20
Group Exercise,Formative,40,20
```

- `group` must be `Formative` or `Summative`
- `score` must be between 0 and 100
- Weights must total 100: Formative = 60, Summative = 40

## Running the Python application

```bash
python3 grade-evaluator.py
```

When prompted, enter the CSV filename (for example `grades.csv`).

The program:
1. Validates that every score is between 0 and 100.
2. Validates weights (total 100, Formative 60, Summative 40).
3. Calculates `GPA = (Total Grade / 100) * 5.0`.
4. Passes the student only if they score at least 50% in **both** Formative and Summative.
5. Lists the failed Formative assignment(s) (score below 50) with the highest weight as eligible for resubmission. Ties are all shown.

### Error handling

Clear messages are shown for: a missing file, an empty file, missing columns, empty rows (skipped), non-numeric or invalid rows (skipped and counted), scores outside 0-100, and incorrect weights.

## Running the organizer

```bash
chmod +x organizer.sh
./organizer.sh
```

The script:
1. Creates an `archive/` directory if it does not exist.
2. Moves `grades.csv` into `archive/` as `grades_YYYYMMDD-HHMMSS.csv`.
3. Creates a new empty `grades.csv`.
4. Appends the timestamp, original filename and archived filename to `organizer.log`.

## Example output

For the sample data: Formative 56.7%, Summative 65.0%, GPA 3.00, status PASSED, and resubmission eligible for Group Exercise and Functions and Debugging Lab (both weight 20).
