from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
import requests

app = Flask(__name__)
es =  Elasticsearch("http://rishipatel:rishipatel@localhost:9200")


def search_data(query):
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["description^3", "question", "content"]
            }
        },
        "highlight": {
            "fields": {
                "content": {
                    "pre_tags": ["<em>"],
                    "post_tags": ["</em>"],
                    "fragment_size": 150,
                    "number_of_fragments": 5
                },
                "description": {
                    "pre_tags": ["<em>"],
                    "post_tags": ["</em>"],
                    "fragment_size": 150,
                    "number_of_fragments": 3
                },
                "question": {
                    "pre_tags": ["<em>"],
                    "post_tags": ["</em>"],
                    "fragment_size": 150,
                    "number_of_fragments": 3
                }
            }
        }
    }

    res = es.search(index="api_index,text_index", body=body)
    return res['hits']['hits']


# "<em>Rishi</em> <em>is</em> developer by profession. <em>Rishi</em> <em>is</em> jugadu person by techniques. <em>Rishi</em> <em>is</em> smart and attaractive good looking person."
# "<em>Rishi</em> is developer by <em>profession</em>. <em>Rishi</em> is jugadu person by techniques. <em>Rishi</em> is smart and attaractive good looking person."


@app.route('/query', methods=['POST'])
def query():
    user_query = request.json.get("query")
    results = search_data(user_query)

    if not results:
        return jsonify({"message": "No matching data found"}), 404

    top_result = results[0]['_source']

    if 'highlight' in results[0]:
        highlight = results[0]['highlight']['content'][0]
        return jsonify({"highlight": highlight})

    if top_result['type'] == 'faq':
        return jsonify({"answer": top_result['answer']})

    elif top_result['type'] == 'api':
        api_details = top_result

        # Check if the required parameters are provided in the request
        required_params = api_details.get('required_params', [])
        missing_params = [param for param in required_params if param not in request.json]

        if missing_params:
            return jsonify({"message": f"Missing required parameters: {', '.join(missing_params)}",
                            "required_params": required_params})

        # Make the API call if all required parameters are present
        response = make_api_call(api_details, request.json)

        return jsonify(response)


def make_api_call(api_details, user_params):
    url = api_details['url']
    method = api_details['method']
    params = {key: user_params[key] for key in api_details.get('required_params', [])}

    if method == 'GET':
        response = requests.get(url, params=params)
    elif method == 'POST':
        response = requests.post(url, json=params)

    return response.json()


if __name__ == '__main__':
    app.run(debug=True)
