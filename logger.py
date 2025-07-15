import datetime
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
SSD_OUTPUT_FILE_PATH = os.path.join(OUTPUT_DIR, 'ssd_output.txt')


class Logger:
    def __init__(self):
        self.log_file_path = f'{OUTPUT_DIR}/log/ssd_log_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}.log'

    def log(self, message):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        full_message = f'[{timestamp}] {message}\n'
        with open(self.log_file_path, 'a', encoding='utf-8') as f:
            f.write(full_message)

    def info(self, message):
        self.log(f'INFO: {message}')

    def error(self, message):
        self.log(f'ERROR: {message}')
