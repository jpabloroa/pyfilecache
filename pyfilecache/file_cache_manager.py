import os
import hashlib
import time
from datetime import datetime, timedelta

class FileCacheManager:
    def __init__(self, file_path, signature_algo='sha256', log_mode='print', log_file=None, interval=timedelta(days=1), remove_old_cache=False):
        self.__file_path = file_path
        self.__directory = os.path.join(os.path.dirname(file_path), f'{os.path.basename(file_path).split(".")[0]}_cache')
        self.__signature_algo = signature_algo
        self.__log_mode = log_mode
        self.__log_file = log_file
        self.__interval = interval if callable(interval) else lambda: datetime.now() + interval

        if not os.path.exists(self.__directory):
            os.makedirs(self.__directory)

        if remove_old_cache:
            self.delete_cache()

    def __generate_signature(self, data: bytes) -> str:
        """Generates a hash signature for the given data."""
        return hashlib.new(self.__signature_algo, data).hexdigest()

    def __get_file_name(self, signature: str) -> str:
        """Generates a cache file name based on the timestamp and signature."""
        timestamp = int(time.time())
        return f"tmp_{timestamp}_{signature}.{self.__get_extension()}"

    def __get_file_path(self, signature: str) -> str:
        """Generates the full cache file path."""
        return os.path.join(self.__directory, self.__get_file_name(signature))

    def __get_extension(self) -> str:
        """Extracts the file extension from the file path."""
        return os.path.splitext(self.__file_path)[1][1:]

    def __print(self, message: str):
        """Handles output based on the log_mode."""
        if self.__log_mode == 'print':
            print(message)
        elif self.__log_mode == 'log' and self.__log_file:
            with open(self.__log_file, 'a') as log:
                log.write(message + '\n')

    def __check_data_change(self, signature: str) -> bool:
        """Checks if the data has changed based on the signature and interval."""
        for file in os.listdir(self.__directory):
            if signature in file:
                timestamp_str = file.split('_')[1]
                file_timestamp = datetime.fromtimestamp(int(timestamp_str))
                if self.__interval() > datetime.now():
                    return False
        return True

    def __delete(self, file_path: str):
        """Deletes a file."""
        if os.path.exists(file_path):
            os.remove(file_path)
            self.__print(f"{file_path} has been deleted.")
        else:
            self.__print(f"{file_path} does not exist.")

    def write(self, data: bytes, force: bool = False):
        """Writes the data to a cache file if it has changed or if force is True."""
        signature = self.__generate_signature(data)
        file_path = self.__get_file_path(signature)
        
        if force or self.__check_data_change(signature):
            with open(file_path, 'wb') as file:
                file.write(data)
            self.__print(f"Data saved to {file_path}.")
        else:
            self.__print("Data has not changed or interval not reached. Skipping file write.")

    def read(self, cache_file: str) -> bytes:
        """Reads the data from a cache file."""
        with open(cache_file, 'rb') as file:
            return file.read()

    def delete_cache(self):
        """Deletes all cached files."""
        for file in os.listdir(self.__directory):
            self.__delete(os.path.join(self.__directory, file))
        self.__print(f"All cache files in {self.__directory} have been deleted.")

    def get_cache_size(self) -> float:
        """Returns the size of all cache files in kilobytes."""
        total_size = 0
        for file in os.listdir(self.__directory):
            total_size += os.path.getsize(os.path.join(self.__directory, file))
        return total_size / 1024  # Convert to kilobytes

    def get_file_creation_date(self, file_path: str) -> float:
        """Returns the creation date of a cache file as a timestamp."""
        return os.path.getctime(file_path)

    def get_signature_algorithm(self) -> str:
        """Returns the signature algorithm used."""
        return self.__signature_algo

    def set_interval(self, interval):
        """Sets the interval for cache overwriting."""
        self.__interval = interval if callable(interval) else lambda: datetime.now() + interval

    def set_interval_5_minutes(self):
        """Sets the interval to 5 minutes."""
        self.set_interval(timedelta(minutes=5))

    def set_interval_10_minutes(self):
        """Sets the interval to 10 minutes."""
        self.set_interval(timedelta(minutes=10))

    def set_interval_30_minutes(self):
        """Sets the interval to 30 minutes."""
        self.set_interval(timedelta(minutes=30))

    def set_interval_1_hour(self):
        """Sets the interval to 1 hour."""
        self.set_interval(timedelta(hours=1))

    def set_interval_6_hours(self):
        """Sets the interval to 6 hours."""
        self.set_interval(timedelta(hours=6))

    def set_interval_12_hours(self):
        """Sets the interval to 12 hours."""
        self.set_interval(timedelta(hours=12))

    def set_interval_24_hours(self):
        """Sets the interval to 24 hours."""
        self.set_interval(timedelta(hours=24))

    def set_interval_next_day_at_8am(self):
        """Sets the interval to the next day at 8 am."""
        next_day = datetime.now() + timedelta(days=1)
        self.set_interval(lambda: next_day.replace(hour=8, minute=0, second=0, microsecond=0))

    def set_interval_next_monday(self):
        """Sets the interval to the next Monday."""
        today = datetime.now()
        next_monday = today + timedelta((7-today.weekday()) % 7)
        self.set_interval(lambda: next_monday.replace(hour=0, minute=0, second=0, microsecond=0))

    def set_interval_first_day_of_month(self):
        """Sets the interval to the first day of the next month."""
        today = datetime.now()
        next_month = today.replace(day=28) + timedelta(days=4)
        first_day_next_month = next_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        self.set_interval(lambda: first_day_next_month)

    def set_interval_first_day_of_year(self):
        """Sets the interval to the first day of the next year."""
        today = datetime.now()
        first_day_next_year = datetime(today.year + 1, 1, 1, 0, 0, 0)
        self.set_interval(lambda: first_day_next_year)
