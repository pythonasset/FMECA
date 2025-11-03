# Docker Setup Guide

This guide explains how to run the FMECA & RCM Analysis Tool using Docker.

## Prerequisites

- Docker installed on your system ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose (included with Docker Desktop)

## Quick Start

### Option 1: Using Docker Compose (Recommended)

1. **Build and start the application:**
   ```bash
   docker-compose up --build
   ```

2. **Access the application:**
   Open your browser to [http://localhost:8501](http://localhost:8501)

3. **Stop the application:**
   Press `Ctrl+C` in the terminal, then run:
   ```bash
   docker-compose down
   ```

### Option 2: Using Docker CLI

1. **Build the Docker image:**
   ```bash
   docker build -t fmeca-rcm-tool .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8501:8501 --name fmeca-app fmeca-rcm-tool
   ```

3. **Access the application:**
   Open your browser to [http://localhost:8501](http://localhost:8501)

4. **Stop the container:**
   ```bash
   docker stop fmeca-app
   docker rm fmeca-app
   ```

## Advanced Usage

### Run in Detached Mode (Background)

```bash
docker-compose up -d
```

View logs:
```bash
docker-compose logs -f
```

### Mount Local Directory for Development

The docker-compose.yml is already configured to mount the local directory, allowing you to make changes and see them reflected immediately (with Streamlit's auto-reload).

### Custom Port

To use a different port (e.g., 8080):

**Docker Compose:**
Edit `docker-compose.yml` and change the ports mapping:
```yaml
ports:
  - "8080:8501"
```

**Docker CLI:**
```bash
docker run -p 8080:8501 --name fmeca-app fmeca-rcm-tool
```

### Data Persistence

To persist exported data and uploaded files, create a volume:

```bash
docker run -p 8501:8501 -v $(pwd)/data:/app/data --name fmeca-app fmeca-rcm-tool
```

## Troubleshooting

### Port Already in Use

If port 8501 is already in use, change the port mapping as described above.

### Container Won't Start

Check logs:
```bash
docker-compose logs
```

Or for Docker CLI:
```bash
docker logs fmeca-app
```

### Permission Issues

If you encounter permission issues with mounted volumes, ensure Docker has access to the directory.

### Rebuild After Changes

If you modify the Dockerfile or requirements.txt:
```bash
docker-compose up --build
```

## Production Deployment

For production deployment:

1. **Remove volume mounts** from docker-compose.yml (comment out the volumes section)
2. **Build optimized image:**
   ```bash
   docker build -t fmeca-rcm-tool:production .
   ```

3. **Use environment-specific configuration** if needed
4. **Consider using a reverse proxy** (nginx, Traefik) for SSL/TLS

## Health Check

The container includes a health check that verifies the application is running:

```bash
docker ps
```

Look for "healthy" status in the STATUS column.

## Useful Commands

```bash
# View running containers
docker ps

# View all containers (including stopped)
docker ps -a

# View logs
docker-compose logs -f fmeca-app

# Execute command in running container
docker exec -it fmeca-app bash

# Remove all stopped containers
docker container prune

# Remove unused images
docker image prune
```

## Security Notes

- The application runs on port 8501 by default - ensure appropriate firewall rules
- For production, consider using HTTPS with a reverse proxy
- Update the base image regularly for security patches
- Review and customize the .dockerignore file for your needs
