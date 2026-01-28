from app import create_app
from extensions import mongo
from models import Video

app = create_app()

with app.app_context():
    # Clear existing videos to avoid duplicates
    mongo.db.videos.delete_many({})
    
    videos = [
        {
            "title": "Big Buck Bunny",
            "description": "A large and lovable rabbit deals with three tiny bullies, led by a flying squirrel, who are determined to squelch his happiness.",
            "youtube_id": "aqz-KE-bpKQ",  # YouTube ID
            "thumbnail_url": "https://img.youtube.com/vi/aqz-KE-bpKQ/maxresdefault.jpg",
            "is_active": True
        },
        {
            "title": "Elephant Dream",
            "description": "The first open movie from Blender Foundation.",
            "youtube_id": "TLkA0RELQ1g", 
            "thumbnail_url": "https://img.youtube.com/vi/TLkA0RELQ1g/maxresdefault.jpg",
            "is_active": True
        },
        {
            "title": "Rick Roll",
            "description": "Never gonna give you up...",
            "youtube_id": "dQw4w9WgXcQ",
            "thumbnail_url": "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
            "is_active": True
        }
    ]

    for v in videos:
        # Create Video object to validate/structure if needed, or insert directly
        # Using insert_one for simplicity with the dicts
        mongo.db.videos.insert_one(v)
    
    print(f"Successfully seeded {len(videos)} videos!")
