import pathlib
import os

sep = str(os.path.sep)
this_path = str(pathlib.Path().absolute()) + sep
distr_path = this_path + 'distr' + sep

def replace_sep(path):
    return path.replace('/', sep)

def new_docker_command(extra_path=None): 
    command = []
    command.append('docker')
    command.append('run')
    command.append('--rm')
    command.append('-v')

    if extra_path != None:
        current_distr_path = this_path + extra_path
        current_distr_path = current_distr_path.replace('/', sep)
    else:
        current_distr_path = distr_path

    command.append(current_distr_path + ':/out_files')
    return command