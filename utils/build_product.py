from core.logger import Logger
from models.product_model import ProductCard
from models.seller import Seller
from services.url_product_generate import ProductURLGenerator


def build_product_dict(product, product_card: ProductCard, seller: Seller, url_gen: ProductURLGenerator, convert_currency) -> dict:
    Logger.debug(f"Создание товара id={product.id}")
    
    first_size = product.sizes[0]
    image_count = product_card.media.photo_count

    return {
        "article": product.id,
        "name": product.name,
        "product_url": url_gen.generate_product_page_url(product.id),
        "price_basic": convert_currency.convert_rub_cop(first_size.price.basic),
        "price_sale": convert_currency.convert_rub_cop(first_size.price.product),
        "description": product_card.description,
        "images": ", ".join(
            url_gen.generate_product_image_url(product.id, i)
            for i in range(1, image_count + 1)
        ),
        "options": product_card.simple_options(),
        "seller_name": seller.seller_name,
        "seller_url": url_gen.generate_seller_url(seller.supplier_id),
        "sizes": ", ".join(s.name for s in product.sizes),
        "quantity": product.totalQuantity,
        "rating": product.review_rating,
        "feedbacks": product.feedbacks,
    }
