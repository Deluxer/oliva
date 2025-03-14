from app.agents.clients.superlinked import superlinked
from app.agents.schema.superlinked import query_search
from langchain_core.messages import AIMessage

def superlinked_amazon_products_retriever(query: str):
    superlinked.setup()
    result = superlinked.app.query(
        query_search.semantic_query,
        natural_query=query,
        limit=3
    )
    
    to_pandas = result.to_pandas()
    
    # Extract relevant fields
    products = []
    for index, row in to_pandas.iterrows():
        title = row["title"]
        price = f"${row['price']:.2f}"
        rating = f"{row['review_rating']} ({row['review_count']} reviews)"
        product_id = row["id"]
        
        formatted_output = f"{title}\nPrice: {price}\nRating: {rating}\n"
        products.append(formatted_output)
    
    result_string = "\n".join(products)

    return result_string
