from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'e_motion.accounts'

    def ready(self):
        import e_motion.accounts.signals