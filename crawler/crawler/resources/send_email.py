import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from crawler.settings import settings


# Replace sender@example.com with your "From" address.
# This address must be verified with Amazon SES.
def send_email(settings):
    SENDER = settings.SENDER

    # Replace recipient@example.com with a "To" address. If your account
    # is still in the sandbox, this address must be verified.
    RECIPIENT = settings.RECIPIENT

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    CONFIGURATION_SET = "ConfigSet"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = settings.AWS_REGION

    # The subject line for the email.
    SUBJECT = "M3HN Recommendation Service - Cralwer has been finished running"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = """
    Dear M3HN Recommendation Service Customer,

    The crawling job that you create have been finished running. Please have a check.

    Sincerely,

    The M3HN Recommendation Service Team.

    """

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    AWS_ACCESS_KEY = settings.AWS_ACCESS_KEY
    client = boto3.client('ses', region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY,
                          aws_secret_access_key=AWS_SECRET_KEY)

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
