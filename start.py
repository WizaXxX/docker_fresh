import subprocess
import os
import modules.helper as helper

host_name = 'test.1cfresh.dev'
configurations = {}


docker_run_str = 'docker run --rm -v ' + helper.this_path + ':/out_files alpine'
docker_compose_str = 'docker-compose -f workdir/docker-compose.yml '

work_dir = '/out_files/workdir/'
work_dir_other = work_dir + 'mnt/other-files/'
local_work_dir = helper.replace_sep(helper.this_path + '/workdir/')

def call(command, remote=True, debug=True):
    commands = []

    if remote:
        commands.append(docker_run_str)
    commands.append(command)
    if debug:
        print(' '.join(commands))
    subprocess.call(' '.join(commands), shell=True)

def get_configurations_data():
    # r=root, d=directories, files = files
    for r, d, files in os.walk(helper.replace_sep(local_work_dir + '/mnt')):
        for file in files:
            conf_key = file.split('.')[0].split('_')[0]
            configurations[conf_key] = '.'.join(file.split('.')[0].split('_')).replace(conf_key + '.', '')

new_server = False

new_server = os.path.isfile('workdir') != True

# if new_server:
    # call('mkdir ' + work_dir)
    # call('mkdir ' + work_dir + 'mnt')
    # call('sh -c "cp /out_files/distr/*.cf ' + work_dir + 'mnt/"')
    # get_configurations_data()

# renew docker-compose.yml
call('cp /out_files/docker-compose.yml /out_files/workdir/docker-compose.yml')
call('sh -c "sed -i \'s/HOSTNAMEREPLACE/' + host_name + '/\' ' + work_dir + '/*.yml"')
call(docker_compose_str + 'down', False)

# renew all nginx conf files
call('rm -rf ' + work_dir + 'nginx_conf/')
call('cp -r /out_files/images/nginx/conf/ ' + work_dir + 'nginx_conf/')

# renew other-files
call('rm -rf ' + work_dir_other)
call('cp -r /out_files/other_files/ ' + work_dir_other)
call('sh -c "sed -i \'s/HOSTNAMEREPLACE/' + host_name + '/\' ' + work_dir_other + 'vrd/*.vrd"')
call('sh -c "sed -i \'s/HOSTNAMEREPLACE/' + host_name + '/\' ' + work_dir_other + 'cfe/params.json"')

# start db srv ras web gate
call(docker_compose_str + 'up -d db srv ras web gate', remote=False)



