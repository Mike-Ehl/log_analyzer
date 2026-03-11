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
    
    #Returns the log data in a dictionary for easier handling
    def return_logs(self) -> dict:
        logs = []
        with open(self.log_file, "r", encoding="utf-8", errors="replace") as file:
            for line in file:
                line = re.split("--", line.strip())

                message = ""
                for string in line[3:]:
                    message += string
                dict = {
                    "timestamp":line[0].strip(),
                    "name": line[1].strip(),
                    "level": line[2].strip(),
                    "message": message
                }
                logs.append(dict)
                
        return logs
    
    #Turns a dict entry to a log (string)
    def dict_to_log(self, entry:dict) ->str:
        timestamp = entry["timestamp"]
        name = entry["name"]
        level = entry["level"]
        message = entry["message"]
        log = f"{timestamp} -- {name} -- {level} -- {message}"
        return log
    

    #Parses the entries by message
    def parse_by_message(self, message):
        matches = [] 
        for entry in self.log_data:
            if message in entry["message"]:
                log = self.dict_to_log(entry)
                matches.append(log)

        print(f"""Entries including: "{message}" """)
        for log in matches:
            print(log)

    #Parses entries by time
    def parse_by_time(self, time):
        pass

    #Parses entries by logger
    def parse_by_logger(self, logger):
        pass
    
    #Parses entries by level
    def parse_by_level(self, level):
        matches = []
        for entry in self.log_data:
            if entry["level"] == level:
                log = self.dict_to_log(entry)
                matches.append(log)

        print(f"{level} Level matches:")
        for match in matches:
            print(match)


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
    logger.error("Error level log with Critical in text")
    logger.critical("Critical level log -- to test hyphens")



def main():

    #Cleaning the log file before each test
    with open(log_file, 'w') as f:
        f.write("")
    test_logger_levels()

    my_parser = LogParser(log_file)
    my_parser.parse_by_level("ERROR")


if __name__ == '__main__':
    main()