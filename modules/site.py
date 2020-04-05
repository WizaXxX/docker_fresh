import subprocess
import pathlib
import os
import modules.helper as helper

def add_site_dir(command):
    command.append('-v')
    command.append(helper.this_path + helper.replace_sep('images/site') + ':/main_dir')

def delete_site_dir():
    command = helper.new_docker_command('images/site/distr')
    command.append('alpine')
    command.append('rm')
    command.append('-rf')
    command.append('/out_files/site')

    return command

def unzip_site_dir():
    command = helper.new_docker_command()
    add_site_dir(command)
    command.append('kubeless/unzip')
    command.append('unzip')
    command.append('/out_files/site_*.zip')
    command.append('-d')
    command.append('/main_dir/distr/site')
    
    return command

def rename_site_file():
    command = helper.new_docker_command('images/site/distr')
    command.append('alpine')
    command.append('sh')
    command.append('-c')
    command.append('"mv /out_files/site/site*.war /out_files/site/ROOT.war"')

    return command

def add_all_commands():

    commands = []
    commands.append(delete_site_dir())
    commands.append(unzip_site_dir())
    commands.append(rename_site_file())

    return commands

class New():

    name = ''
    commands = []

    def __init__(self):
        self.name = 'site'
        self.commands = add_all_commands()