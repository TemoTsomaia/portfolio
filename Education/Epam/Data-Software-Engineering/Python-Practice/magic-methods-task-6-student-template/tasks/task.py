import os


class Cd:

    def __init__(self, given_path):
        self.given_path = given_path


    def __enter__(self):
        self.previous_dir = os.getcwd()
        if os.path.isdir(self.given_path):
            os.chdir(self.given_path)
        else:
            raise ValueError(f'{self.given_path} is not a directory')

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.previous_dir)
