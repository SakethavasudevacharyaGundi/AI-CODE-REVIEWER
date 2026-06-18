from datetime import datetime,timezone
reviews ={}

def save_review(review_id, review_data):
    reviews[review_id] = {
        "review": review_data,
        "created_at":datetime.now(timezone.utc).isoformat()    
        }
def get_review(review_id):
    return reviews.get(review_id)
def list_reviews():
    return reviews