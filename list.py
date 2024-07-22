#!/bin/python3
import argparse
import os
import magic
import random

# Colors
class color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Converts from byte to unit
def convert_to_unit(num: int) -> float:
    global args

    for _ in range(0, args.unit-1):
        num = num / 1024

    return num


# Get the mime type
def get_mime(path: str) -> str:
    global args

    mime = magic.Magic(mime=True)
    try:
        mime_str = get_cutstr(mime.from_file(path))
        return mime_str
    except IsADirectoryError:
        return get_cutstr("inode/directory")
    except (PermissionError, FileNotFoundError, OSError):
        try:
            if os.path.isdir(path):
                return get_cutstr("inode/directory")
            elif os.path.islink(path):
                return get_cutstr("inode/symlink")
            elif os.path.isfile(path):
                return get_cutstr("file")
            else:
                return get_cutstr("device")
        except (PermissionError, FileNotFoundError, OSError):
            return get_cutstr("unreadable")


# Get the size of a file
def get_size(path: str) -> int:
    global args
    import shutil
    # Returns in kilobytes
    try:
        if os.path.isdir(path) and args.real:
            size_num = 0
            for root, _, files in os.walk(path):
                for file in files:
                    full_path = os.path.join(root, file)
                    if os.path.isfile(full_path):
                        size_num += os.path.getsize(full_path)
            
            return convert_to_unit(size_num)
        else:
            return convert_to_unit(os.path.getsize(path))
    except OSError:
        return 0


def get_permission(path: str) -> str:
    try:
        return str(oct(os.stat(path=path).st_mode)[-3:])
    except (FileNotFoundError, PermissionError):
        return "---"


# Get the spacing value
def get_spacing(initial: int, subs: int) -> int:
    if initial >= 10:
        return initial - subs
    else:
        print("Too small, try a 'char' larger than 10!")
        exit(1)


# Gets the unit of measurement
def get_unit() -> str:
    global args

    pot = args.unit

    if pot < 1:
        print("\nUnit needs to be larger than 0!")
        exit(-1)

    units = ["b", "kb", "mb", "gb", "tb"]

    try:
        return units[pot-1]
    except IndexError:
        print(f"\nMax unit number is {len(units)} currently.")
        exit(-1)


# Gets the cutten text of a string
def get_cutstr(name: str) -> str:
    global args

    return name[0:(int(args.chars/1.25))-1] + "..." if len(name) > args.chars / 1.25 else name



# Get the content of a path and its informations
def list_content(path: str) -> dict:
    global args

    isfile = False

    try:
        files = os.listdir(path)
    except PermissionError:
        print("Permission denied!")
        exit(-1)
    except NotADirectoryError:
        isfile = True

    dict_files = {}
    key_names = [0]

    # First, each file on its dict
    if not isfile:
        for f in files:
            kn = 0
            while kn in key_names:
                kn = random.randint(1, 1000000000)
            key_names.append(kn)

            dict_files[f"{kn}"] = {
                "name": f,
                "mime": get_mime(os.path.join(path, f)),
                "size": get_size(os.path.join(path, f)),
                "permissions": get_permission(os.path.join(path, f))
            }
    else:
        dict_files[f"0"] = {
            "name": os.path.basename(path),
            "mime": get_mime(path),
            "size": get_size(path),
            "permissions": get_permission(path)
        } 
    
    return dict_files


# print table of content
def print_table(content: dict, schars: int) -> None:
    global args

    # Just to print table's meanings
    for file, value in content.items():
        for key in value.keys():
            print(color.BOLD, end="")
            spacing = get_spacing(schars, len(key))

            print(key, end=" "*spacing)
            print(color.ENDC, end="")
        break

    print("\n", end="")

    for file, info in content.items():
        for key, value in info.items():

            suffix_sz = 0 if key != "size" else len(get_unit()) + 1
            is_int = False

            path = os.path.join(args.path, info["name"])

            if key == "mime":
                if os.path.isdir(path):
                    print(color.OKGREEN, end="")
                elif os.path.isfile(path) and "inode/symlink" not in value:
                    print(color.OKCYAN, end="")
                elif os.path.islink(path):
                    print(color.WARNING, end="")
                else:
                    print(color.HEADER, end="")

            try:
                val = get_cutstr(value)
            except TypeError:
                val = value
                is_int = True

            spacing = get_spacing(schars, (len(f"{val:.2f}" if is_int else f"{val}") + suffix_sz))
            print(f"{val if not is_int else f'{val:.3f}'}{f' {get_unit()}' if key == 'size' else ''}", end=" "*spacing)

            print(color.ENDC, end="")
        print('\n', end="")
    
    if args.real:
        print(f"\nTotal: {get_size(args.path):.3f} {get_unit()}")



# Main function
def main(path: str) -> int:
    global args

    try:
        content = list_content(path)
    except FileNotFoundError:
        print("No such file or directory")
        return 1

    print_table(content=content, schars=args.chars)
    
    return 0

if __name__ == '__main__':
    # Args
    parser = argparse.ArgumentParser(prog="list", description="A simpler version of ls")
    parser.add_argument("path", help="Path to check contents", type=str, default=".")
    parser.add_argument("--chars", "-c", help="Number of chars of spacing", type=int, default=19)
    parser.add_argument("--unit", "-u", help="Unit of measurement in how big the unit is (bit is 1, kilobit is 2 etc.)", type=int, default=2)
    parser.add_argument("--real", "-r", help="Show the real size of directories? WILL be slower. (true or false)", type=bool, default=False)


    args = parser.parse_args()

    exit_code = main(path=args.path)

    exit(exit_code)

