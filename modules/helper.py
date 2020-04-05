import pathlib
import os

sep = str(os.path.sep)
this_path = str(pathlib.Path().absolute()) + sep
distr_path = this_path + 'distr' + sep

def replace_sep(path):
    return path.replace('/', sep)

def new_docker_command(extra_path=None): 
    command = []
    command.append('docker')
    command.append('run')
    command.append('--rm')
    command.append('-v')

    if extra_path != None:
        current_distr_path = this_path + extra_path
        current_distr_path = current_distr_path.replace('/', sep)
    else:
        current_distr_path = distr_path

    command.append(current_distr_path + ':/out_files')
    return command

def web_publish_command(host_name, conf_name, internal, descriptor, base_name=''):
    
    if internal:
        prefix = 'a'
    else:
        prefix = 'int'

    command = []
    command.append('docker')
    command.append('exec')
    command.append('web.' + host_name)
    command.append('/opt/1C/v8.3/x86_64/webinst')
    command.append('-apache24')
    command.append('-wsdir')
    command.append(prefix + '/' + conf_name)
    command.append('-dir')
    command.append('/var/www/' + conf_name)
    command.append('-connstr')

    if base_name != '':
        command.append('\'Srvr=srv;Ref=' + base_name + ';\'')
    else:
        command.append('\'Srvr=srv;Ref=' + conf_name + ';\'')
    command.append('-confpath')
    command.append('\'/etc/httpd/conf/httpd.conf\'')
    command.append('-descriptor')
    command.append('\'/mnt/other-files/vrd/' + descriptor + '.vrd\'')
    
    return command

def create_ib_command(host_name, ib_name, conf_ver=''):
    command = []
    command.append('docker')
    command.append('exec')
    command.append('-t')
    command.append('srv.' + host_name)
    command.append('/opt/1C/v8.3/x86_64/1cv8')
    command.append('CREATEINFOBASE')
    command.append('\'Srvr="srv";Ref="' + ib_name + '";DBMS=PostgreSQL;DBSrvr="db";DB="' + ib_name + '";DBUID="postgres";LicDstr="Y";Locale="ru_RU";CrSQLDB="Y";SchJobDn="N";\'')
    command.append('/UseTemplate')
    command.append('/mnt/' + ib_name + '_' + conf_ver.replace('.', '_') + '.cf')
    command.append('/Out "/mnt/create_ib_' + ib_name + '.out"')
    command.append('/DumpResult "/mnt/create_ib_' + ib_name + '.result"')

    return command