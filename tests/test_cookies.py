from app.utils.cookies import COOKIES, get_random_cookie


def test_cookies_not_empty():
    """Список предсказаний не пустой."""
    assert len(COOKIES) > 0
    assert all(isinstance(c, str) for c in COOKIES)
    assert all(len(c) > 10 for c in COOKIES)


def test_get_random_cookie():
    """Функция возвращает строку из списка."""
    cookie = get_random_cookie()
    assert isinstance(cookie, str)
    assert cookie in COOKIES


def test_randomness():
    """За несколько вызовов могут выпадать разные предсказания."""
    results = {get_random_cookie() for _ in range(20)}
    # Хотя бы 2 разных (на 20 попыток — почти гарантированно)
    assert len(results) >= 2