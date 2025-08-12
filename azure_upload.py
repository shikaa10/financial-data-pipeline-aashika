from access_vault import service_client
from datetime import datetime
import os
import logging

def upload_file(container_name:str, local_file_path:str, destination_path:str):
     file_system_client = service_client.get_file_system_client(file_system=container_name)
     file_client = file_system_client.get_file_client(destination_path)

     with open(local_file_path, 'rb') as file:
          file_client.upload_data(file, overwrite=True)

def upload_folder(container_name:str, local_folder_path:str, destination_folder:str):
    file_system_client = service_client.get_file_system_client(file_system=container_name)

    for root, dirs, files in os.walk(local_folder_path):
        for file in files:
            if file == "_SUCCESS":
                continue
            local_file_path = os.path.join(root,file)
            relative_path = os.path.relpath(local_file_path, local_folder_path)
            destination_path =os.path.join(destination_folder, relative_path)

            file_client = file_system_client.get_file_client(destination_path)
            with open(local_file_path, 'rb') as f:
                file_client.upload_data(f, overwrite=True)

def main():
     logging.basicConfig(level=logging.INFO)
     current_date = datetime.now().strftime('%Y%m%d')

     raw_stocks_file = 'raw_stocks.csv'
     raw_stocks_destination = f'stocks/raw_stocks_{current_date}.csv'
    
     processed_stocks_folder = '/home/kris/Code/Financial-Data-Engineering-Pipeline/processed_stocks'
     destination_folder = f'stocks/parquet_{current_date}'

     try:
       upload_file('rawdata', raw_stocks_file, raw_stocks_destination)
       logging.info(f'Successfully uploaded {raw_stocks_file} to {raw_stocks_destination}')
       
       upload_folder('rawdata', processed_stocks_folder, destination_folder)
       logging.info(f'Successfully uploaded parquet folder to {destination_folder}')
      
     except Exception as e:
        logging.error(f"Uploading data failed {str(e)}")
        raise
    


if __name__ == "__main__":
    main()
