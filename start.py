import subprocess
import os
import modules.helper as helper
import sys
from datetime import datetime

host_name = 'test.1cfresh.dev'
sup_password = '123Qwer'
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

def prepare_new_ib(key):
    print('creating', key)
    start_time = datetime.now()
    call(' '.join(helper.create_ib_command(host_name, key, configurations[key])), remote=False)
    print(key, 'creation', 'is fihish')
    print('duration:', datetime.now() - start_time)

    print('install control extension')
    #TODO


new_server = True

if len(sys.argv) > 1:
    new_server = sys.argv[1] == 'new'

call(docker_compose_str + 'down', False)

if new_server:
    call('rm -rf /out_files/workdir')
    call('mkdir -p ' + work_dir + 'mnt')
    call('sh -c "cp /out_files/distr/*.cf ' + work_dir + 'mnt/"')
    get_configurations_data()

# renew docker-compose.yml
call('cp /out_files/docker-compose.yml /out_files/workdir/docker-compose.yml')
call('sh -c "sed -i \'s/HOSTNAMEREPLACE/' + host_name + '/\' ' + work_dir + '/*.yml"')

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

# publish a services
call(' '.join(helper.web_publish_command(host_name, 'adm', False, 'zoneless', 'sm')), remote=False)
call(' '.join(helper.web_publish_command(host_name, 'smtl', False, 'withzone')), remote=False)
call(' '.join(helper.web_publish_command(host_name, 'sa', False, 'zoneless')), remote=False)
call(' '.join(helper.web_publish_command(host_name, 'openid', False, 'openid', 'sm')), remote=False)

# publish int services
call(' '.join(helper.web_publish_command(host_name, 'sm', True, 'zoneless')), remote=False)
call(' '.join(helper.web_publish_command(host_name, 'smtl', True, 'zoneless')), remote=False)
call(' '.join(helper.web_publish_command(host_name, 'sa', True, 'zoneless')), remote=False)
call(' '.join(helper.web_publish_command(host_name, 'am', True, 'zoneless')), remote=False)
call(' '.join(helper.web_publish_command(host_name, 'sc', True, 'sessioncontrol', 'sm;Usr=SessionControl;Pwd=' + sup_password)), remote=False)
call(' '.join(helper.web_publish_command(host_name, 'extreg', True, 'extreg', 'sm;Usr=ExtReg;Pwd=' + sup_password)), remote=False)

# restart Apache
call('docker exec web.' + host_name + ' chown -R usr1cv8:grp1cv8 /var/www', remote=False)
call('docker exec web.' + host_name + ' httpd -k graceful', remote=False)

if new_server:
    prepare_new_ib('smtl')
    



