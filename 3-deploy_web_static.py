#!/usr/bin/python3
""" this script contains the function definition of deploy
"""
from fabric.api import env, put, run, local, runs_once
from datetime import datetime
import os


env.hosts = ['54.210.42.244', '54.160.120.100']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/ALX/id_rsa_alx'


@runs_once
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

        put(archive_path, "/tmp/")
        run("mkdir -p {}/".format(release_path))
        run("tar -xzf /tmp/{} -C {}/".format(archive_basename, release_path))

        run("rm /tmp/{}".format(archive_basename))

        run("mv {}/web_static/* {}/".format(release_path, release_path))
        run("rm -rf {}/web_static".format(release_path))

        current_path = '/data/web_static/current'
        run("rm -f {}".format(current_path))
        run("ln -s {}/ {}".format(release_path, current_path))

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
