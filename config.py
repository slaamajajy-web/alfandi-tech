import os
from cryptography.fernet import Fernet

class Config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # مفتاح Fernet - سيتم قراءته من إعدادات السيرفر
    FERNET_KEY = os.getenv("FERNET_KEY")
    if FERNET_KEY:
        cipher = Fernet(FERNET_KEY.encode())
    else:
        cipher = None

    # التوكن المشفر - يتم فكه في الذاكرة فقط
    ENCRYPTED_BOT_TOKEN = os.getenv("ENCRYPTED_BOT_TOKEN")
    
    @classmethod
    def get_token(cls):
        if cls.cipher and cls.ENCRYPTED_BOT_TOKEN:
            return cls.cipher.decrypt(cls.ENCRYPTED_BOT_TOKEN.encode()).decode()
        return None

    # إعدادات الأمان
    SECRET_KEY = os.getenv("SECRET_KEY", "Alfandi_Default_77")
    API_URL = os.getenv("API_URL", "http://localhost:5000")
    HANDSHAKE = os.getenv("SECRET_HANDSHAKE", "ALFANDI_SECURE_INTERNAL")

    ADMIN_ID = 6227779307
    DB_PATH = os.path.join(BASE_DIR, "alfandi.db")
    TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
    TOOLS_DIR = os.path.join(BASE_DIR, "tools")
