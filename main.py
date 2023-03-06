import json
import os
import requests
import re
from colors import *

API_KEY = ""


class API:
    MAIN = "https://api.anonfiles.com"
    UPLOAD = f"{MAIN}/upload"


def file_explorer() -> tuple[str, str]:
    '''
    Returns file name and file path when a file is chosen
    '''

    current_path = (os.getcwd()).replace("\\", "/")  # this returns path in \, but we need path in /

    while True:
        files = []  # stores all files and directories in current path

        print("\nCurrent path: " + current_path)
        print(f"{BCOLORS.BLUE}Blue is directory{BCOLORS.ENDC}")
        print(f"{BCOLORS.GREEN}Green is file{BCOLORS.ENDC}")
        print("-" * 20)

        for file in os.listdir(current_path):
            files.append(file)
            if os.path.isfile(current_path+"/"+file):
                print(f"[{BCOLORS.YELLOW}{files.index(file) + 1}{BCOLORS.ENDC}] "
                      f"{BCOLORS.GREEN}{file}{BCOLORS.ENDC}")
            else:
                print(f"[{BCOLORS.YELLOW}{files.index(file) + 1}{BCOLORS.ENDC}] "
                      f"{BCOLORS.BLUE}{file}{BCOLORS.ENDC}")
        print("-" * 20)
        print(f"[{BCOLORS.YELLOW}0{BCOLORS.ENDC}] Go back")
        index = int(input("Your choice: "))

        if index == 0:
            current_path = os.path.dirname(current_path)

        # Anon File won't upload whole directory directly, so you can only choose a single file (for now)
        elif index in range(1, len(files) + 1):
            if os.path.isdir(current_path + "/" + files[index-1]):
                current_path = current_path + "/" + files[index-1]
            else:
                return files[index-1], current_path+"/"+files[index-1]

        else:
            print(f"{BCOLORS.RED}Invalid choice, please try again!{BCOLORS.ENDC}")


def main():
    while True:
        print("AnonFiles CLI Tool")
        print("-"*20)
        print(f"[{BCOLORS.YELLOW}1{BCOLORS.ENDC}] Upload anonymously")
        print(f"[{BCOLORS.YELLOW}2{BCOLORS.ENDC}] Upload to account")
        print("-" * 20)
        print(f"[{BCOLORS.YELLOW}0{BCOLORS.ENDC}] Exit")
        choice = int(input("Your choice: "))

        match choice:
            case 0:
                print(f"\n{BCOLORS.RED}Exiting AnonFiles CLI Tool....{BCOLORS.ENDC}\nHave a nice day!")
                break

            case 1:
                chosen_file, path = file_explorer()
                print(f"Uploading {chosen_file}...")

                result = requests.post(
                    API.UPLOAD,
                    files = {"file": open(path, "rb")}
                )

                if (result.status_code == 200):
                    print("File uploaded successfully!")
                    link = json.loads(result.text)["data"]["file"]["url"]["short"]
                    print(f"Link: {link}\n")
                    print(f"{BCOLORS.RED}Save the link now or it will be lost forever!{BCOLORS.ENDC}")
                else:
                    print("Error uploading file")

            case 2:
                API_KEY = input("Enter your account API key (Login then check API tab at the bottom of the page):\n")
                chosen_file, path = file_explorer()
                print(f"Uploading {chosen_file}...")

                result = requests.post(
                    API.UPLOAD + "?token=" + API_KEY,
                    files={"file": open(path, "rb")}
                )

                if (result.status_code == 200):
                    print("File uploaded successfully!")
                    link = json.loads(result.text)["data"]["file"]["url"]["short"]
                    print(f"Link: {link}\n")
                    print(f"{BCOLORS.YELLOW}The file is now uploaded to your account{BCOLORS.ENDC}")
                else:
                    print("Error uploading file")


if __name__ == '__main__':
    main()
