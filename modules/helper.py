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
        prefix = 'int'
    else:
        prefix = 'a'

    command = []
    command.append('docker')
    command.append('exec')
    command.append('web.' + host_name)
    command.append('/opt/1C/v8.3/x86_64/webinst')
    command.append('-apache24')
    command.append('-wsdir')
    command.append(prefix + '/' + conf_name)
    command.append('-dir')
    command.append('/var/www/{}/{}'.format(prefix, conf_name))
    command.append('-connstr')

    if base_name != '':
        command.append('\'Srvr=srv;Ref={};\''.format(base_name))
    else:
        command.append('\'Srvr=srv;Ref={};\''.format(conf_name))
    command.append('-confpath')
    command.append('\'/etc/httpd/conf/httpd.conf\'')
    command.append('-descriptor')
    command.append('\'/mnt/other-files/vrd/{}.vrd\''.format(descriptor))
    
    return command

def create_ib_command(host_name, ib_name, conf_ver=''):
    command = []
    command.append('docker')
    command.append('exec')
    command.append('-t')
    command.append('srv.' + host_name)
    command.append('/opt/1C/v8.3/x86_64/1cv8')
    command.append('CREATEINFOBASE')
    command.append('\'Srvr="srv";Ref="{0}";DBMS=PostgreSQL;DBSrvr="db";DB="{0}";DBUID="postgres";LicDstr="Y";Locale="ru_RU";CrSQLDB="Y";SchJobDn="N";\''.format(
        ib_name))
    command.append('/UseTemplate')
    command.append('/mnt/' + ib_name + '_' + conf_ver.replace('.', '_') + '.cf')
    command.append('/Out "/mnt/create_ib_' + ib_name + '.out"')
    command.append('/DumpResult "/mnt/create_ib_' + ib_name + '.result"')

    return command

def install_control_ext_command(host_name, ib_name):
    command = []
    command.append('docker')
    command.append('exec')
    command.append('-t')
    command.append('srv.' + host_name)
    command.append('/opt/1C/v8.3/x86_64/1cv8')
    command.append('DESIGNER')
    command.append('/S')
    command.append('"srv\\{}"'.format(ib_name))
    command.append('/LoadCfg')
    command.append('"/mnt/other-files/cfe/api_1cfresh.cfe"')
    command.append('-Extension')
    command.append('"api_1cfresh"')
    command.append('/UpdateDBCfg')
    command.append('/Out "/mnt/install_control_ext_{}.out"'.format(ib_name))
    command.append('/DumpResult "/mnt/install_control_ext_{}.result"'.format(ib_name))

    return command

def install_ext_command(host_name, ib_name):
    command = []
    command.append('docker')
    command.append('exec')
    command.append('-t')
    command.append('srv.' + host_name)
    command.append('/opt/1C/v8.3/x86_64/1cv8')
    command.append('DESIGNER')
    command.append('/S')
    command.append('"srv\\{}"'.format(ib_name))
    command.append('/LoadCfg')
    command.append('"/mnt/{}"'.format(ib_name))
    command.append('-Extension')
    command.append('"fresh"')
    command.append('/UpdateDBCfg')
    command.append('/Out "/mnt/install_ext_{}.out"'.format(ib_name))
    command.append('/DumpResult "/mnt/install_ext_{}.result"'.format(ib_name))

    return command

def disable_safe_mode(host_name, ib_name):
    command = []
    command.append('docker')
    command.append('exec')
    command.append('-t')
    command.append('srv.' + host_name)
    command.append('/opt/1C/v8.3/x86_64/1cv8')
    command.append('ENTERPRICE')
    command.append('/S')
    command.append('"srv\\{}"'.format(ib_name))
    command.append('/Execute')
    command.append('"/mnt/other-files/cfe/disable.epf"')
    command.append('/Out "/mnt/disable_safe_mode_{}.out"'.format(ib_name))
    command.append('/DumpResult "/mnt/disable_safe_mode_{}.result"'.format(ib_name))

    return command

def get_host_name(argv):

    if '-h' not in argv:
        print('parameter -р not specified')
        exit(1)
    host_index = argv.index('-h')
    return argv[host_index + 1]