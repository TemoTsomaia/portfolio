from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import CharField
from toy_factory.models import Toy, Coal


# Create your models here.

class Kid(models.Model):
    name = models.CharField(max_length=50)
    niceness_coefficient = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    wanted_toy = CharField(max_length=50)
    santas_list = models.ForeignKey(
        'Santas_list',
        on_delete=models.CASCADE,
        related_name='kids',
        null=True,
        blank=True
    )
    toy = models.OneToOneField(
        Toy,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='kid_toy'
    )
    coal = models.OneToOneField(
        Coal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='kid_coal'
    )
    def __str__(self):
        return self.name

'''
class Kid(models.Model):
    name = models.CharField(max_length=50)
    niceness_coefficient = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    #gift = models.OneToOneField(
       # 'Toy_factory.Toy',  # Replace 'Toy_factory' with the actual name of your app
        #on_delete=models.CASCADE,
       # related_name='kids'
    #)
    santa_list = models.ForeignKey(
        'Santas_list',  # We use a string here to reference the class before it's defined
        on_delete=models.CASCADE,
        related_name='kids',
        default = lambda: Santas_list.objects.first()
    )

    def __str__(self):
        return self.name
'''

class Santas_list(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def naughty_list(self):
        return Kid.objects.filter(niceness_coefficient__lte=5, santas_list__isnull=False)

    @property
    def nice_list(self):
        return Kid.objects.filter(niceness_coefficient__gt=5, santas_list__isnull=False)

    @property
    def get_all_kids(self):
        return Kid.objects.all()

    def __str__(self):
        return "Santa's List"

