import subprocess
import sys
import platform
from datetime import datetime

import modules.site as site
import modules.centos as centos
import modules.db as db
import modules.forum as forum
import modules.core as core
import modules.gate as gate

class colors:
    GREEN = '\033[92m'
    WHITE = '\033[97m'
    RED = '\033[91m'

def get_docker_image_command():
    if platform.system().lower() == 'windows':
        return ['docker', 'images']
    else:
        return ['docker images']

def image_exist(image_name):
    full_image_name = 'fresh/' + image.name
    result = subprocess.run(get_docker_image_command(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    return full_image_name in str(result.stdout)

images = []
images.append(centos.New())
images.append(db.New())
images.append(site.New())
images.append(forum.New())
images.append(core.New())
images.append(gate.New())

debug = '-debug' in sys.argv
start_time = datetime.now()
print('{}Build is starting{}'.format(colors.GREEN, colors.WHITE))

if debug:
    stdout = None
    stderr = None
else:
    stdout = subprocess.PIPE
    stderr = subprocess.PIPE

for image in images:

    print('Building', image.name, '...', end='\r')

    for command in image.commands_before:
        if debug: print(command)
        subprocess.call(' '.join(command), shell=True, stdout=stdout, stderr=stderr)

    result = subprocess.run(['docker', 'build', '-t', 'fresh/' + image.name, 'images/' + image.name],
        stdout=stdout, stderr=stderr)

    if result.returncode != 0 or not image_exist(image.name):
        print('Building', image.name , '...', '{}error'.format(colors.RED), colors.WHITE)
        exit(1)    

    for command in image.commands_after:
        if debug: print(command)
        subprocess.call(' '.join(command), shell=True, stdout=stdout, stderr=stderr)

    print('Building', image.name , '...', '{}done'.format(colors.GREEN), colors.WHITE)

end_time = datetime.now() - start_time
print('{}Build finished{}'.format(colors.GREEN, colors.WHITE), 'Duration:', end_time)
