import subprocess
import os
import modules.helper as helper
import sys
from datetime import datetime

host_name = '.1cfresh.dev'
sup_password = '123Qwer'
new_server = False
global_debug = False
configurations = {}


docker_run_str = 'docker run --rm -v {}:/out_files alpine'.format(helper.this_path)
docker_compose_str = 'docker-compose -f workdir/docker-compose.yml '

work_dir = '/out_files/workdir/'
work_dir_other = work_dir + 'mnt/other-files/'
local_work_dir = helper.replace_sep(helper.this_path + '/workdir/')

def call(command, remote=True, debug=False, action='', measure_duration=False):
    commands = []

    if remote: commands.append(docker_run_str)
    commands.append(command)

    if action != '': print(action)
    if debug or global_debug: print(' '.join(commands))

    start_time = datetime.now()
    subprocess.call(' '.join(commands), shell=True)
    end_time = datetime.now() - start_time

    if action != '': 
        print(action, 'is fihish.', 'Duration:{}'.format(end_time) if measure_duration else '')

def get_configurations_data():
    # r=root, d=directories, files = files
    for r, d, files in os.walk(helper.replace_sep(local_work_dir + 'mnt')):
        for file in files:
            conf_key = file.split('.')[0].split('_')[0]
            configurations[conf_key] = '.'.join(file.split('.')[0].split('_')).replace(conf_key + '.', '')

def prepare_new_ib(key, post_data=''):

    call(' '.join(helper.create_ib_command(host_name, key, configurations[key])), 
        remote=False,
        action='creating ' + key,
        measure_duration=True)

    call(' '.join(helper.install_control_ext_command(host_name, key)), 
        remote=False,
        action='installing control extension',
        measure_duration=True)

    ext_name = helper.replace_sep(local_work_dir + 'mnt/' + key + '.cfe')
    if os.path.isfile(ext_name):
        call(' '.join(helper.install_ext_command(host_name, key)), 
            remote=False,
            action='installing extension',
            measure_duration=True)

    call(' '.join(helper.disable_safe_mode(host_name, key)), 
        remote=False,
        action='disabling safe mode for extensions',
        measure_duration=True)
        
    str_post = '-d @{}'.format(post_data) if post_data != '' else ''
    call('docker exec web.{} curl {} -X POST http://localhost/int/{}/hs/api.1cfresh/init'.format(host_name, str_post, key), 
        remote=False,
        action='initialization',
        measure_duration=True)

def renew_nginx_files():
    conf_catalog = work_dir + 'artifacts/nginx/conf/'
    call('mkdir -p {}'.format(conf_catalog))
    call('sh -c \'cp -r /out_files/conf/nginx/* {}'.format(conf_catalog) + '\'')

    call('sh -c \'sed -i \'s/hosthosthost/{}/g\' {}*.conf\''.format(host_name, conf_catalog))
    call('sh -c \'sed -i \'s/sitesitesite/site.{}/g\' {}*.conf\''.format(host_name, conf_catalog))
    call('sh -c \'sed -i \'s/webwebweb/web.{}/g\' {}*.conf\''.format(host_name, conf_catalog))
    call('sh -c \'sed -i \'s/gategategate/gate.{}/g\' {}*.conf\''.format(host_name, conf_catalog))

    call('sh -c \'sed -i \'s/sitesitesite/site.{}/g\' {}conf.d/*.conf\''.format(host_name, conf_catalog))
    call('sh -c \'sed -i \'s/hosthosthost/{}/g\' {}conf.d/*.conf\''.format(host_name, conf_catalog))

def renew_workdir():
    call('rm -rf /out_files/workdir')
    call('mkdir -p {}mnt'.format(work_dir))
    call('mkdir -p {}artifacts'.format(work_dir))
    call('sh -c "cp /out_files/distr/*.cf {}mnt/"'.format(work_dir))

def renew_docker_compose():
    call('cp /out_files/docker-compose.yml /out_files/workdir/docker-compose.yml')
    call('sh -c "sed -i \'s/HOSTNAMEREPLACE/{}/\' {}/*.yml"'.format(host_name, work_dir))

def renew_other_files():
    call('rm -rf ' + work_dir_other)
    call('cp -r /out_files/other_files/ ' + work_dir_other)
    call('sh -c "sed -i \'s/HOSTNAMEREPLACE/{}/\' {}vrd/*.vrd"'.format(host_name, work_dir_other))
    call('sh -c "sed -i \'s/HOSTNAMEREPLACE/{}/\' {}cfe/params.json"'.format(host_name, work_dir_other))

def publish_sevises():
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

def set_full_host_name(is_new):
    global host_name
    if is_new:
        part_host_name = helper.get_host_name(sys.argv)
        f = open(local_work_dir + 'hostname', 'x+') 
        f.write(part_host_name)
        f.close()
    else:
        f = open(local_work_dir + 'hostname')
        part_host_name = f.read() + host_name
        f.close()

    host_name = part_host_name + host_name
    print('host name is', host_name)


# Destroy exist conteiners and network
call(docker_compose_str + 'down', False)

new_server = '-new' in sys.argv
global_debug = '-debug' in sys.argv
new_server = True
if new_server:
    renew_workdir()
    get_configurations_data()
    
set_full_host_name(new_server)

if new_server: 
    renew_nginx_files()
    renew_docker_compose()
    renew_other_files()
    
# start db srv ras web gate conteiners
call(docker_compose_str + 'up -d db srv ras web gate', remote=False)

if new_server:
    publish_sevises()
    prepare_new_ib('smtl')
    prepare_new_ib('sa')
    prepare_new_ib('am')
    prepare_new_ib('sm', post_data='/mnt/other-files/cfe/params.json')
    



