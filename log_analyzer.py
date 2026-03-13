import logging
import json
import re
from datetime import datetime
import os
from time import sleep

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
                    "timestamp":datetime.strptime(line[0].strip(), "%Y-%m-%d %H:%M:%S,%f"),
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
    

    #Handles entering the datetime data, validates and turns it into datetime <obj>
    def enter_time_data(self):
        date_is_valid = False
        while not date_is_valid:
            print("""Enter the date using the following format: YYYY:MM:DD\nor\nPress"Enter" to exit""")
            date_str = input("\nDate: ")
            if date_str == "":
                self.exit_animation()
                return 0
            else:
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                    date_is_valid = True
                except:
                    print("""The date format is not valid, please try again\nor\nPress"Enter" to exit""")
                    sleep(3)
                    clear_screen()
        
        time_is_valid = False
        while not time_is_valid:
            print("""Enter the date using the following format: HH:MM:SS\nor\nPress"Enter" to exit""")
            time_str = input("\nTime: ")
            if time_str == "":
                self.exit_animation()
                return 0
            else:
                try:
                    time = datetime.strptime(time_str, "%H:%M:%S")
                    time_is_valid = True
                except:
                    print("The date format is not valid")
                
        timestamp_str = f"{date_str} {time_str}"

        log_time = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        return log_time
    

    #Creates an animation that signals the porogram is closing
    def exit_animation(self):
        for i in range(1,4):
            clear_screen()
            set = ">"
            print(f"""Exiting the program\n{set*i}""")
            sleep(1)


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


    #Parses entries by date and time
    def parse_by_time(self):
        matches = []
        clear_screen()
        print("""Parse logs by time using specific date or time:
Options:

1- Show logs from an specific timestamp:
2- Show logs before or after a certain timestamp
3- Show logs between two timestamps

The format will be:
              
"YYYY-MM-DD"--->for the Date
"H:M:S"------>for the Time
              
""")    
        #Menu that lets the user choose how to parse by datetime
        option = 0
        while not option:
            try:
                option = int(input("Choose one option: "))
                if option > 3 or option < 1:
                    option = 0
                    raise SyntaxError
            except:
                clear_screen()
                print("""Choose one number between 1 and 3 for the following options:
                      
1- Show logs from an specific timestamp:
2- Show logs before or after a certain timestamp
3- Show logs between two timestamps""")
                option = 0


        #Matches logs with specific timestamp
        if option == 1:
            timestamp = self.enter_time_data()

            for entry in self.log_data:
                entry_time = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
                if entry_time == timestamp:
                    matches.append(entry)
            print(f"""Logs with timestamp {timestamp}:\n""")
        

        #Matches logs after or before the entered timestamp
        if option == 2:
            clear_screen()
            timestamp = self.enter_time_data()
            if not timestamp:
                return 0
                
            after_before = 0
            while not after_before:
                clear_screen()
                try:
                    after_before = int(input("Would you like to see entries before or after the timestamp you entered?\nChoose one option:\n\n1- Before\n2- After\n\n>>>"))
                except:
                    after_before = 0
                if after_before < 0 or after_before > 2:
                    after_before = 0

            if after_before == 1:
                after_before_str = "before"
                for entry in self.log_data:
                    entry_time = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
                    if entry_time < timestamp:
                        matches.append(entry)

            if after_before == 2:
                after_before_str = "after"
                for entry in self.log_data:
                    entry_time = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
                    if entry_time > timestamp:
                        matches.append(entry)

            print(f"""Logs {after_before_str} {timestamp}:\n""")
            

        #Matches logs between two timestamps
        if option == 3:
            clear_screen()
            print("Enter the first timestamp")
            timestamp1 = self.enter_time_data()

            clear_screen()
            print("Enter the second timestamp")
            timestamp2 = self.enter_time_data()
            
            first_less_than_second = timestamp1 < timestamp2

            if first_less_than_second:
                for log in self.log_data:
                    print(type(log["timestamp"]), type(timestamp1))
                    if log["timestamp"] > timestamp1 and log["timestamp"] < timestamp2:
                        matches.append(log)
            else:
                for log in self.log_data:
                    if log["timestamp"] < timestamp1 and log["timestamp"] > timestamp2:
                        matches.append(log)


        if matches:
            for match in matches:
                match = self.dict_to_log(match)
                print(match)
        else:
            clear_screen()
            print("No logs matched your search.")



def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


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