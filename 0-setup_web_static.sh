#!/usr/bin/env bash
# this script set up web server for the deployment of web_static

# install Nginx if not installed
apt-get -y update
apt-get -y install nginx

# create the neccessary directories if they dont exist
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/
touch /data/web_static/releases/test/index.html

# create a simple HTML file
echo "<html><head></head><body>Hello World</body></html>" \
> /data/web_static/releases/test/index.html

# create or recreate the symbolic link
rm -f /data/web_static/current
ln -sf /data/web_static/releases/test/ /data/web_static/current

# set ownership of the /data/ folder to ubuntu user
chown -R ubuntu:ubuntu /data/

# update Nginx configuration with alias
config_file="/etc/nginx/sites-available/default"
config_content=$(cat <<EOF
server {
    listen 80 default_server;
    server_name _;

    location /hbnb_static {
        alias /data/web_static/current/;
    }

    location / {
        proxy_set_header Host \$host;
        proxy_pass http://127.0.0.1:80;
    }
}
EOF
)

echo "$config_content" > "$config_file"

# restart Nginx
service nginx restart
