import modules.helper as helper

def download_postgresql_connector():
    command = helper.new_docker_command()
    command.append('alpine')
    command.append('wget')
    command.append('-O')
    command.append('/out_files/postgresql.jar')
    command.append('https://jdbc.postgresql.org/download/postgresql-42.2.4.jar')

    return command

def add_all_commands():

    commands = []
    commands.append(download_postgresql_connector())

    return commands

class New():

    name = ''
    commands = []

    def __init__(self):
        self.name = 'centos'
        self.commands = add_all_commands()