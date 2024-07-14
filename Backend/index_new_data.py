from elasticsearch import helpers, Elasticsearch
import pandas as pd
import numpy as np
from tqdm.auto import tqdm
from sentence_transformers import SentenceTransformer
from joblib import Memory

# Create a cache directory
cache_dir = './cache'
memory = Memory(cache_dir, verbose=0)

# Initialize SentenceTransformer model with caching
@memory.cache
def load_sentence_transformer_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

# Load the model
model = load_sentence_transformer_model()


# Elasticsearch connection
es = Elasticsearch("http://rishipatel:rishipatel@localhost:9200")




# Define Tokenizer class for generating vector embeddings
class Tokenizer:
    def __init__(self):
        self.model = model

    def get_token(self, text):
        sentences = [text]
        sentence_embeddings = self.model.encode(sentences)
        return sentence_embeddings[0].tolist()


token_instance = Tokenizer()

# Define sample API data with required parameters and FAQs, including keywords
data = [
    {
        "_index": "api_index",
        "_id": "1",
        "_source": {
            "type": "api",
            "name": "payment_api",
            "description": "API for fetching payment details including phone number verification and password validation.",
            "url": "http://localhost:5001/payment",
            "method": "POST",
            "required_params": ["phone_num", "otp", "password"],
            "keywords": ["payment", "phone verification", "password validation"],
            "vector": token_instance.get_token(
                "API for fetching payment details including phone number verification and password validation.")
        }
    },
    {
        "_index": "api_index",
        "_id": "2",
        "_source": {
            "type": "api",
            "name": "dummy_weather_api",
            "description": "API that provides simulated weather information for a specified city.",
            "url": "http://localhost:5001/dummy_weather",
            "method": "GET",
            "required_params": ["city"],
            "keywords": ["weather", "simulated data"],
            "vector": token_instance.get_token("API that provides simulated weather information for a specified city.")
        }
    },
    {
        "_index": "api_index",
        "_id": "3",
        "_source": {
            "type": "faq",
            "question": "What is the capital of France?",
            "answer": "The capital of France is Paris.",
            "keywords": ["capital", "France", "Paris"],
            "vector": token_instance.get_token("What is the capital of France?")
        }
    },
    {
        "_index": "api_index",
        "_id": "4",
        "_source": {
            "type": "faq",
            "question": "How to reset my password?",
            "answer": "To reset your password, navigate to the settings page and click on 'Reset Password'.",
            "keywords": ["password reset", "account security"],
            "vector": token_instance.get_token("How to reset my password?")
        }
    },
    {
        "_index": "api_index",
        "_id": "5",
        "_source": {
            "type": "api",
            "name": "user_profile_api",
            "description": "API for managing user profile information including name, email, and preferences.",
            "url": "http://localhost:5001/user_profile",
            "method": "POST",
            "required_params": ["user_id", "name", "email"],
            "keywords": ["user profile", "preferences management"],
            "vector": token_instance.get_token(
                "API for managing user profile information including name, email, and preferences.")
        }
    },
    {
        "_index": "api_index",
        "_id": "6",
        "_source": {
            "type": "api",
            "name": "product_catalog_api",
            "description": "API for retrieving product catalog information such as categories, prices, and availability.",
            "url": "http://localhost:5001/product_catalog",
            "method": "GET",
            "required_params": ["category"],
            "keywords": ["product catalog", "category information"],
            "vector": token_instance.get_token(
                "API for retrieving product catalog information such as categories, prices, and availability.")
        }
    },
    {
        "_index": "api_index",
        "_id": "7",
        "_source": {
    "type": "api",
    "name": "check_loan_eligibility",
    "description": "API to check loan eligibility, loan check, loan approval checker",
    "url": "http://localhost:5001/check_loan_eligibility",
    "method": "POST",
    "required_params": [
        "Gender",
        "Married",
        "Dependents",
        "Education",
        "Self_Employed",
        "ApplicantIncome",
        "CoapplicantIncome",
        "LoanAmount",
        "Loan_Amount_Term",
        "Credit_History",
        "Property_Area"
    ],
    "keywords": [
        "loan",
        "loan approval",
        "loan checker",
        "Eligible for loan",
        "loan eligibility",
        "financial approval",
        "credit check",
        "loan application",
        "loan terms",
        "income verification",
        "self-employed loan",
        "graduate loan",
        "loan dependents",
        "property area loan",
        "credit history check",
        "loan amount",
        "loan term"
    ],
    "vector": token_instance.get_token(
        "API to check loan eligibility, loan check, loan approval checker."
    )
}
    }
#     ,
# {
#         "_index": "api_index",
#         "_id": "7",
#         "_source": {
#             "type": "api",
#             "name": "download_pdf_api",
#             "description": "API for downloading a sample PDF file.",
#             "url": "http://localhost:5001/download_pdf",
#             "method": "GET",
#             "required_params": [],
#             "keywords": ["download", "PDF"],
#             "vector": token_instance.get_token("API for downloading a sample PDF file.")
#         }
#     },
#     {
#         "_index": "api_index",
#         "_id": "8",
#         "_source": {
#             "type": "api",
#             "name": "submit_file_api",
#             "description": "API for submitting a file and receiving a response.",
#             "url": "http://localhost:5001/submit_file",
#             "method": "POST",
#             "required_params": ["file"],
#             "keywords": ["submit", "file upload"],
#             "vector": token_instance.get_token("API for submitting a file and receiving a response.")
#         }
#     }

]

# Index the data
helpers.bulk(es, data)

# Define sample large textual data with keywords and vectors
large_texts = [
    {
        "_index": "text_index",
        "_id": "1",
        "_source": {
            "title": "Article on Financial Literacy: Understanding Personal Finance Management",
            "content": """
            Financial literacy is the ability to understand and effectively use various financial skills, 
            including personal financial management, budgeting, and investing. It is the foundation of your 
            relationship with money, and it is a lifelong journey of learning. The earlier you start, the better off you will be.
            Some key aspects of financial literacy include understanding how to create a budget, the importance of savings, 
            the basics of credit, and how to invest for the future. In today's world, financial literacy is more important 
            than ever as individuals are increasingly responsible for their own financial security and well-being.""",
            "keywords": ["financial literacy", "budgeting", "investing"],
            "vector": token_instance.get_token("""
            Financial literacy is the ability to understand and effectively use various financial skills, 
            including personal financial management, budgeting, and investing. It is the foundation of your 
            relationship with money, and it is a lifelong journey of learning. The earlier you start, the better off you will be.
            Some key aspects of financial literacy include understanding how to create a budget, the importance of savings, 
            the basics of credit, and how to invest for the future. In today's world, financial literacy is more important 
            than ever as individuals are increasingly responsible for their own financial security and well-being.""")
        }
    },
    {
        "_index": "text_index",
        "_id": "2",
        "_source": {
            "title": "Guide to Programming in Python: Features, Syntax, and Applications",
            "content": """
            Python is a high-level, interpreted programming language with dynamic semantics. Its high-level built-in data structures, 
            combined with dynamic typing and dynamic binding, make it very attractive for Rapid Application Development, 
            as well as for use as a scripting or glue language to connect existing components together. Python's simple, easy-to-learn syntax 
            emphasizes readability and therefore reduces the cost of program maintenance. Python supports modules and packages, 
            which encourages program modularity and code reuse. The Python interpreter and the extensive standard library are available 
            in source or binary form without charge for all major platforms, and can be freely distributed.""",
            "keywords": ["Python programming", "Rapid Application Development", "code reuse"],
            "vector": token_instance.get_token("""
            Python is a high-level, interpreted programming language with dynamic semantics. Its high-level built-in data structures, 
            combined with dynamic typing and dynamic binding, make it very attractive for Rapid Application Development, 
            as well as for use as a scripting or glue language to connect existing components together. Python's simple, easy-to-learn syntax 
            emphasizes readability and therefore reduces the cost of program maintenance. Python supports modules and packages, 
            which encourages program modularity and code reuse. The Python interpreter and the extensive standard library are available 
            in source or binary form without charge for all major platforms, and can be freely distributed.""")
        }
    },
    {
        "_index": "text_index",
        "_id": "3",
        "_source": {
            "title": "Details about Rishi: Professional Background and Skills",
            "content": """
            Rishi is a professional developer known for innovative techniques and problem-solving skills. He is recognized for his 
            smart and attractive personality, making him a valuable asset as an employee. Rishi's proficiency spans across various 
            technologies and domains, ensuring effective delivery and robust solutions.""",
            "keywords": ["developer", "innovative techniques", "problem-solving"],
            "vector": token_instance.get_token("""
            Rishi is a professional developer known for innovative techniques and problem-solving skills. He is recognized for his 
            smart and attractive personality, making him a valuable asset as an employee. Rishi's proficiency spans across various 
            technologies and domains, ensuring effective delivery and robust solutions.""")
        }
    }
]

# Index the data
helpers.bulk(es, large_texts)

