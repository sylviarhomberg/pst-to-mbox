import os
import subprocess

def run_live(cmd):
    """Run a command and stream its output live to the console."""
    print("Running:", " ".join(cmd), flush=True)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in proc.stdout:
        print(line, end="")  # stream live output
    proc.wait()
    if proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, cmd)

def pst_to_mbox(target_dir, mbox_dir):
    """Convert all PST/OST files in target_dir to MBOX format with folder hierarchy preserved."""
    os.makedirs(mbox_dir, exist_ok=True)
    for _root, _dirs, files in os.walk(target_dir):
        for file in files:
            if file.lower().endswith((".pst", ".ost")):
                print(f"Converting {file} to MBOX (preserving folder hierarchy)...", flush=True)
                cmd = ["readpst", "-D", "-b", "-r", "-o", mbox_dir, os.path.join(target_dir, file)]
                run_live(cmd)

if __name__ == "__main__":
    os.chdir("/app")
    target_dir = "target_files"
    mbox_dir = "mbox_dir"

    if not os.path.exists(mbox_dir) or not os.listdir(mbox_dir):
        print("No MBOX files found — starting PST to MBOX conversion...\n", flush=True)
        print("Contents of target_files:", os.listdir(target_dir), flush=True)
        pst_to_mbox(target_dir, mbox_dir)
    else:
        print(f"Skipping PST conversion — found existing MBOX files in {mbox_dir}", flush=True)

    print("✅ Conversion complete. MBOX files are ready for import.", flush=True)
