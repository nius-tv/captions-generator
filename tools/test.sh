docker build \
-t plasmic-captions-generator \
.

docker run \
-v $(pwd):/app \
-w /app \
-it plasmic-captions-generator \
python3 tools/reload.py
