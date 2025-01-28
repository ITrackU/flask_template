#!/bin/bash

check() {
    # Get the containers (skip the header and take image names only)
    docker_list="$(docker ps -a --format '{{.Names}}')"
    flask_docker="flask-secure-web-app"

    # Check if the flask_docker image is already present
    image_exists=0
    if docker images | awk 'NR>1 {print $1}' | grep -q "^$flask_docker$"; then
       image_exists=1
       echo "Flask Secure Web App is already built"
    fi

    # Check if the flask_docker container is already running or exists
    container_exists=0
    for docker in $docker_list; do
        if [[ $docker == $flask_docker ]]; then
           container_exists=1
           echo "Container already exists!"
           break
       fi
    done
}

launch() {
    # Build the Docker image if it's not already in the list
    if [[ $image_exists -eq 0 ]]; then
        docker build -t "$flask_docker:latest" .
        echo "Flask docker image has been successfully built"
    fi
    # Run the Docker container if it's not already running
    if [[ $container_exists -eq 0 ]]; then
        docker run --name $flask_docker -d -p 9090:9090 $flask_docker
        echo "Flask Secure Web App has been successfully launched!"
    else
        if docker ps --filter "name=$flask_docker" --filter "status=running" --format "{{.Names}}" | grep -q "^$flask_docker$"; then
            echo "Flask Secure Web App is already running!"
        else
            docker start $flask_docker
            echo "Flask Secure Web App has been successfully launched!"
        fi
    fi
}

erase() {
    docker stop $flask_docker
    docker rm $flask_docker
    docker rmi "$flask_docker:latest"
    echo "Flask Secure Web App has been erased ! Ready to update"
}

help() {
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Options:"
    echo "  -u    Update the Flask app (erase, rebuild, and restart the container)"
    echo "  -r    Remove the Flask app (stop and remove the container and image)"
    echo "  -h    Display this help message"
    echo
    echo "If no options are provided, the script will check and launch the Flask app."
}

# Analyze options
while getopts "u" opt; do
    case ${opt} in
        u)
            check
            erase
            check
            launch
            ;;
        r)
            check
            erase
            ;;
        h)
            help
            ;;
        \?)
            echo "Invalid option"
            exit 1
            ;;
    esac
done

# Run the launch function if no options are provided
if [[ $OPTIND -eq 1 ]]; then
    check
    launch
fi
