source .env
docker build -t "$INIT_STAGE_IMAGE_NAME" -f "$INIT_STAGE_DOCKERFILE_PATH" .
docker build -t "$SILVER_STAGE_IMAGE_NAME" -f "$SILVER_STAGE_DOCKERFILE_PATH" .
docker build -t "$GOLD_STAGE_IMAGE_NAME" -f "$GOLD_STAGE_DOCKERFILE_PATH" .
docker compose down
docker compose up --build