from flask import Flask, request, jsonify
from FlagEmbedding import FlagReranker
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import logging
import os

app = Flask(__name__)

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize the reranker
reranker = FlagReranker('BAAI/bge-reranker-v2-m3', use_fp16=True) # Setting use_fp16 to True speeds up computation with a slight performance degradation

# Thread pool for timeout handling
executor = ThreadPoolExecutor(max_workers=1)


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring.
    """
    return jsonify({'status': 'ok'}), 200


@app.route('/rerank', methods=['POST'])
def rerank():
    """
    Endpoint to compute reranker scores.
    """
    try:
        data = request.get_json()
        if not data or 'query' not in data or 'passages' not in data:
            return jsonify({'error': 'Please provide "query" and "passages".'}), 400

        query = data['query']
        passages = data['passages']

        # Validate input
        if not query or not isinstance(query, str):
            return jsonify({'error': '"query" must be a non-empty string.'}), 400

        if not passages or not all(isinstance(p, str) and p.strip() for p in passages):
            return jsonify({'error': '"passages" must be a list of non-empty strings.'}), 400

        # Prepare input for reranker
        input_data = [[query, passage] for passage in passages]
        normalize = True

        # Compute scores with timeout
        future = executor.submit(reranker.compute_score, input_data, normalize=normalize)
        scores = future.result(timeout=10)  # Timeout in seconds

        return jsonify({'scores': scores})

    except TimeoutError:
        logging.error("Reranking operation timed out.")
        return jsonify({'error': 'Reranking operation timed out.'}), 504
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
