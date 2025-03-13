from app.agents.implementations.blog_post.agent import agent
import logging
import time

# logging.basicConfig(
#     level=logging.DEBUG,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
# )
# logger = logging.getLogger(__name__)

if __name__ == "__main__":
    """Search blog posts using the BlogPostAgent"""
    start_time = time.time()
    try:
        result = agent.process({
            "query": "How Harrison Chase defines an agent?"
        })
        print(result)
    except Exception as e:
        print(f"Error: {str(e)}")
        raise
    finally:
        execution_time = time.time() - start_time
        print(f"\nTotal execution time: {execution_time:.2f} seconds")