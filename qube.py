#!/bin/python3

import sys
import os

# Create container file
def create_container(container_name):
    path = f"{os.path.expanduser('~')}/.container/{container_name}/rootfs/"
    print(f"[+] Creating container at {path}")
    os.makedirs(path)

    print("[+] Extracting rootfs image into container")
    copy_rootfs = f"tar -xf /opt/qube-container-template/debian-12.tar.gz -C {path} && mv {path}debian-12/* {path}"
    os.system(copy_rootfs)
    print(f"[+] Succesfully created container {container_name}")

# Connect container image to modifieable file system
def connect_container(container_name):
    command = f"ln -s {os.path.expanduser('~')}/.container/{container_name}/rootfs/* {os.path.expanduser('~')}/.container/{container_name}/fs/"
    try:
        os.mkdir(f"{os.path.expanduser('~')}/.container/{container_name}/fs/")
    except FileExistsError:
        print("[!] Container already connected.")
        exit(1)
    except FileNotFoundError:
        print("[!] Container rootfs not found.")

    os.system(command)
    print(f"[+] Connected container {container_name}.")

# Copy directory to container
def connect_container_dir(container_name, dest, src):
    command = f"cp -r {src}/* {os.path.expanduser('~')}/.container/{container_name}/fs/{dest}/"
    print("Copying files...")
    os.system(command)
    print(f"[+] Done copying files into {container_name}")

# Remove container file
def remove_container(container_name):
    os.system(f"sudo rm -rf {os.path.expanduser('~')}/.container/{container_name}")
    print(f"[-] Removed container {container_name}")

def chroot_container(container_name):
    os.system(f"sudo chroot {os.path.expanduser('~')}/.container/{container_name}/rootfs")

# Print help menu
def print_help():
    print("qube help menu:")
    print("    create:   Create a container file.")
    print("    connect:   Connect rootfs image to file system.")
    print("    connect-dir:   Copy directory to container file system.")
    print("    remove:   Remove container.")
    print("    chroot:   chroot into container.")

# Main function
def main():
    option = ""
    file = ""
    file1 = ""
    file2 = ""

    for i in range(len(sys.argv)):
        if sys.argv[i] == "/usr/bin/qube":
            continue

        if option == "create":
            file = sys.argv[i]
            break

        if option == "connect":
            file = sys.argv[i]
            break

        if option == "connect-dir":
            file = sys.argv[i]
            i += 1
            file1 = sys.argv[i]
            i += 1
            file2 = sys.argv[i]
            break

        if option == "remove":
            file = sys.argv[i]
            break

        if option == "chroot":
            file = sys.argv[i]
            break

        if sys.argv[i] == "create":
            option = "create"
            continue

        if sys.argv[i] == "connect":
            option = "connect"
            continue

        if sys.argv[i] == "connect-dir":
            option = "connect-dir"
            continue
            
        if sys.argv[i] == "remove":
            option = "remove"
            continue

        if sys.argv[i] == "chroot":
            option = "chroot"
            continue

    else:
        print_help()

    if option == "create":
        create_container(file)
    if option == "connect":
        connect_container(file)
    if option == "connect-dir":
        connect_container_dir(file, file2, file1)
    if option == "remove":
        remove_container(file)
    if option == "chroot":
        chroot_container(file)
        

if __name__ == "__main__":
    main()