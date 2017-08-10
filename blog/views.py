# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.http import HttpResponse, JsonResponse
from tablib import Dataset
from rest_framework.viewsets import ModelViewSet
from .models import Article
from .resources import ArticleResource
from .serializers import ArticleSerializer

class ArticleView(ListView):
    model = Article
    paginate_by = 5
    context_object_name = 'articles'
    template_name = 'blog/articles.html'

def generate_fake_data(request):
    from model_mommy import mommy
    mommy.make('blog.Article', _quantity=20)
    return redirect('blog')

def export(request):
    article_resource = ArticleResource()
    dataset = article_resource.export()
    response = HttpResponse(dataset.json, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="articles.json"'
    return response

def simple_upload(request):
    if request.method == 'POST':
        article_resource = ArticleResource()
        dataset = Dataset()
        new_articles = request.FILES['myfile']

        imported_data = dataset.load(new_articles.read())
        result = article_resource.import_data(dataset, dry_run=True)

        if not result.has_errors():
            article_resource.import_data(dataset, dry_run=False)

    return render(request, 'blog/import.html')

def get_articles(request):
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    return JsonResponse(serializer.data, safe=False)

def list(request):
    return render(request, 'blog/list.html')

class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
