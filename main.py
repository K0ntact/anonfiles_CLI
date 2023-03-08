import requests
from colors import *
from file_explorer import *


class API:
    MAIN = "https://api.anonfiles.com"
    UPLOAD = f"{MAIN}/upload"
    GET = "https://api.anonfiles.com/v2/file/"  # +{id}/info


def main():
    while True:
        print("AnonFiles CLI Tool")
        print("-"*20)
        print(f"[{BCOLORS.YELLOW}1{BCOLORS.ENDC}] Upload anonymously")
        print(f"[{BCOLORS.YELLOW}2{BCOLORS.ENDC}] Upload to account")
        # print(f"[{BCOLORS.YELLOW}3{BCOLORS.ENDC}] Download from account")
        print("-" * 20)
        print(f"[{BCOLORS.YELLOW}0{BCOLORS.ENDC}] Exit")
        choice = int(input("Your choice: "))

        match choice:
            case 0:
                print(f"\n{BCOLORS.RED}Exiting AnonFiles CLI Tool....{BCOLORS.ENDC}\nHave a nice day!")
                break

            case 1:
                chosen_file, path, isDir = file_explorer()
                if chosen_file == "" and path == "":
                    print(f"\n{BCOLORS.RED}Exiting AnonFiles CLI Tool....{BCOLORS.ENDC}\nHave a nice day!")
                    break

                print(f"Uploading {chosen_file}...")

                result = requests.post(
                    API.UPLOAD,
                    files = {"file": open(path, "rb")}
                )

                if result.status_code == 200:
                    print("File uploaded successfully!")
                    link = result.json()["data"]["file"]["url"]["short"]
                    print(f"Link: {link}\n")
                    print(f"{BCOLORS.RED}Save the link now or it will be lost forever!{BCOLORS.ENDC}")

                    # if the uploaded file is a compressed directory, remove it from local after uploading
                    if isDir:
                        os.remove(path)

                else:
                    error_code = result.json()["error"]["code"]
                    error_type = result.json()["error"]["type"]
                    error_message = result.json()["error"]["message"]
                    print(f"{BCOLORS.RED}Code {error_code}: {error_type}{BCOLORS.ENDC}")
                    print(f"{BCOLORS.RED}{error_message}{BCOLORS.ENDC}")

            case 2:
                API_KEY = input("Enter your account API key (Login then check API tab at the bottom of the page):\n")
                chosen_file, path, isDir = file_explorer()
                print(f"Uploading {chosen_file}...")

                result = requests.post(
                    API.UPLOAD + "?token=" + API_KEY,
                    files={"file": open(path, "rb")}
                )

                if result.status_code == 200:
                    print("File uploaded successfully!")
                    link = result.json()["data"]["file"]["url"]["short"]
                    print(f"Link: {link}\n")
                    print(f"{BCOLORS.YELLOW}The file is now uploaded to your account{BCOLORS.ENDC}")

                    # if the uploaded file is a compressed directory, remove it from local after uploading
                    if isDir:
                        os.remove(path)

                else:
                    error_code = result.json()["error"]["code"]
                    error_type = result.json()["error"]["type"]
                    error_message = result.json()["error"]["message"]
                    print(f"{BCOLORS.RED}Code {error_code}: {error_type}{BCOLORS.ENDC}")
                    print(f"{BCOLORS.RED}{error_message}{BCOLORS.ENDC}")


if __name__ == '__main__':
    main()
