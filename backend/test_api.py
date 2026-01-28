import requests

BASE_URL = "http://localhost:5000"

def test_backend():
    print("Testing Backend...")
    
    # 1. Signup
    email = "newuser@example.com"
    password = "password123"
    print(f"\n[1] Signup user: {email}")
    try:
        resp = requests.post(f"{BASE_URL}/auth/signup", json={
            "name": "New User",
            "email": email,
            "password": password
        })
        print(f"Status: {resp.status_code}, Body: {resp.json()}")
        if resp.status_code == 201:
            token = resp.json()['token']
        elif resp.status_code == 409:
             # Login if exists
             print("User exists, logging in...")
             resp = requests.post(f"{BASE_URL}/auth/login", json={
                "email": email,
                "password": password
             })
             token = resp.json()['token']
        else:
            print("Signup failed.")
            return
    except Exception as e:
        print(f"Request failed: {e}")
        return

    # 2. Login (Double check)
    print(f"\n[2] Login user")
    resp = requests.post(f"{BASE_URL}/auth/login", json={
        "email": email,
        "password": password
    })
    print(f"Status: {resp.status_code}")
    token = resp.json().get('token')
    if not token:
        print("Login failed, no token.")
        return
    
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Get Dashboard
    print(f"\n[3] Get Dashboard")
    resp = requests.get(f"{BASE_URL}/dashboard", headers=headers)
    print(f"Status: {resp.status_code}")
    videos = resp.json()
    print(f"Videos: {videos}")
    
    if not videos:
        print("No videos found?")
        return
        
    first_video = videos[0]
    vid_id = first_video['id']
    playback_token = first_video.get('playback_token')
    
    if not playback_token:
        print("Method A detected? No playback token.")
        # If we implemented Option B, this should fail or be different.
    else:
        print(f"Got playback token: {playback_token[:20]}...")

    # 4. Stream Video (Option B)
    print(f"\n[4] Request Stream with Token")
    stream_url = f"{BASE_URL}/video/{vid_id}/stream?token={playback_token}"
    resp = requests.get(stream_url, headers=headers)
    print(f"Status: {resp.status_code}")
    print(f"Body: {resp.json()}")

if __name__ == "__main__":
    test_backend()
