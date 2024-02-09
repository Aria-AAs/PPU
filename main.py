"""A module that check for outdated package and update them
"""

import subprocess
import re


class PPU:
    """Work with python outdated packages and update them."""

    def run_command(self, command: str) -> list[str]:
        """run a command and show the stdout and stderr.

        Args:
            command (str): the command to run.

        Returns:
            tuple: A list of command output lines and a return code.
        """
        print(f"\033[33mRunning `\033[0m{command}\033[33m` command...\033[0m")
        command_outputs = []
        with subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ) as process:
            while True:
                output = process.stdout.readline().decode()
                if output == "" and process.poll() is not None:
                    error = process.stderr.read().decode()
                    if error:
                        print("\033[31mCommand error:\033[0m", error.strip())
                    break
                if output:
                    print("\033[32mCommand output:\033[0m", output.strip())
                    command_outputs.append(output)
        return_code = process.poll()
        if return_code:
            print("\n\033[31mFinish with bellow error!\033[0m")
            return ([], 1)
        print("\033[32mFinish.\033[0m")
        return (command_outputs, 0)

    def get_outdated_packages(self) -> list | None:
        """Get outdated python packages using `pip list --outdated` command

        Returns:
            list | None: A list of name of outdated packages or None if there is no outdated package
        """
        command = "pip list --outdated"
        print("\033[33mGetting outdated packages ...\033[0m")
        command_output, return_code = self.run_command(command)
        if return_code:
            print("\033[31mError raised while getting outdated packages\033[0m")
        if not command_output:
            return None
        print("\033[33mOutdated packages:\033[0m")
        outdated_packages_list = []
        for line in command_output:
            # package_name = line.split(" ")[0]
            package_name = re.split("^([a-z,A-Z,0-9,_,.,-]*)", line)[1]
            if package_name == "Package" or re.match("-+", package_name):
                continue
            if line == command_output[-1]:
                print(package_name)
            else:
                print(package_name, end=" - ")
            outdated_packages_list.append(package_name)
        return outdated_packages_list

    def update_package(self, package_name: str) -> None:
        """Update a python package

        Args:
            package_name (str): Name of package to update
        """
        command = f"pip install --upgrade {package_name}"
        print(f"\033[33mUpdating '\033[0m{package_name}\033[33m' ...\033[0m")
        _, return_code = self.run_command(command)
        if return_code:
            print(f"\033[31mError raised while updating '{package_name}'.\033[0m\n")
        else:
            print(f"\033[32m'{package_name}' is up to date now.\033[0m")

    def update_all(self) -> None:
        """Update all python packages."""
        outdated_packages = self.get_outdated_packages()
        if outdated_packages is None:
            print("\033[32mThere is no outdated package.\033[0m")
            return
        if "pip" in outdated_packages:
            self.update_package("pip")
        for outdated_package in outdated_packages:
            self.update_package(outdated_package)
        print("\033[32mAll packages are up to date now.\033[0m")


def main() -> None:
    """Main function of the module"""
    ppu = PPU()
    ppu.update_all()


if __name__ == "__main__":
    main()
