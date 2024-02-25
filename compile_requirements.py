import os
import subprocess

# Path to directory containing requirements.in files
REQUIREMENTS_PATH = os.path.join(os.path.dirname(__file__), "requirements")

# Arguments to pass to pip-compile
PIP_COMPILE_ARGS = ["--strip-extras"]


def main() -> None:
    processes = []

    for requirements_file in os.listdir(REQUIREMENTS_PATH):
        if requirements_file.endswith(".in"):
            input_path = os.path.join(REQUIREMENTS_PATH, requirements_file)
            p = subprocess.Popen(["pip-compile", input_path, *PIP_COMPILE_ARGS])
            processes.append(p)

    for p in processes:
        p.wait()


if __name__ == "__main__":
    main()
