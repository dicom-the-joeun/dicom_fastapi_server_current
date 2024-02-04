from ftplib import FTP
from io import BytesIO
import os

from dotenv import load_dotenv


load_dotenv("./app/.env")
FTP_SERVER = os.environ.get("FTP_SERVER")   # FTP Full path
FTP_USERNAME = os.environ.get("FTP_USERNAME")
FTP_PASSWORD = os.environ.get('FTP_PASSWORD')


class FTPConfig:
    def __init__(self):
        self.host = FTP_SERVER
        self.username = FTP_USERNAME
        self.password = FTP_PASSWORD
        self.ftp = FTP(host=self.host)

    def getFTP(self):
        return self.ftp

    def connect(self):
        try:
            self.ftp.connect()
            self.ftp.login(user=self.username, passwd=self.password)
            print(f"Connected to {self.host}")
        except Exception as e:
            print(f"FTP 연결 문제, {e}")

    def getdata(self, filepath, filename):
        file_data = BytesIO()
        self.ftp.cwd("/sts01/" + filepath)
        self.ftp.retrbinary(f'RETR {filename}', file_data.write)
        return file_data.getvalue()

    def disconnect(self):
        self.ftp.quit()
        print("Disconnected from FTP server")


