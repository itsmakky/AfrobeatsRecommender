from pymongo import MongoClient
import random

# Your connection string
MONGO_URI = "mongodb+srv://makkyyy:Amamanwa2004!@cluster0.rl51hjn.mongodb.net/?appName=Cluster0"

# Create a SINGLE connection (reused)
_client = None

def get_db():
    """Get the database connection - reuses the same connection"""
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI)
    return _client['afrobeats_recommender']

def init_db():
    """Initialize database with sample artists and songs"""
    db = get_db()
    
    # Clear existing data
    db.artists.delete_many({})
    db.songs.delete_many({})
    
    # Sample data
    artist_songs = {
        "wizkid": ["Essence", "Ojuelegba", "Joro", "Come Closer", "Soco"],
        "burna boy": ["Last Last", "Ye", "On The Low", "Anybody"],
        "rema": ["Calm Down", "Dumebi", "Soundgasm"],
        "davido": ["Fall", "If", "Assurance", "Fia"],
        "ayra starr": ["Rush", "Bloody Samaritan"],
        "ckay": ["Love Nwantiti", "Emiliana"],
        "fireboy dml": ["Peru", "Scatter", "Bandana"],
        "olamide": ["Dangote", "Wo", "Caro"],
        "kizz daniel": ["Buga", "Fever", "Lie"],
        "joeboy": ["Baby", "Alcohol", "Sip"],
        "tems": ["Free Mind", "Damages", "Try Me"],
    }
    
    # Insert artists and songs
    for artist_name, songs in artist_songs.items():
        artist = {'name': artist_name.lower()}
        artist_id = db.artists.insert_one(artist).inserted_id
        
        for song_title in songs:
            song = {
                'artist_id': artist_id,
                'title': song_title
            }
            db.songs.insert_one(song)
    
    print("✅ Database initialized successfully!")

def get_song_for_artist(artist_name):
    """Get a random song for an artist - uses cached connection"""
    db = get_db()
    
    try:
        # Find the artist
        artist = db.artists.find_one({'name': artist_name.lower()})
        
        if artist:
            # Get all songs for this artist
            songs = list(db.songs.find({'artist_id': artist['_id']}))
            if songs:
                return random.choice(songs)['title']
        
        # If artist not found, get a random song from any artist
        random_song = db.songs.aggregate([{'$sample': {'size': 1}}]).next()
        return random_song['title'] if random_song else "Unknown Song"
    
    except Exception as e:
        print(f"❌ Error getting song: {e}")
        return "Unknown Song"

if __name__ == '__main__':
    init_db()