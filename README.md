# Environment Variables

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token.
- `N8N_WEBHOOK_URL`: The webhook URL to forward messages to.
- `TELEGRAM_USER_IDS`: A comma-separated list of allowed Telegram user IDs.

# Usage

1. Set up the `.env` file with the required environment variables:
   ```env
   TELEGRAM_BOT_TOKEN=your-telegram-bot-token
   N8N_WEBHOOK_URL=https://your-webhook-url
   TELEGRAM_USER_IDS=123456789,987654321
   ```

2. Build and run the Docker container:
   ```bash
   docker build -t telegram-forwarder .
   docker run --env-file .env telegram-forwarder
   ```

# Deploy and Publish Docker Image

To build and publish the Docker image for multiple platforms (linux/amd64 and linux/arm64), use the following command:

```bash
docker buildx build --platform linux/amd64,linux/arm64 \
   -t ghcr.io/josearias210/app-telegram-forwarder:latest \
   -t ghcr.io/josearias210/app-telegram-forwarder:$(date +%Y%m%d) \
   --push .
```