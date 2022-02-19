import os
import traceback
from datetime import datetime
import smtplib
import mimetypes
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from dotenv import load_dotenv
from django.shortcuts import render


load_dotenv()


class Email():

    
    def __init__(self,
            user: str,
            domain: str,
            password: str,
            server: list
            ):
        self.user = user
        self.domain = domain
        self.from_address = f"{user}@{domain}"
        if not password:
            password = os.getenv("MAIL_VALIDATION_PASSWORD")
        self.to_addresses = list()
        self.subject = str()
        self.content = MIMEMultipart() #.set_charset("utf-8")
        self.message = str()
        self.rendered = str()
        self.context = dict()
        self.template_path = str()
        self.template = str()
        self.server_address = server[0]
        self.server_port = server[1]

        self.connect(
            self.user,
            self.domain,
            password,
            server
        )
    
    def duplicate(self, password: str):
        return self.__init__(
            self.user,
            self.domain,
            password,
            [self.server_address, self.server_port]
        )
    
    def create_localserver(self, password: str="", port: int=1025):
        import subprocess
        command = f"sudo python -m smtpd -c DebuggingServer -n localhost:{port}"
        #subprocess.Popen(args=command.split(),stdin=subprocess.PIPE).communicate(input=password)
        with subprocess.Popen(command.split(),
                stdin=subprocess.PIPE,
                universal_newlines=True) as process:
            print(password, file=process.stdin) # provide answer
            process.stdin.flush()

    def connect(self,
            user: str,
            domain: str,
            password: str,
            server: list=['smtp.gmail.com', 587]):
        SMTPFailedException = smtplib.SMTPConnectError
        try:
            self.user = user
            self.domain = domain
            self.from_address = f'{user}@{domain}'
            self.server_address = server[0]
            self.server_port = server[1]
            self.connection = smtplib.SMTP(
                self.server_address,
                self.server_port
                )
            self.connection.ehlo()
            self.connection.starttls()  # Enables security
            self.connection.ehlo()
            if all([self.from_address, password]):
                self.connection.login(
                    self.from_address,
                    password
                )
                return True
            return False

        except Exception as Error: # noqa

            print(traceback.format_exc())
            raise SMTPFailedException(0, 'Failed to login to SMTP')
    
    def create(self, to_addresses: list=[], subject: str=""):
        try:
            self.to_addresses = self.to_addresses if not to_addresses else to_addresses
            self.subject = self.subject if not subject else subject

            self.content = MIMEMultipart() #set_charset("utf-8")
            self.content['From'] = self.from_address
            if type(self.to_addresses) == str:
                self.content['To'] = self.to_addresses
            elif type(self.to_addresses) == list and len(self.to_addresses) > 1:
                self.content['To'] = ', '.joint(self.to_addresses)
            else:
                self.content['To'] = self.to_addresses[0]
            self.content['Subject'] = self.subject

            return True
        except Exception as _Error: # noqa
            print(f"Report: {traceback.format_exc()}.")
    
    def write_by_text(self, message: str=""):
        self.message = self.message if not message else message
        text = MIMEText(self.message, 'plain')
        self.content.attach(text)
    
    def write_by_template(self,
            app=None,
            context: dict={},
            template: str='',
            template_path: str=''):
        try:
            self.template = self.template if not template else template
            self.template_path = self.template_path if not template_path else template_path
            if not self.template_path: self.template_path = os.getcwd()+'/'
            else:
                if self.template_path[-1]!='/': self.template_path += '/'
            # Flask integration
            if app:
                self.rendered = render(template, **context)
                email_message = MIMEText(self.rendered, 'html')
                self.content.attach(email_message)
            else:
                if os.path.exists(self.template_path + self.template):
                    with open(self.template_path + self.template, 'r') as _file:
                        self.html = _file.read()
                    self.rendered = self.html # not rendering, should
                    email_message = MIMEText(self.rendered, 'html')
                    self.content.attach(email_message)
        except Exception as _Error: #noqa
            print(f"Report: {traceback.format_exc()}.")
    
    def send_email(self,
            to_addresses: list=[],
            subject: str="",
            content: str=""):
        """Sends template email to given address."""
        try:
            message = MIMEMultipart()
            message['From'] = self.from_address
            message['To'] = to_addresses
            message['Subject'] = subject
            message.attach(MIMEText(content, 'html'))
            text = message.as_string()
            self.connection.sendmail(self.from_address, to_addresses, text)
            #self.sent_today += 1
            #self.mongo_interface.update_email_as_sent(to_addresses)
            #self.mongo_interface.update_count(self.username, self.sent_today)
            return {'success': True, 'address': to_addresses}
        except (smtplib.SMTPRecipientsRefused, UnicodeEncodeError):    # noqa
            #self.logger.debug("Server Refused to send: {}".format(to_addresses))
            #self.mongo_interface.update_email_status(
            #    to_addresses,
            #    self.mongo_interface.INVALID)
            return {'success': False, 'address': to_addresses}
        except Exception as _Error: #noqa
            print(f"Report: {traceback.format_exc()}.")
    
    def send_raw_email(self,
            from_address: str="",
            to_addresses: list=[],
            subject: str="<no-reply>",
            text: str='',
            template: str='__template__',
            html: str='',
            context: dict={},
            attachment_folder: str="files",
            attachment: str='',
            ):
        """static method: send => bool response_status"""
        try:
            # PROCESS INPUT
            source = from_address or self.from_address
            destination = to_addresses \
                if type(to_addresses) is list \
                else [to_addresses]
            directory = os.getcwd()
            if template != '__template__':
                if template.find('/') == -1 \
                        or template.find('\\') == -1:
                    templatepath = os.path.join(
                        directory,
                        "templates",
                        template
                    )
            if not html and os.path.exists(templatepath):
                with open(templatepath, 'r') as file:
                    html = file.read()
            if html and context:
                html = render(context, html) #flask is render_template
            if attachment:
                if attachment.find('/') == -1 \
                        and attachment.find('\\') == -1:
                    attachment = os.path.join(
                        directory, 
                        attachment_folder,
                        attachment
                    )
            
            # MAIL COMPOSE
            message = MIMEMultipart('mixed')
            message['Subject'] = subject
            message['From'] = source
            try:
                message['To'] = ', '.join(destination)
            except:
                to_addresses = [str(address) \
                    for address in destination]
                message['To'] = ', '.join(destination)
            msg_body = MIMEMultipart('alternative')
            if text:
                textpart = MIMEText(
                    text.encode("utf-8"),
                    'plain',
                    "utf-8"
                )
                msg_body.attach(textpart)
            if html:
                htmlpart = MIMEText(
                    html.encode("utf-8"),
                    'html',
                    "utf-8"
                )
                msg_body.attach(htmlpart)
            message.attach(msg_body)
            message.add_header(
                'Cache-Control',
                'no-store, no-cache, must-revalidate, max-age=0'
            )
            message.add_header(
                'Cache - Control',
                'post - check = 0, pre - check = 0'
            )
            message.add_header('Pragma', 'no-cache')
            if attachment:
                attached = MIMEApplication(
                    open(attachment, 'rb').read()
                )
                attached.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename=os.path.basename(attachment)
                )
                message.attach(attached)
            
            self.connection.sendmail(
                source,
                destination,
                message.as_string()
            )
            return True

        except Exception as Error: #noqa

            print(traceback.format_exc())
            return False
    
    def send(self):
        try:
            text = self.content.as_string()
            self.connection.sendmail(
                self.from_address,
                self.to_addresses,
                text)
            #self.sent_today += 1
            #self.mongo_interface.update_email_as_sent(to_addresses)
            #self.mongo_interface.update_count(self.username, self.sent_today)
            return {'success': True, 'address': self.to_addresses}
        except (smtplib.SMTPRecipientsRefused, UnicodeEncodeError):    # noqa
            #self.logger.debug(f"Server Refused to send: {to_addresses}")
            #self.mongo_interface.update_email_status(to_addresses, self.mongo_interface.INVALID)
            return {'success': False, 'address': self.to_addresses}
        except Exception as _Error: #noqa
            print(f"Report: {traceback.format_exc()}.")

    def finish(self):
        self.connection.quit()
        self.connection.close()


## UNIT-TESTING

if __name__ == '__main__':
    try:
        email = Email(
            user="esganadinhoneto",
            domain="gmail.com",
            password="Intexfy7799",
            server=['localhost', 1025])
        email.create(to_addresses="alves.engleandro@gmail.com", subject="test 1")
        
        path = os.getcwd()
        print(f'path>{path}'); os.chdir('..')
        print(f'path>{os.getcwd()}'); os.chdir(path)

        email.write_by_template(template='new_list.html')

        email.send()
        email.finish()

    except Exception as _Error:
        print(f"Report: {traceback.format_exc()}.")








"""
        #def write_by_template(self, context
        #self.template = self.template if not template else template
        #'//'.join(os.path.abspath(__name__).split(r'/')[0:-3].append("//templates"))
        #if self.template: self.html = open(self.template, 'r')
        #else: self.html = open('../../../templates/email.html', 'r'
        # render with jinja
        #from jinja2 import Template
        #t = Template("Hello {{ something }}!")
        #t.render(**self.context)
"""



"""
# SUBPROCESS
subprocess.run(["ls", "-l"], capture_output=False, shell=False, check=False) # default, not capture output
subprocess.run(["ls", "-l"], capture_output=True, shell=True, check=True)
subprocess.run(
    args,
    *,
    stdin=None,
    input=None,
    stdout=None,
    stderr=None,
    capture_output=False,
    shell=False,
    cwd=None,
    timeout=None, # in seconds
    check=False,
    encoding=None,
    errors=None,
    text=None,
    env=None,
    universal_newlines=None,
    **other_popen_kwargs)
# For advance: use the interface subprocess.Popen
"""



"""
def using_ssl():
    try:
        server = SMTP_SSL(host='smtp.gmail.com', port=465, context=create_default_context())
        server.login(sender, password)
        server.send_message(msg=msg)
        server.quit()
        server.close()
    except SMTPAuthenticationError:
        print('Login Failed')

def using_tls():
    try:
        server = SMTP(host='smtp.gmail.com', port=587)
        server.starttls(context=create_default_context())
        server.ehlo()
        server.login(sender, password)
        server.send_message(msg=msg)
        server.quit()
        server.close()
    except SMTPAuthenticationError:
        print('Login Failed')
"""