"""Module which is used to recover and structure the corrected data in csv files by usinng pandas package"""
import os
import pandas as pd
import json



class XlsxClass:
    """
        XlsxClass performs the xlsx read and write operations.
        1. read ==> Method to read the .xls file
        2. write ==> Method to create or write the .xls file
    """

    def read(self, folder_path, files):    
        """
            This method performs the read operation of xlsx file
            folder_path (string) ==> folder name of the files present which is to read.
            files (string) ==> file names to read
        """    
        combined_data = pd.DataFrame()
        for csv_file in files:
            file_path = os.path.join(folder_path, csv_file)
            df = pd.read_csv(file_path, delimiter=";", skiprows=lambda x: '--' in str(x))
            combined_data = pd.concat([combined_data, df], ignore_index=True)
        return combined_data
    
    def write(self, folder_path, filename, file_dataframe):
        """
            This method performs the create or write operation of xlsx file
            folder_path (string) ==> folder name of the files present where the files need to be create or write.
            files (string) ==> file names need to create or write
            file_dataframe (list) ==> list of cleaned datas need to written in the ouput file
        """  
        file_path = os.path.join(folder_path, filename)
        file_dataframe.to_excel(file_path, index=False)
        return True

        
class JSONClass:
    """ To perform JSON operations"""

    def read_json(self, filename):
        """
            This method performs the read operation of json file
            filename (string) ==> configuration file name
        """  
        config_path = os.path.join(os.getcwd(), filename)
        try:
            with open(config_path, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            print(f"File does not exists in the path {config_path}")
        

class ParserClass(JSONClass, XlsxClass):
    """
        To perform validations and clean up of the datas from the corruupted files
    """

    def __init__(self):
        self.cwd = os.getcwd()
        self.config_file = "config.json"
        self.get_config()
        self.header_string = False
    
    def get_config(self):
        """
            To get the input details from the configuration file and update the variables
        """
        config_data = super().read_json(self.config_file)
        self.corrupted_folder = config_data.get("corrupted_folder", False)
        self.cleaned_folder = config_data.get("cleaned_folder", False)
        self.files_only = config_data.get("files_only", False)
        self.output_filename = config_data.get("output_filename", False)
    
    def validate(self, data):
        """
            Performing validation and forms the list values into the string after cleanup
            data (str) ==> value to be cleaned up
        """
        is_valid = False
        final_string = ';'.join(list(map(lambda x: x.strip().replace("-", ""), data.split("|"))))[1:]
        if data.count("*") > 1:
            is_valid = True
        elif 'Stat' in data and not self.header_string:
            self.header_string  = final_string
        if is_valid:
            return {self.header_string: final_string}
        return False

    def parse_data(self):
        """
            Performing end to end parsing operation and creating or updating the output file with cleaned data
        """
        file_list = os.listdir(self.corrupted_folder)
        files = [file for file in file_list if file.endswith(self.files_only)]
        cleaned_dataframe = pd.DataFrame()
        if len(files) > 0:
            dataframe = super().read(self.corrupted_folder, files)
            cleaned_values = []
            for index, row in dataframe.iterrows():
                is_valid = False
                validated_data = self.validate(row[0])
                if validated_data:
                    cleaned_values.append(validated_data)
        cleaned_dataframe = pd.DataFrame(cleaned_values)
        response = super().write(self.cleaned_folder, self.output_filename, cleaned_dataframe)
        if response:
            print (f"Data cleaning is completed successfully..!. Please check the file name for clean data {self.output_filename}")
            return True
        else:
            print (f"Data cleaning process interrupted..")
            return False

if __name__ == "__main__":
    parser = ParserClass()
    parser.parse_data()

