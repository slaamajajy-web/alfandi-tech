FROM python:3.10-slim

WORKDIR /app

# تثبيت المتطلبات
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ الكود
COPY . .

# فتح المنفذ (Port) الافتراضي
EXPOSE 7860

# تشغيل البوت والموقع
CMD ["python", "app.py"]
