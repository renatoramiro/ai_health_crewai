# Flask Weather App Deployment Guide

This guide explains how to deploy the Flask Weather App to a VPS using Docker and Gunicorn for production use.

## Local Machine Steps

1. Clean up unnecessary files and prepare for zipping:
```bash
# Remove any unnecessary files
rm -rf __pycache__
rm -rf .pytest_cache
rm -rf .venv

# Create the deployment package
tar -czvf flask_weather_app.tar.gz .
```

2. Transfer the zip file to your VPS:
```bash
scp flask_weather_app.tar.gz username@your-vps-ip:/path/to/deployment
```

## VPS Steps

1. Connect to your VPS:
```bash
ssh username@your-vps-ip
```

2. Navigate to your deployment directory and unzip:
```bash
cd /path/to/deployment
tar -xzf flask_weather_app.tar.gz
cd flask_weather_app
```

3. Build and deploy with Docker:
```bash
# Build the Docker image
docker build -t flask_app:0.01 .

# Deploy using Portainer
# Access your Portainer interface and:
# 1. Go to Stacks
# 2. Add a new stack
# 3. Upload or paste the docker-compose.yml content
# 4. Deploy the stack
```

## Production Setup

This application uses Gunicorn as a production-grade WSGI server with the following features:
- Multiple worker processes (automatically scaled based on CPU cores)
- Production-grade HTTP server
- Error logging and monitoring
- Process management

## Environment Variables

Make sure to set these environment variables in Portainer:
- `OPENAI_MODEL_NAME`: The OpenAI model to use (e.g., gpt-4)
- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENCAGE_API_KEY`: Your OpenCage API key

## Performance Tuning

The Gunicorn configuration (`gunicorn_config.py`) is set up with:
- Automatic worker process scaling (CPU cores * 2 + 1)
- Connection backlog of 2048
- Worker timeout of 30 seconds
- Keep-alive connections
- Comprehensive logging

To adjust these settings, modify `gunicorn_config.py` and rebuild the Docker image.

## Verification

After deployment:
1. Check if the container is running:
```bash
docker ps
```

2. Check the container logs:
```bash
docker logs container_name
```

3. Test the API endpoint:
```bash
curl http://your-vps-ip:5005/api/coordinates
```

## Testing Locally

1. Start the application:
```bash
docker-compose up -d
```

2. Test the webhook endpoint:
```bash
curl -X POST http://localhost:5005/api/webhook/agent_zero \
-H "Content-Type: application/json" \
-d '[{
  "body": {
    "event": "messages.upsert",
    "instance": "NOME_DA_SUA_INSTANCIA",
    "data": {
      "key": {
        "remoteJid": "55<seu_numero_whatsapp_com_ddd>@s.whatsapp.net",
        "fromMe": false,
        "id": "3AB943940864A837CD4E"
      },
      "message": {
        "conversation": "What is the weather in London?"
      },
      "messageType": "extendedTextMessage",
      "messageTimestamp": 1727783931
    }
  }
}]'
```

This simulates a WhatsApp message asking about the weather in London. The webhook endpoint will process this request and respond with weather information.

## Troubleshooting

If you encounter issues:
1. Check container logs:
```bash
docker logs container_name
```

2. Verify environment variables are set correctly in Portainer

3. Ensure all ports are properly exposed and accessible

4. Check network configuration in docker-compose.yml matches your VPS network setup
