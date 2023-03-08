from colors import *
import os, shutil

def file_explorer() -> tuple[str, str, bool]:
    '''
    Returns file/directory name, the path and whether if it is a compressed directory
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
        print(f"[{BCOLORS.YELLOW}.{BCOLORS.ENDC}] Upload current directory")
        print(f"{BCOLORS.RED}[x]{BCOLORS.ENDC} Exit program")
        index = input("Your choice: ")

        if index == ".":
            folder_name = os.path.basename(current_path)
            compressed_path = shutil.make_archive(current_path, "zip", current_path)
            return folder_name, compressed_path, True

        if index == "x":
            return "", "", False

        if int(index) == 0:
            current_path = os.path.dirname(current_path)

        elif int(index) in range(1, len(files) + 1):
            # Anon Files can't upload a directory as a whole, only its files
            if os.path.isdir(current_path + "/" + files[int(index)-1]):
                current_path = current_path + "/" + files[int(index)-1]
            else:
                return files[int(index)-1], current_path+"/"+files[int(index)-1], False

        else:
            print(f"{BCOLORS.RED}Invalid choice, please try again!{BCOLORS.ENDC}")