from elasticsearch import Elasticsearch, helpers

# Connect to Elasticsearch with authentication
es = Elasticsearch("http://rishipatel:rishipatel@localhost:9200")
# Define some sample large textual data
large_texts = [
    {
        "_index": "text_index",
        "_id": "1",
        "_source": {
            "title": "Article on Financial Literacy",
            "content": """
            Financial literacy is the ability to understand and effectively use various financial skills, 
            including personal financial management, budgeting, and investing. It is the foundation of your 
            relationship with money, and it is a lifelong journey of learning. The earlier you start, the better off you will be.
            Some key aspects of financial literacy include understanding how to create a budget, the importance of savings, 
            the basics of credit, and how to invest for the future. In today's world, financial literacy is more important 
            than ever as individuals are increasingly responsible for their own financial security and well-being.
            """
        }
    },
    {
        "_index": "text_index",
        "_id": "2",
        "_source": {
            "title": "Guide to Programming in Python",
            "content": """
            Python is a high-level, interpreted programming language with dynamic semantics. Its high-level built-in data structures, 
            combined with dynamic typing and dynamic binding, make it very attractive for Rapid Application Development, 
            as well as for use as a scripting or glue language to connect existing components together. Python's simple, easy-to-learn syntax 
            emphasizes readability and therefore reduces the cost of program maintenance. Python supports modules and packages, 
            which encourages program modularity and code reuse. The Python interpreter and the extensive standard library are available 
            in source or binary form without charge for all major platforms, and can be freely distributed.
            """
        }
    },
    {
        "_index": "text_index",
        "_id": "3",
        "_source": {
            "title": "Details about Rishi",
            "content": """
            Rishi is developer by profession. Rishi is jugadu person by techniques. Rishi is smart and attaractive good looking person. Rishi is good person as a employee.
            """
        }
    }
]

# Index the data
helpers.bulk(es, large_texts)
