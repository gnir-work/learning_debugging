from utils import get_all_possible_passwords
from zipfile import ZipFile
import zlib
import argparse


def break_zip_password(
    path_to_zip: str,
    extract_to: str,
    password_length: int = 5,
    common_passwords_path: str = "",
    verbose: bool = False,
) -> str:
    """
    Try breaking the given zip file by brute forcing it.
    We use autogenerated passwords and all of the passwords given in common_passwords_path, please read
    utils.load_common_passwords for a more detailed explanation about the file format.
    :path_to_zip: The path to the zip file that should be broken.
    :extract_to: The path to folder in which the files will be extracted.
    :common_passwords_path: The path to the folder with the common passwords.
    :verbose: If given, the function will print all of the passwords tried and the correct password.
    :return: Returns the correct password
    """
    zipfile = ZipFile(path_to_zip)
    for password in get_all_possible_passwords(
        generated_password_length=password_length,
        common_passwords_path=common_passwords_path,
    ):
        try:
            zipfile.extractall(extract_to, pwd=password.encode("utf-8"))
        except (RuntimeError, zlib.error):
            if verbose:
                print(password, "Failed!")
        else:
            if verbose:
                print(
                    password,
                    f"Succeeded!, Please look at your files here: {extract_to}",
                )
            break


def get_arguments():
    """
    Get the arguments for the worker from the command line.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("zip_file", help="The zip to crack")
    parser.add_argument("extract_to", help="The folder to extact to")
    parser.add_argument(
        "--password-length",
        help="The length of the generated password",
        type=int,
        default=5
    )
    parser.add_argument(
        "--common-passwords-file",
        help="The path to the file containing passwords you want to try",
        default="",
    )
    parser.add_argument(
        "--verbose", help="increase output verbosity", action="store_true"
    )
    return parser.parse_args()


if __name__ == "__main__":
    arguments = get_arguments()
    break_zip_password(
        arguments.zip_file,
        arguments.extract_to,
        arguments.password_length,
        arguments.common_passwords_file,
        arguments.verbose,
    )
