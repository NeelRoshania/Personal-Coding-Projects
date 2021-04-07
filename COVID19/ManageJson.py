class ManageJsonFile():

    # Simple class helper to download and update a json file

    # library dependencies
    from datetime import datetime
    import json
    import re

    # setup global class variables
    def __init__(self):
        self.load_status   = False
        self.update_status = False
        pass
    
    # load json from location
    def load_json(self, file_name):

        self.file_name = file_name

        # read current file
        try:
            with open(self.file_name) as f:
                self.json_data = self.json.load(f)

            self.load_status = True
            # print("{} - {} found".format(self.datetime.now(), self.file_name))
            
            return self.json_data

        except:
            self.load_status = False
            print("\n**{} - {} not found".format(self.datetime.now(), self.file_name))
            return None

    # update json file
    def update_json(self, json_data, ignore_keys):

        # ignore_keys requires list of keys to ignore

        # read the current file and update before updating new key value paits
        try:
            with open(self.file_name) as f:
                self.current_json = self.json.load(f)

        except:
            return print("\n**{} - {} not found".format(self.datetime.now(), self.file_name))
        
        # ignore keys by overwriting what is read and what is updated
        for ignore_key in ignore_keys:
            json_data[ignore_key] = self.current_json[ignore_key]

            # temp_json                          = self.load_json(self.file_name)
            # json_data["meta"]["keep_updating"] = temp_json["meta"]["keep_updating"]
            # json_data["meta"]["kill_process"] = temp_json["meta"]["kill_process"]

        # dump to file location
        try:
            with open(self.file_name, 'w') as outfile:
                self.json.dump(json_data, outfile, indent=4, sort_keys=True)
            
            self.update_status = True
            # print("{} - json data updated at {}".format(self.datetime.now(), self.file_name))

            # read json_data again
            return self.load_json(self.file_name)

        except:
            self.update_status = False
            print("\n**{} - {} failed to update".format(self.datetime.now(), self.file_name))
            return None

    # get status of load and update
    def get_status(self):
        return {
            "load_status"   : self.load_status,
            "update_status" : self.update_status
        }

# # # implementation
# MJ = ManageJsonFile()

# # get json data
# previous_batch_data = MJ.load_json("meta/previous_batch_meta.json")
# # print(previous_batch_data)

# # update json data
# previous_batch_data["meta"]["kill_process"] = "Neel is the man"
# previous_batch_data = MJ.update_json(previous_batch_data)

# print(previous_batch_data.keys())