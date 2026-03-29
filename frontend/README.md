# Frontend for Crypto Tracker
The frontend is built using React.

## LOCAL DEVELOPMENT

### Installation
Install dependencies using `npm install`
```aiignore
npm install
```

### Running the app
Start the development server using `npm start`
The server will be run on port 3000 at http://127.0.0.1:3000.
```aiignore
npm start
```

## DOCKER DEVELOPMENT

### Build Docker Image
```aiignore
docker build -t crypto_tracker_frontend -f Dockerfile.dev .  
```

### Run Docker Container
A new docker container will be created and run in the background on port 8000.

The name of the image is crypto_tracker_frontend.
The name of the container is frontend.
App port 3000 is mapped to port 3000 on the host machine.

```aiignore
docker run -d -p 3000:3000 --name frontend crypto_tracker_frontend 
```

### Start Docker Container
This command will restart the docker container.

```aiignore
docker start frontend
```

### Test Docker Container
Open the browser and go to http://localhost:3000. You will see the main page of the app.