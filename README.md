<<<<<<< HEAD
# API-First Video App

A secure, API-first mobile application for streaming videos.

## Prerequisites
*   **Python 3.12+**
*   **Node.js & npm**
*   **Expo Go** app on your physical device (Android/iOS)

## 1. Backend Setup (Flask)

1.  Navigate to the backend folder:
    ```bash
    cd backend
    ```

2.  Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4.  Configure Environment Variables:
    *   Rename `.env.example` to `.env`.
    *   Update `MONGO_URI` if you have a custom database (otherwise it defaults to the configured Cloud instance).

5.  **Run the Server**:
    ```bash
    python app.py
    ```
    *   You should see: `* Running on all addresses (0.0.0.0)`

6.  (Optional) Seed/Reset Data:
    ```bash
    python seed.py
    ```
    *   Run this if your dashboard is empty.

## 2. Frontend Setup (React Native / Expo)

1.  Open a new terminal and navigate to the mobile folder:
    ```bash
    cd mobile
    ```

2.  Install dependencies:
    ```bash
    npm install
    ```

3.  **Run the App**:
    ```bash
    npx expo start
    ```

4.  **Connect your Device**:
    *   Scan the QR code printed in the terminal with the **Expo Go** app (Android) or Camera (iOS).

## 3. Troubleshooting

### "Network Error" or Signup Failed on Phone
If your phone cannot connect to the backend:
1.  **Windows Firewall**: It often blocks Port 5000.
    *   Open "Windows Defender Firewall with Advanced Security".
    *   Inbound Rules -> New Rule -> Port -> TCP -> 5000 -> Allow Connection.
2.  **Same WiFi**: Ensure your Laptop and Phone are on the exact same WiFi network.

### "AttributeError: 'NoneType' ... 'users'"
*   This means MongoDB is not connected. Check your `backend/.env` or `config.py` credentials.
*   Ensure you have internet access (Cloud DB).

## License
Assignment Project.
=======
>>>>>>> 0963ddea46c5c530565879a5179ed2443e9c0d88
"# assignment" 
"# assesment" 
