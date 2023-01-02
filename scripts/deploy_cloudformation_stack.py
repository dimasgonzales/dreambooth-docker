import boto3
from botocore.exceptions import ClientError
import click
import logging
import time
import os

logging.basicConfig(level=logging.INFO)

CFT_CLIENT = boto3.client("cloudformation")


def get_cft_stacks():
    for root, folders, files in os.walk("cloudformation"):
        for file in files:
            cft_filepath = os.path.join(root, file)
            stack_name = os.path.splitext(file)[0]
            yield stack_name, cft_filepath


def publish_cft_stack(stack_name, cft_stack_filepath):
    cft_body = _get_stack_body(cft_stack_filepath)
    stack_exists, stack_status = _does_stack_exist(stack_name)

    if stack_exists and stack_status in ("ROLLBACK_COMPLETE"):
        logging.info(
            f"Deleting existing stack '{stack_name}' in order to deploy updated definition as a new stack"
        )
        aws_response = CFT_CLIENT.delete_stack(
            StackName=stack_name,
        )
        stack_exists, stack_status = _does_stack_exist(stack_name)
        while stack_exists:
            logging.info(
                "Delete request sent. Waiting 30 seconds to retry stack creation"
            )
            logging.info(f"Stack Status: '{stack_status}'.")
            time.sleep(30)
            stack_exists, stack_status = _does_stack_exist(stack_name)

    if stack_exists:
        try:
            logging.info(f"Updating existing stack '{stack_name}'")
            aws_response = CFT_CLIENT.update_stack(
                StackName=stack_name,
                TemplateBody=cft_body,
                Capabilities=[
                    "CAPABILITY_NAMED_IAM",
                ],
            )
        except ClientError as ex:
            error_message = ex.response["Error"]["Message"]
            if error_message == "No updates are to be performed.":
                logging.debug(
                    f"Error caught updating stack '{stack_name}'. "
                    "Stack doesn't have changes to apply."
                )
            else:
                logging.exception(
                    f"Unknown error caught while attempting to update stack '{stack_name}'."
                )
                raise ex
    else:
        logging.info(f"Creating new stack '{stack_name}'")
        aws_response = CFT_CLIENT.create_stack(
            StackName=stack_name,
            TemplateBody=cft_body,
            Capabilities=[
                "CAPABILITY_NAMED_IAM",
            ],
        )


def _get_stack_body(cft_stack_filepath):
    with open(cft_stack_filepath, "r") as infile:
        body = infile.read()

    _ = CFT_CLIENT.validate_template(TemplateBody=body)
    return body


def _does_stack_exist(name):
    stack_exists = True
    stack_status = None
    try:
        data = CFT_CLIENT.describe_stacks(StackName=name)
        stack_status = data["Stacks"][0]["StackStatus"]
    except ClientError:
        stack_exists = False
    return stack_exists, stack_status


@click.command()
@click.argument('target_stack_filepath')
def main(target_stack_filepath):
    if target_stack_filepath and target_stack_filepath.startswith("cloudformation/"):
        stack_name = target_stack_filepath.split("cloudformation/")[1].split(".json")[0]
        logging.info(f"Publishing a single stack: '{stack_name}'")
        publish_cft_stack(stack_name, target_stack_filepath)
    

if __name__ == "__main__":
    logging.info(f"Starting script '{__file__}'")
    main()
    logging.info(f"Finished script '{__file__}'")
