from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from rest_framework.generics import (CreateAPIView, GenericAPIView,
                                     ListAPIView, ListCreateAPIView,
                                     RetrieveAPIView, RetrieveDestroyAPIView,
                                     RetrieveUpdateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     UpdateAPIView)
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from test_template.serializers import (TicketSerializer, TicketID,
                                       ReadingTextSerializer,
                                       AskQuestionSerializer,
                                       ImageComparisonSerializer,
                                       ImageDescriptionSerializer,
                                       EssaySerializer, AnswerSerializer,
                                       PersonalLetterSerializer)
from test_template.models import (ImageDescription, Ticket,
                                  ReadingText, AskQuestion, ImageComparison,
                                  PersonalLetter, Essay, AnswerModel)


class TicketView(ListModelMixin, CreateModelMixin, GenericAPIView):
    def get_serializer_class(self):
        if 'reading-text' or 'reading-text/random' in self.request.GET:
            return ReadingTextSerializer
        elif 'ask-question' or 'ask-uestion/random' in self.request.GET:
            return AskQuestionSerializer
        elif 'image-description' or 'image-description/random' in self.request.GET:
            return ImageDescriptionSerializer
        elif 'image-comparison' or 'image-comparison/random' in self.request.GET:
            return ImageComparisonSerializer
        elif 'personal-letter' or 'personal-letter/random' in self.request.GET:
            return PersonalLetterSerializer
        elif 'essay' or 'essay/random' in self.request.GET:
            return EssaySerializer
        return TicketSerializer

    def get_queryset(self):
        if 'reading-text' in self.request.GET:
            return ReadingText.objects.all()
        elif 'reading-text/random' in self.request.GET:
            return ReadingText.objects.order_by('?')[:1]
        elif 'ask-question' in self.request.GET:
            return AskQuestion.objects.all()
        elif 'ask-question/random' in self.request.GET:
            return AskQuestion.objects.order_by('?')[:1]
        elif 'image-description' in self.request.GET:
            return ImageDescription.objects.all()
        elif 'image-description/random' in self.request.GET:
            return ImageDescription.objects.order_by('?')[:1]
        elif 'image-comparison' in self.request.GET:
            return ImageComparison.objects.all()
        elif 'image-comparison/random' in self.request.GET:
            return ImageComparison.objects.order_by('?')[:1]
        elif 'personal-letter' in self.request.GET:
            return PersonalLetter.objects.all()
        elif 'personal-letter/random' in self.request.GET:
            return PersonalLetter.objects.order_by('?')[:1]
        elif 'essay' in self.request.GET:
            return Essay.objects.all()
        elif 'essay/random' in self.request.GET:
            return Essay.objects.order_by('?')[:1]
        return Ticket.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(
            queryset,
            context={'request': request},
            many=True
        )
        page = self.paginate_queryset(serializer.data)
        if page is not None:
            return self.get_paginated_response(page)
        else:
            return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        instance = get_object_or_404(queryset, pk=kwargs['pk'])
        serializer = TicketSerializer(instance)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        ticket_num = serializer.validated_data['number']
        if Ticket.objects.filter(number=ticket_num).count() >= 1:
            return Response({'error' : 'ticket with this number already exists'})
        else:
            serializer.save()
            return Response({'message': 'Ticket created'})

    def update(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class TicketIDView(ListAPIView):
    def get_serializer_class(self):
        return TicketID

    def get_queryset(self, ticket_id):
        return Ticket.objects.filter(pk=ticket_id)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset(ticket_id)
        serializer = self.get_serializer(
            queryset,
            context={'request': request},
            many=True
        )
        ticket_id = serializer.validated_data['id']
        page = self.paginate_queryset(serializer.data)
        if page is not None:
            return self.get_paginated_response(page)
        else:
            return Response(serializer.data)


class AnswerView(CreateModelMixin, ListModelMixin, GenericAPIView):
    serializer_class = AnswerSerializer

    def get_queryset(self):
        return AnswerModel.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(
            queryset,
            context={'request': request},
            many=True
        )
        page = self.paginate_queryset(serializer.data)
        if page is not None:
            return self.get_paginated_response(page)
        else:
            return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, files=request.FILES)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)