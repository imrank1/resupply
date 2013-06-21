import requests

def send_mail(to_address, from_address, subject, plaintext, html):
    r = requests. \
        post("https://api.mailgun.net/v2/%s/messages" % 'resupply.mailgun.org',
             auth=("api", 'key-0tv5b0tr16dz-86zophipsh5htylj2h2'),
             data={
                 "from": from_address,
                 "to": to_address,
                 "subject": subject,
                 "text": plaintext,
                 "html": html
             }
    )
    return r