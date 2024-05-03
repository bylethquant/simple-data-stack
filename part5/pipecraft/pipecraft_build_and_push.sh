# define the image name, tag, and dockerfile name
CONTAINER_REGISTRY="ghcr.io/bylethquant/"
IMAGE_NAME="sds-pipecraft"
TAG="latest"
DOCKERFILE_NAME="pipecraft.Dockerfile"

# build the docker image
docker build -t $CONTAINER_REGISTRY$IMAGE_NAME:$TAG -f $DOCKERFILE_NAME .

# push the docker image to the repository
docker push $CONTAINER_REGISTRY$IMAGE_NAME:$TAG
