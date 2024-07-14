from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch, helpers
import requests
from index_new_data import Tokenizer
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # Enable CORS for specific origin

# Elasticsearch connection
es = Elasticsearch("http://rishipatel:rishipatel@localhost:9200")

token_instance = Tokenizer()

def search_data(query):
    token_vector = token_instance.get_token(query)
    # print("token_vector",token_vector)
    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "script_score": {
                            "query": {
                                "match_all": {}
                            },
                            "script": {
                                "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                                "params": {
                                    "query_vector": token_vector
                                }
                            }
                        }
                    }
                ],
                "should": [
                    {
                        "multi_match": {
                            "query": query,
                            "fields": ["description^3", "title^3", "required_params^2", "question", "content"]
                        }
                    },
                    {
                        "match_phrase": {
                            "answer": {
                                "query": query,
                                "boost": 2.0
                            }
                        }
                    },
                    {
                        "match": {
                            "keywords": {
                                "query": query,
                                "boost": 4
                            }
                        }
                    }
                ],
                "minimum_should_match": 1
            }
        },
        "highlight": {
            "fields": {
                "content": {
                    "pre_tags": ["<em>"],
                    "post_tags": ["</em>"],
                    "fragment_size": 150,
                    "number_of_fragments": 1
                },
                "description": {
                    "pre_tags": ["<em>"],
                    "post_tags": ["</em>"],
                    "fragment_size": 150,
                    "number_of_fragments": 1
                },
                "question": {
                    "pre_tags": ["<em>"],
                    "post_tags": ["</em>"],
                    "fragment_size": 150,
                    "number_of_fragments": 1
                }
            }
        }
    }

    res = es.search(index="api_index,text_index", body=body)
    return res['hits']['hits']

def clean_query(query):
    # List of words to filter out
    stopwords = [
        "is", "am", "are", "what", "how", "to", "my", "do", "does", "can", "could", "should",
        "would", "will", "have", "has", "had", "been", "being", "with", "without", "of",
        "in", "on", "at", "by", "for", "from", "about", "above", "below", "under", "over",
        "through", "into", "onto", "until", "during", "after", "before", "between", "among",
        "throughout", "within", "around", "against", "behind", "beside", "between", "beyond",
        "except", "instead", "upon", "toward", "behind", "below", "beneath", "among", "besides"
    ]

    # Split query into words, filter out stopwords, and join back into a cleaned query
    cleaned_query = " ".join([word for word in query.split() if word.lower() not in stopwords])
    return cleaned_query

@app.route('/query', methods=['POST'])
def query():
    user_query = request.json.get("query")
    cleaned_query = clean_query(user_query)
    results = search_data(cleaned_query)

    if not results:
        return jsonify({"message": "No matching data found"}), 404

    top_result = results[0]['_source']
    # print('top_res RP', top_result)
    if 'type' in top_result and top_result['type'] == 'faq':
        return jsonify({"answer": top_result['answer']})
    elif 'type' in top_result and top_result['type'] == 'api':
        api_details = top_result
        required_params = api_details.get('required_params', [])
        missing_params = [param for param in required_params if param not in request.json]

        if missing_params:
            return jsonify({"message": f"Missing required parameters: {', '.join(missing_params)}",
                            "required_params": required_params})

        response = make_api_call(api_details, request.json)
        return jsonify(response)
    elif 'highlight' in results[0]:
        highlights = results[0]['highlight']
        highlighted_text = []
        for field in highlights:
            highlighted_text.extend(highlights[field])
        best_snippet = select_best_snippet(highlighted_text, user_query)
        return jsonify({"highlight": best_snippet})
    else:
        return jsonify({"message": "No matching data found"}), 404

def select_best_snippet(highlighted_text, user_query):
    query_terms = set(user_query.lower().split())
    best_snippet = ""

    for snippet in highlighted_text:
        snippet = snippet.replace('<em>', '').replace('</em>', '')

        snippet_terms = set(snippet.lower().split())
        overlap = len(query_terms.intersection(snippet_terms))

        if overlap > 0:
            best_snippet = snippet
            break

    return best_snippet

def make_api_call(api_details, user_params):
    url = api_details['url']
    method = api_details['method']
    params = {key: user_params[key] for key in api_details.get('required_params', [])}
    print('data',url, method, params)
    if method == 'GET':
        response = requests.get(url, params=params)
    elif method == 'POST':
        response = requests.post(url, json=params)

    return response.json()

if __name__ == '__main__':
    app.run(debug=True, port=5002)
