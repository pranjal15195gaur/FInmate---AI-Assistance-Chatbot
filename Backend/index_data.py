# from elasticsearch import helpers, Elasticsearch
#
# # Connect to Elasticsearch with authentication
# es = Elasticsearch("http://rishipatel:rishipatel@localhost:9200")
#
# # Define some sample API data with required parameters and FAQs
# data = [
#     {
#         "_index": "api_index",
#         "_id": "1",
#         "_source": {
#             "type": "api",
#             "name": "payment_api",
#             "description": "API for fetching payment details including phone number verification and password validation.",
#             "url": "http://localhost:5001/payment",
#             "method": "POST",
#             "required_params": ["phone_num", "otp", "password"]
#         }
#     },
#     {
#         "_index": "api_index",
#         "_id": "2",
#         "_source": {
#             "type": "api",
#             "name": "dummy_weather_api",
#             "description": "API that provides simulated weather information for a specified city.",
#             "url": "http://localhost:5001/dummy_weather",
#             "method": "GET",
#             "required_params": ["city"]
#         }
#     },
#     {
#         "_index": "api_index",
#         "_id": "3",
#         "_source": {
#             "type": "faq",
#             "question": "What is the capital of France?",
#             "answer": "The capital of France is Paris."
#         }
#     },
#     {
#         "_index": "api_index",
#         "_id": "4",
#         "_source": {
#             "type": "faq",
#             "question": "How to reset my password?",
#             "answer": "To reset your password, navigate to the settings page and click on 'Reset Password'."
#         }
#     }
# ]
#
# # Index the data
# helpers.bulk(es, data)
#
# # Define some sample large textual data
# large_texts = [
#     {
#         "_index": "text_index",
#         "_id": "1",
#         "_source": {
#             "title": "Article on Financial Literacy: Understanding Personal Finance Management",
#             "content": """
#             Financial literacy is the ability to understand and effectively use various financial skills,
#             including personal financial management, budgeting, and investing. It is the foundation of your
#             relationship with money, and it is a lifelong journey of learning. The earlier you start, the better off you will be.
#             Some key aspects of financial literacy include understanding how to create a budget, the importance of savings,
#             the basics of credit, and how to invest for the future. In today's world, financial literacy is more important
#             than ever as individuals are increasingly responsible for their own financial security and well-being.
#             """
#         }
#     },
#     {
#         "_index": "text_index",
#         "_id": "2",
#         "_source": {
#             "title": "Guide to Programming in Python: Features, Syntax, and Applications",
#             "content": """
#             Python is a high-level, interpreted programming language with dynamic semantics. Its high-level built-in data structures,
#             combined with dynamic typing and dynamic binding, make it very attractive for Rapid Application Development,
#             as well as for use as a scripting or glue language to connect existing components together. Python's simple, easy-to-learn syntax
#             emphasizes readability and therefore reduces the cost of program maintenance. Python supports modules and packages,
#             which encourages program modularity and code reuse. The Python interpreter and the extensive standard library are available
#             in source or binary form without charge for all major platforms, and can be freely distributed.
#             """
#         }
#     },
#     {
#         "_index": "text_index",
#         "_id": "3",
#         "_source": {
#             "title": "Details about Rishi: Professional Background and Skills",
#             "content": """
#             Rishi is a professional developer known for innovative techniques and problem-solving skills. He is recognized for his
#             smart and attractive personality, making him a valuable asset as an employee. Rishi's proficiency spans across various
#             technologies and domains, ensuring effective delivery and robust solutions.
#             """
#         }
#     }
# ]
#
#
# # Index the data
# helpers.bulk(es, large_texts)



from elasticsearch import helpers, Elasticsearch

# Connect to Elasticsearch with authentication
es = Elasticsearch("http://rishipatel:rishipatel@localhost:9200")

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
            "keywords": ["payment", "phone verification", "password validation"]
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
            "keywords": ["weather", "simulated data"]
        }
    },
    {
        "_index": "api_index",
        "_id": "3",
        "_source": {
            "type": "faq",
            "question": "What is the capital of France?",
            "answer": "The capital of France is Paris.",
            "keywords": ["capital", "France", "Paris"]
        }
    },
    {
        "_index": "api_index",
        "_id": "4",
        "_source": {
            "type": "faq",
            "question": "How to reset my password?",
            "answer": "To reset your password, navigate to the settings page and click on 'Reset Password'.",
            "keywords": ["password reset", "account security"]
        }
    }
]

# Index the data
helpers.bulk(es, data)

# Define sample large textual data with keywords
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
            "keywords": ["financial literacy", "budgeting", "investing"]
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
            "keywords": ["Python programming", "Rapid Application Development", "code reuse"]
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
            "keywords": ["developer", "innovative techniques", "problem-solving"]
        }
    }
]

# Index the data
helpers.bulk(es, large_texts)
