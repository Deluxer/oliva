import time
start_time = time.time()
from app.agents.implementations.supervisor import agent, graph

def agent_supervisor():
    try:
        result = agent.process({
            "query": "products with a price lower than 50 and a rating lower than 2"
            # "query": "How Harrison Chase defines an agent?"
            # "query": 'prvide information about "Before MCP, How Were AI Systems Handling Context And Tool Access?" topic'
        })
        print(result)
    except Exception as e:
        print(f"Error in main: {str(e)}")
        raise
    finally:
        execution_time = time.time() - start_time
        print(f"\nTotal execution time: {execution_time:.2f} seconds")

def agent_supervisor_graph():
    try:
        config = {
            "configurable": {
                "thread_id": "1",
                "user_id": "1"  # Add user_id to config
            }
        }
        result = graph.invoke(
            {"messages": [{"role": "user", "content": "products with a price lower than 100 and a rating bigger than 4"}]},
            config,
        )
        if "messages" in result:
            message = result["messages"][-1]
            message.pretty_print()
        else:
            print("No messages in result")

    except Exception as e:
        print(f"Error in main: {str(e)}")
        raise
    finally:
        execution_time = time.time() - start_time
        print(f"\nTotal execution time: {execution_time:.2f} seconds")        

if __name__ == "__main__":
    agent_supervisor_2()