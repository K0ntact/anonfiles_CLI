import requests
import shutil
from bs4 import BeautifulSoup
from file_explorer import *


class SESSION:
    ID = "eyJpdiI6IkZsYU95RGg4RFA0Mnd6eXgyRVJEa0E9PSIsInZhbHVlIjoiTlY0cjA2a0VlNWZnQWc2YkQyNlBZOTFRM2JBb0hBSmt3STNIZzEwdVZxbWRxd3FnVlVmdWdYb3h3Zk92VVZlNCIsIm1hYyI6Ijk1MDUzZWRjYmIyMGM3NzkzY2YwNjQyZTM1YmZjYWE4NzJkYTFlOWYzZjIxMjU2MGZiYTg5YTlhYjMxNTA4YjcifQ%3D%3D"
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
        # print(f"[{BCOLORS.YELLOW}3{BCOLORS.ENDC}] Download from account")
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

            # case 3:
            #     cookie = input("Enter your cookie (Please check README.md for more info):\n")
            #     r = requests.get(API.MAIN, cookies=cookie)
            #
            #     soup = BeautifulSoup(r.content, 'html.parser')
            #     file_name = soup.find_all("div", class_="upload-filename")
            #     pg_link = soup.find_all("input", class_="form-control upload-file-input")
            #
            #     no_files = len(file_name)
            #
            #     for index in range(0, no_files):
            #         print("[{}{}{}] {}",
            #                 BCOLORS.YELLOW,
            #                 index + 1,
            #                 BCOLORS.ENDC,
            #                 file_name[index]
            #               )
            #     print("-" * 20)
            #     print(f"{BCOLORS.RED}[x] Exit the program{BCOLORS.ENDC}")
            #     choice = input("Your choice: ")
            #
            #     if choice == "x":
            #         break
            #
            #     if int(choice) in range(1, no_files + 1):
            #         dl_link = download_extractor(pg_link[int(choice)-1])

if __name__ == '__main__':
    main()
