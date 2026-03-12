import logging
import json
import re
from datetime import datetime
import os


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
            if message.lower() in entry["message"].lower():
                log = self.dict_to_log(entry)
                matches.append(log)
        if matches:
            print(f"""Log entries including: "{message}": 
                """)
            for log in matches:
                print(log)
        else:
            print(f"""No entries were found including the message:
"{message}" 
""")


    #Parses entries by logger
    def parse_by_logger(self, logger_name):
        matches = []
        for entry in self.log_data:
            if entry["name"] == logger_name:
                log = self.dict_to_log(entry)
                matches.append(log)
        if matches:
            print(f"""Log entries from: "{logger_name}" Logger:
                """)
            for match in matches:
                print(match)
        else:
            print(f"""No entries were found from "{logger_name}" Logger.
                  """)
    

    #Parses entries by level
    def parse_by_level(self, level):
        matches = []
        for entry in self.log_data:
            if entry["level"] == level.upper():
                log = self.dict_to_log(entry)
                matches.append(log)
        if matches:
            print(f"""Log entries from "{level}"" Level :
                """)
            for match in matches:
                print(match)
        else:
            print(f"No entries were found with Level {level}")


    #Parses entries by time
    def parse_by_time(self):
        matches = []

        print("""Parse logs by time using specific date or time:
Instructions:
1- The program will take one or two values. If it receives just one it will return
all logs that have that specific date or time. If it receives two it will return 
all logs between those timestamps. 
              
2- To enter just one value press "Enter" when asked to enter the second value.
              
3- To show all logs from from before or after a specific date, enter the number "0" 
as the other value:
              
Example 1:
First value: 0 
Second value: 2026/02/12
Will return all logs before 2026/02/12
              
Example 1:
First value: 2026/02/12
Second value: 0
Will return all logs after 2026/02/12

The format will be:
              
"YYYY-MM-DD"  for the date
"H:M:S,-03-11F"     for the hour
              
              
""")
        print("""Enter the first value""")
        date1 = input("Date: ")
        if date1 == "":
            clear_screen()
            print("""No data was entered
...
Exiting the program>>>""")
            return 0

        time1 = input("Time: ")
        timestamp1_str = f"{date1} {time1}"
        log1_time = datetime.strptime(timestamp1_str, "%Y-%m-%d %H:%M:%S,%f")


        print("""Enter the second value or press enter to return logs matching value 1""")
        date2 = input("Date: ")
        if date2 == "":
            for entry in self.log_data:
                if datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S,%f") == log1_time:
                    log = self.dict_to_log(entry)
                    matches.append(log)
            if matches:
                print(f"""Log entries from "{timestamp1_str}":
                    """)
                for match in matches:
                    print(match)
            else:
                print(f"No entries were found with {timestamp1_str} Timestamp")
            return 0

        time2 = input("Time: ")


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_datetimne_format(string):
    pass


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
    logger.error("Error level log with critical lowecase in text")
    logger.critical("Critical level log -- to test hyphens")



def main():

    #Cleaning the log file before each test
    with open(log_file, 'w') as f:
        f.write("")
    test_logger_levels()
    my_parser = LogParser(log_file)
    my_parser.parse_by_time()


if __name__ == '__main__':
    main()