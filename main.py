import json
import os
import requests
import re

API_KEY = ""


class BCOLORS:
    HEADER = '\033[95m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class API:
    MAIN = "https://api.anonfiles.com"
    UPLOAD = f"{MAIN}/upload"


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
                files = []
                print("Choose file to upload: ")
                for file in os.listdir("."):
                    files.append(file)
                    print(f"[{BCOLORS.YELLOW}{files.index(file)}{BCOLORS.ENDC}] {file}")

                chosen_flies = int(input("Your choice: "))
                print(f"Uploading {files[chosen_flies]}...")

                result = requests.post(
                    API.UPLOAD,
                    files = {"file": open(files[chosen_flies], "rb")}
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
                files = []
                print("Choose file to upload: ")
                for file in os.listdir("."):
                    files.append(file)
                    print(f"[{BCOLORS.YELLOW}{files.index(file)}{BCOLORS.ENDC}] {file}")

                chosen_flies = int(input("Your choice: "))
                print(f"Uploading {files[chosen_flies]}....")

                result = requests.post(
                    API.UPLOAD + "?token=" + API_KEY,
                    files={"file": open(files[chosen_flies], "rb")}
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
