# Projekt plotio

# Setup

## Server

1. Open server directory
2. Run `pip -r requirements.txt`
3. Run `uvicorn main:app --reload --host=0.0.0.0 --port=5000`

## Client

1. Open client directory
2. Run `npm install`
3. Run `npm run serve`

# Usage

Application can be accessed on `http://localhost:8080/plotter`
Documentation can be accessed on `http://localhost:5000/docs`

To generate server api for client you have:
1. Run serve (command `uvicorn main:app --reload --host=0.0.0.0 --port=5000` on server directory)
2. `openapi --file http://localhost:5000/openapi.json --output-dir client\src\api\`
