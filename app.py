import datetime
import json
import logging.config
import os

import requests as r
from flask import Flask, request, make_response

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Set variables from environment variables
app_name = os.getenv("APP_NAME").strip()
api_endpoint = os.getenv("TG_API_ENDPOINT").strip() + os.getenv("TG_API_KEY").strip()
bot_webhook_key = os.getenv("BOT_WEBHOOK_KEY").strip()
ln_invoice = os.getenv("LN_INVOICE").strip()


# Main webhook to receive notifications from Telegram
@app.route(f"/telegram/{bot_webhook_key}/webhook", methods=["POST"])
def webhook():
    """Main webhook to receive Telegram notifications.

    :return: A response that Telegram understands as a chat action or answer callback query message
    """
    if request.method == "POST":
        # Insert raw payload into a variable
        tg_payload = request.data.decode("utf-8")
        # Parse payload body as JSON, it becomes the notification coming from Telegram
        tg_notification = json.loads(tg_payload)
        # Live print of the JSON payload, done with print() because of encoding errors
        print(
            str(datetime.datetime.now()).replace(".", ",")[:-3],
            f"Incoming notification: {json.dumps(tg_notification)}",
        )
        # Response method to return with the request
        response_method = "sendChatAction"
        # Response ID to return with the request
        response_user_id = ""
        # Default action in case it's not overriden in a later statement
        response_action = "typing"
        try:
            # Extract JSON keys and set the notification type based on keys present
            tg_notification_keys = tg_notification.keys()
            tg_notification_type = ""
            for key in tg_notification_keys:
                if key != "update_id":
                    tg_notification_type = key

            # When I'm messaged
            if tg_notification_type == "message":
                user_tgid = tg_notification["message"]["from"]["id"]
                logger.info(
                    f"Received a message notification: {tg_notification_type=} from {user_tgid=}"
                )
                response_user_id = user_tgid
                command = "start"
                try:
                    command = tg_notification["message"]["text"]
                    if command.startswith("/"):
                        command = command.replace("/", "", 1)
                    command = command.lower().strip()

                    params = {
                        "chat_id": user_tgid,
                        "parse_mode": "Markdown",
                        "disable_web_page_preview": 1,
                        "text": (
                            "¡Hola!\n\n"
                            "Please send funds to this Lightning invoice! \u26A1\n\n"
                            f"```{ln_invoice}```"
                        ),
                    }
                    api_method = api_endpoint + "/sendMessage"
                    reply = r.post(
                        api_method,
                        params=params,
                    )

                except KeyError as exception:
                    logger.debug(
                        f"Caught {type(exception)}: {exception} key not present"
                    )
                except Exception as exception:
                    logger.debug(
                        f"Caught {type(exception)}: Generic handler on {exception}"
                    )

                logger.info(
                    f"Returning to Telegram: {user_tgid=} {command=} {response_action=}"
                )

        except KeyError as exception:
            logger.debug(f"Caught {type(exception)}: {exception} key not present")
        except Exception as exception:
            logger.debug(f"Caught {type(exception)}: Generic handler on {exception}")
        finally:
            response_obj = {
                "method": response_method,
                "chat_id": response_user_id,
                "action": response_action,
            }
            if response_method == "answerCallbackQuery":
                tg_n = tg_notification
                del response_obj["action"], response_obj["chat_id"]
                response_obj["callback_query_id"] = tg_n["callback_query"]["id"]
                response_obj["text"] = "Processing request..."
            response = make_response(response_obj)
            response.headers["Content-Type"] = "application/json"
            return response


@app.route("/", methods=["GET"])
def bot_index():
    """Redirection to the main website in case the server is hit with browser requests on the main route.

    :return: Returns a redirect to the main website
    """
    redirection_http_code, redirection_http_message = (301, "Moved Permanently")
    remote_addr = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)
    redirect = (
        '<head><meta http-equiv="refresh" content="0; URL=\'https://github.com/IvanMontillaM/btcpplntipbot\'" '
        "/></head>"
    )
    logger.info(
        f"{remote_addr} hit the main route; Redirecting ({redirection_http_code} {redirection_http_message})"
    )
    logger.info(f"{app.url_map}")
    return redirect, redirection_http_code


# Application's main entry point (app.py:app)
if __name__ == "__main__":
    app.run()
