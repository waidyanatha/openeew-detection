## Usage

```shell script
docker run \
  --interactive \
  --tty \
  --detach \
  --env port=1883 \
  --env username=admin \
  --env password=admin \
  --publish 1883:1883 \
  openeew-detection:0.0.1
```
