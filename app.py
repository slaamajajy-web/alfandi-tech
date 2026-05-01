import os, uuid, threading
from flask import Flask, request, jsonify, render_template, redirect, session
from config import Config
from models import init_db, get_db, log_event
from generator import render_html

app = Flask(__name__, template_folder=Config.TEMPLATE_DIR)
app.secret_key = Config.SECRET_KEY

# ======================
# API: توليد الرخص (للبوت فقط)
# ======================
@app.route("/generate_license", methods=["POST"])
def api_generate():
    # التحقق من المصافحة السرية لضمان أمان البوت
    if request.headers.get("X-SECURE-KEY") != Config.HANDSHAKE:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    tier = data.get("tier", "basic")
    
    # توليد مفتاح فريد
    new_key = uuid.uuid4().hex[:16].upper()

    conn = get_db()
    c = conn.cursor()
    c.execute("""
        INSERT INTO licenses(license_key, tier, created_at)
        VALUES (?,?,datetime('now'))
    """, (new_key, tier))
    conn.commit()
    conn.close()

    log_event(f"تم توليد رخصة جديدة: {new_key} [{tier}]")
    return jsonify({"key": new_key})

# ======================
# API: التحقق من الرخصة (للأداة)
# ======================
@app.route("/api/validate", methods=["POST"])
def validate():
    data = request.json
    key = data.get("key")
    hwid = data.get("hwid")

    conn = get_db()
    c = conn.cursor()
    lic = c.execute("SELECT hwid FROM licenses WHERE license_key=?", (key,)).fetchone()

    if not lic:
        conn.close()
        return jsonify({"valid": False, "msg": "Key not found"})

    stored_hwid = lic[0]

    # ربط المفتاح بالجهاز (HWID) لأول مرة
    if stored_hwid is None:
        c.execute("UPDATE licenses SET hwid=? WHERE license_key=?", (hwid, key))
        conn.commit()
        conn.close()
        return jsonify({"valid": True, "msg": "Activated & Bound"})

    conn.close()
    return jsonify({"valid": stored_hwid == hwid})

# ======================
# لوحة التحكم والأدمن
# ======================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # كلمة المرور السيادية الخاصة بك
        if request.form.get("pass") == "Alfandi_2026_Secure":
            session["admin"] = True
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if not session.get("admin"): return redirect("/login")
    
    conn = get_db()
    lics = conn.execute("SELECT license_key, tier, hwid FROM licenses ORDER BY id DESC").fetchall()
    logs = conn.execute("SELECT event, created_at FROM logs ORDER BY id DESC LIMIT 10").fetchall()
    conn.close()
    
    return render_template("dashboard.html", licenses=lics, logs=logs)

if __name__ == "__main__":
    from threading import Thread
    Thread(target=lambda: bot.infinity_polling(timeout=10, long_polling_timeout=5)).start()
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 7860)))
