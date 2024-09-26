import smtplib
from email.mime.text import MIMEText
from datetime import datetime

def structuredMessage(error):

    return '<!DOCTYPE html> ' \
    '<html lang="en">' \
    '<head>' \
        '<meta charset="UTF-8" />' \
        '<meta name="viewport" content="width=device-width, initial-scale=1.0" />' \
        '<link rel="preconnect" href="https://fonts.googleapis.com" />' \
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />' \
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap">' \
        '<title>Mail</title>' \
        '<style>' \
            '* { ' \
                'margin: 0px;' \
                'padding: 0px;' \
            '}' \
            'body {' \
                'background-color: #f5f5f5;' \
            '}' \
            '.header {' \
                'background-color: #05203a;' \
                'text-align: center;' \
            '}' \
            '.header img {' \
                'padding: 14px 0px 14px 0px;' \
            '}' \
            '.content {' \
                'background-color: #ffffff;' \
                'padding: 58px 80px 0px 80px;' \
            '}' \
            '.footer {' \
                'display: flex;' \
                'justify-content: space-between;' \
                'background-color: #ffffff;' \
                'padding: 38px 80px 16px 80px;' \
                'border-style: none;' \
            '}' \
            '.footer p {' \
                'font-size: 12px' \
            '}' \
            'a {' \
                'color: #05203A;' \
            '}' \
            'a:hover {' \
                'color: #FE9501;' \
            '}' \
            '.button {' \
                'text-decoration: none;' \
                'display: block;' \
                'color: #ffffff;' \
                'margin: 32px 30% 32px 30%;' \
                'background-color: #FE9501;' \
                'padding: 12px;' \
                'border-radius: 7px;' \
                'text-align: center;' \
                'font-size: 16px;' \
                'letter-spacing: 0.5px;' \
                'font-weight: 700;' \
            '}' \
            '.button a {' \
                'color: #ffffff;' \
                'margin: 0 auto;' \
            '}' \
            '.buttonD a:hover {' \
                'background-color: #F1801B !important;' \
                'color: #ffffff !important;' \
            '}' \
            'p {' \
                'margin-bottom: 26.72px;' \
                'line-height: 25.12px;' \
            '}' \
            'table {' \
                'font-family: "Lato", sans-serif;' \
                'border: 0 solid;' \
                'border-style: none;' \
                'background-color: #ffffff;' \
                'margin: 0 auto;' \
                'max-width: 800px;' \
                'height: auto;' \
                'width: 90%;' \
                'gap: 0;' \
                'font-family: "Lato", sans-serif;' \
                'font-size: 16px;' \
            '}' \
            '@media only screen and (max-width: 610px) {' \
                '.card {' \
                    'width: 95%;' \
                '}' \
                '.content {' \
                    'padding: 32px;' \
                '}' \
                '.footer {' \
                    'flex-flow: column;' \
                    'background-color: #ffffff;' \
                    'padding: 0 32px 80px 32px;' \
                '}' \
                '.footer p {' \
                    'margin-bottom: 8px;' \
                '}' \
            '}' \
            '@media only screen and (max-width: 710px) {' \
                '.button {' \
                    'margin-left: 25%;' \
                    'margin-right: 25%;' \
                '}' \
            '}' \
            '@media only screen and (max-width: 500px) {' \
                '.button {' \
                    'margin-left: 10%;' \
                    'margin-right: 10%;' \
                '}' \
            '}' \
        '</style>' \
    '</head>' \
    '<body>' \
        '<table class="table" style="width: 90%">' \
            '<tr class="header">' \
                '<th>' \
                    '<a href="https://www.infinivirt.com"><img src="data:image/png;base64,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"></a>' \
                '</th>' \
            '</tr>' \
            '<tbody>' \
                '<tr>' \
                    '<td class="content">' \
                        rf'{error}' \
                        '<p>' \
                            'Sincerely,' \
                        '</p>' \
                        '<p>' \
                            '<h3 style="margin-bottom: 96px">' \
                                'Infinivirt Security Team' \
                            '</h3>' \
                        '</p>' \
                        '<hr />' \
                    '</td>' \
                '</tr>' \
                '<tr>' \
                    '<td class="footer">' \
                        '<p>' \
                            '<a href="https://www.infinivirt.com">' \
                                'www.infinivirt.com' \
                            '</a>' \
                        '</p>' \
                        '<p>' \
                            '<a href="https://www.infinivirt.com">' \
                                'Terms and conditions' \
                            '</a>' \
                             '* ' \
                            '<a href="https://www.infinivirt.com">' \
                                'Privacy policy</p>' \
                            '</a>' \
                    '</td>' \
                '</tr>' \
            '</tbody>' \
        '</table>' \
    '</body>' \
    '</html>'

def sendMail(error):
    destination = 'camilo.zuleta@infinivirt.com, julian.berrio@infinivirt.com'
    subject = 'Error en el script'
    message = structuredMessage('<p>' \
                '<strong>Alerta:</strong>' \
            '</p>' \
            '<p>' \
                'Error en la ejecución del script, ha ocurrido un fallo en el JOB de inserción de datos.' \
            '</p>' \
            '<p>' \
                rf'<strong>Informacion relevante del archivo: </strong> {error}' \
                '</br>' \
                rf'<strong>Fecha de fallo: </strong> {datetime.now()}' \
            '</p>')

    smtp_server = 'smtp.office365.com'
    smtp_port = 587
    smtp_user = 'sos@infinivirt.com'
    smtp_pass = 'aDV1Sad23'

    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['From'] = smtp_user
    msg['To'] = destination

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)

# try:
#     string = 'hello'
#     string.append("Hola")
# except Exception  as error:
#         #mail
#     sendMail(error)