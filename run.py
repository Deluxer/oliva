from app.agents.implementations.blog_post.agent import BlogPostAgent
from app.agents.implementations.semantic_search_amz_products.agent import SemanticSearchAmazonProductsAgent
import pprint

def main():
    # Create and process with agent
    agent = SemanticSearchAmazonProductsAgent()
    result = agent.process()
    
    # Pretty print the results
    for item in result["results"]:
        pprint.pprint(f"Output from node '{item['node']}':")
        pprint.pprint("---")
        pprint.pprint(item['output'], indent=2, width=80, depth=None)
        pprint.pprint("\n---\n")

if __name__ == "__main__":
    main()