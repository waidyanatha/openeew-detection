## Build the Docker image

```shell script
cd algorithms
docker build --tag openeew-detection:0.0.1 .
```

## Usage

```shell script
docker run \
  --interactive \
  --tty \
  --detach \
  --env username=admin \
  --env password=admin \
  --publish 1883:1883 \
  openeew-detection:0.0.1
```
