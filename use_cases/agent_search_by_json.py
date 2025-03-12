import time
start_time = time.time()
from app.agents.implementations.search_amazon_products.agent_by_json import agent

def agent_search_in_amazon_products_by_json():
    """Search amazon products using the SearchAmazonProductsAgentByJson"""
    try:
        result = agent.process({
            "query": "products with a price lower than 100 and a rating bigger than 3"
        })
        print(result)
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    agent_search_in_amazon_products_by_json()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"\nTotal execution time: {execution_time:.2f} seconds")