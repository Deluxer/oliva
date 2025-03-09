from app.utils.constants import constants
import superlinked.framework as sl

class ProductSchema(sl.Schema):
    id: sl.IdField
    type: sl.String
    category: sl.StringList
    title: sl.String
    description: sl.String
    review_rating: sl.Float
    review_count: sl.Integer
    price: sl.Float


product = ProductSchema()

category_space = sl.CategoricalSimilaritySpace(
    category_input=product.category,
    categories=constants.SPLK_CATEGORIES,
    uncategorized_as_category=True,
    negative_filter=-1,
)
title_space = sl.TextSimilaritySpace(
    text=product.title, model="Alibaba-NLP/gte-large-en-v1.5"
)
description_space = sl.TextSimilaritySpace(
    text=product.description, model="Alibaba-NLP/gte-large-en-v1.5"
)
review_rating_maximizer_space = sl.NumberSpace(
    number=product.review_rating, min_value=-1.0, max_value=5.0, mode=sl.Mode.MAXIMUM
)
price_minimizer_space = sl.NumberSpace(
    number=product.price, min_value=0.0, max_value=1000, mode=sl.Mode.MINIMUM
)

product_index = sl.Index(
    spaces=[
        title_space,
        description_space,
        review_rating_maximizer_space,
        price_minimizer_space,
    ],
    fields=[product.type, product.category, product.review_rating, product.price],
)
