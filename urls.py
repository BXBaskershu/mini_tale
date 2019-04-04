from controllers import CustomerController

public_urls = [
    (CustomerController, '/customer', '/customer/<string:method>'),
]
