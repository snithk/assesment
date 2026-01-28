from flask import Blueprint, request, jsonify, current_app
import jwt
import datetime
from models import User, Video
from bson.objectid import ObjectId
import secrets

auth_bp = Blueprint('auth', __name__)
video_bp = Blueprint('video', __name__)

def generate_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
        'sub': str(user_id)
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

def token_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            current_user = User.get_by_id(data['sub'])
        except Exception as e:
            return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password') or not data.get('name'):
        return jsonify({'message': 'Missing fields'}), 400
    
    if User.get_by_email(data['email']):
        return jsonify({'message': 'User already exists'}), 409
    
    user_id = User.create(data['name'], data['email'], data['password'])
    token = generate_token(user_id)
    
    return jsonify({'token': token, 'user': {'name': data['name'], 'email': data['email']}}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing fields'}), 400
        
    user = User.get_by_email(data['email'])
    if not user or not User.verify_password(user, data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    token = generate_token(user['_id'])
    return jsonify({'token': token, 'user': {'name': user['name'], 'email': user['email']}}), 200

@auth_bp.route('/me', methods=['GET'])
@token_required
def get_me(current_user):
    return jsonify({'name': current_user['name'], 'email': current_user['email']})

@auth_bp.route('/logout', methods=['POST'])
def logout():
    # Stateless JWT, client just throws away token
    return jsonify({'message': 'Logged out successfully'}), 200

# --- Video Routes ---

@video_bp.route('/dashboard', methods=['GET'])
@token_required
def get_dashboard(current_user):
    videos = Video.get_active_videos()
    output = []
    for vid in videos:
        # Generate a temporary signed token for this specific video playback
        # This corresponds to Option B: "Backend returns video_id, playback_token"
        playback_payload = {
            'vid': str(vid['_id']),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        playback_token = jwt.encode(playback_payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
        
        output.append({
            'id': str(vid['_id']),
            'title': vid['title'],
            'description': vid['description'],
            'thumbnail_url': vid['thumbnail_url'],
            # Intentionally NOT implementing youtube_id here to "Hide" it
            'playback_token': playback_token
        })
    # Limit to 2 as per requirement
    return jsonify(output[:2])

@video_bp.route('/video/<video_id>/stream', methods=['GET'])
@token_required
def stream_video(current_user, video_id):
    # Check for the specific playback token
    token = request.args.get('token')
    if not token:
        # Fallback: if they are authenticated via header, maybe we allow it?
        # But requirement says "request /stream?token=..."
        # Let's enforce the token for the "Option B" strictness.
        return jsonify({'message': 'Missing playback token'}), 403
        
    try:
        data = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        if data['vid'] != video_id:
            return jsonify({'message': 'Invalid token for this video'}), 403
    except:
        return jsonify({'message': 'Invalid or expired playback token'}), 403

    video = Video.get_by_id(video_id)
    if not video:
        return jsonify({'message': 'Video not found'}), 404

    # Now we reveal the source or proxy it.
    # Since we can't easily PROXY a youtube stream without heavy bandwidth,
    # and the requirement says "returns playable stream URL or proxy",
    # returning the YouTube ID here is the "Reveal" step, but only to the secure player.
    # Alternatively, if we really need a URL, we could return a Youtube embed link or raw stream URL if we could fetch it (yt-dlp style),
    # but for this assignment, returning the ID or a constructed URL that the frontend 'Wrapper' understands is likely the goal.
    # Let's return the ID, but wrapped in a JSON that the frontend "Wrapper" will verify.
    
    return jsonify({
        'stream_url': f"https://www.youtube.com/embed/{video['youtube_id']}?playsinline=1", 
        'video_id': video['youtube_id'], # Exposed only here
        'provider': 'youtube' 
    })
