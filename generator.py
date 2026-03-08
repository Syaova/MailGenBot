import random, string

def generate_email(domain: str) -> str:
    name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{name}@{domain}"

def generate_emails(domain: str, count: int) -> list:
    return [generate_email(domain) for _ in range(count)]
