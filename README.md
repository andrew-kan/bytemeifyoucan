# bytemeifyoucan

## Building and running
1. Create the Docker image
```docker build -t effixo:1.0 .```
2. Run the image and expose port 8080
```docker run --name server --publish 8080:8080 effixo:1.0```

## Run the MongoDB database separately
To debug using a database without having to build the Docker image, you can run the following command and keep it open while you develop the Python project:
1. Pull the MongoDB Docker image
```docker pull mongo:latest```
2. Run the MongoDB container
```docker run --name mongodb --publish 27017:27017 mongo:latest```