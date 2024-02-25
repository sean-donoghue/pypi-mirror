import asyncio
import os
import subprocess

# Path to directory containing requirements.in files
REQUIREMENTS_PATH = os.path.join(os.path.dirname(__file__), "requirements")

# Arguments to pass to pip-compile
PIP_COMPILE_ARGS = ["--strip-extras"]


async def main() -> None:
    print(f"Looking for requirements.in files in path: {REQUIREMENTS_PATH}")

    coros = []
    for requirements_file in os.listdir(REQUIREMENTS_PATH):
        if requirements_file.endswith(".in"):
            print(f"Found requirements file: {requirements_file}")
            input_path = os.path.join(REQUIREMENTS_PATH, requirements_file)
            coro = pip_compile_async(input_path)
            coros.append(coro)

    print(f"Running pip-compile on {len(coros)} requirements files")
    await asyncio.gather(*coros)

    print("All requirements files have been compiled")


async def pip_compile_async(input_path: str) -> None:
    cmd = ["pip-compile", input_path, *PIP_COMPILE_ARGS]
    process = await asyncio.create_subprocess_exec(*cmd, stderr=subprocess.DEVNULL)
    await process.wait()

    print(f"pip-compile finished for file: {input_path}")


if __name__ == "__main__":
    asyncio.run(main())
