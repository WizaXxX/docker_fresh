import modules.helper as helper

def copy_distrib_file():
    command = helper.new_docker_command()
    command.append('-v')
    command.append(helper.this_path + helper.replace_sep('images/gate') + ':/main_dir')
    command.append('alpine')
    command.append('sh -c')
    command.append('"cp /out_files/appgate*.deb /main_dir/distr/appgate.deb"')
    return command

def delete_distrib_file():
    command = helper.new_docker_command('images/gate/distr')
    command.append('alpine')
    command.append('sh -c "rm -rf /out_files/*.deb"')
    return command

def add_all_before_commands():
    commands = []
    commands.append(copy_distrib_file())
    return commands

def add_all_after_commands():
    commands = []
    commands.append(delete_distrib_file())
    return commands

class New():

    name = ''
    commands_before = []
    commands_after = []

    def __init__(self):
        self.name = 'gate'
        self.commands_before = add_all_before_commands()
        self.commands_after = add_all_after_commands()