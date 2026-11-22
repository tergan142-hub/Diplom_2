import uuid

def generate_email():
    return f"test_{uuid.uuid4().hex[:8]}@yandex.ru"

def generate_password():
    return "password123"

def generate_name():
    return "TestUser"