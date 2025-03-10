from app.agents.schema.superlinked import index
from app.utils.constants import constants
import superlinked.framework as sl

openai_config = sl.OpenAIClientConfig(
    api_key=constants.OPENAI_API_KEY.get_secret_value(), model=constants.LLM_MODEL
)

title_similar_param = sl.Param(
    "query_title",
    description=(
        "The text in the user's query that is used to search in the products' title."
        "Extract info that does not apply to other spaces or params."
    ),
)
text_similar_param = sl.Param(
    "query_description",
    description=(
        "The text in the user's query that is used to search in the products' description."
        " Extract info that does not apply to other spaces or params."
    ),
)

base_query = (
    sl.Query(
        index.product_index,
        weights={
            index.title_space: sl.Param("title_weight"),
            index.description_space: sl.Param("description_weight"),
            index.review_rating_maximizer_space: sl.Param(
                "review_rating_maximizer_weight"
            ),
            index.price_minimizer_space: sl.Param("price_minimizer_weights"),
        },
    )
    .find(index.product)
    .limit(sl.Param("limit"))
    .with_natural_query(sl.Param("natural_query"), openai_config)
    .filter(
        index.product.type
        == sl.Param(
            "filter_by_type",
            description="Used to only present items that have a specific type",
            options=constants.SPLK_TYPES,
        )
    )
)

semantic_query = (
    base_query.similar(
        index.description_space,
        text_similar_param,
        sl.Param("description_similar_clause_weight"),
    )
    .similar(
        index.title_space,
        title_similar_param,
        sl.Param("title_similar_clause_weight"),
    )
    .filter(
        index.product.category
        == sl.Param(
            "filter_by_category",
            description="Used to only present items that have a specific category",
            options=constants.SPLK_CATEGORIES,
        )
    )
)