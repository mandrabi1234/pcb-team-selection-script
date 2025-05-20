import subprocess
import sys
import os

# Replace these with the actual paths to your .py files on Windows
script1 = r"C:\Users\Mohi Andrabi\Documents\GitHub\pcb_teamSelection\pcb-team-selection-script\Factor Calculations\test_t20.py"
script2 = r"C:\Users\Mohi Andrabi\Documents\GitHub\pcb_teamSelection\pcb-team-selection-script\Rankings\test_t20_rankings.py"

def run_script(script_path):
    print(f"\nRunning: {script_path}\n{'-'*60}")
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)

    if result.returncode == 0:
        print(" Success")
        print(result.stdout[:1000])  # Print first 1000 characters of output
    else:
        print(" Failed")
        print(result.stderr)
        raise RuntimeError(f"Script failed: {script_path}")

if __name__ == "__main__":
    run_script(script1)
    run_script(script2)
    print("\nAll scripts executed successfully.")
