from contextlib import ContextDecorator
import datetime, time

class LogFile(ContextDecorator):

    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        self.start_date = datetime.datetime.now()
        self.start_perf_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        run = datetime.timedelta(seconds=time.perf_counter() - self.start_perf_time)
        context = f"Start: {self.start_date} | Run: {run} | An error occurred: {exc_val}\n"
        with open(self.filename, "a") as f:
            f.write(context)

        return False


