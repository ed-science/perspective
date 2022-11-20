################################################################################
#
# Copyright (c) 2019, the Perspective Authors.
#
# This file is part of the Perspective library, distributed under the terms of
# the Apache License 2.0.  The full license can be found in the LICENSE file.
#

import os
import subprocess
from bench import VirtualEnvHandler

if __name__ == "__main__":
    """Benchmark the `perspective-python` runtime locally."""
    VERSIONS = ["master", "0.4.1", "0.4.0-rc.6"]

    # Access the benchmark virtualenv
    HERE = os.path.abspath(os.path.dirname(__file__))
    VIRTUALENV_NAME = "benchmark_venv"
    VIRTUALENV_PATH = os.path.join(HERE, VIRTUALENV_NAME)
    venv_handler = VirtualEnvHandler(VIRTUALENV_PATH)

    # Run master in current env always
    if venv_handler._is_activated:
        venv_handler.deactivate_virtualenv()

    print("Benchmarking perspective-python==master")
    subprocess.check_output(
        f"python3 {HERE}/perspective_benchmark.py master", shell=True
    )


    # Run previous versions in virtualenv
    if not venv_handler.virtualenv_exists():
        venv_handler.create_virtualenv()

    if not venv_handler._is_activated:
        venv_handler.activate_virtualenv()

    print("Installing pyarrow==0.16.0")
    subprocess.check_output("yes | python3 -m pip install pyarrow==0.16.0", shell=True)

    for version in VERSIONS[1:]:
        print(f"Installing perspective-python=={version}")
        subprocess.check_output(
            "yes | python3 -m pip uninstall perspective-python", shell=True
        )
        subprocess.check_output(
            f"yes | python3 -m pip install perspective-python=={version}",
            shell=True,
        )

        print(f"Benchmarking perspective-python=={version}")
        subprocess.check_output(
            f"python3 {HERE}/perspective_benchmark.py {version}", shell=True
        )
