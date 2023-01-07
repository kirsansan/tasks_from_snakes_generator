""" file operations utilities """
import os


def open_and_create_file(filename: str) -> bool:
    try:
        file = open(filename, 'x')
    except FileNotFoundError:
        return False
    file.close()
    return True


def delete_file(filename: str) -> bool:
    # path = '/path/to/file/filename.ext'
    if os.path.isfile(filename):
        try:
            os.remove(filename)
        except FileExistsError:
            return False
        return True
    else:
        return False


def get_path() -> str:
    return os.getcwd()
