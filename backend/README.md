# Backend for Binance Tracker
The backend is written in Python using FastAPI.

## LOCAL DEVELOPMENT

### Installation
Create a virtual environment using venv
```
python -m venv venv
```

Activate virtual environment
```
source venv/bin/activate
```

Install requirements
```aiignore
pip install -r requirements.txt
```

### Run development server
The server will be running on port 8000 at http://localhost:8000
```aiignore
python -m uvicorn --port 8000 --host 0.0.0.0 --reload main:app
```

## DOCKER DEVELOPMENT

### Build Docker Image
```aiignore
docker build -t crypto_tracker_backend -f Dockerfile.dev .  
```

### Run Docker Container
A new docker container will be created and run in the background on port 8000.

The environment variable STREAMS is used to specify the streams to subscribe to.
The environment variable ALLOWED_HOSTS is used to specify the allowed hosts.
The name of the image is crypto_tracker_backend.
The name of the container is backend.
App port 8000 is mapped to port 8000 on the host machine.

```aiignore
docker run -d -e STREAMS=ethusdt@ticker/solusdt@ticker/btcusdt@ticker -e ALLOWED_HOSTS=http://frontend:3000 -p 8000:8000 --name backend crypto_tracker_backend 
```

### Start Docker Container
This command will restart the docker container.

```aiignore
docker start backend
```

### Test Backend
Open the browser and navigate to http://localhost:8000/api/health. You should see the following response:

```json
{"status": "healthy", "message": "System is up and running, ready to receive requests."}
```
