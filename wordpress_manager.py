import os
import subprocess
import sys
import webbrowser
import argparse
import shutil
import platform

def check_dependencies():
    # Check if Docker is installed
    try:
        subprocess.run(['docker', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError:
        print("Docker is not installed. Please install Docker before running this script.")
        sys.exit(1)

    # Check if Docker Compose is installed
    try:
        subprocess.run(['docker-compose', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError:
        print("Docker Compose is not installed. Please install Docker Compose before running this script.")
        sys.exit(1)

def create_wordpress_site(site_name):
    # Create a directory for the WordPress site
    os.makedirs(site_name, exist_ok=True)

    # Create docker-compose.yml file for the WordPress site
    with open(f"{site_name}/docker-compose.yml", "w") as compose_file:
        compose_file.write(f'''version: '3'
services:
  db:
    image: mysql:5.7
    restart: always
    environment:
      MYSQL_DATABASE: wordpress
      MYSQL_USER: root
      MYSQL_PASSWORD: example
      MYSQL_RANDOM_ROOT_PASSWORD: "yes"
    volumes:
      - db_data:/var/lib/mysql
  wordpress:
    depends_on:
      - db
    image: wordpress:latest
    restart: always
    environment:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_NAME: wordpress
      WORDPRESS_DB_USER: root
      WORDPRESS_DB_PASSWORD: example
    volumes:
      - ./wp-content:/var/www/html/wp-content
  nginx:
    image: nginx:latest
    restart: always
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
      - ./wp-content:/var/www/html/wp-content
volumes:
  db_data:
''')

    # Create nginx.conf file for Nginx configuration
    with open(f"{site_name}/nginx.conf", "w") as nginx_conf:
        nginx_conf.write(f'''server {{
    listen 80;
    server_name {site_name};
    root /var/www/html;
    index index.php;

    location / {{
        try_files $uri $uri/ /index.php?$args;
    }}

    location ~ \.php$ {{
        include fastcgi_params;
        fastcgi_pass wordpress:9000;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    }}
}}
''')

    # Add entry to /etc/hosts
    if platform.system() == "Windows":
        add_host_entry_windows(site_name)
    else:
        add_host_entry_unix(site_name)

    print(f"WordPress site '{site_name}' with a LEMP stack created successfully!")
    print(f"Please wait for a moment while the site is being set up...")
    print("Opening the site in your default browser...")
    webbrowser.open(f"http://{site_name}")
    
# Function to add entry to the hosts file on Windows
def add_host_entry_windows(site_name):
    import ctypes

    # Check if the script is running with administrator privileges
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("Error: The script needs to be run with administrator privileges to modify the hosts entry.")
        sys.exit(1)

    try:
        import winreg

        # Open the Windows Registry key for the hosts entry
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters")

        # Read the existing value of the "DataBasePath" entry
        data_path, _ = winreg.QueryValueEx(key, "DataBasePath")

        # Construct the full path to the hosts file
        hosts_path = os.path.join(data_path, "hosts")

        # Add the entry to the hosts file
        with open(hosts_path, 'a') as hosts_file:
            hosts_file.write(f'127.0.0.1 {site_name}\n')

        print("Hosts entry added successfully.")
    except Exception as e:
        print(f"Error: {e}")

# Function to add entry to /etc/hosts on Unix-based systems
def add_host_entry_unix(site_name):
    hosts_path = '/etc/hosts'
    with open(hosts_path, 'a') as hosts_file:
        hosts_file.write(f'127.0.0.1 {site_name}\n')

def enable_wordpress_site(site_name):
    # Start the Docker containers for the site
    subprocess.run(['docker-compose', 'up', '-d'], cwd=site_name, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"WordPress site '{site_name}' is now enabled and running!")

def disable_wordpress_site(site_name):
    # Stop and remove the Docker containers for the site
    subprocess.run(['docker-compose', 'down'], cwd=site_name, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"WordPress site '{site_name}' is now disabled and stopped!")

def delete_wordpress_site(site_name):
    # Stop and remove the Docker containers for the site
    subprocess.run(['docker-compose', 'down'], cwd=site_name, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Delete the site directory and its contents
    try:
        shutil.rmtree(site_name)
        print(f"WordPress site '{site_name}' is deleted successfully!")
    except FileNotFoundError:
        print(f"WordPress site '{site_name}' does not exist.")
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage WordPress sites with Docker.")
    parser.add_argument("site_name", help="Name of the WordPress site")
    parser.add_argument("action", choices=["create", "enable", "disable", "delete"], help="Action to perform: create, enable, disable, or delete")

    args = parser.parse_args()

    if args.action == "create":
        check_dependencies()
        create_wordpress_site(args.site_name)
        print(f"Please wait for a moment while the site is being set up...")
        print("Opening the site in your default browser...")
        webbrowser.open(f"http://{args.site_name}")
    elif args.action == "enable":
        enable_wordpress_site(args.site_name)
    elif args.action == "disable":
        disable_wordpress_site(args.site_name)
    elif args.action == "delete":
        delete_wordpress_site(args.site_name)
    else:
        print("Invalid action. Please use 'create', 'enable', 'disable', or 'delete' as the action.")
