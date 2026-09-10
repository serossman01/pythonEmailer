from flask import Flask, request, render_template
import smtplib
import socket

app = Flask(__name__)

GMAIL_USER = "adam.poodleschool.founder@gmail.com"
GMAIL_PASSWORD = "zlnzowjgeoalhwcj"



def spammer(to_addr):
    from_addr = GMAIL_USER
    message = "Hi, I'm requesting you ."
    num_times = 10

    with smtplib.SMTP("smtp.gmail.com", 587) as smtpserver:
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        smtpserver.login(GMAIL_USER, GMAIL_PASSWORD)

        for i in range(num_times):
            smtpserver.sendmail(from_addr, [to_addr], message)
            print(f"Sent email {i + 1}/{num_times}")

    print("Done!")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/test-smtp")
def test_smtp():
    results = {}

    try:
        addresses = socket.getaddrinfo(
            "smtp.gmail.com",
            None,
            socket.AF_UNSPEC,
            socket.SOCK_STREAM
        )

        results["dns"] = list({
            (x[4][0], x[0])
            for x in addresses
        })

    except Exception as e:
        results["dns_error"] = f"{type(e).__name__}: {e}"

    for host, port in [
        ("smtp.gmail.com", 465),
        ("smtp.gmail.com", 587),
        ("google.com", 443),
    ]:
        try:
            s = socket.create_connection((host, port), timeout=10)
            s.close()
            results[f"{host}:{port}"] = "CONNECTED"
        except Exception as e:
            results[f"{host}:{port}"] = f"{type(e).__name__}: {e}"

    return results


@app.route("/send", methods=["POST"])
def send():
    data = request.json
    user_input = data.get("input", "")

    print("Received:", user_input)

    spammer(user_input)

    return "", 204
