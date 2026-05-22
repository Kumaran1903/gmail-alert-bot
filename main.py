import os
import time
import requests

from dotenv import load_dotenv

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# =====================================
# LOAD ENV VARIABLES
# =====================================

load_dotenv()


WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
TO_PHONE = os.getenv("TO_PHONE")



# =====================================
# GMAIL CONFIG
# =====================================

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# Infosys detection keywords
INFOSYS_KEYWORDS = [
    "infosys",
    "@infosys.com",
    "infosys limited",
]

checked_messages = set()


# =====================================
# AUTHENTICATE GMAIL
# =====================================

def authenticate_gmail():

    creds = None

    if os.path.exists("token.json"):

        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    if not creds or not creds.valid:

        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json",
            SCOPES
        )

        creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build(
        'gmail',
        'v1',
        credentials=creds
    )

    return service


# =====================================
# SEND WHATSAPP TEMPLATE MESSAGE
# =====================================

def send_whatsapp(subject):

    url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": TO_PHONE,
        "type": "template",
        "template": {
            "name": "infosys_alert",
            "language": {
                "code": "en"
            },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": subject
                        }
                    ]
                }
            ]
        }
    }

    response = requests.post(
        url,
        headers=headers,
        json=data
    )

    print("\nWhatsApp STATUS CODE:")
    print(response.status_code)

    print("\nWhatsApp RESPONSE:")
    print(response.text)


# =====================================
# EXTRACT EMAIL DETAILS
# =====================================

def extract_headers(headers):

    subject = ""
    sender = ""
    date = ""

    for h in headers:

        if h['name'] == 'Subject':
            subject = h['value']

        if h['name'] == 'From':
            sender = h['value']

        if h['name'] == 'Date':
            date = h['value']

    return subject, sender, date


# =====================================
# CHECK EMAILS
# =====================================

def check_emails(service):

    labels = [
        "INBOX",
        "SPAM",
        "CATEGORY_PROMOTIONS",
        "CATEGORY_SOCIAL",
        "CATEGORY_UPDATES"
    ]

    for label in labels:

        print(f"\nChecking {label}...")

        results = service.users().messages().list(
            userId='me',
            labelIds=[label],
            q='is:unread',
            maxResults=10
        ).execute()

        messages = results.get('messages', [])

        if not messages:
            print("No unread emails found.")
            continue

        for msg in messages:

            msg_id = msg['id']

            if msg_id in checked_messages:
                continue

            checked_messages.add(msg_id)

            message = service.users().messages().get(
                userId='me',
                id=msg_id
            ).execute()

            payload = message.get('payload', {})
            headers = payload.get('headers', [])

            subject, sender, date = extract_headers(headers)

            text_to_check = f"{subject} {sender}".lower()

            # CHECK FOR INFOSYS
            is_infosys = any(
                keyword in text_to_check
                for keyword in INFOSYS_KEYWORDS
            )

            if is_infosys:

                print(f"""
🚨 INFOSYS EMAIL DETECTED

👤 From:
{sender}

📩 Subject:
{subject}

📂 Folder:
{label}

🕒 Date:
{date}
""")

                # SEND WHATSAPP ALERT
                send_whatsapp(subject)

            # MARK AS READ
            service.users().messages().modify(
                userId='me',
                id=msg_id,
                body={
                    'removeLabelIds': ['UNREAD']
                }
            ).execute()


# =====================================
# MAIN LOOP
# =====================================

def main():

    print("\nStarting Infosys Email Alert Bot...\n")

    service = authenticate_gmail()

    while True:

        try:

            check_emails(service)

        except Exception as e:

            print("\nERROR:")
            print(e)

        print("\nSleeping for 10 seconds...\n")

        time.sleep(10)


# =====================================
# START PROGRAM
# =====================================

if __name__ == "__main__":
    main()



# import os
# import time
# import requests

# from dotenv import load_dotenv

# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build


# # =====================================
# # LOAD ENV VARIABLES
# # =====================================

# load_dotenv()

# WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
# PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
# TO_PHONE = os.getenv("TO_PHONE")


# # =====================================
# # GMAIL CONFIG
# # =====================================

# SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# TARGET_EMAIL = "kumaranofficial7@gmail.com"

# checked_messages = set()


# # =====================================
# # AUTHENTICATE GMAIL
# # =====================================

# def authenticate_gmail():

#     creds = None

#     if os.path.exists("token.json"):

#         creds = Credentials.from_authorized_user_file(
#             "token.json",
#             SCOPES
#         )

#     if not creds or not creds.valid:

#         flow = InstalledAppFlow.from_client_secrets_file(
#             "credentials.json",
#             SCOPES
#         )

#         creds = flow.run_local_server(port=0)

#         with open("token.json", "w") as token:
#             token.write(creds.to_json())

#     service = build(
#         'gmail',
#         'v1',
#         credentials=creds
#     )

#     return service


# # =====================================
# # SEND WHATSAPP TEMPLATE MESSAGE
# # =====================================

# def send_whatsapp():

#     url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"

#     headers = {
#         "Authorization": f"Bearer {WHATSAPP_TOKEN}",
#         "Content-Type": "application/json"
#     }

#     # Meta sandbox template message
#     data = {
#         "messaging_product": "whatsapp",
#         "to": TO_PHONE,
#         "type": "template",
#         "template": {
#             "name": "hello_world",
#             "language": {
#                 "code": "en_US"
#             }
#         }
#     }

#     response = requests.post(
#         url,
#         headers=headers,
#         json=data
#     )

#     print("\nWhatsApp STATUS CODE:")
#     print(response.status_code)

#     print("\nWhatsApp RESPONSE:")
#     print(response.text)


# # =====================================
# # EXTRACT EMAIL DETAILS
# # =====================================

# def extract_headers(headers):

#     subject = ""
#     sender = ""
#     date = ""

#     for h in headers:

#         if h['name'] == 'Subject':
#             subject = h['value']

#         if h['name'] == 'From':
#             sender = h['value']

#         if h['name'] == 'Date':
#             date = h['value']

#     return subject, sender, date


# # =====================================
# # CHECK EMAILS
# # =====================================

# def check_emails(service):

#     labels = [
#         "INBOX",
#         "SPAM",
#         "CATEGORY_PROMOTIONS",
#         "CATEGORY_SOCIAL",
#         "CATEGORY_UPDATES"
#     ]

#     for label in labels:

#         print(f"\nChecking {label}...")

#         results = service.users().messages().list(
#             userId='me',
#             labelIds=[label],
#             q=f'from:{TARGET_EMAIL} is:unread',
#             maxResults=10
#         ).execute()

#         messages = results.get('messages', [])

#         if not messages:
#             print("No matching emails found.")
#             continue

#         for msg in messages:

#             msg_id = msg['id']

#             if msg_id in checked_messages:
#                 continue

#             checked_messages.add(msg_id)

#             message = service.users().messages().get(
#                 userId='me',
#                 id=msg_id
#             ).execute()

#             payload = message.get('payload', {})
#             headers = payload.get('headers', [])

#             subject, sender, date = extract_headers(headers)

#             print(f"""
# 🚨 NEW EMAIL DETECTED

# 👤 From:
# {sender}

# 📩 Subject:
# {subject}

# 📂 Folder:
# {label}

# 🕒 Date:
# {date}
# """)

#             # SEND WHATSAPP TEMPLATE MESSAGE
#             send_whatsapp()

#             # MARK EMAIL AS READ
#             service.users().messages().modify(
#                 userId='me',
#                 id=msg_id,
#                 body={
#                     'removeLabelIds': ['UNREAD']
#                 }
#             ).execute()


# # =====================================
# # MAIN LOOP
# # =====================================

# def main():

#     print("\nStarting Gmail WhatsApp Alert Bot...\n")

#     service = authenticate_gmail()

#     while True:

#         try:

#             check_emails(service)

#         except Exception as e:

#             print("\nERROR:")
#             print(e)

#         print("\nSleeping for 10 seconds...\n")

#         time.sleep(10)


# # =====================================
# # START PROGRAM
# # =====================================

# if __name__ == "__main__":
#     main()