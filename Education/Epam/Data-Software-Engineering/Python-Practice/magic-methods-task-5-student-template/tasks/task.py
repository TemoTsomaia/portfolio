import os
import shutil
import random
import tempfile

class TempDir:


    def __enter__(self):
        self.original_dir = os.getcwd()
        self.temp_path = tempfile.mkdtemp(
            prefix="my_temp_dir_",
            dir=self.original_dir
        )

        os.chdir(self.temp_path)
        return self.temp_path

    def __exit__(self, exc_type, exc_value, traceback):
        os.chdir(self.original_dir)
        shutil.rmtree(self.temp_path)

        if exc_type:
            # An exception occurred inside the 'with' block
            print(f"An error occurred: {exc_type.__name__}: {exc_value}")

        return False
