from os import environ
from time import monotonic, sleep
from traceback import format_exc

from rest_framework.views import APIView
from rest_framework.response import Response

from rest import Rest
from interfaces.whatsapp.whatsapp import WhatsApp
from interfaces.mail.mail import Email


def validateWhatsApp(
        whatsapp: WhatsApp,
        from_phone: str,
        email: str,
        timeout: float=15.0,
        through: str="SMTP"
        ):
    """docstring"""
    start = monotonic()
    try:
        user, domain = str(
            environ.get("MAIL_VALIDATION_ACCOUNT")
        ).split('@')

        mail = Email(
            user=user,
            domain=domain,
            password=environ.get("MAIL_VALIDATION_PASSWORD"),
            server=['gmail.smtp.com', 687]
        )

        whatsapp.toAccess()
        sleep(timeout)

        while (monotonic() - start) < 110*timeout:
            
            if not whatsapp.is_connected:
                whatsapp.toComment(comment='Printing screen...')
                whatsapp.takePrintScreen()
                
                whatsapp.toComment(comment='Sending email...')
                if through == "SMTP":
                    mail.send_raw_email(
                        to_addresses=[email],
                        subject="<NO-REPLY> WHATSAPP AUTHENTICATION IS REQUIRED",
                        template='whatsapp_validation.html',
                        attachment_folder="files",
                        attachment="screenshot.png"
                    )
                sleep(10*timeout)
                """
                    from django.core.mail import send_mail
                    send_mail(
                        'Subject',
                        "Please, no-reply, it's a test.",
                        'no-reply@intexfy.com',
                        ['alves.engleandro@gmail.com']
                    )
                """
                
                whatsapp.is_connected = whatsapp.toCheck()
                if whatsapp.is_connected:
                    whatsapp.dumpCookies()
                
                whatsapp.toAccess()
                sleep(timeout)

            elif whatsapp.is_connected:

                whatsapp.dumpCookies()
                return True

        return False

    except Exception: #noqa

        print(format_exc())
        return False


class SendMessageAPIView(APIView):

    #serializer_class=WABotMessageSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            to_phone = request.data.get("to_phone")
            message = request.data.get("message")
            email = environ.get('MAIL_VALIDATION_ACCOUNT')
            from_phone = environ.get('WHATSAPP_ACCOUNT')

            whatsapp = WhatsApp(
                from_phone=from_phone,
                headless=True
            )
            whatsapp.toComment(
                f'WhatsApp is_connected to {from_phone} ' \
                + f'>> {whatsapp.is_connected}'
            )

            if not whatsapp.is_connected:
                validated = validateWhatsApp(
                    whatsapp,
                    from_phone=from_phone,
                    email=email,
                    through="SMTP"
                )
            
            status = False
            if whatsapp.is_connected:
                status = whatsapp.sendMessage(
                    phone=to_phone,
                    message=message
                )
            
            if status:
                return Rest.Responses.returnSuccess()
            return Rest.Responses.returnFailure()

        except Exception: #noqa

            return Rest.Responses.returnFailure()

