import logging
import json
from datetime import datetime


#Defining a JSON formatter which inherits from the logging.Formatter class
class JSONFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()

    #record is defined in the parent class and is where we get out data from
    def format(self, record):
        now = datetime.now()
        log_record = [{
            "time": now.isoformat(),
            "level": record.levelname,
            "msg": record.getMessage(),
        }]
        obj =  json.dumps(log_record, ensure_ascii=False)
        print(type(obj))
        return obj

class JSONParser():
        
    def __init__(self, log_file):
        self.log_file = log_file
        self.log_data = self.return_logs()
    
    def return_logs(self):
        print("in return logs function")
        logs = []
        with open(self.log_file, "r") as file:
            for line in file.readlines():
                logs.append(line)
                print(f"{line} was added to ''logs")
        return logs

log_file = "test.log"

#Create the logger
logger = logging.getLogger("MyLogger")
logger.setLevel(logging.INFO)

#Adding Handler and Formatter
handler = logging.FileHandler(log_file)
formatter = JSONFormatter()
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
    my_parser = JSONParser(log_file)
    test_logger_levels()
    my_parser.return_logs()


if __name__ == '__main__':
    main()