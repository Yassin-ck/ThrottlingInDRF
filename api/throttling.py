from rest_framework.throttling import UserRateThrottle

class customThrottle(UserRateThrottle):
    scope = 'custom'