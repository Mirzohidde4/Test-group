from django.db import models


class UserMod(models.Model):
    user_id = models.PositiveBigIntegerField(verbose_name='telegram id')
    user_name = models.CharField(verbose_name='foydalanuvchi ism', max_length=100, null=True, blank=True)
    full_name = models.CharField(verbose_name='to\'liq ism', max_length=150)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'


class AdminMod(models.Model):
    user_id = models.PositiveBigIntegerField(verbose_name='telegram id')
    user_name = models.CharField(verbose_name='foydalanuvchi ism', max_length=100, null=True, blank=True)
    full_name = models.CharField(verbose_name="to'liq ism", max_length=150)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Admin'
        verbose_name_plural = 'Adminlar'


class GroupMod(models.Model):
    group_id = models.BigIntegerField(verbose_name='guruh/kanal id')
    group_name = models.CharField(verbose_name='guruh/kanal nomi', max_length=150)

    def __str__(self):
        return self.group_name

    class Meta:
        verbose_name = 'Guruh'
        verbose_name_plural = 'Guruhlar'


class BotMessage(models.Model):
    message_text = models.TextField(verbose_name='xabar matni')
    to_group = models.ForeignKey(GroupMod, on_delete=models.CASCADE, verbose_name='guruh/kanal')

    class Meta:
        verbose_name = 'Xabar'
        verbose_name_plural = 'Xabarlar'

    def __str__(self):
        return self.message_text    


class InlineButton(models.Model):
    bot_message = models.ForeignKey(BotMessage, on_delete=models.CASCADE, verbose_name='savol')
    text = models.CharField(max_length=100, verbose_name='tugma matni')
    text_response = models.CharField(max_length=100, verbose_name='tugma bosilganda')
    is_correct = models.BooleanField(default=False, verbose_name="to'g'ri / hato")
    static = models.BooleanField(default=False, verbose_name='static')

    class Meta:
        verbose_name = 'Tugma'
        verbose_name_plural = 'Tugmalar'
        ordering = ['id']

    def __str__(self):
        return self.text