from rest_framework import serializers
from test_template.models import (ImageDescription, Ticket,
                                  ReadingText, AskQuestion, ImageComparison,
                                  PersonalLetter, Essay, AnswerModel)


# class ImageDescriptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ImageDescription

#     images = serializers.SerializerMethodField()

#     def get_images(self, obj):
#         img_qs = obj.image_description.filter(in_archive=False)
#         if img_qs.exists():
#             img_list = []
#             for x in img_qs:
#                 img_list.append({'id': x.id,
#                                  'url': self.context.get('request', None).
#                                  build_absolute_uri(x.image_str.url),
#                                  'default': x.default})
#             return img_list
#         else:
#             return None


# class ImageClassSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(label='TaskID', required=True)

#     class Meta:
#         model = ImageClass
#         fields = ('id', 'image', 'default', 'in_archive')

#     def create(self, validated_data):
#         images_data = self.context['request'].FILES
#         if images_data.getlist('image'):
#             imgs = []
#             for img in images_data.getlist('image'):
#                 image = ImageClass.objects.create(
#                     image=img,
#                     default=False,
#                     user=self.context['request'].user
#                 )
#                 imgs.append(image)
#             return imgs
#         return self.context['request'].user


class TicketSerializer(serializers.Serializer):
    class Meta:
        model = Ticket
        fields = ('id', 'number', 'reading_text', 'ask_question', 'essay'
                  'image_description', 'image_comparison', 'personal_letter')

    number = serializers.IntegerField(label="ticket_number")
    reading_text = serializers.CharField(label="reading_text_id")
    ask_question = serializers.CharField(label="ask_question_id")
    image_description = serializers.CharField(label="image_description_id")
    image_comparison = serializers.CharField(label="image_comparison_id")
    personal_letter = serializers.CharField(label="personal_letter_id")
    essay = serializers.CharField(label="essay_id")

    def save(self, **kwargs):
        ticket_obj = Ticket.objects.create(
            number=self.validated_data['number'],
            reading_text=ReadingText.objects.get(
                pk=self.validated_data['reading_text']
            ),
            ask_question=AskQuestion.objects.get(
                pk=self.validated_data['ask_question']
            ),
            image_description=ImageDescription.objects.get(
                pk=self.validated_data['image_description']
            ),
            image_comparison=ImageComparison.objects.get(
                pk=self.validated_data['image_comparison']
            ),
            personal_letter=PersonalLetter.objects.get(
                pk=self.validated_data['personal_letter']
            ),
            essay=Essay.objects.get(pk=self.validated_data['essay'])
        )
        return ticket_obj

    # def update(self, instance, validated_data):
    #     return super(TicketSerializer, self).update(instance, validated_data)

class TicketID(serializers.Serializer):
    class Meta:
        model = Ticket
        fields = "__all__"

    id = serializers.IntegerField()


class ReadingTextSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    task = serializers.CharField()
    description = serializers.CharField()
    text = serializers.CharField()

    class Meta:
        model = ReadingText
        fields = ('id', 'title', 'task', 'description', 'text')


class AskQuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    task = serializers.CharField()
    description = serializers.CharField()
    image = serializers.CharField()

    class Meta:
        model = AskQuestion
        fields = "__all__"


class ImageDescriptionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    task = serializers.CharField()
    description = serializers.CharField()
    first_image = serializers.CharField()
    second_image = serializers.CharField()
    thirt_image = serializers.CharField()

    class Meta:
        model = ImageDescription
        fields = "__all__"


class ImageComparisonSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    task = serializers.CharField()
    description = serializers.CharField()
    first_image = serializers.CharField()
    second_image = serializers.CharField()

    class Meta:
        model = ImageComparison
        fields = "__all__"


class PersonalLetterSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    task = serializers.CharField()
    description = serializers.CharField()
    text = serializers.CharField()

    class Meta:
        model = PersonalLetter
        fields = "__all__"


class EssaySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    task = serializers.CharField()
    description = serializers.CharField()
    text = serializers.CharField()

    class Meta:
        model = Essay
        fields = "__all__"


class AnswerSerializer(serializers.Serializer):
    task = serializers.CharField()
    answer = serializers.SerializerMethodField()

    def save(self, **kwargs):
        answer_obj = AnswerModel.objects.create(
            student=self.context['request'].user,
            task=self.validated_data['task']
        )
        return answer_obj

    def get_answer(self, value):
        if value.answer:
            return self.context.get('request', None) \
                .build_absolute_uri(value.answer.url)
        return None