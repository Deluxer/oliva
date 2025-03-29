import time
start_time = time.time()
from app.agents.implementations.supervisor import agent

if __name__ == "__main__":
    try:
        result = agent.process({
            # "query": "products with a price lower than 100 and a rating bigger than 4"
            "query": "How Harrison Chase defines an agent?"
            # "query": 'prvide information about "Before MCP, How Were AI Systems Handling Context And Tool Access?" topic'
        })
        print(result)
    except Exception as e:
        print(f"Error in main: {str(e)}")
        raise
    finally:
        execution_time = time.time() - start_time
        print(f"\nTotal execution time: {execution_time:.2f} seconds")