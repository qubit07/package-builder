import argparse
import yaml
import subprocess
from pathlib import Path


def load_tasks(path: str):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def run_command(cmd: str, cwd: str):
    print(f"Running: {cmd} (cwd={cwd})")
    subprocess.run(cmd, shell=True, cwd=Path(cwd), check=True)


def execute_commands(task: dict):
    name = task.get("name", "unknown")
    cwd = task.get("cwd", ".")
    commands = task.get("commands", [])

    print(f"\n=== Task: {name} ===")
    for cmd in commands:
        run_command(cmd, cwd)

def copy_files(task: dict):
    src = task.get("src")
    dst = task.get("dst")
    if not src or not dst:
        raise ValueError("Copy task must have 'src' and 'dst'")
    print(f"Copying from {src} to {dst}")
    run_command(f"cp -r {src} {dst}", ".")

def package_files(task: dict):
    src = task.get("src")
    dst = task.get("dst")
    if not src or not dst:
        raise ValueError("Tar task must have 'src' and 'dst'")
    print(f"Packaging {src} into {dst}")
    run_command(f"tar -czf {dst} {src}", ".")

def copy_ssh(task: dict):
    src = task.get("src")
    dst = task.get("dst")
    if not src or not dst:
        raise ValueError("SSH task must have 'src' and 'dst'")
    print(f"Copying {src} to {dst} via SSH")
    run_command(f"scp -r {src} {dst}", ".")

def run_tasks(tasks: list):
    """Execute a list of tasks."""
    for task in tasks:
        type = task.get("type", "unknown")

        if type == "command":
            execute_commands(task)
        elif type == "copy":
            copy_files(task)
        elif type == "tar":
            package_files(task)
        elif type == "ssh":
            copy_ssh(task)
        else:
            raise ValueError(f"Unknown task type: {type}")

def main():
    parser = argparse.ArgumentParser(description="Run tasks defined in a YAML file.")
    parser.add_argument("file", help="YAML task file")
    args = parser.parse_args()
    data = load_tasks(args.file)
    tasks  = data.get("tasks", [])
    print(f"Loaded {len(tasks)} tasks from {args.file}")
    run_tasks(tasks)


if __name__ == "__main__":
    main()