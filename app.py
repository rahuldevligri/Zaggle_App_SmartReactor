from flask import Flask, render_template, request
import pandas as pd
from faq_loader import load_faqs, embed_faqs
from vector_store import FAQVectorStore
from responder import get_review_embedding, generate_response
import traceback

app = Flask(__name__)

def initialize_app():
    try:
        print("🔍 Loading FAQs...")
        faq_df = load_faqs("faqs.csv")
        print(f"✅ Loaded {len(faq_df)} FAQs")
        
        print("🧠 Processing embeddings...")
        faq_embeddings = embed_faqs(faq_df['user_query'].tolist())
        
        print("🔧 Building vector store...")
        global vector_store
        vector_store = FAQVectorStore(faq_embeddings, faq_df)
        print("✅ Initialization complete\n")
        return True
    except Exception as e:
        print(f"\n❌ Startup failed: {str(e)}")
        traceback.print_exc()
        return False

if not initialize_app():
    exit(1)

@app.route('/', methods=['GET', 'POST'])
def home():
    response = None
    review_text = ''
    rating = None
    
    if request.method == 'POST':
        review_text = request.form['review'].strip()
        try:
            rating = int(request.form['rating'])
            if rating < 4:
                try:
                    review_embedding = get_review_embedding(review_text)
                    best_faq = vector_store.search(review_embedding)
                    response = generate_response(
                        review_text, 
                        rating, 
                        best_faq['product_responses'],
                        product=best_faq['product']
                    )
                except Exception as e:
                    response = f"""🛎️ Support Response\n\n😔 We apologize for the inconvenience. 
                    Please contact us directly:\n📞 18605001231 | ✉️ care@zaggle.in"""
            else:
                response = generate_response(review_text, rating)
            
        except Exception as e:
            print(f"\n🔥 Critical Error: {str(e)}")


            print(f"\n🔥 Error: {str(e)}")
            traceback.print_exc()
            response = f"""🛎️ Support Response\n\n😔 We're here to help! 
            Contact us directly:\n📞 18605001231 | ✉️ care@zaggle.in"""

    return render_template(
        'index.html',
        response=response,
        review_text=review_text,
        rating=rating or 0,
        generating=request.method == 'POST'
    )

if __name__ == '__main__':
    print("🚀 Starting server at http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)