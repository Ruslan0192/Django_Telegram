from django.db import models


class Users(models.Model):
    telegram_id = models.BigIntegerField(unique=True, verbose_name='ID телеграм')
    name = models.CharField(max_length=50, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')

    class Meta:
        db_table = 'user'
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ("id",)

    def __str__(self):
        return f'Имя:{self.name}. ID: {self.telegram_id}'


class Questions(models.Model):
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE, verbose_name='Клиент')
    question = models.TextField(verbose_name='Вопрос')
    answer = models.TextField(null=True, verbose_name='Ответ')

    class Meta:
        db_table = 'question'
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'
        ordering = ("id",)

    def __str__(self):
        return f'Вопрос: {self.question}. Ответ: {self.answer}.'


class Dispatchs(models.Model):
    text = models.TextField(verbose_name='Текст рассылки')
    ready = models.BooleanField(default=False, verbose_name='Выполнено')

    class Meta:
        db_table = 'dispatch'
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ("id",)

    def __str__(self):
        return f'Рассылка: {self.text}.'


class Subscriptions(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название канала/группы/чата в ТГ')
    url = models.CharField(max_length=50, verbose_name='URL')

    class Meta:
        db_table = 'subscription'
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ("id",)

    def __str__(self):
        return f'Подписка: {self.name}.'
