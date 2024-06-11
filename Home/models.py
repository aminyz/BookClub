from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django_jalali.db import models as jmodels
from django.urls import reverse
from django_resized import ResizedImageField



class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Literature.Status.PUBLISHED)


class Literature(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PN', 'در حال آماده سازی'
        PUBLISHED = 'PB', 'منتشر شده'
        Rejected = 'RJ', 'رد صلاحیت'

    class Topic(models.TextChoices):
        NONE = 'NN', 'None'
        FOREIGN_NOVEL_LATIN_AMERICA = 'FNL', 'رمان خارجی آمریکا لاتین'
        FOREIGN_NOVEL_NORTH_AMERICA = 'FNA', 'رمان خارجی آمریکا شمالی'
        FOREIGN_NOVEL_ENGLAND = 'FNE', 'رمان خارجی انگلستان'
        FOREIGN_NOVEL_SPAIN = 'FNS', 'رمان خارچی اسپانیا'
        FOREIGN_NOVEL_FRANCE = 'FNF', 'رمان خارجی فرانسه'
        FOREIGN_NOVEL_GERMANY = 'FNG', 'رمان خارچی آلمان'
        FOREIGN_NOVEL_RUSSIA = 'FNR', 'رمان خارجی روسیه'
        SHORT_STORY = 'SS', 'داستان کوتاه'
        kids_teenager = 'KT', 'کودک و نوجوان'
        FANTASY = 'FA', 'فانتزی'
        PRACTICAL = 'PR', 'جنایی و کارآگاهی'
        POLITICAL = 'PO', 'سیاسی'
        RELIGION = 'RE', 'دینی و مذهبی'
        SPORTS = 'SP', 'ورزشی'
        WOMEN = 'WO', 'زنان'
        POEM = 'PM', 'شعر'
        HISTORICAL = 'HIST', 'تاریخی'
        BIOGRAPHIC = 'BG', 'زندگینامه'
        TRAVELOGUE = 'TR', 'سفرنامه'

    class Type(models.TextChoices):
        BOOK = 'bk', 'کتاب'
        JOURNAL = 'jn', 'مجله'
        ARTICLE = 'ar', 'مقاله'

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150, verbose_name='عنوان')
    date = jmodels.jDateTimeField(default=timezone.now, verbose_name='تاریخ چاپ')
    description = models.TextField(null=True, verbose_name='توضیحات')
    author = models.ForeignKey("Authors", on_delete=models.CASCADE, max_length=150, null=True, blank=True, verbose_name='نویسنده')
    publishers = models.CharField(max_length=150, verbose_name='انتشارات')
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.PENDING, verbose_name='وضعیت')
    slug = models.SlugField(max_length=150, unique=True, verbose_name='اسلاگ')
    type = models.CharField(max_length=50, choices=Type.choices, default=Type.BOOK, verbose_name='نوع')
    topics = models.CharField(max_length=50, choices=Topic.choices, default=Topic.NONE, verbose_name='موضوع')
    # post information
    author_post = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts', verbose_name='سازنده پست')
    publish_post_time = jmodels.jDateTimeField(default=timezone.now, verbose_name='تاریخ انتشار پست')
    created = jmodels.jDateTimeField(auto_now_add=True)
    updated = jmodels.jDateTimeField(auto_now=True)

    objects = jmodels.jManager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish_post_time']
        indexes = [
            models.Index(fields=['-publish_post_time'])
        ]
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

    def __str__(self):
        return self.title or ''

    def get_absolute_url(self):
        return reverse('Home:post_detail', args=[self.id])


class AuthorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Authors.Status.PUBLISHED)


class Authors(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PN', 'در حال آماده سازی'
        PUBLISHED = 'PB', 'منتشر شده'
        Rejected = 'RJ', 'رد صلاحیت'

    name = models.CharField(max_length=150, verbose_name='نام')
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='Author_Images/', verbose_name='تصویر نویسندگان', blank=True, null=True)
    slug = models.SlugField(max_length=150, unique=True, verbose_name='اسلاگ')
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.PENDING, verbose_name='وضعیت')
    inmate = models.CharField(max_length=150, verbose_name='ملیت')
    description = models.TextField(null=True, verbose_name='توضیحات')
    age = models.CharField(max_length=50, verbose_name='سن (سال تولد)')
    created = jmodels.jDateTimeField(auto_now_add=True)
    updated = jmodels.jDateTimeField(auto_now=True)

    objects = jmodels.jManager()
    published = AuthorManager()

    class Meta:
        ordering = ['id']
        indexes = [
            models.Index(fields=['id'])
        ]
        verbose_name = 'نویسنده'
        verbose_name_plural = 'نویسنده ها و شاعران'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Home:author_detail', args=[self.id])


class Ticket(models.Model):
    massage = models.TextField(verbose_name='پیام')
    name = models.CharField(max_length=150, verbose_name='نام')
    email = models.EmailField(verbose_name='ایمیل')
    phone = models.CharField(max_length=11, verbose_name='شماره تلفن')
    subject = models.CharField(max_length=150, verbose_name='موضوع')

    class Meta:
        verbose_name = 'تیکت ها'
        verbose_name_plural = 'نظرات و انتقادات'

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(Literature, on_delete=models.CASCADE, related_name="comment", verbose_name="پست")
    name = models.CharField(max_length=150, verbose_name='نام')
    description = models.TextField(verbose_name='متن')
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ انتشار')
    updated = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ تصحیح")
    active = models.BooleanField(default=False, verbose_name='تاییدیه')

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'

    def __str__(self):
        return self.name or ''


class Image(models.Model):
    post = models.ForeignKey(Literature, on_delete=models.CASCADE, related_name="images", verbose_name="پست")
    image = models.ImageField(upload_to="Home_images/", verbose_name='تصویر')
    title = models.CharField(max_length=150, verbose_name='عنوان', null=True, blank=True)
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ تولید')

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصویر ها'

    def __str__(self):
        return self.title or ''


class Account(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    date_of_birth = jmodels.jDateField(blank=True, null=True, verbose_name='تاریخ تولد')
    bio = models.TextField(verbose_name='بایو', null=True, blank=True)
    photo = ResizedImageField(upload_to='User_images/', size=[500, 500], crop=['middle', 'center'], quality=80, null=True, blank=True, verbose_name='تصویر')
    job = models.CharField(max_length=150, verbose_name='شغل', null=True, blank=True)
    phone = models.CharField(max_length=11, verbose_name='شماره تلفن')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'اکانت'
        verbose_name_plural = 'اکانت ها'
