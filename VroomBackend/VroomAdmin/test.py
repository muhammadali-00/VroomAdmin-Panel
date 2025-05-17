# test.py

import firebase  # This should run initialize_app()

from firebase_admin import firestore

# Initialize Firestore DB
db = firestore.client()

# Test write
doc_ref = db.collection('testCollection').document('testDoc')
doc_ref.set({
    'status': 'connected',
    'timestamp': firestore.SERVER_TIMESTAMP
})

# Test read
result = doc_ref.get()
if result.exists:
    print("✅ Firebase connection successful. Document data:", result.to_dict())
else:
    print("❌ Failed to fetch document.")
