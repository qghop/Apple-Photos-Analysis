import osxphotos

print("Opening database, may take a moment...")
_db = osxphotos.PhotosDB()
if not _db:
    print("No Photos Library found. Exiting.")
    exit(1)
print("Database opened successfully.")

def get_photos():
    return _db.photos()
