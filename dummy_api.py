from flask import Flask, jsonify, request, send_file
import os
from loan_validator import predict_loan_status
app = Flask(__name__)

# Ensure the directory for the sample PDF exists
os.makedirs('static', exist_ok=True)

# Create a sample PDF file for download (only for demo purposes)
sample_pdf_path = 'static/sample.pdf'
with open(sample_pdf_path, 'wb') as f:
    f.write(b'%PDF-1.4\n%...\n')  # Minimal PDF content for demonstration

@app.route('/download_pdf', methods=['GET'])
def download_pdf():
    ans = send_file(sample_pdf_path, as_attachment=True, download_name='sample.pdf')
    print('ans', ans)
    return ans

@app.route('/submit_file', methods=['POST'])
def submit_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the file (you might want to do more processing here)
    file.save(os.path.join('uploads', file.filename))

    return jsonify({'status': 'success', 'filename': file.filename})

@app.route('/payment', methods=['POST'])
def payment():
    phone_num = request.json.get('phone_num')
    otp = request.json.get('otp')
    password = request.json.get('password')

    # Dummy response for payment details
    data = {
        "status" : True,
        "phone_num": phone_num,
        "otp": otp,
        "password": password,
        "payment_details": {
            "status": "success",
            "amount": "100.00",
            "currency": "USD"
        }
    }
    return jsonify(data)


@app.route('/dummy_weather', methods=['GET'])
def dummy_weather():
    city = request.args.get('city', 'New York')
    data = {
        "status": True,
        "city": city,
        "temperature": "22°C",
        "description": "Clear sky"
    }
    return jsonify(data)


@app.route('/dummy_currency', methods=['GET'])
def dummy_currency():
    data = {
        "status": True,
        "USD": 1.0,
        "EUR": 0.85,
        "JPY": 110.0
    }
    return jsonify(data)

@app.route('/user_profile', methods=['POST'])
def user_profile_api():
    data = request.json
    # Dummy implementation
    return jsonify({"message": "User profile information updated successfully", "data": data})

@app.route('/product_catalog', methods=['GET'])
def product_catalog_api():
    category = request.args.get('category')
    # Dummy implementation
    products = [
        {"name": "Product 1", "price": 100},
        {"name": "Product 2", "price": 150},
        {"name": "Product 3", "price": 200}
    ]
    return jsonify({"message": f"Product catalog for category '{category}'", "products": products})


def run_ml_model(data):
    return "Eligible"


@app.route('/check_loan_eligibility', methods=['POST'])
def check_loan_eligibility():
    try:
        # Get JSON payload
        data = request.get_json()

        # Validate payload
        if not isinstance(data, dict):
            return jsonify({"error": "Invalid payload format"}), 400

        # Predict loan status
        result = predict_loan_status(data)

        # Return the result as a JSON response
        return jsonify({"message": result.get('message'), "status": result.get('status')})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001)
