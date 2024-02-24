# bitcoin++'s Lightning Tip Bot (btcpplntipbot)
Bitcoin++'s Buenos Aires '24 [Hackathon submission](https://base58btc.notion.site/base58btc/bitcoin-let-s-hack-payments-5f68fa52957e4854a4a5c55d15e8163e).

## Required environment variables:
- `APP_NAME`: Bot name to show when a message is received.
- `BOT_WEBHOOK_KEY`: Bot webhook key to be shared with Telegram when receiving notifications.
  - So the Telegram notifications URL becomes: `https://{server_fqdn}/telegram/{bot_webhook_key}/webhook`.
- `LN_INVOICE`: Current Bitcoin Lightning invoice to show to the user (soon to be deprecated).
- `TG_API_ENDPOINT`: Telegram's API endpoint.
  - This normally is `https://api.telegram.org/bot`.
- `TG_API_KEY`: Telegram's bot API key. It can be obtained by talking to the [BotFather](https://t.me/BotFather).