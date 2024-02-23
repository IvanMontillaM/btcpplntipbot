import logging.config

from flask import Flask, request  # make_response

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def bot_index():
    """Redirection to the main website in case the server is hit with browser requests on the main route.

    :return: Returns a redirect to the main website
    """
    redirection_http_code, redirection_http_message = (301, "Moved Permanently")
    remote_addr = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)
    redirect = '<head><meta http-equiv="refresh" content="0; URL=\'https://github.com/IvanMontillaM/btcpplntipbot\'" /></head>'
    logger.info(
        f"{remote_addr} hit the main route; Redirecting ({redirection_http_code} {redirection_http_message})"
    )
    logger.info(f"{app.url_map}")
    return redirect, redirection_http_code


# Application's main entry point (app.py:app)
if __name__ == "__main__":
    app.run()
