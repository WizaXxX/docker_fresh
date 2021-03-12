#!/usr/bin/python3
# -*- coding: utf-8 -*-

import glob
import re
import os
import sys
import subprocess
import urllib
import json
import time
import uuid


path_to_1c = ''

# define regexps
regex_process_pid = re.compile(r'/([^/.]+?)\.(\d+?)\.(\d+?)\.core')
regex_offset = re.compile(r'#0\s+?([\dxa-f]+?)\s')
regex_extension_replacement = re.compile(r'\.zip$')
regex_extension_replacement2 = re.compile(r'\.core$')


# BEGIN helper functions------------------------------------------------------------------------------------------------

def write_to_log(msg):
    msg = time.ctime() + ' ' + msg
    print(msg)


def run_shell(cmd):
    pipe = subprocess.PIPE
    p = subprocess.Popen(cmd, shell=True, stdin=pipe, stdout=pipe, stderr=pipe, close_fds=True, cwd='/')
    return p.stdout.read(), p.stderr.read()

def run_shell_get_stdout(cmd):
    pipe = subprocess.PIPE
    p = subprocess.Popen(cmd, shell=True, stdin=pipe, stdout=pipe, stderr=pipe, close_fds=True, cwd='/')
    return p.stdout.read()

def run_shell_get_result(cmd):
    result = subprocess.call(cmd, shell=True)
    return result


def check_size_static(core_file):
    size_1 = os.path.getsize(core_file)
    time.sleep(5)
    size_2 = os.path.getsize(core_file)
    return size_1 == size_2

def get_path_to_1c():
    global path_to_1c
    if path_to_1c == '':
        result = run_shell_get_stdout("find / -name '1cv8c' | sed 's/1cv8c//g' | sed 's/\.\/opt/\/opt/g'")
        path_to_1c = result.decode('utf-8').strip()
    return path_to_1c


# END helper functions--------------------------------------------------------------------------------------------------

# BEGIN prepare date----------------------------------------------------------------------------------------------------


def get_pid_process_ctime(core_file):
    rez = regex_process_pid.search(core_file)
    process = rez.groups()[0]
    ctime = rez.groups()[1]
    pid = rez.groups()[2]
    return process, ctime, pid


def get_platform_offset(core_file, process):
    # run gdb for getting offset of core
    cmd = 'echo -e "bt\nexit" | gdb ' + get_path_to_1c() + process + ' ' + core_file
    (gdb_result, gdb_error) = run_shell(cmd)

    if not gdb_result:
        offset = '000000000000'
        platform = '8.3.0.0000'
        write_to_log('cant work with gdb: ' + gdb_error)
    else:
        rez = regex_offset.search(gdb_result)
        if rez is None:
            offset = '000000000000'
        else:
            offset = rez.groups()[0]
            offset = offset[6:-1]
        # getting platform version
        cmd = 'strings ' + get_path_to_1c() + process + """ | grep -oP '[8-9]\.[3-90]\.\d\d?\.\d{2,4}' """
        (ver_result, ver_error) = run_shell(cmd)
        if ver_result:
            platform = ver_result.strip()
        else:
            platform = '8.3.0.0000'
    return platform, offset


def get_creation_date_string(ctime):
    ctime_sturct = time.localtime(int(ctime))
    ctime_string = '_%.4d%.2d%.2d%.2d%.2d%.2d_' % (ctime_sturct[0], ctime_sturct[1], ctime_sturct[2], ctime_sturct[3],
                                                   ctime_sturct[4], ctime_sturct[5])
    creation_date = '%.4d-%.2d-%.2dT%.2d:%.2d:%.2d' % (ctime_sturct[0], ctime_sturct[1], ctime_sturct[2],
                                                       ctime_sturct[3], ctime_sturct[4], ctime_sturct[5])
    return ctime_string, creation_date


def get_file_name(process, platform, offset, ctime_string, pid):
    return process + '_' + platform + '_' + offset + ctime_string + pid + '.core'


def get_file_size_hostname(core_file):
    file_size = os.path.getsize(core_file)
    hostname = os.uname()[1]
    return file_size, hostname


def make_libs_tar(core_file, process):
    if os.path.exists(libs_file):
        os.remove(libs_file)
    cmd = """echo -e "info shared\nq" | """
    cmd += """ gdb """ + get_path_to_1c() + process + " " + core_file + """ 2>/dev/null | """
    cmd += """ grep 0x0000 | grep -v /opt/1C/v8.3 | grep -v ?? | perl -alne 'print $F[-1]' | """
    cmd += """ while read file; do tar --dereference --append -f """ + libs_file + """ $file  2> /dev/null ; done"""
    stdout, stderr = run_shell(cmd)

    # Если стек не раскрылся, то создадим пустой файл
    if not os.path.exists(libs_file):
        cmd = 'touch ' + libs_file
        run_shell_get_result(cmd)

    if stderr:
        write_to_log('cant work with gdb and make libs tar, result: ' + str(stderr))

    if os.path.getsize(libs_file) == 0:
        write_to_log('libs_file size = 0.')


def change_extension(core_gz_file):
    core_gz_file = regex_extension_replacement.sub('.tar.gz', core_gz_file)
    return regex_extension_replacement2.sub('.tar.gz', core_gz_file)

# END prepare date------------------------------------------------------------------------------------------------------


def gz_core_file(core_file, file_name):
    # Костыль, меняем расшинерие на gz
    core_gz_file = os.path.basename(file_name)
    core_gz_file = change_extension(core_gz_file)

    # Зипуем
    cmd = 'cd {} && mv {} {} && '.format(cores_dir, core_file, file_name)
    cmd += 'tar -czf {} {} {} 2>/dev/null && '.format(core_gz_file, file_name, libs_short_file)
    cmd += 'rm -f {} && rm -f {}'.format(file_name, libs_short_file)
    rez = run_shell_get_result(cmd)

    # Если не получилось загзиповать, то выходим из процедуры
    if rez:
        write_to_log('cant work with tar')
        return

# BEGIN main program ---------------------------------------------------------------------------------------------------


def work_with_dump(core_file):

    while not check_size_static(core_file):
        print('{} file size: {}'.format(core_file, os.path.getsize(core_file)))

    process, ctime, pid = get_pid_process_ctime(core_file)
    platform, offset = get_platform_offset(core_file, process)
    ctime_string, creation_date = get_creation_date_string(ctime)
    make_libs_tar(core_file, process)

    file_name = get_file_name(process, platform, offset, ctime_string, pid)
    gz_core_file(core_file, file_name)


cores_dir = '/tmp/cores/'  # директория в которой должны лежать дампы
libs_short_file = 'libs.tar'
libs_file = os.path.join(cores_dir, 'libs.tar')


if __name__ == "__main__":
    # finding core files
    cores_path = cores_dir + '*.core*'
    for file in glob.glob(cores_path):
        work_with_dump(file)