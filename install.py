import subprocess
import sys
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

images = []
# images.append(centos.New())
# images.append(db.New())
images.append(site.New())
# images.append(forum.New())
# images.append(core.New())
# images.append(gate.New())
# images.append(nginx.New())

debug = '-debug' in sys.argv
start_time = datetime.now()
print('{}Build is starting{}'.format(colors.GREEN, colors.WHITE))

if  debug:
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


    subprocess.run(['docker', 'build', '-t', 'fresh/' + image.name, 'images/' + image.name],
        stdout=stdout, stderr=stderr)

    for command in image.commands_after:
        if debug: print(command)
        subprocess.call(' '.join(command), shell=True, stdout=stdout, stderr=stderr)

    print('Building', image.name , '...', '{}done'.format(colors.GREEN), colors.WHITE)

end_time = datetime.now() - start_time
print('{}Build finished{}'.format(colors.GREEN, colors.WHITE), 'Duration:', end_time)
