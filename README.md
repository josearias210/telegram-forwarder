# Deploy

docker buildx build --platform linux/amd64,linux/arm64   -t ghcr.io/josearias210/app-telegram-forwarder:latest   -t ghcr.io/josearias210/app-telegram-forwarder:$(date +%Y%m%d)   --push .
