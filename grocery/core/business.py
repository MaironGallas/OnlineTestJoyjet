def get_price(id: int, articles: list, discounts: list = None) -> list:
    """
        Returns the price of a specific article from a given list.
        Parameters:
            id: An integer that means the article id. This parameter is mandatory.
            articles: A list of articles with all articles and their prices. This parameter is mandatory.
            discounts: A list of discounts if applicable. This parameter is optional.
        Returns:
            price: Price of the article and if applicable with its discount.
        """
    for article in articles:
        if article['id'] == id:
            price = article['price']

    type = ''
    value = 0
    if discounts:
        for discount in discounts:
            if discount['article_id'] == id:
                value = discount['value']
                type = discount['type']
        price = price - value if type == 'amount' else int(price - (price * value / 100))
    return price



def get_total_price(cart: dict, articles: list, delivery_fees: list = None, discounts: list = None) -> int:
    """
    Returns the sum of the prices of all items in the cart
    Parameters:
        cart: A dict of cart with their articles and their quantities. This parameter is mandatory.
        articles: A list with all articles. This parameter is mandatory.
        delivery_fees: A list of delivery fees if applicable. This parameter is optional.
        discounts: A list of discounts if applicable. This parameter is optional.
    Returns:
        total_price: A sum of price for all items in the cart.
    """
    total_item_price = 0
    delivery_value = 0

    for item in cart['items']:
        total_item_price += get_price(item['article_id'], articles, discounts) * item['quantity']

    if delivery_fees:
        for delivery_fee in delivery_fees:
            if delivery_fee['eligible_transaction_volume']['max_price'] is None:
                min = delivery_fee['eligible_transaction_volume']['min_price']
                max = float('inf')
            else:
                min = delivery_fee['eligible_transaction_volume']['min_price']
                max = delivery_fee['eligible_transaction_volume']['max_price']

            if min <= total_item_price < max:
                delivery_value = delivery_fee['price']

    total_price = total_item_price + delivery_value

    return total_price
