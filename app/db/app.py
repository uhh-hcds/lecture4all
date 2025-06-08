from flask import Flask, request, jsonify
from src.query import process_query as pq

app = Flask(__name__)

#in app.py postet er die query hierhin, sobald ein user eine anfrage stellt
@app.route('/app/process_query', methods=['POST'])
def process_query():
    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({'error': 'No query provided'}), 400

    result = pq(query)

    return jsonify(result)   

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7001)
    
#@app.route('/app/get_subtitles_for_video', methods=['POST'])
#def process_query_subtitles