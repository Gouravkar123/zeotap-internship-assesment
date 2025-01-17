from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser

app = Flask(__name__)
CORS(app)

# Define the schema for Whoosh
schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True))

# Create an index directory
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")

# Create an index
ix = create_in("indexdir", schema)

# Sample data for the CDPs (In a real application, this would be loaded from documentation)
cdp_data = {
    "Segment": [
        {"title": "Setting up a new source", "content": "To set up a new source in Segment, go to the Sources tab..."},
        {"title": "Creating a user profile", "content": "To create a user profile in Segment, use the identify call..."},
    ],
    "mParticle": [
        {"title": "Creating a user profile", "content": "To create a user profile in mParticle, use the Identity API..."},
    ],
    "Lytics": [
        {"title": "Building an audience segment", "content": "To build an audience segment in Lytics, navigate to the Audiences tab..."},
    ],
    "Zeotap": [
        {"title": "Integrating data", "content": "To integrate your data with Zeotap, follow the integration guide..."},
    ],
}

# Index the sample data
def index_data():
    writer = ix.writer()
    for cdp, entries in cdp_data.items():
        for entry in entries:
            writer.add_document(title=entry["title"], content=entry["content"])
    writer.commit()

index_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.json.get('question')
    response = search_index(user_question)
    return jsonify(response)

def search_index(query):
    results = []
    with ix.searcher() as searcher:
        query_parser = QueryParser("content", ix.schema)
        parsed_query = query_parser.parse(query)
        search_results = searcher.search(parsed_query, limit=5)
        for result in search_results:
            results.append({"title": result['title'], "content": result['content']})
    return results

if __name__ == '__main__':
    app.run(debug=True)