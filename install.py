import subprocess
import pathlib
import os
import modules.site as site
import modules.centos as centos
import modules.db as db
import modules.forum as forum

sep = str(os.path.sep)
this_path = str(pathlib.Path().absolute()) + sep
distr_path = this_path + 'distr' + sep

images = []
images.append(centos.New())
images.append(db.New())
images.append(site.New())
images.append(forum.New())

print('Building start')
for image in images:

    for command in image.commands:
        print(command)
        subprocess.call(' '.join(command), shell=True)

    subprocess.run(['docker', 'build', '-t', 'fresh/' + image.name, 'images/' + image.name])
    print('Building', image.name, 'is fihish')

print('Building finish')
