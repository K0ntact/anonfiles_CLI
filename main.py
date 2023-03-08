import requests
import shutil
from bs4 import BeautifulSoup
from file_explorer import *


class SESSION:
    ID = "eyJpdiI6IkJ5aU9EMFRZS0c0Zjg5TmZCV3g5SGc9PSIsInZhbHVlIjoiczl6bTlJU2JwT3hSa1VQdzAzODBHeHJQWEVOcVRucktCWHErdHM5eG9VdE9TNmNERkdCNGNDVUdDSTBramhBaiIsIm1hYyI6Ijg0OGU5MDc2NGMxYTI0ZjY3ZTE1YWQ4Y2FhYmJiY2I0Y2IxYjBjNTUwZGQwM2QzZGI2OTAzZmFhYzQ4MDIzZDgifQ"
    COOKIE = {'USERSESSID': ID}


class API:
    MAIN = "https://api.anonfiles.com"
    UPLOAD = f"{MAIN}/upload"
    GET = "https://api.anonfiles.com/v2/file/"  # +{id}/info


def download_extractor(file_link: str) -> str:
    r = requests.get(file_link)
    soup = BeautifulSoup(r.content, 'html.parser')
    link = soup.findAll('a')
    return link[2]['href']


def main():
    while True:
        print("AnonFiles CLI Tool")
        print("-"*20)
        print(f"[{BCOLORS.YELLOW}1{BCOLORS.ENDC}] Upload anonymously")
        print(f"[{BCOLORS.YELLOW}2{BCOLORS.ENDC}] Upload to account")
        print(f"[{BCOLORS.YELLOW}3{BCOLORS.ENDC}] Download from account")
        print("-" * 20)
        print(f"[{BCOLORS.YELLOW}0{BCOLORS.ENDC}] Exit")
        choice = int(input("Your choice: "))

        match choice:
            case 0:
                print(f"\n{BCOLORS.RED}Exiting AnonFiles CLI Tool....{BCOLORS.ENDC}\nHave a nice day!")
                break

            case 1:
                file_name, path = file_explorer()
                if file_name == "" and path == "":
                    print(f"\n{BCOLORS.RED}Exiting AnonFiles CLI Tool....{BCOLORS.ENDC}\nHave a nice day!")
                    break
                print(f"Uploading {file_name}...")

                # if chosen file is a folder, compress it and return the path to compressed folder
                isDir = False
                if os.path.isdir(path):
                    compressed_path = shutil.make_archive(path, "zip", path)
                    path = compressed_path
                    isDir = True

                result = requests.post(
                    API.UPLOAD,
                    files={"file": open(path, "rb")}
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
                file_name, path = file_explorer()
                print(f"Uploading {file_name}...")

                isDir = False
                if os.path.isdir(path):
                    compressed_path = shutil.make_archive(path, "zip", path)
                    path = compressed_path
                    isDir = True

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

            case 3:
                # cookie = input("Enter your cookie (Please check README.md for more info):\n")
                r = requests.get('https://anonfiles.com', cookies=SESSION.COOKIE)

                soup = BeautifulSoup(r.content, 'html.parser')
                file_name = soup.find_all("div", class_="upload-filename")
                pg_link = soup.find_all("input", class_="form-control upload-file-input")

                save_path = (os.getcwd()).replace("\\", "/")
                while True:
                    print(f"\nSave file at: {save_path}")
                    print("-" * 20)
                    no_files = len(file_name)
                    for index in range(0, no_files):
                        print("[{}{}{}] {}".format(
                                BCOLORS.YELLOW,
                                index + 1,
                                BCOLORS.ENDC,
                                file_name[index].text.strip()
                              )
                        )
                    print("-" * 20)
                    print(f"[{BCOLORS.YELLOW}.{BCOLORS.ENDC}] Change save path")
                    print(f"[{BCOLORS.YELLOW}x{BCOLORS.ENDC}] Back")
                    choice = input("Your choice: ")

                    if choice == "x":
                        break

                    elif choice == ".":
                        name, path = file_explorer()
                        save_path = path

                    elif int(choice) in range(1, no_files + 1):
                        dl_link = download_extractor(pg_link[int(choice)-1]['value'])

                        save = save_path + f"/{file_name[int(choice)-1].text.strip()}"
                        with requests.get(dl_link, stream=True) as r:
                            with open(save, "wb") as f:
                                for chunk in r.iter_content(1024*1024*2):
                                    print("Downloading...")
                                    f.write(chunk)
                        print("Download completed")

if __name__ == '__main__':
    main()
