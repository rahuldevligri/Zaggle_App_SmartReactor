# ⚡️ Zaggle App SmartReactor 🤖🔥  
**AI-Powered Smart Responder for App Reviews**

Welcome to **Zaggle App SmartReactor**, your intelligent assistant for handling app reviews like a pro! Built with ❤️ using OpenAI GPT models, this tool **automatically analyzes user feedback**, matches it with relevant FAQs, and responds empathetically — all in real time ⚡

---

## ✨ Key Features

| 🚀 Feature                         | 💡 Description                                                                 |
|----------------------------------|-------------------------------------------------------------------------------|
| 🤖 **AI Responses**              | Generates warm, human-like replies using OpenAI GPT-4 / GPT-3.5-turbo-0125   |
| 🔍 **Semantic FAQ Matching**     | Matches reviews to your FAQ database using vector similarity with FAISS      |
| 🧠 **Fast Embedding Lookup**     | Uses OpenAI’s embedding models with local caching for super-fast responses   |
| 🧪 **Live Web UI**               | Easy-to-use Flask app for testing responses manually                         |
| ⚙️ **Customizable Contact Info** | Dynamic contact details based on product (SAVE, Propel, EMS, etc.)           |

---

## 🧰 Tech Stack

- 🐍 Python 3.10+
- 🧠 OpenAI GPT-4 / GPT-3.5-turbo-0125
- 🔍 FAISS (Facebook AI Similarity Search)
- 🌐 Flask (Web Interface)
- 📊 Pandas + NumPy
- 📁 CSV (FAQ database)
- 🔁 Tenacity (retry handling)

---

## 📁 Folder Structure

```bash
zaggle-app-smartreactor/
│
├── app.py                    # Flask app entrypoint
├── faq_loader.py             # Loads and embeds FAQ CSV
├── responder.py              # GPT prompt and reply logic
├── vector_store.py           # FAISS vector search
├── templates/
│   └── index.html            # UI Template
├── static/
│   ├── css/
│   │   └── style.css         # Custom styles
│   ├── js/
│   │   └── script.js         # Custom JavaScript
│   └── images/
│       ├── icon.png          # App icon
│       └── logo.jpeg         # Zaggle logo
├── embeddings_cache/         # Cached embeddings
├── faqs.csv                  # Your FAQ database
├── requirements.txt
└── README.md
=======
# My Project
>>>>>>> 04f70024 (Initial commit)
