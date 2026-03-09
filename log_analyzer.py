import logging
import json
import re
from datetime import datetime


#First we define the classes:
#Creating a LogParser class to parse logs
class LogParser():

    def __init__(self, log_file):
        self.log_file = log_file
        self.log_data = self.return_logs()
    
    def return_logs(self):
        logs = []
        with open(self.log_file, "r", encoding="utf-8", errors="replace") as file:
            for line in file:
                line = re.split("--", line.strip())
                dict = {
                    "timestamp":line[0],
                    "name": line[1],
                    "level": line[2],
                    "message": line[3]
                }
                logs.append(dict)
                
        return logs
    
    def parse_by_message(self, message):
        matches = [] 
        for entry in self.log_data:
            if message in entry["message"]:
                matches.append(entry)
        print(f"""Entries including: "{message}" """)
        for entry in matches:
            print(entry)


log_file = "test.log"

#Create the logger
logger = logging.getLogger("MyLogger")
logger.setLevel(logging.INFO)

#Adding Handler and Formatter
handler = logging.FileHandler(log_file)
formatter = logging.Formatter("%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


#Function to test logger on all levels
def test_logger_levels():
    logger.info("Info level log")
    logger.debug("Debug level log")
    logger.warning("Warning level log")
    logger.error("Error level log")
    logger.critical("Critical level log")



def main():

    #Cleaning the log file before each test
    with open(log_file, 'w') as f:
        f.write("")
    test_logger_levels()

    my_parser = LogParser(log_file)
    my_parser.parse_by_message("Critical")


if __name__ == '__main__':
    main()