import modules.helper as helper

def delete_site_dir():
    command = helper.new_docker_command('images/site/distr')
    command.append('alpine')
    command.append('rm')
    command.append('-rf')
    command.append('/out_files/site')
    return command

def unzip_site_dir():
    command = helper.new_docker_command()
    command.append('-v')
    command.append(helper.this_path + helper.replace_sep('images/site') + ':/main_dir')
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
    command.append('"mv /out_files/site/*.war /out_files/site/ROOT.war"')
    return command

def add_all_before_commands():
    commands = []
    commands.append(unzip_site_dir())
    commands.append(rename_site_file())
    return commands

def add_all_after_commands():
    commands = []
    commands.append(delete_site_dir())
    return commands

class New():

    name = ''
    commands_before = []
    commands_after = []

    def __init__(self):
        self.name = 'site'
        self.commands_before = add_all_before_commands()
        self.commands_after = add_all_after_commands()