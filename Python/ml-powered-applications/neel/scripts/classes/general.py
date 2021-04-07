import traceback
import yaml
import pandas as pd
import csv
from datetime import datetime
import io

class YAMLHandler():
    
    # dependencies
    
    # class to handle reading and writing yaml files to location
    
    def __init__(self):
        self.yml = {}
        pass
    
    def read(self, read_loc):
        
        # read_loc str
        
        self.read_loc = read_loc
        try:
            with open(read_loc, 'r') as stream:
                self.yml = yaml.safe_load(stream)
                return self.yml
        except:
            traceback.print_exc()
        pass

    def write(self, write_loc, data):
        
        # write_loc str
        # data json
        
        try:
            with io.open(write_loc, 'w', encoding='utf8') as outfile:
                yaml.dump(
                    data, 
                    outfile, 
                    default_flow_style=False, 
                    allow_unicode=True
                )
            print('- Data written to {}'.format(write_loc))

        except Exception as e:
            print(e)
        pass

    def get_yaml(self):
        return self.read(self.read_loc)

class LogToFile():

    # class object to log data to file
    # Data produced by these files should be available to view on a page

    def __init__(self, YAML_Handler=None):
        
        if YAML_Handler is not None:
            self.params_yaml = YAML_Handler.get_yaml()
        
        return None

    # create a new log csv file
    def create_csv(self, write_loc, cols):
        pd.DataFrame(columns=cols).to_csv(path_or_buf=write_loc, index=False)
        return None

    def log_csv(self, read_loc, log_message):
        
        # append log to file - https://docs.python.org/3/tutorial/inputoutput.html
        with open(read_loc, mode='a') as logfile:
            log_writer = csv.writer(logfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')
            log_writer.writerow([datetime.now(), '{}'.format(log_message)])

        print('- {}'.format(log_message))
        return None