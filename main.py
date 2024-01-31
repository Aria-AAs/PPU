"""A module that check for outdated package and update them
"""
import subprocess
import re

SHELL_COMMAND = "pip list --outdated"

result = subprocess.run(
    SHELL_COMMAND,
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)

if result.returncode == 0:
    command_outputs = result.stdout
    command_outputs = command_outputs.split("\n")
    package_list = []
    if command_outputs == [""]:
        print("There is no outdated package.")
    else:
        print("Outdated packages:")
    for command_output in command_outputs:
        if command_output in (
            "Package                   Version   Latest      Type",
            "------------------------- --------- ----------- -----",
            "",
        ):
            continue
        package_name = re.split("^([a-z,A-Z,0-9,_,.,-]*)", command_output)[1]
        REGEX_PATTERN = r"^-(.*)-$"
        match_result = re.match(REGEX_PATTERN, command_output)
        if package_name in ("Package", "------------------"):
            continue
        if match_result:
            continue
        if package_name in package_list:
            continue
        package_list.append(package_name)
        if command_output == command_outputs[-2]:
            print(package_name)
        else:
            print(package_name, end=", ")
    if "pip" in package_list:
        SHELL_COMMAND = "python -m pip install --upgrade pip"
        print("Updating 'pip' ...")
        result = subprocess.run(
            SHELL_COMMAND,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            print("Package 'pip' is up to date now.")
        else:
            print("Error:\n", result.stderr)
    for package in package_list:
        SHELL_COMMAND = f"pip install --upgrade {package}"
        print(f"Updating '{package}' ...")
        result = subprocess.run(
            SHELL_COMMAND,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            print(f"Package '{package}' is up to date now.")
        else:
            print("Error:\n", result.stderr)
            continue
else:
    print("Error:\n", result.stderr)
