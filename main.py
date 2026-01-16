from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
import aiosmtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

# .env dosyasındaki şifreleri yükle
load_dotenv()

MAIL_HOST = os.getenv("MAIL_HOST")
MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
MAIL_USER = os.getenv("MAIL_USER")
MAIL_PASS = os.getenv("MAIL_PASS")

app = FastAPI()

# Gelen isteğin formatını belirliyoruz (DTO gibi)
class MailRequest(BaseModel):
    email: EmailStr
    subject: str = Field(alias="baslik") # Java'dan 'baslik' diye gelecek
    message: str = Field(alias="mesaj")  # Java'dan 'mesaj' diye gelecek

    class Config:
        populate_by_name = True

@app.post("/send-mail")
async def send_mail(req: MailRequest):
    try:
        msg = EmailMessage()
        msg["From"] = MAIL_USER
        msg["To"] = req.email
        msg["Subject"] = req.subject
        msg.set_content(req.message)

        # Gmail sunucusuna bağlanıp maili at
        await aiosmtplib.send(
            msg,
            hostname=MAIL_HOST,
            port=MAIL_PORT,
            username=MAIL_USER,
            password=MAIL_PASS,
            start_tls=True
        )
        return {"status": "ok", "message": "Mail başarıyla gönderildi"}

    except Exception as e:
        print("MAIL HATASI:", e)
        raise HTTPException(status_code=500, detail=str(e))