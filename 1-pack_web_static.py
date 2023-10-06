#!/usr/bin/python3
""" this script contains the function definition for do_pack
"""
from fabric.api import local
from datetime import datetime


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
