from rest_framework.throttling import UserRateThrottle

class QuizCreationThrottle(UserRateThrottle):
    rate="10/hour"

class RegisterUserThrottle(UserRateThrottle):
    rate="10/hour"

class LoginUserThrottle(UserRateThrottle):
    rate="20/hour"

    