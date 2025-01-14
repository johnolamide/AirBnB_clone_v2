#!/usr/bin/python3
""" this script contains the function definition of deploy
"""
from fabric.api import env, put, run, local, lcd
from datetime import datetime
import os


env.hosts = ['54.210.42.244', '54.160.120.100']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/ALX/id_rsa_alx'


def do_pack():
    """ creates a .tgz archive from web_static folder
    """
    local("mkdir -p versions")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "versions/web_static_{}.tgz".format(timestamp)

    result = local("tar -czvf {} web_static".format(archive_name))

    if result.failed:
        return None
    else:
        return archive_name


def do_deploy(archive_path):
    """ Distributes and deploy an archive to webservers
        Args:
            archive_path (str): path to the archive
    """
    if not os.path.exists(archive_path):
        return False

    try:
        archive_basename = os.path.basename(archive_path)
        archive_filename = os.path.splitext(archive_basename)[0]
        release_path = '/data/web_static/releases/{}'.format(archive_filename)

        put(archive_path, '/tmp/')
        run("mkdir -p {}".format(release_path))
        run("tar -xzf /tmp/{} -C {}".format(archive_basename, release_path))

        run("rm /tmp/{}".format(archive_basename))

        run("mv {}/web_static/* {}/".format(release_path, release_path))
        run("rm -rf {}/web_static".format(release_path))

        current_path = '/data/web_static/current'
        run("rm -f {}".format(current_path))
        run("ln -s {} {}".format(release_path, current_path))

        print("New version deployed")
        return True
    except Exception:
        return False


def deploy():
    """ creates and distributes an archive to the web servers
    """
    archive_path = do_pack()

    if not archive_path:
        return False

    return do_deploy(archive_path)


def do_clean(number=0):
    """ removes outdated archives
    """
    #try:
    number = int(number)

    if number < 0:
        number = 0

    directory = "~/alx/AirBnB_clone_v2/versions"
    with lcd(directory):
        archives = sorted(os.listdir(directory), reverse=True)
        archives_to_keep = archives[:number]

        for archive in archives:
            if archive not in archives_to_keep:
                #local('rm -f {}'.format(archive))
                print("**** ARCHIVE ***")
                print(archive)

    #releases = run('ls -l /data/web_static/releases').split()
    releases_to_keep = releases[:number]

    for release in releases:
        if release not in releases_to_keep:
            #run('rm -rf /data/web_static/releases/{}'.format(release))
            print("*** RELEASE ***")
            print(release)

    return True

    #except Exception:
    #    return False
