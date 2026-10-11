from django.apps import AppConfig


class NucleoConfig(AppConfig):
    """App responsável pelas páginas institucionais de conteúdo estático do site."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.nucleo"
    verbose_name = "Núcleo institucional"
