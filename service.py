import os

from dotenv import load_dotenv

from flask import Flask, Response

from flask_httpauth import HTTPBasicAuth

from switchbot_py3 import Driver


load_dotenv()
blue_mac = os.environ.get("BLUETOOTH_MAC")
blue_intf = os.environ.get("BLUETOOTH_INTF")
user = os.environ.get("FLASK_USER")
passw = os.environ.get("FLASK_PASS")

connect_timeout = 10.0
auth = HTTPBasicAuth()
driver = Driver(device=blue_mac, bt_interface=blue_intf, timeout_secs=connect_timeout)
app = Flask(__name__)


@auth.verify_password
def authenticate(username, password):
    if username and password:
        if username == user and password == passw:
            return True
        else:
            return False
    return False


@app.route("/")
def verify():
    return Response(
        "Uh, we had a slight weapons malfunction, but uh... everything's perfectly all right now. We're fine. We're all fine here now, thank you. How are you?",
        status=200,
    )


@app.route("/on", methods=["GET"])
@auth.login_required
def light_on():
    try:
        driver.run_command("on")
        return "Light on!"
    except ConnectionError as e:
        return f"Connection Error: {e}"


@app.route("/off", methods=["GET"])
@auth.login_required
def light_off():
    try:
        driver.run_command("off")
        return "Light off!"
    except ConnectionError as e:
        return f"Connection Error: {e}"


def main():
    app.run(host="0.0.0.0", debug=True, port=8080)


if __name__ == "__main__":
    main()
