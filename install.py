import subprocess

import modules.site as site
import modules.centos as centos
import modules.db as db
import modules.forum as forum
import modules.core as core
import modules.gate as gate
import modules.nginx as nginx

images = []
images.append(centos.New())
images.append(db.New())
images.append(site.New())
images.append(forum.New())
images.append(core.New())
images.append(gate.New())
images.append(nginx.New())

print('Building start')
for image in images:

    for command in image.commands_before:
        print(command)
        subprocess.call(' '.join(command), shell=True)

    subprocess.run(['docker', 'build', '-t', 'fresh/' + image.name, 'images/' + image.name])

    for command in image.commands_after:
        print(command)
        subprocess.call(' '.join(command), shell=True)

    print('Building', image.name, 'is fihish')

print('Building finish')
