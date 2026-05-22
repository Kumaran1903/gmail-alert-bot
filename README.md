# Email to WhatsApp Alert Bot

A Python-based automation system that monitors incoming emails and sends instant WhatsApp notifications for important messages in real time.

---

## Features

* Real-time Gmail monitoring
* WhatsApp notification alerts
* Background automation workflow
* Gmail API integration
* WhatsApp Cloud API integration
* Detects emails across:

  * Inbox
  * Spam
  * Promotions
  * Social
  * Updates
* Automatic email state management
* Deployable on cloud platforms

---

## Tech Stack

* Python
* Gmail API
* WhatsApp Cloud API
* Google OAuth 2.0
* Render / Railway Deployment

---

## Project Structure

```bash
gmail-alert-bot/
│
├── main.py
├── requirements.txt
├── render.yaml
├── credentials.json
├── token.json
├── .env
└── README.md
```

---

## Installation

### 1. Clone Repository

```bash
git clone <your-repository-url>
cd gmail-alert-bot
```

---

### 2. Create Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Gmail API Setup

1. Create a project in Google Cloud Console
2. Enable Gmail API
3. Configure OAuth Consent Screen
4. Create OAuth Client Credentials
5. Download `credentials.json`
6. Place it inside the project folder

---

## WhatsApp Cloud API Setup

1. Create a Meta Developer App
2. Add WhatsApp Product
3. Generate Access Token
4. Configure WhatsApp test number
5. Create and approve message template
6. Add environment variables

---

## Environment Variables

Create a `.env` file:

```env
WHATSAPP_TOKEN=your_token
PHONE_NUMBER_ID=your_phone_number_id
TO_PHONE=your_phone_number
```

---

## Run the Project

```bash
python main.py
```
