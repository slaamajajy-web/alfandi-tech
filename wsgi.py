from app import app, init_db

# تهيئة قاعدة البيانات عند بدء التشغيل لأول مرة
init_db()

if __name__ == "__main__":
    app.run()
