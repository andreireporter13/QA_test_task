#
#
#
#
# My name is Andrei Cojocaru, self-taught programmer
# Knowlegde - Python, Linux, Bash, SQL, WEB;
#
import os  # -> work with files
import shutil
import time


def return_list_dir(path):
    """
    This func() return all links from folders.
    DRY.
    """

    return os.listdir(path)


def get_list_f_replica(path) -> list:
    """
    This func() return a list of links with files from replica.
    """

    lst_replica = []
    for data in return_list_dir(path):
        lst_replica.append(data)

    return lst_replica


def get_list_f_source(path) -> list:
    """
    Get list of links with files from source.
    """

    lst_source = []
    for data in return_list_dir(path):
        lst_source.append(data)

    return lst_source


def main(source_folder: str, replica_folder: str) -> None:
    """
    All logic of code is here. Only os library.
    """

    # folders and files!
    lst_from_replica = set(get_list_f_replica(replica_folder))
    lst_from_source = set(get_list_f_source(source_folder))

    # check if backup:
    for data in lst_from_source:
        if data not in lst_from_replica:
            item_path = os.path.join(source_folder, data)
            if os.path.isfile(item_path):
                # item este un fișier
                shutil.copy2(item_path, replica_folder)
            elif os.path.isdir(item_path):
                # item este un director
                shutil.copytree(item_path, os.path.join(replica_folder, data))

            # write changes to log!
            with open('logs.md', 'a') as file_data:
                file_data.write(f'{data} moved to backup\n')

            # print to console
            print(f'{data} data moved to backup')

    # remove from backup
    for data_b in lst_from_replica:

        if data_b not in lst_from_source:
            abs_path_data_b = os.path.join(replica_folder, data_b)

            if os.path.isdir(abs_path_data_b):
                shutil.rmtree(abs_path_data_b)
            elif os.path.isfile(abs_path_data_b):
                os.remove(abs_path_data_b)

            # write changes to log!
            with open('logs.md', 'a') as remove_file:
                remove_file.write(f'{data_b} removed from backup!\n')

            print(f'{data_b} was deleted from backup!')


if __name__ == "__main__":

    source_folder = input('Insert your source active folder: ')
    replica_folder = input('Insert your replica backup folder: ')

    # interval
    set_interval = int(input('Set synchronization interval in min: '))

    # main function
    while True:

        # run script
        main(source_folder, replica_folder)

        time.sleep(set_interval)
