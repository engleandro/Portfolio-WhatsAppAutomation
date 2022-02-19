import os, sys
import logging, traceback
from datetime import datetime
import json
import dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# add to requirements import pytest, boto3 

from flask import render_template
#from flask_restx import Namespace, Resource, reqparse

import boto3
from botocore.config import Config as ConfigBoto3
from botocore.exceptions import ClientError

dotenv.load_dotenv()

class AWS(): # import AWS in the future

    AWS_SERVICE = {
        "instance": "ec2",
        "email": 'ses',
        "storage": "s3",
        "default": "ses",
        }
    CHARSET = {
        'default': 'UTF-8',
        }
    CONFIG = {
        "default": "ConfigSet",
        }
    LANGUAGE = {
        "default": "pt-br",
        }
    REGION_NAME = {
        "default": "us-east-1",
        }


class SES(AWS):
    """Class SES - Simple Email Service (AWS) Object
    Returns:
        AWS Client: A connection with Simple Email Service (SES) on AWS.
    """


    # SETTINGS OPTIONS
    SMTP_SERVER = {
        'aws-us-east-1': ['email-smtp.us-east-1.amazonaws.com', 587],
        'gmail.com': ['smtp.gmail.com', 587],
        'hotmail.com': [None, None],
        'outlook.com': [None, None],
        'default': ['smtp.gmail.com', 587],
        }
    

    # STANDARD CONFIG
    DEFAULT_SETTINGS = {
        'charset': 'UTF-8',
        'config': 'ConfigSet',
        'language': 'pt-br',
        'region_name': 'us-east-1',
        'aws_service': 'ses',
        }
    DEFAULT_CONFIG = {
        'region_name': 'us-east-1',
        'signature_version': 'v4',
        's3': {},
        'proxies': {},
        'proxies_config': {},
        'retries': {'max_attempts': 2, 'mode': 'standard'},
        }
    
    # CONTRUCTORS
    def __init__(self,
            user: str="no-reply",
            domain: str="intexfy.com",
            settings: dict={'region_name': 'us-east-1'},
            ):
        """Constructor __init__ => SES Object"""
        self.user = user
        self.domain = domain
        self.from_address = f"{user}@{domain}"
        #self.config = SES.to_config(settings)
        self.region_name = 'us-east-1' # self.region_name = self.config.region_name 
        
        print(os.getenv('AWS_ACCESS_KEY_ID'))
        print(os.getenv('AWS_SECRET_ACCESS_KEY'))
        
        self.client = boto3.client('ses',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name='us-east-1')
            #config=self.config)
        self.logger = logging.getLogger(f'app.ses::{self.from_address}')
        self.buffer = None
    

    # CLASS METHODS
    @classmethod
    def to_config(cls, settings: dict):
        """class method: to_config(settings: dic) => obj ConfigBoto3
        Args:
            settings (dict, optional): [description]. Defaults to {'region_name': 'us-east-1'}.
        Returns:
            [type]: [description]
        """
        settings = settings or SES.DEFAULT_CONFIG
        boto_settings = {
            'region_name': settings.get('region_name') or 'us-east-1',
            'signature_version': settings.get('signature_version') or 'v4',
            's3': settings.get('s3') or {},
            'proxies': settings.get('proxies') or {},
            'proxies_config': settings.get('proxies_config') or {},
            'retries': settings.get('retries') or {'max_attempts': 2, 'mode': 'standard'},
            }
        return ConfigBoto3(**boto_settings)
        #proxies = dict:{'https': 'https://proxy.amazon.org:2010'}
    
    @classmethod
    def get_client(cls, settings: dict={'region_name': "us-east-1"}):
        """static method: SES.get_client => obj ClientBoto3
        Args:
            settings (dict, optional): [description]. Defaults to {'region_name': "us-east-1"}.
        Returns:
            [type]: [description]
        """
        boto_config = cls.to_config(settings)
        object = boto3.client('ses',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            config=boto_config)
        return object
    

    # STATIC METHODS
    def to_config(self, settings: dict={}):
        my_config = SES.to_config(settings)
        self.config = my_config
        #return my_config
    
    def connect(self, service: str='ses',
            settings: dict={'region_name': "us-east-1"}):
        """staticmethod: client => attribute obj SES
        Args:
            service (str, optional): [description]. Defaults to 'ses'.
            settings (dict, optional): [description]. Defaults to {'region_name': "us-east-1"}.
        """
        boto_config = SES.to_config(settings)
        self.client = boto3.client(service,
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            config=boto_config)
    
    def get_client(self, service: str='ses',
            settings: dict={'region_name': "us-east-1"}):
        """staticmethod: SES.set_client => obj ClientBoto3
        Args:
            service (str, optional): AWS Services. Defaults to 'ses'.
            settings (dict, optional): [description]. Defaults to {'region_name': "us-east-1"}.
        Returns:
            [type]: [description]
        """
        boto_config = SES.to_config(settings)
        object = boto3.client(service,
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            config=boto_config)
        return object
    
    def verify_email_identity(self, email_address: str=""):
        """static method
        Args:
            email_address (str, optional): [description]. Defaults to "".
        Returns:
            [type]: [description]
        """
        email_address = email_address or self.from_address
        response = self.client.verify_email_identity(
            EmailAddress=email_address)
        return response
    
    def send_by_template(self,
            from_address: str="",
            to_addresses: list=[],
            subject: str="<no-reply>",
            template: str="",
            ):
        """static method: send_by_html => bool response_status
        response = client.send_email(
            Source='string',
            Destination={
                'ToAddresses': [
                    'string',
                ],
                'CcAddresses': [
                    'string',
                ],
                'BccAddresses': [
                    'string',
                ]
            },
            Message={
                'Subject': {
                    'Data': 'string',
                    'Charset': 'string'
                },
                'Body': {
                    'Text': {
                        'Data': 'string',
                        'Charset': 'string'
                    },
                    'Html': {
                        'Data': 'string',
                        'Charset': 'string'
                    }
                }
            },
            ReplyToAddresses=[
                'string',
            ],
            ReturnPath='string',
            SourceArn='string',
            ReturnPathArn='string',
            Tags=[
                {
                    'Name': 'string',
                    'Value': 'string'
                },
            ],
            ConfigurationSetName='string')
        """
        try:
            if os.path.exists(template):
                with open(template, 'r') as file:
                    html = file.read()
            source = from_address or self.from_address
            destination = {'ToAddresses': to_addresses or self.to_addresses}
            message = {
                'Subject': {'Data': subject,'Charset': 'UTF-8'},
                'Body': {'Html': {"Data": html,'Charset': 'UTF-8'} }
                }
            response = self.client.send_email(Source=source,
                Destination=destination, Message=message)
            return response
        except ClientError as Error:
            print(Error.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])
    
    def send_by_text(self,
            from_address: str="",
            to_addresses: list=[],
            subject: str='<no-reply>',
            text: str='Please, no reply this email.',
            template: str='',
            ):
        """staticmethod: send_by_text => bool response_status"""
        try:
            if not text and template:
                if os.path.exists(template):
                    with open(template, 'r') as file:
                        text = file.read()
            source = from_address or self.from_address
            destination = {'ToAddresses': to_addresses or self.to_addresses}
            message = {
                'Subject': {'Data': subject, 'Charset': 'UTF-8'},
                'Body': {'Text': {"Data": text, 'Charset': 'UTF-8'}}
                }
            response = self.client.send_email(Source=source,
                Destination=destination, Message=message)
            return response
        except ClientError as Error:
            print(Error.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])
    
    def send(self,
            from_address: str="",
            to_addresses: list=[],
            subject: str="<no-reply>",
            text: str='',
            template: str='__template__',
            html: str='',
            context: dict={},
            attachment: str='',
            ):
        """static method: send => bool response_status"""
        try:
            source = from_address or self.from_address
            destination = {'ToAddresses': to_addresses or self.to_addresses}
            dir = os.getcwd()
            if template != '__template__':
                if template.find('/') == -1:
                    templatepath = os.path.join(dir, "intexfyInternalPlatform/templates", template)
                elif template.find('\\') == -1:
                    templatepath = os.path.join(dir, "intexfyInternalPlatform/templates", template)
            if not html and os.path.exists(templatepath):
                with open(templatepath, 'r') as file:
                    html = file.read()
            if html and context:
                html = render_template(html, **context)
            message = {
                'Subject': {'Data': subject, 'Charset': 'UTF-8'},
                'Body': {}
                }
            if text: message.get('Body')['Text'] = {"Data": text, 'Charset': 'UTF-8'}
            if html: message.get('Body')['Html'] = {"Data": html, 'Charset': 'UTF-8'}
            response = self.client.send_email(
                Source=source,
                Destination=destination,
                Message=message
                )
            # ATTACHMENT
            return response
        except ClientError as Error:
            print(Error.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])


'''
    SENDER = "Sender Name <sender@example.com>"
    RECIPIENT = "recipient@example.com"
    CONFIGURATION_SET = "ConfigSet"
    AWS_REGION = "us-west-2"
    SUBJECT = "Customer service contact info"
    ATTACHMENT = "path/to/customers-to-contact.xlsx"
    BODY_TEXT = "Hello,\r\nPlease see the attached file for a list of customers to contact."
    BODY_HTML = """
        <html>
        <head></head>
        <body>
        <h1>Hello!</h1>
        <p>Please see the attached file for a list of customers to contact.</p>
        </body>
        </html>"""
    CHARSET = "utf-8"
    client = boto3.client('ses',region_name=AWS_REGION)
    msg = MIMEMultipart('mixed')
    msg['Subject'] = SUBJECT 
    msg['From'] = SENDER 
    msg['To'] = RECIPIENT
    msg_body = MIMEMultipart('alternative')
    textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
    htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)
    att = MIMEApplication(open(ATTACHMENT, 'rb').read())
    att.add_header('Content-Disposition','attachment',filename=os.path.basename(ATTACHMENT))
    msg.attach(msg_body)
    msg.attach(att)
    try:
        #Provide the contents of the email.
        response = client.send_raw_email(
            Source=SENDER,
            Destinations=[
                RECIPIENT
            ],
            RawMessage={
                'Data':msg.as_string(),
            },
            ConfigurationSetName=CONFIGURATION_SET
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])


    import os
    import boto3
    from botocore.exceptions import ClientError
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication

    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = "Sender Name <sender@example.com>"

    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT = "recipient@example.com"

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the 
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    CONFIGURATION_SET = "ConfigSet"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-west-2"

    # The subject line for the email.
    SUBJECT = "Customer service contact info"

    # The full path to the file that will be attached to the email.
    ATTACHMENT = "path/to/customers-to-contact.xlsx"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = "Hello,\r\nPlease see the attached file for a list of customers to contact."

    # The HTML body of the email.
    BODY_HTML = """\
    <html>
    <head></head>
    <body>
    <h1>Hello!</h1>
    <p>Please see the attached file for a list of customers to contact.</p>
    </body>
    </html>
    """

    # The character encoding for the email.
    CHARSET = "utf-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)

    # Create a multipart/mixed parent container.
    msg = MIMEMultipart('mixed')
    # Add subject, from and to lines.
    msg['Subject'] = SUBJECT 
    msg['From'] = SENDER 
    msg['To'] = RECIPIENT

    # Create a multipart/alternative child container.
    msg_body = MIMEMultipart('alternative')

    # Encode the text and HTML content and set the character encoding. This step is
    # necessary if you're sending a message with characters outside the ASCII range.
    textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
    htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)

    # Add the text and HTML parts to the child container.
    msg_body.attach(textpart)
    msg_body.attach(htmlpart)

    # Define the attachment part and encode it using MIMEApplication.
    att = MIMEApplication(open(ATTACHMENT, 'rb').read())

    # Add a header to tell the email client to treat this part as an attachment,
    # and to give the attachment a name.
    att.add_header('Content-Disposition','attachment',filename=os.path.basename(ATTACHMENT))

    # Attach the multipart/alternative child container to the multipart/mixed
    # parent container.
    msg.attach(msg_body)

    # Add the attachment to the parent container.
    msg.attach(att)
    #print(msg)
    try:
        #Provide the contents of the email.
        response = client.send_raw_email(
            Source=SENDER,
            Destinations=[
                RECIPIENT
            ],
            RawMessage={
                'Data':msg.as_string(),
            },
            ConfigurationSetName=CONFIGURATION_SET
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
'''



#===== METHODS =====#


if __name__ == '__main__':
    template = os.getcwd()
    os.chdir('../../../')
    try:
        ses = SES()
        response = ses.send(
            to_addresses=['alves.engleandro@gmail.com'],
            subject="LIST NOVA DE SMARTLEADS",
            template=os.getcwd() + '/templates/new_list.html'
            )
    except Exception:
        print(traceback.format_exc())













#===== BACKUP =====#


#logger = logging.getLogger(f'{function.__module__}:{function.__name__}')

"""
ses = SES(user="noreply", domain="intexfy.com.br")
#pprint(ses.config.region_name)
ses.send_by_html(to_addresses=['alves.engleandro@gmail.com'],subject='Teste',)



if not password:
    password = os.getenv("SES_PASSWORD")  # ALTER PSSWRD ON ENV FILE
self.to_addresses = list()
self.subject = str()
self.content = MIMEMultipart() #.set_charset("utf-8")
self.message = str()
self.rendered = str()
self.context = dict()
self.template_path = str()
self.template = str()
self.logger = logging.getLogger(f'app.account_manager_{user}@{domain}')
self.server_address = server[0]
self.server_port = server[1]
self.connect(self.user, self.domain, password, server)
"""


'''
SENDER = "Sender Name <sender@example.com>"
RECIPIENT = "recipient@example.com"
SUBJECT = "Amazon SES Test (SDK for Python)"
BODY_TEXT = ("Amazon SES Test (Python)\r\n"
    "This email was sent with Amazon SES using the "
    "AWS SDK for Python (Boto)."
    )
BODY_HTML = """<html>
<head></head>
<body>
<h1>Amazon SES Test (SDK for Python)</h1>
<p>This email was sent with
    <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
    <a href='https://aws.amazon.com/sdk-for-python/'>
    AWS SDK for Python (Boto)</a>.</p>
</body>
</html>
"""



client = boto3.client(
    'ses',
    region_name='us-east--1',
    aws_access_key_id='aws_access_key_string',
    aws_secret_access_key='aws_secret_key_string'
    )

def verify_email_identity():
    ses_client = boto3.client("ses", region_name="us-west-2")
    response = ses_client.verify_email_identity(
        EmailAddress="abhishek@learnaws.org"
    )
    print(response)

def send_email_ses_smtp():
    import smtplib  
    import email.utils
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    # Replace sender@example.com with your "From" address. 
    # This address must be verified.
    SENDER = 'sender@example.com'  
    SENDERNAME = 'Sender Name'

    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT  = 'recipient@example.com'

    # Replace smtp_username with your Amazon SES SMTP user name.
    USERNAME_SMTP = "smtp_username"

    # Replace smtp_password with your Amazon SES SMTP password.
    PASSWORD_SMTP = "smtp_password"

    # (Optional) the name of a configuration set to use for this message.
    # If you comment out this line, you also need to remove or comment out
    # the "X-SES-CONFIGURATION-SET:" header below.
    CONFIGURATION_SET = "ConfigSet"

    # If you're using Amazon SES in an AWS Region other than US West (Oregon), 
    # replace email-smtp.us-west-2.amazonaws.com with the Amazon SES SMTP  
    # endpoint in the appropriate region.
    HOST = "email-smtp.us-west-2.amazonaws.com"
    PORT = 587

    # The subject line of the email.
    SUBJECT = 'Amazon SES Test (Python smtplib)'

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Amazon SES Test\r\n"
                "This email was sent through the Amazon SES SMTP "
                "Interface using the Python smtplib package."
                )

    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
    <h1>Amazon SES SMTP Email Test</h1>
    <p>This email was sent with Amazon SES using the
        <a href='https://www.python.org/'>Python</a>
        <a href='https://docs.python.org/3/library/smtplib.html'>
        smtplib</a> library.</p>
    </body>
    </html>
                """

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT
    msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
    msg['To'] = RECIPIENT
    # Comment or delete the next line if you are not using a configuration set
    msg.add_header('X-SES-CONFIGURATION-SET',CONFIGURATION_SET)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(BODY_TEXT, 'plain')
    part2 = MIMEText(BODY_HTML, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Try to send the message.
    try:  
        server = smtplib.SMTP(HOST, PORT)
        server.ehlo()
        server.starttls()
        #stmplib docs recommend calling ehlo() before & after starttls()
        server.ehlo()
        server.login(USERNAME_SMTP, PASSWORD_SMTP)
        server.sendmail(SENDER, RECIPIENT, msg.as_string())
        server.close()
    # Display an error message if something goes wrong.
    except Exception as e:
        print ("Error: ", e)
    else:
        print ("Email sent!")

def send_regular_mail():
    return response = client.send_email(
        Destination={
            'ToAddresses': ['recipient1@domain.com', 'recipient2@domain.com'],
        },
        Message={
            'Body': {
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': 'email body string',
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': 'email subject string',
            },
        },
        Source='sender.email@domain.com',
    )

def send_attachment_email():
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication
    from email.mime.multipart import MIMEMultipartmessage = MIMEMultipart()
    message['Subject'] = 'email subject string'
    message['From'] = 'sender.email@domain.com'
    message['To'] = ', '.join(['recipient1@domain.com', 'recipient2@domain.com'])# message body
    part = MIMEText('email body string', 'html')
    message.attach(part)# attachment
    if attachment_string:   # if bytestring available
        part = MIMEApplication(str.encode('attachment_string'))
    else:    # if file provided
        part = MIMEApplication(open(attachment_file.csv, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename='name_of_attachment.csv')
    message.attach(part)response = client.send_raw_email(
        Source=message['From'],
        Destinations=['recipient1@domain.com', 'recipient2@domain.com'],
        RawMessage={
            'Data': message.as_string()
        }
    )

def send_plain_email():
    ses_client = boto3.client("ses", region_name="us-west-2")
    CHARSET = "UTF-8"

    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                "abhishek@learnaws.org",
            ],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": "Hello, world!",
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "Amazing Email Tutorial",
            },
        },
        Source="abhishek@learnaws.org",
    )


def send_html_email():
    ses_client = boto3.client("ses", region_name="us-west-2")
    CHARSET = "UTF-8"
    HTML_EMAIL_CONTENT = """
        <html>
            <head></head>
            <h1 style='text-align:center'>This is the heading</h1>
            <p>Hello, world</p>
            </body>
        </html>
    """

    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                "abhishek@learnaws.org",
            ],
        },
        Message={
            "Body": {
                "Html": {
                    "Charset": CHARSET,
                    "Data": HTML_EMAIL_CONTENT,
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "Amazing Email Tutorial",
            },
        },
        Source="abhishek@learnaws.org",
    )


# How to send an email with attachments using SES?
from email import encoders
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email_with_attachment():
    msg = MIMEMultipart()
    msg["Subject"] = "This is an email with an attachment!"
    msg["From"] = "abhishek@learnaws.org"
    msg["To"] = "abhishek@learnaws.org"

    # Set message body
    body = MIMEText("Hello, world!", "plain")
    msg.attach(body)

    filename = "document.pdf"  # In same directory as script

    with open(filename, "rb") as attachment:
        part = MIMEApplication(attachment.read())
        part.add_header("Content-Disposition",
                        "attachment",
                        filename=filename)
    msg.attach(part)

    # Convert message to string and send
    ses_client = boto3.client("ses", region_name="us-west-2")
    response = ses_client.send_raw_email(
        Source="abhishek@learnaws.org",
        Destinations=["abhishek@learnaws.org"],
        RawMessage={"Data": msg.as_string()}
    )
    print(response)

def create_custom_verification_email_template():
    ses_client = boto3.client('ses')
    response = ses_client.create_custom_verification_email_template(
        TemplateName="CustomVerificationTemplate",
        FromEmailAddress="abhishek@learnaws.org",
        TemplateSubject="Please confirm your email address",
        TemplateContent="""
            <html>
            <head></head>
            <h1 style='text-align:center'>Please verify your account</h1>
            <p>Before we can let you access our product, please verify your email</p>
            </body>
            </html>
        """,
        SuccessRedirectionURL="https://yourdomain.com/success",
        FailureRedirectionURL="https://yourdomain.com/fail"
    )
    print(response)

def send_custom_verification_email():
    ses_client = boto3.client("ses")
    response = ses_client.send_custom_verification_email(
        EmailAddress= "receipientemail@gmail.com",
        TemplateName= "CustomVerificationTemplate"
    )
    print(response)
'''