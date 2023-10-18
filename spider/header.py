from fake_useragent import UserAgent


def get_header():
    headers = {
        "User-Agent": UserAgent().random,
        "Accept":
        "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "Accept-Language": "en",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.google.com/",
    }
    return headers
