import file_helper
from mainline import *

def main():
    folder_path = file_helper.create_folder()
    file_helper.save_parameters(folder_path)
    record_save_file = f"{folder_path}/{folder_path.split('/')[-1]}.xlsx"
    data_path = config.seed_table

    if config.use_instruction_gradient:
        instruction_gradient(data_path, record_save_file)
    elif config.use_response_gradient:
        response_gradient(data_path, record_save_file)

if __name__ == "__main__":
    main()