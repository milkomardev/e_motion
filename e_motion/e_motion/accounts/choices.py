from django.db import models


class SubscriptionChoices(models.TextChoices):
    ONE_MONTH = '1M', '1 Month'
    THREE_MONTHS = '3M', '3 Months'
    SIX_MONTHS = '6M', '6 Months'


class AttendanceLimitChoices(models.TextChoices):
    FOUR = 4, '4 Attendances'
    EIGHT = 8, '8 Attendances'
    TWELVE = 12, '12 Attendances'
    TWENTY_FOUR = 24, '24 Attendances'


