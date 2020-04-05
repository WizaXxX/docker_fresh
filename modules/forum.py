import modules.helper as helper

def add_forum_dir(command):
    command.append('-v')
    command.append(helper.this_path + helper.replace_sep('images/forum') + ':/main_dir')

def delete_forum_dir():
    command = helper.new_docker_command('images/forum/distr')
    command.append('alpine')
    command.append('sh')
    command.append('-c')
    command.append('"rm -rf /out_files/forum"')

    return command

def unzip_forum_dir():
    command = helper.new_docker_command()
    add_forum_dir(command)
    command.append('kubeless/unzip')
    command.append('unzip')
    command.append('/out_files/forum_*.zip')
    command.append('-d')
    command.append('/main_dir/distr/forum')
    
    return command

def rename_forum_file():
    command = helper.new_docker_command('images/forum/distr')
    command.append('alpine')
    command.append('sh')
    command.append('-c')
    command.append('"mv /out_files/forum/forum*.war /out_files/forum/ROOT.war"')

    return command

def add_all_before_commands():
    commands = []
    commands.append(unzip_forum_dir())
    commands.append(rename_forum_file())

    return commands

def add_all_after_commands():
    commands = []
    commands.append(delete_forum_dir())

    return commands

class New():

    name = ''
    commands_before = []
    commands_after = []

    def __init__(self):
        self.name = 'forum'
        self.commands_before = add_all_before_commands()
        self.commands_after = add_all_after_commands()