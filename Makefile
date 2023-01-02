# make simple interface for instructions
# defaults to start the test instruction

default: test

test: build run
	echo "Testing docker image"

build: dockerlogin
	echo "Building docker image"
	docker build docker/$(TARGET_CONTAINER) --tag $(TARGET_CONTAINER)
	docker tag $(TARGET_CONTAINER):latest "$(AWS_ACCOUNT_ID).dkr.ecr.us-east-1.amazonaws.com/$(TARGET_CONTAINER):latest"

run:
	echo "Running docker image"
	docker run --name $(TARGET_CONTAINER)_cntnr -it --rm $(TARGET_CONTAINER)

push: build
	echo "Pushing docker image to AWS ECR"
	docker push $(AWS_ACCOUNT_ID).dkr.ecr.us-east-1.amazonaws.com/$(TARGET_CONTAINER):latest

dockerlogin:
	echo "Log in to AWS ECR"
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $(AWS_ACCOUNT_ID).dkr.ecr.us-east-1.amazonaws.com

calcversion:
	echo "Calculate the appropriate version/tag for the container"
	export IMAGE_TAG='20221227.1'

trainstack:
	python scripts/deploy_cloudformation_stack.py cloudformation/SDTrainingStack.json

startsandbox:
	python scripts/deploy_cloudformation_stack.py cloudformation/SDEC2Sandbox.json