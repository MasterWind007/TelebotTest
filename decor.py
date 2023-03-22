from functools import wraps


def currency(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        return f'${result}'
    return wrapper


@currency
def net_price(price, tax):
    """ подсчитывает стоимость интернета исходя из цены и налога
    Аргументы:
        price: цена интернета
        tax: налог на добавленную стоимость или налог с продаж
    Возвращает
       стоимость интернета
    """
    return price * (1 + tax)


help(net_price)
print(net_price.__name__)