import modules.helper as helper

def download_onescript():
    command = helper.new_docker_command('images/core/distr/')
    command.append('alpine')
    command.append('wget')
    command.append('-O')
    command.append('/out_files/onescript.rpm')
    command.append('http://oscript.io/downloads/1_1_1/onescript-engine-1.1.1-1.fc26.noarch.rpm')

    return command

def unzip_platform_distr():
    command = helper.new_docker_command()
    command.append('-v')
    command.append(helper.this_path + helper.replace_sep('images/core') + ':/main_dir')
    command.append('alpine')
    command.append('sh')
    command.append('/main_dir/get_platform.sh')

    return command


def add_all_before_commands():
    commands = []
    commands.append(download_onescript())
    commands.append(unzip_platform_distr())

    return commands

def delete_core_distr_files():
    command = helper.new_docker_command('images/core/distr/')
    command.append('alpine')
    command.append('sh -c "rm -rf /out_files/*.rpm"')

    return command

def delete_license_tools_files():
    command = helper.new_docker_command('images/core/distr/')
    command.append('alpine')
    command.append('sh -c "rm -rf /out_files/license-tools"')

    return command

def add_all_after_commands():
    commands = []
    commands.append(delete_core_distr_files())
    commands.append(delete_license_tools_files())

    return commands

class New():

    name = ''
    commands_before = []
    commands_after = []

    def __init__(self):
        self.name = 'core'
        self.commands_before = add_all_before_commands()
        self.commands_after = add_all_after_commands()