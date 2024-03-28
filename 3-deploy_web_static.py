#!/usr/bin/python3
from fabric.api import env, local
from os.path import isfile
from datetime import datetime
from fabric.operations import put, run
from fabric.contrib.files import exists

env.hosts = ['54.144.154.53', '100.26.246.14']  # Replace with actual IP addresses
env.user = 'deenyshomar'  # Replace with your username


def do_pack():
        try:
                    # Create the versions folder if it doesn't exist
                            local("mkdir -p versions")

                                    # Generate the current date and time for the archive name
                                            now = datetime.now()
                                                    timestamp = now.strftime("%Y%m%d%H%M%S")

                                                            # Name the archive
                                                                    archive_name = "web_static_{}.tgz".format(timestamp)

                                                                            # Compress the web_static folder into the archive
                                                                                    local("tar -cvzf versions/{} web_static".format(archive_name))

                                                                                            # Return the archive path
                                                                                                    return "versions/{}".format(archive_name)
                                                                                                    except Exception as e:
                                                                                                                print("Error occurred while creating the archive:", e)
                                                                                                                        return None


                                                                                                                    def do_deploy(archive_path):
                                                                                                                            if not isfile(archive_path):
                                                                                                                                        return False

                                                                                                                                        try:
                                                                                                                                                    # Upload the archive to /tmp/ directory of the web server
                                                                                                                                                            put(archive_path, '/tmp/')

                                                                                                                                                                    # Extract archive filename without extension
                                                                                                                                                                            file_name = archive_path.split('/')[-1]
                                                                                                                                                                                    folder_name = file_name.split('.')[0]

                                                                                                                                                                                            # Create directory to uncompress the archive if it doesn't exist
                                                                                                                                                                                                    run('mkdir -p /data/web_static/releases/{}/'.format(folder_name))

                                                                                                                                                                                                            # Uncompress the archive to /data/web_static/releases/ folder
                                                                                                                                                                                                                    run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
                                                                                                                                                                                                                                        .format(file_name, folder_name))

                                                                                                                                                                                                                            # Delete the archive from the web server
                                                                                                                                                                                                                                    run('rm /tmp/{}'.format(file_name))

                                                                                                                                                                                                                                            # Delete the symbolic link /data/web_static/current
                                                                                                                                                                                                                                                    run('rm -rf /data/web_static/current')

                                                                                                                                                                                                                                                            # Create a new symbolic link linked to the new version of code
                                                                                                                                                                                                                                                                    run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
                                                                                                                                                                                                                                                                                        .format(folder_name))

                                                                                                                                                                                                                                                                            print("New version deployed!")
                                                                                                                                                                                                                                                                                    return True
                                                                                                                                                                                                                                                                                    except Exception as e:
                                                                                                                                                                                                                                                                                                print("Deployment failed:", e)
                                                                                                                                                                                                                                                                                                        return False


                                                                                                                                                                                                                                                                                                    def deploy():
                                                                                                                                                                                                                                                                                                            archive_path = do_pack()
                                                                                                                                                                                                                                                                                                                if not archive_path:
                                                                                                                                                                                                                                                                                                                            return False
                                                                                                                                                                                                                                                                                                                            return do_deploy(archive_path)

