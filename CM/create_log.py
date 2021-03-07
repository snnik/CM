import os
import datetime


def create_log(file_name='CM'):
    file_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_extention = '.log'
    file_name = file_name + '_' + datetime.datetime.today().strftime('%Y%m%d') + file_extention
    file_full_directory = file_dir + 'log/' + file_name
    try:
        file_handler = open(file_full_directory)
    except IOError:
        file_handler = open(file_full_directory, 'w')
    file_handler.close()
    return file_full_directory


