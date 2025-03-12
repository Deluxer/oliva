import time
start_time = time.time()
from app.agents.implementations.search_amazon_products.agent_by_superlinked import agent

if __name__ == "__main__":
    try:
        result = agent.process({
            "query": "books with a price lower than 100 and a rating bigger than 4"
        })
        print(result)
    except Exception as e:
        print(f"Error in main: {str(e)}")
        raise
    finally:
        execution_time = time.time() - start_time
        print(f"\nTotal execution time: {execution_time:.2f} seconds")