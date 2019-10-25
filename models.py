from django.db import models
from userdata.models import UserProfile


# Create your models here.
class BaseTemplateClass(models.Model):
    title = models.CharField(max_length=100)
    task = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.id


class ReadingText(BaseTemplateClass):
    """
    Структура шаблона «Чтение текста»
    Заголовок задания (varchar)
    Задания (тестовое поле)
    Описание задания (тестовое поле)
    Текст (текстовое поле)
    """
    text = models.TextField()

    def __str__(self):
        return self.title


class AskQuestion(BaseTemplateClass):
    """
    Структура шаблона «Задать вопрос»
    Заголовок задания (varchar)
    Задания (тестовое поле)
    Описание задания (тестовое поле)
    Картинка
    """
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title


class ImageDescription(BaseTemplateClass):
    """
    Структура шаблона «Описание картинки»
    Заголовок задания (varchar)
    Задания (тестовое поле)
    Описание задания (тестовое поле)
    Картинки (3 картинки, ученик выбирает одну)
    """
    first_image = models.ImageField(blank=True, null=True)
    second_image = models.ImageField(blank=True, null=True)
    thirt_image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.title


class ImageComparison(BaseTemplateClass):
    """
    Структура шаблона «Сравнение картинок»
    Заголовок задания (varchar)
    Задания (тестовое поле)
    Описание задания (тестовое поле)
    Картинка 1
    Картинка 2
    """
    first_image = models.ImageField(blank=True, null=True)
    second_image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.title


class PersonalLetter(BaseTemplateClass):
    """
    Структура шаблона «Личное письмо»
    Заголовок задания (varchar)
    Задания (тестовое поле)
    Описание задания (тестовое поле)
    Текст (текстовое поле)
    """
    text = models.TextField()

    def __str__(self):
        return self.title


class Essay(BaseTemplateClass):
    """
    Структура шаблона «Эссе»
    Заголовок задания (varchar)
    Задания (тестовое поле)
    Описание задания (тестовое поле)
    Текст (текстовое поле)
    """
    text = models.TextField()

    def __str__(self):
        return self.title


# class ImageClass(models.Model):
#     image = models.ImageField(upload_to='media/', blank=True, null=True)
#     task = models.ForeignKey(ImageDescription,  on_delete=models.CASCADE,
#                              related_name='image_description')
#     default = models.BooleanField()
#     in_archive = models.BooleanField(default=False)

#     def save(self, *args, **kwargs):
#         return self.task


class Ticket(models.Model):
    number = models.IntegerField()
    reading_text = models.ForeignKey(ReadingText, on_delete=models.CASCADE,
                                     blank=True, null=True)
    ask_question = models.ForeignKey(AskQuestion, on_delete=models.CASCADE,
                                     blank=True, null=True)
    image_description = models.ForeignKey(ImageDescription, on_delete=models.CASCADE,
                                          blank=True, null=True)
    image_comparison = models.ForeignKey(ImageComparison, on_delete=models.CASCADE,
                                         blank=True, null=True)
    personal_letter = models.ForeignKey(PersonalLetter, on_delete=models.CASCADE,
                                        blank=True, null=True)
    essay = models.ForeignKey(Essay, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.number


class AnswerModel(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                                blank=True, null=True)
    task = models.ForeignKey(BaseTemplateClass, on_delete=models.CASCADE,
                             blank=True, null=True)
    answer = models.FileField()

    def __str__(self):
        return self.id
