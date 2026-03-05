import logging
import json

json_file = "json_file.json"

def read_json_file():
    filename = "json_file.json"
    try:
        with open (filename, "r") as file:
            data = json.load(file)
            logger.info(f"Data was loaded: {data}")
    except FileNotFoundError as e:
        logger.error(f"File nowt found error: {e}")



#Create the logger
logger = logging.getLogger("MyLogger")
logger.setLevel(logging.INFO)

#Adding Handler and Formatter
handler = logging.FileHandler("test.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


#Function to test logger on all levels
def test_logger_levels():
    logger.info("Info level log")
    logger.debug("Debug level log")
    logger.warning("Warning level log")
    logger.error("Error level log")
    logger.critical("Critical level log")


#Creating a class to parse logs
class Parser():
        
    def __init__(self, log_file):
        self.log_file = log_file
        self.log_data = self.return_logs()
        print(f"{self.log_data}, {log_file}")
    
    def return_logs(self):
        logs = []
        with open(self.log_file, "r") as file:
            line = file.readline()
            while line:
                log = json.loads(line)
                for info in log.keys():
                    print(info, log.keys)

log_file = "test.log"

def main():
    my_parser = Parser(log_file)
    my_parser.return_logs()


if __name__ == '__main__':
    main()