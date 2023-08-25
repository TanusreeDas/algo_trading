from pathlib import Path
from datetime import datetime

def generate_csv_file(file_name,file_content,column_name=None):

    destination_directory = Path("../data/csv")
    current_time = datetime.now().strftime('%d-%m-%Y')
    new_file_name = destination_directory / (file_name+'_'+current_time+'.csv')

    file_content.to_csv(new_file_name,header=column_name)


def main():
    generate_csv_file()

if __name__=="__main__":
    main()