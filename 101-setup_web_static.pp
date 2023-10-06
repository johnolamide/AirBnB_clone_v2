# Define a class for setting up web servers
class web_server_setup {

  # Install Nginx if not already installed
  package { 'nginx':
    ensure => 'installed',
  }

  # Create the necessary directories if they don't exist
  file { '/data':
    ensure  => 'directory',
    owner   => 'ubuntu',
    group   => 'ubuntu',
    recurse => true,
  }

  file { '/data/web_static':
    ensure  => 'directory',
    owner   => 'ubuntu',
    group   => 'ubuntu',
    recurse => true,
  }

  file { '/data/web_static/releases':
    ensure  => 'directory',
    owner   => 'ubuntu',
    group   => 'ubuntu',
    recurse => true,
  }

  file { '/data/web_static/shared':
    ensure  => 'directory',
    owner   => 'ubuntu',
    group   => 'ubuntu',
    recurse => true,
  }

  file { '/data/web_static/releases/test':
    ensure  => 'directory',
    owner   => 'ubuntu',
    group   => 'ubuntu',
    recurse => true,
  }

  # Create a simple HTML file for testing
  file { '/data/web_static/releases/test/index.html':
    ensure  => 'file',
    content => '<html><head></head><body>Test Page</body></html>',
    owner   => 'ubuntu',
    group   => 'ubuntu',
  }

  # Create or recreate the symbolic link
  file { '/data/web_static/current':
    ensure => 'link',
    target => '/data/web_static/releases/test',
    owner  => 'ubuntu',
    group  => 'ubuntu',
    force  => true,
  }

  # Update Nginx configuration with alias
  file { '/etc/nginx/sites-available/default':
    ensure  => 'file',
    content => "
        server {
            listen 80 default_server;
            server_name _;

            locaion /hbnb_static {
                alias /data/web_static/current/;
            }

            location / {
                proxy_set_header Host $host;
                proxy_pass http://127.0.0.1:80;
            }
        }
",
    require => Package['nginx'],
    notify  => Service['nginx'],
  }
}

# Apply the web_server_setup class
include web_server_setup

# Define an Nginx service
service { 'nginx':
  ensure => 'running',
  enable => true,
}

