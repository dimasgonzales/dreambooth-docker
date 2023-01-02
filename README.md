# Dreambooth Container Tests
A repo to help documenent a containerized workflow for `Stable-Diffusion` + `Dreambooth` with AWS resources(e.g.: AWS ECR, AWS Batch).

## Makefile Commands


- `make build`
  Build target docker image. Automatically tags image(ie: Date.buildrun e.g.: 20221127.1 for the first run of the day on 2022/11/27). Required parameter TARGET_CONTAINER
- `make run`
  Run the target docker image. Remove after execution. Required parameter TARGET_CONTAINER
- `make test`
  Build and then run target docker image. Required parameter TARGET_CONTAINER
- `make push`
  Build and then run target docker image. Required parameter TARGET_CONTAINER

### Examples
You must pass the runtime arguements to the make instructions as environment variables.
```bash
# build dreambooth image, with persistant environment variable
export TARGET_CONTAINER=dreambooth 
make build

# build dreambooth image, with session environment variable
TARGET_CONTAINER=dreambooth make build

# "test" rule (build and run) pytorchsandbox
TARGET_CONTAINER=pytorchsandbox make test
```


### Push Commands
```bash
aws ecr get-login-password | docker login --username AWS --password-stdin $amazon_url
```

```bash
aws ecr get-login-password | docker login --username AWS --password-stdin 953370256968.dkr.ecr.us-east-1.amazonaws.com/pytorchsandbox
docker run -it --gpus=all --ipc=host 953370256968.dkr.ecr.us-east-1.amazonaws.com/pytorchsandbox
```