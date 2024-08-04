# AI-FriendBot

How to run it at this time

Requirements
Before you begin, ensure your system meets the following requirements:

Python 3.10.6
Node.js and npm
CUDA compatible hardware and drivers (for PyTorch with CUDA support)
LM Studio software installed and set up

For CUDA-enabled PyTorch, ensure you install it specifically if it’s not included in requirements.txt:

CD to root directory AI-FriendBot/ and run pip install -r requirements.txt

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

cd to frontend/ run npm install

Starting the Servers

1. Start the LM Studio Server
Open the LM Studio application:

Navigate to the Local Server tab.
Load the model alphamonarch-7b.Q2_K.gguf.
Ensure the server is started by clicking the Start Server button.

2. Start the Backend Server
Open a new terminal or command line interface, navigate to the backend directory, and start the FastAPI server using uvicorn:

cd backend/
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


3. Start the Frontend Server
Open another terminal, navigate to the frontend directory, and start the Vue.js server:

cd frontend/
npm run serve

This command will compile the frontend and typically serves it on http://localhost:8080. The terminal will display the exact address once it's up and running.

Testing the Chatbot

After starting both the backend and frontend servers and ensuring the LM Studio server is running:

Open a web browser.
Ctrl + click (Cmd + click on macOS) on the local address shown in the frontend terminal (e.g., http://localhost:8080).
The web page for the chatbot should load, and you should be able to type messages into the chat interface.
After sending a message, wait a few seconds, and you should see a response from the AI model displayed in the chat interface.

Troubleshooting

If you encounter issues:

Verify all servers are running correctly.
Check the console in the web browser for any JavaScript errors.
Check the terminal running the backend for any errors related to requests or the AI model.
Ensure CUDA drivers and compatible hardware are properly configured if using PyTorch with CUDA.