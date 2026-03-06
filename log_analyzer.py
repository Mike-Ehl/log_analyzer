import logging
import json
from datetime import datetime

json_file = "json_file.json"

def read_json_file():
    filename = "json_file.json"
    try:
        with open (filename, "r") as file:
            data = json.load(file)
            logger.info(f"Data was loaded: {data}")
    except FileNotFoundError as e:
        logger.error(f"File nowt found error: {e}")


#First we define the classes:
#Defining a JSON formatter which inherits from the logging.Formatter class
class JSONFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()

    #record is defined in the parent class and is where we get out data from
    def format(self, record):
        now = datetime.now()
        log_record = {
            "time": now.isoformat(),
            "level": record.levelname,
            "msg": record.getMessage(),
        }
        return json.dumps(log_record)


#Creating a LogParser class to parse logs
class LogParser():
        
    def __init__(self, log_file):
        print("Initializing Log Parser")
        self.log_file = log_file
        self.log_data = self.return_logs()
        print(f"{self.log_data}, {log_file}")
    
    def return_logs(self):
        logs = []
        with open(self.log_file, "r") as file:
            line = file.readline()
            while line:
                log = json.loads(line)
                logs.append(log)
        return logs


#Create the logger
logger = logging.getLogger("MyLogger")
logger.setLevel(logging.INFO)

#Adding Handler and Formatter
handler = logging.FileHandler("test.log")
formatter = logging.Formatter(JSONFormatter())
handler.setFormatter(formatter)
logger.addHandler(handler)


#Function to test logger on all levels
def test_logger_levels():
    logger.info("Info level log")
    logger.debug("Debug level log")
    logger.warning("Warning level log")
    logger.error("Error level log")
    logger.critical("Critical level log")




log_file = "test.log"


def main():
    my_parser = LogParser(log_file)
    test_logger_levels()
    my_parser.return_logs()


if __name__ == '__main__':
    main()