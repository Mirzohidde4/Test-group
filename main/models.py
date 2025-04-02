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
    group_id = models.BigIntegerField(verbose_name='guruh / kanal id')
    group_name = models.CharField(verbose_name='guruh / kanal nomi', max_length=150)

    def __str__(self):
        return self.group_name

    class Meta:
        verbose_name = 'Guruh / Kanal'
        verbose_name_plural = 'Guruhlar / Kanallar'


class BotMessage(models.Model):
    message_text = models.TextField(verbose_name='xabar matni')
    to_group = models.ManyToManyField(GroupMod, verbose_name='manzil', related_name='manzillar')
    photo = models.ImageField(upload_to='images/', verbose_name='rasm', null=True, blank=True)

    class Meta:
        verbose_name = 'Xabar'
        verbose_name_plural = 'Xabarlar'

    def __str__(self):
        return self.message_text    


class InlineButton(models.Model):
    bot_message = models.ForeignKey(BotMessage, on_delete=models.CASCADE, verbose_name='savol', related_name='buttons')
    text = models.CharField(max_length=100, verbose_name='tugma matni')
    text_response = models.CharField(max_length=100, verbose_name='tugma bosilganda')
    row = models.IntegerField(default=1, null=True, blank=True, verbose_name='qator') 
    position = models.IntegerField(default=1, null=True, blank=True, verbose_name='raqam') 
    is_correct = models.BooleanField(default=False, verbose_name="to'g'ri")
    static = models.BooleanField(default=False, verbose_name='static')

    class Meta:
        verbose_name = 'Tugma'
        verbose_name_plural = 'Tugmalar'
        ordering = ['id']

    def __str__(self):
        return self.text