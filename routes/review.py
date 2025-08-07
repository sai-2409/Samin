# Review routes for the project

from flask import Blueprint, request, jsonify, render_template, session
import json
import os
from datetime import datetime
from config import SECRET_KEY, UPLOADS_DIR, ALLOWED_EXTENSIONS, MAX_FILE_SIZE
from werkzeug.utils import secure_filename
import uuid

review_bp = Blueprint("review", __name__)

# Use configuration variables instead of hardcoded values
UPLOAD_FOLDER = os.path.join(UPLOADS_DIR, 'reviews')

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@review_bp.route("/api/submit-review", methods=["POST"])
def submit_review():
    """Submit a new review for a product"""
    try:
        # Check if user is logged in
        user = session.get("user")
        if not user:
            return jsonify({"error": "User must be logged in to submit a review"}), 401
        
        data = request.get_json()
        product_id = data.get("product_id")
        rating = data.get("rating")
        review_text = data.get("review_text")
        order_id = data.get("order_id")
        image_data = data.get("image_data")  # Base64 image data
        
        # Validate required fields
        if not all([product_id, rating, review_text, order_id]):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Validate rating (1-5 stars)
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                return jsonify({"error": "Rating must be between 1 and 5"}), 400
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid rating format"}), 400
        
        # Allow general reviews about the store (no purchase verification needed)
        if product_id == "general" and order_id == "general":
            # Check if user has already reviewed the store
            if has_user_reviewed_product(user["login"], "general"):
                return jsonify({"error": "You have already left a review about our store"}), 409
        else:
            # For specific product reviews, check purchase
            if not has_user_purchased_product(user["login"], product_id, order_id):
                return jsonify({"error": "You can only review products you have purchased"}), 403
            
            # Check if user has already reviewed this product
            if has_user_reviewed_product(user["login"], product_id):
                return jsonify({"error": "You have already reviewed this product"}), 409
        
        # Handle image upload if provided
        image_filename = None
        if image_data:
            try:
                import base64
                # Remove data URL prefix if present
                if image_data.startswith('data:image/'):
                    image_data = image_data.split(',')[1]
                
                # Decode base64 and save file
                image_bytes = base64.b64decode(image_data)
                image_filename = f"review_{generate_review_id()}.jpg"
                image_path = os.path.join(UPLOAD_FOLDER, image_filename)
                
                with open(image_path, 'wb') as f:
                    f.write(image_bytes)
                    
            except Exception as e:
                print(f"Error saving image: {e}")
                image_filename = None
        
        # Create review object
        review = {
            "id": generate_review_id(),
            "user_id": user["login"],
            "user_name": user.get("real_name", user.get("display_name", user.get("login", "Anonymous"))),
            "user_avatar": user.get("avatar", ""),
            "product_id": product_id,
            "order_id": order_id,
            "rating": rating,
            "review_text": review_text,
            "image_filename": image_filename,
            "timestamp": datetime.now().isoformat(),
            "verified_purchase": True
        }
        
        # Save review to JSON file
        save_review(review)
        
        return jsonify({
            "success": True,
            "message": "Review submitted successfully",
            "review": review
        }), 201
        
    except Exception as e:
        print(f"Error submitting review: {e}")
        return jsonify({"error": "Internal server error"}), 500

@review_bp.route("/api/get-reviews/<product_id>")
def get_reviews(product_id):
    """Get all reviews for a specific product"""
    try:
        reviews = load_reviews()
        product_reviews = [review for review in reviews if review.get("product_id") == product_id]
        
        # Calculate average rating
        if product_reviews:
            avg_rating = sum(review["rating"] for review in product_reviews) / len(product_reviews)
            total_reviews = len(product_reviews)
        else:
            avg_rating = 0
            total_reviews = 0
        
        return jsonify({
            "reviews": product_reviews,
            "average_rating": round(avg_rating, 1),
            "total_reviews": total_reviews
        })
        
    except Exception as e:
        print(f"Error getting reviews: {e}")
        return jsonify({"error": "Internal server error"}), 500

@review_bp.route("/api/get-all-reviews")
def get_all_reviews():
    """Get all reviews for display on main page"""
    try:
        reviews = load_reviews()
        
        # Return all reviews sorted by date (newest first)
        sorted_reviews = sorted(reviews, key=lambda x: x.get("timestamp", ""), reverse=True)
        
        return jsonify({
            "reviews": sorted_reviews,
            "total_reviews": len(sorted_reviews)
        })
        
    except Exception as e:
        print(f"Error getting all reviews: {e}")
        return jsonify({"error": "Internal server error"}), 500

@review_bp.route("/api/user-reviews")
def get_user_reviews():
    """Get all reviews by the current user"""
    try:
        user = session.get("user")
        if not user:
            return jsonify({"error": "User must be logged in"}), 401
        
        reviews = load_reviews()
        user_reviews = [review for review in reviews if review.get("user_id") == user["login"]]
        
        return jsonify({"reviews": user_reviews})
        
    except Exception as e:
        print(f"Error getting user reviews: {e}")
        return jsonify({"error": "Internal server error"}), 500

@review_bp.route("/api/user-orders")
def get_user_orders():
    """Get all orders by the current user"""
    try:
        user = session.get("user")
        if not user:
            return jsonify({"error": "User must be logged in"}), 401
        
        orders = load_orders()
        user_orders = [order for order in orders if order.get("user_id") == user["login"]]
        
        return jsonify({"orders": user_orders})
        
    except Exception as e:
        print(f"Error getting user orders: {e}")
        return jsonify({"error": "Internal server error"}), 500

@review_bp.route("/api/delete-review/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    """Delete a user's own review"""
    try:
        user = session.get("user")
        if not user:
            return jsonify({"error": "User must be logged in"}), 401
        
        reviews = load_reviews()
        
        # Find the review
        review_index = None
        for i, review in enumerate(reviews):
            if review.get("id") == review_id and review.get("user_id") == user["login"]:
                review_index = i
                break
        
        if review_index is None:
            return jsonify({"error": "Review not found or you don't have permission to delete it"}), 404
        
        # Remove the review
        deleted_review = reviews.pop(review_index)
        save_reviews_to_file(reviews)
        
        return jsonify({
            "success": True,
            "message": "Review deleted successfully",
            "deleted_review": deleted_review
        })
        
    except Exception as e:
        print(f"Error deleting review: {e}")
        return jsonify({"error": "Internal server error"}), 500

@review_bp.route("/reviews")
def reviews_page():
    """Reviews page for users to view and manage their reviews"""
    user = session.get("user")
    if not user:
        return render_template("login_required.html")
    
    return render_template("reviews.html", user=user)

# Helper functions

def generate_review_id():
    """Generate a unique review ID"""
    return str(uuid.uuid4())

def load_reviews():
    """Load reviews from JSON file"""
    try:
        with open(os.path.join(DATA_DIR, 'reviews.json'), 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def load_orders():
    """Load orders from JSON file"""
    try:
        with open(os.path.join(DATA_DIR, 'orders.json'), 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_review(review):
    """Save a new review to the JSON file"""
    reviews = load_reviews()
    reviews.append(review)
    save_reviews_to_file(reviews)

def save_reviews_to_file(reviews):
    """Save reviews list to JSON file"""
    with open(os.path.join(DATA_DIR, 'reviews.json'), 'w', encoding='utf-8') as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)

def has_user_purchased_product(user_id, product_id, order_id):
    """Check if user has purchased the specific product"""
    try:
        orders = load_orders()
        
        # Find the specific order
        for order in orders:
            if order.get("order_id") == order_id and order.get("user_id") == user_id:
                # Check if the product is in the cart items
                cart_items = order.get("cart_items", [])
                for item in cart_items:
                    # Check both id and productName since cart items might not have id
                    if (str(item.get("id", "")) == str(product_id) or 
                        str(item.get("productName", "")) == str(product_id)):
                        return True
        return False
    except Exception as e:
        print(f"Error checking purchase: {e}")
        return False

def has_user_reviewed_product(user_id, product_id):
    """Check if user has already reviewed this product"""
    reviews = load_reviews()
    for review in reviews:
        if review.get("user_id") == user_id and review.get("product_id") == product_id:
            return True
    return False 