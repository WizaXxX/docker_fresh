import subprocess
import os
import modules.helper as helper
import sys
import json
from datetime import datetime

host_name = '.1cfresh.dev'
sup_password = '123Qwer'
new_server = False
global_debug = False
info_base_list = []
configurations = {}

docker_run_str = 'docker run --rm -v {}:/out_files alpine'.format(helper.this_path)
docker_compose_str = 'docker-compose -f workdir/docker-compose.yml '

work_dir = '/out_files/workdir/'
work_dir_other = work_dir + 'mnt/other-files/'
local_work_dir = helper.replace_sep(helper.this_path + '/workdir/')


class colors:
    GREEN = '\033[92m'
    WHITE = '\033[97m'

class ib_prop:
    a_name = 'ИмяВнешнейПубликации'
    a_desc = 'ИмяФайлаШаблонаВнешненийПубликации'
    int_name = 'ИмяВнутреннейПубликации'
    int_desc = 'ИмяФайлаШаблонаВнутреннейПубликации'
    conf_file = 'ИмяФайлаКонфигурации'
    name = 'ИмяВКластере'
    job = 'БлокироватьРаботуРегЗаданийПриСоздании'
    adm = 'Администратор'


def print_description(function_to_decorate):

    def wrapper(*args, **kwargs):

        if 'desc' in kwargs:
            desc = kwargs['desc']
        else:
            desc = ''

        print(function_to_decorate.__doc__, desc, '...', end='\r')
        function_to_decorate(*args, **kwargs)
        print(function_to_decorate.__doc__,
              desc, '...', '{}done'.format(colors.GREEN), colors.WHITE)
    return wrapper


def call(command, remote=True, debug=False, action='', measure_duration=False, silent=True):
    commands = []

    if remote:
        commands.append(docker_run_str)
    commands.append(command)

    if action != '' and (debug or global_debug):
        print(action, end='\r')
    if debug or global_debug:
        print(' '.join(commands))

    if not silent or global_debug:
        stdout = None
        stderr = None
    else:
        stdout = subprocess.PIPE
        stderr = subprocess.PIPE

    start_time = datetime.now()
    subprocess.call(' '.join(commands), shell=True,
                    stdout=stdout, stderr=stderr)
    end_time = datetime.now() - start_time

    if action != '' and (debug or global_debug):
        print(action, 'is fihish.', 'Duration:{}'.format(
            end_time) if measure_duration else '')


@print_description
def get_configurations_data():
    """Get configuration data"""

    with open('other_files/params.json') as json_file:
        data = json.load(json_file)
        for ib_data in data['ИнформационныеБазы']:
            if not os.path.isfile('distr/{}'.format(ib_data['ИмяФайлаКонфигурации'])):
                print('File {} not found'.format(ib_data['ИмяФайлаКонфигурации']))
            else:
                info_base_list.append(ib_data)


def prepare_new_ib(ib_name, int_name, conf_file_name, job_block):

    job_dn_str = 'Y' if job_block else 'N'

    call(' '.join(helper.create_ib_command(host_name, ib_name, conf_file_name, job_dn_str)),
         remote=False,
         action='Creating ' + ib_name,
         measure_duration=True)

    call(' '.join(helper.install_control_ext_command(host_name, ib_name)),
         remote=False,
         action='Installing control extension',
         measure_duration=True)

    ext_name = helper.replace_sep(local_work_dir + 'mnt/' + ib_name + '.cfe')
    if os.path.isfile(ext_name):
        call(' '.join(helper.install_ext_command(host_name, ib_name)),
             remote=False,
             action='Installing extension',
             measure_duration=True)

    if ib_name == 'sm':
        post_data = '/mnt/other-files/params.json'
        call(' '.join(helper.install_sm_ext_command(host_name, ib_name)),
            remote=False,
            action='Installing gate control extension',
            measure_duration=True)
    else:
        post_data = ''    

    call(' '.join(helper.disable_safe_mode(host_name, ib_name)),
         remote=False,
         action='Disabling safe mode for extensions',
         measure_duration=True)

    str_post = '-d @{}'.format(post_data) if post_data != '' else ''
    call('docker exec web.{} curl {} -X POST http://localhost/int/{}/hs/api.1cfresh/init'.format(host_name, str_post, int_name),
         remote=False,
         action='Initialization',
         measure_duration=True)

@print_description
def prepare_bases():
    """Prepare all bases"""

    sm_ib = None

    for ib_data in info_base_list:
        if ib_data[ib_prop.name] == 'sm': 
            sm_ib = ib_data
            continue
        prepare_new_ib(
            ib_name=ib_data[ib_prop.name],
            int_name=ib_data[ib_prop.int_name],
            conf_file_name=ib_data[ib_prop.conf_file],
            job_block=ib_data[ib_prop.job]
        )
    
    # prepare sm base 
    prepare_new_ib(
            ib_name=sm_ib[ib_prop.name],
            int_name=sm_ib[ib_prop.int_name],
            conf_file_name=sm_ib[ib_prop.conf_file],
            job_block=sm_ib[ib_prop.job]
        )    

@print_description
def renew_nginx_files():
    """Renew nginx files"""

    conf_catalog = work_dir + 'artifacts/nginx/conf/'
    call('mkdir -p {}'.format(conf_catalog))
    call('sh -c \'cp -r /out_files/conf/nginx/* {}'.format(conf_catalog) + '\'')

    call('sh -c \'sed -i \'s/hosthosthost/{}/g\' {}*.conf\''.format(host_name, conf_catalog))
    call('sh -c \'sed -i \'s/sitesitesite/site.{}/g\' {}*.conf\''.format(host_name, conf_catalog))
    call('sh -c \'sed -i \'s/webwebweb/web.{}/g\' {}*.conf\''.format(host_name, conf_catalog))
    call('sh -c \'sed -i \'s/gategategate/gate.{}/g\' {}*.conf\''.format(host_name, conf_catalog))

    call('sh -c \'sed -i \'s/sitesitesite/site.{}/g\' {}conf.d/*.conf\''.format(host_name, conf_catalog))
    call('sh -c \'sed -i \'s/hosthosthost/{}/g\' {}conf.d/*.conf\''.format(host_name, conf_catalog))


@print_description
def renew_workdir():
    """Renew wordir"""

    call('rm -rf /out_files/workdir')
    call('mkdir -p {}mnt'.format(work_dir))
    call('mkdir -p {}artifacts'.format(work_dir))
    call('mkdir -p {}artifacts/web/conf'.format(work_dir))
    call('sh -c "cp /out_files/conf/web/httpd.conf {}artifacts/web/conf/httpd.conf"'.format(work_dir))
    call('sh -c "cp /out_files/distr/*.cf {}mnt/"'.format(work_dir))


@print_description
def renew_docker_compose():
    """Renew docker-compose file"""

    call('cp /out_files/docker-compose_pattern.yml /out_files/workdir/docker-compose.yml')
    call('sh -c "sed -i \'s/HOSTNAMEREPLACE/{}/\' {}/*.yml"'.format(host_name, work_dir))


@print_description
def renew_other_files():
    """Renew other-files"""

    call('rm -rf ' + work_dir_other)
    call('cp -r /out_files/other_files/ ' + work_dir_other)
    call('sh -c "sed -i \'s/HOSTNAMEREPLACE/{}/\' {}vrd/*.vrd"'.format(host_name, work_dir_other))
    call('sh -c "sed -i \'s/HOSTNAMEREPLACE/{}/\' {}params.json"'.format(host_name, work_dir_other))


@print_description
def publish_sevises():
    """Publish services"""

    for ib_data in info_base_list:
        if ib_data[ib_prop.a_name] != '':
            call(' '.join(helper.web_publish_command(
                host_name=host_name,
                conf_name=ib_data[ib_prop.a_name],
                internal=False,
                descriptor=ib_data[ib_prop.a_desc],
                base_name=ib_data[ib_prop.name])), remote=False)

        call(' '.join(helper.web_publish_command(
            host_name=host_name,
            conf_name=ib_data[ib_prop.int_name],
            internal=True,
            descriptor=ib_data[ib_prop.int_desc],
            base_name=ib_data[ib_prop.name])), remote=False)
    
    # publish special services
    call(' '.join(helper.web_publish_command(
        host_name, 'openid', False, 'openid', 'sm')), remote=False)    
    call(' '.join(helper.web_publish_command(host_name, 'sc', True,
        'sessioncontrol', 'sm;Usr=SessionControl;Pwd=' + sup_password)), remote=False)
    call(' '.join(helper.web_publish_command(host_name, 'extreg', True,
        'extreg', 'sm;Usr=ExtReg;Pwd=' + sup_password)), remote=False)

    # restart Apache
    call('docker exec web.{} chown -R usr1cv8:grp1cv8 /var/www'.format(host_name), remote=False)
    call('docker exec web.{} httpd -k graceful'.format(host_name), remote=False)


@print_description
def set_full_host_name(is_new):
    """Set full hostname"""

    global host_name
    if is_new:
        part_host_name = helper.get_host_name(sys.argv)
        f = open('.hostname', 'w+')
        f.write(part_host_name)
        f.close()
    else:
        f = open('.hostname')
        part_host_name = f.read()
        f.close()

    host_name = part_host_name + host_name
    print('host name is', host_name)


@print_description
def create_db_site():
    """Create db for site"""

    call('docker exec -t db.{} sh -c \'/usr/bin/psql -U postgres -f {}'.format(host_name, '/create_db_site.psql\''),
         remote=False)


@print_description
def create_db_forum():
    """Create db for forum"""

    call('docker exec -t db.{} sh -c \'/usr/bin/psql -U postgres -f {}'.format(host_name, '/create_db_forum.psql\''),
         remote=False)


@print_description
def delete_control_extension(ib_name, user, desc):
    """Delete control extension"""

    call(' '.join(helper.delete_control_extension(ib_name, host_name, user)), remote=False)

def delete_all_control_ext():
    for ib_data in info_base_list:
        delete_control_extension(
            ib_name=ib_data[ib_prop.name],
            user= None if ib_data[ib_prop.adm] == '' else ib_data[ib_prop.adm],
            desc=ib_data[ib_prop.name]
        )

@print_description
def configurate_site():
    """Configurate site settings"""

    call(' '.join(helper.edit_site_settings(host_name, sup_password)), remote=False)
    call('docker exec -t web.{0} curl https://{0}/settings/finish_configuration'.format(host_name), remote=False)
    call(' '.join(helper.enable_manual_registration(host_name)), remote=False)
    call(' '.join(helper.enable_openid(host_name)), remote=False)
    call(' '.join(helper.add_solution(
        host_name=host_name,
        brief_desc='БТС',
        full_desc='БТС',
        display_order=0,
        id='smtl',
        possibilities='БТС',
        title='Библиотека технологии сервиса'
    )), remote=False)


@print_description
def init_gate():
    """Initialization gate"""

    call('docker exec -t web.{0} curl --user Администратор: https://{0}/a/adm/hs/docker_control/update_appgate'.format(host_name),
        remote=False)


@print_description
def wait_postgres():
    """Waiting for postgres"""

    call('docker exec -t db.{} /wait_postgres.sh'.format(host_name), remote=False)


@print_description
def wait_site():
    """Waiting for site"""

    call('docker exec -t site.{} /wait_site.sh'.format(host_name), remote=False)


@print_description
def enable_job_in_sm():
    """Enable scheduled jobs sm"""

    call('docker exec -t ras.{} deployka scheduledjobs unlock -db sm -db-user \'Администратор\''.format(host_name),
        remote=False)


global_start_time = datetime.now()
print('{}Fresh is starting{}'.format(colors.GREEN, colors.WHITE))

# destroy exist conteiners and network
call(docker_compose_str + 'down', remote=False, silent=False)

new_server = '-new' in sys.argv
global_debug = '-debug' in sys.argv

set_full_host_name(new_server)

if new_server:
    renew_workdir()
    get_configurations_data()
    renew_nginx_files()
    renew_docker_compose()
    renew_other_files()

# start db srv ras web gate conteiners
call(docker_compose_str + 'up -d db srv ras web gate', remote=False, silent=False)
wait_postgres()

if new_server:
    publish_sevises()
    prepare_bases()
    enable_job_in_sm()
    create_db_site()
    create_db_forum()

# start site forum nginx conteiners
call(docker_compose_str + 'up -d nginx site', remote=False, silent=False)
wait_site()

if new_server:
    delete_all_control_ext()
    configurate_site()

init_gate()

global_end_time = datetime.now() - global_start_time
print('{}Fresh started{}'.format(colors.GREEN, colors.WHITE), 'Duration:', global_end_time)
