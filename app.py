from flask import Flask, request, render_template_string

app = Flask(__name__)

LOG_FILE = "log.txt"

# หน้าเว็บฟอร์ม (ใช้ Jinja2 ซึ่ง escape HTML ให้อัตโนมัติ ป้องกัน XSS)
PAGE = """
<!doctype html>
<html lang="th">
<head>
  <meta charset="utf-8">
  <title>Submit Message</title>
</head>
<body>
  {% if message is not none %}
    <h1>Message received:</h1>
    <p>{{ message }}</p>
    <a href="/">ส่งข้อความอีกครั้ง</a>
  {% else %}
    <h1>Submit your message</h1>
    <form method="post">
      <textarea name="message" rows="5" cols="40" required></textarea><br>
      <input type="submit" value="Submit">
    </form>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        message = request.form.get("message", "").strip()
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(message + "\n")
        return render_template_string(PAGE, message=message)
    return render_template_string(PAGE, message=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
