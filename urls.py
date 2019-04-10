from controllers import CustomerController, AchievementController

public_urls = [
    (CustomerController, '/customer', '/customer/<string:method>'),
    (AchievementController, '/achievement', '/achievement/<string:method>'),
]
