from django.db import models

from user.models import Users


class Catalogs(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')

    class Meta:
        db_table = 'catalog'
        verbose_name = 'Каталог'
        verbose_name_plural = 'Каталоги'
        ordering = ("id",)

    def __str__(self):
        return self.name


class Categories(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    catalog = models.ForeignKey(to=Catalogs, on_delete=models.CASCADE, verbose_name='Каталог')

    class Meta:
        db_table = 'category'
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
        ordering = ("id",)

    def __str__(self):
        return self.name


class UnderCategories(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    categories = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name='Категория')

    class Meta:
        db_table = 'under_category'
        verbose_name = 'Подкатегорию'
        verbose_name_plural = 'Подкатегории'
        ordering = ("id",)

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(max_length=250, upload_to='bot\images', null=True, verbose_name='Изображение')
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена')
    undercategories = models.ForeignKey(to=UnderCategories, on_delete=models.CASCADE, verbose_name='Подкатегория')

    class Meta:
        db_table = 'product'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ("id",)

    def __str__(self):
        return f'Название: {self.name}. Цена: {self.price}'


class Orders(models.Model):
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE, verbose_name='Клиент')
    address = models.CharField(max_length=250, null=True, verbose_name='Адрес')
    ammont = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Итого')
    payment_number = models.CharField(max_length=250, null=True, verbose_name='Номер документа оплаты')
    date_paid = models.TimeField(null=True, verbose_name='Дата оплаты')

    class Meta:
        db_table = 'order'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ("id",)

    def __str__(self):
        return f'Клиент: {self.user}. Итого: {self.ammont} руб. Квитанция: {self.payment_number}'


class Carts(models.Model):
    order = models.ForeignKey(to=Orders, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.IntegerField(verbose_name='Количество')
    ammont = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Сумма')

    class Meta:
        db_table = 'cart'
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        ordering = ("id",)

    def __str__(self):
        return f'Заказ: {self.order}. Товар: {self.product}.'
