import pathlib2
import time
import shutil
import os
import re
import unidecode


class FileHelper:

    time_keys = {
        "ctime": os.path.getctime,
        "mtime": os.path.getmtime,
        "atime": os.path.getatime
    }

    def __init__(self, target_path: str = ""):
        self.target_path = target_path
        self.target_path_os = pathlib2.Path(target_path)

    def get_oldest(self, search_param: str = "*", *, time_criteria: str = "ctime") -> pathlib2.Path:
        """
        Get the oldest file found according to the search parameters.
        """

        # Input validation
        # ==================================================

        if not self.target_path_os.is_dir():
            raise InvalidInput("Input 'target_path' needs to be a dir.",
                               type(self.target_path),
                               self.target_path)

        time_c = self.time_keys.get(time_criteria, None)
        if time_c is None:
            raise InvalidInput("Input 'time_criteria' isn't valid.",
                               type(time_criteria),
                               time_criteria)

        # File searching
        # ==================================================

        all_files = [path for path in self.target_path_os.glob(search_param) if path.is_file()]
        try:
            return min(all_files, key=time_c)
        except ValueError:
            raise NoFileFound("No file found according to search parameters.")

    def move_to(self, new_path: str = "") -> str:
        """
        Move a folder or file to a given directory, both target_path and
        target_path_os are updated to the new path.
        """

        # File manipulation
        # ==================================================

        new_path_os = pathlib2.Path(new_path)
        is_file = self.target_path_os.is_file()
        shutil.move(self.target_path, new_path)

        if is_file:
            self.target_path_os = new_path_os.joinpath(self.target_path_os.name)
            self.target_path = new_path
        else:
            self.target_path = new_path
            self.target_path_os = new_path_os

        return new_path

    @property
    def target_path(self):
        return self._target_path

    @target_path.setter
    def target_path(self, target_path):
        if not os.path.isfile(target_path) and not os.path.isdir(target_path):
            raise InvalidInput(f"Invalid input 'target_path' has to be dir or file", type(target_path), target_path)
        self._target_path = target_path


def string_normalizer(input_str, *, use_unicode=True, strip=True, lower=False, upper=False, **kwargs):

    if not isinstance(input_str, str):
        raise InvalidInput("Parameter 'input_str' has to be string.")

    if use_unicode:
        input_str = unidecode.unidecode(input_str)
    if strip:
        input_str = input_str.strip()
    if lower and not upper:
        input_str = input_str.lower()
    if upper and not lower:
        input_str = input_str.upper()
    if kwargs.get("remove_separation"):
        input_str = re.sub('[\|,-./_]+', '', input_str)
    if kwargs.get("remove_break_lines"):
        input_str = input_str.replace('\n', '')
    if kwargs.get("remove_digits") and not kwargs.get("only_digits"):
        input_str = re.sub('\d+', '', input_str)
    if kwargs.get("only_digits") and not kwargs.get("remove_digits"):
        input_str = re.sub('\d+', '', input_str)
    if kwargs.get("only_numbers"):
        input_str = re.sub('\D+', '', input_str)
    if kwargs.get("remove_spaces"):
        input_str = input_str.replace(' ', '')

    return input_str
        

class Timer:
    def __init__(self, duration=10):
        self.duration = float(duration)
        self.start = time.perf_counter()

    def reset(self):
        self.start = time.perf_counter()

    def explode(self):
        self.duration = 0

    def increment(self, increment=0):
        self.duration += increment

    @property
    def not_expired(self):
        if self.duration == -1:
            return True
        return False if time.perf_counter() - self.start > self.duration else True

    @property
    def expired(self):
        return not self.not_expired

    @property
    def at(self):
        return time.perf_counter() - self.start


class Error(Exception):
    """Base class for other exceptions"""
    pass


class InvalidInput(Exception):
    def __init__(self, message, received_type=None, received_value=None):
        self.message = message
        self.received_type = received_type
        self.received_value = received_value
        super().__init__(self.message)


class NoFileFound(Error):
    """Raised when no file is found"""
    pass