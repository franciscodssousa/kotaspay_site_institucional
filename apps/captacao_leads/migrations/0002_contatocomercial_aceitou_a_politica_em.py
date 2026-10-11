from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("captacao_leads", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="contatocomercial",
            name="aceitou_a_politica_em",
            field=models.DateTimeField(
                blank=True,
                null=True,
                verbose_name="aceitou a política de privacidade em",
            ),
        ),
    ]
