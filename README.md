# Docker WordPress Manager

This is a command-line script written in Python to manage WordPress sites using Docker and a LEMP stack (Linux, Nginx, MySQL, PHP). The script allows you to create, enable, disable, and delete WordPress sites inside Docker containers, providing an isolated and convenient way to work with WordPress.

## Prerequisites

Before using this script, ensure that you have the following prerequisites installed on your system:

1. **Docker**: Docker is required to run containers. Follow the official documentation to install Docker for your operating system:
   - Docker Desktop for macOS and Windows: [Docker Desktop](https://www.docker.com/products/docker-desktop)
   - Docker for Linux: Follow the instructions for your specific Linux distribution.

2. **Docker Compose**: Docker Compose is required to manage multi-container applications. Follow the official documentation to install Docker Compose:
   - Docker Compose installation guide: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

1. Clone or download this repository to your local machine.

2. Open a terminal or command prompt and navigate to the directory where you saved the `wordpress_manager.py` script.

3. Ensure the script has the necessary permissions to execute. If needed, run the following command to make the script executable:
   ```bash
   chmod +x wordpress_manager.py
   ```
   
4. Now you are ready to use the script to manage WordPress sites.

## Usage

### Step 1: Check Dependencies

Before creating or managing a WordPress site, check if Docker and Docker Compose are installed on your system. Run the following command:
```bash
python wordpress_manager.py check
```

### Step 2: Create a New WordPress Site
To create a new WordPress site with a LEMP stack, use the following command:
```bash
python wordpress_manager.py create <site_name>
```
Replace <site_name> with your desired site name (e.g., mywordpresssite). This will create a new directory with the given site name and set up the LEMP stack inside Docker containers.

### Step 3: Enable a WordPress Site
To enable/start a previously created WordPress site, use the following command:
```bash
python wordpress_manager.py enable <site_name>
```

Replace <site_name> with the name of the site you want to enable.

### Step 4: Disable a WordPress Site
To disable/stop a running WordPress site, use the following command:

```bash
python wordpress_manager.py disable <site_name>
```

Replace <site_name> with the name of the site you want to disable.


### Step 5: Delete a WordPress Site
To delete an existing WordPress site (including containers and local files), use the following command:
```bash
python wordpress_manager.py delete <site_name>
```
Replace <site_name> with the name of the site you want to delete.

## Troubleshooting
If you encounter any issues while running the script, please check the following:
- Ensure you have followed the prerequisites installation steps and have Docker and Docker Compose installed on your system.
- Make sure the wordpress_manager.py script has the necessary permissions to execute.
- If you are running on Windows, ensure you run the script with administrator privileges when required (e.g., when adding entries to the hosts file).

## Conclusion
With this Python script, you can easily manage WordPress sites with Docker and the LEMP stack using a command-line interface. The script handles all the Docker-related tasks and configurations, making it straightforward to create, enable, disable, and delete WordPress sites with ease.

Enjoy managing your WordPress sites efficiently with Docker! If you have any feedback or encounter any issues, feel free to raise an issue or reach out for support. Happy coding!
