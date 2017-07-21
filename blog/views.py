# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import redirect
from django.views.generic.list import ListView
from .models import Article

class ArticleView(ListView):
    model = Article
    paginate_by = 5
    context_object_name = 'articles'
    template_name = 'blog/articles.html'

def generate_fake_data(request):
    from model_mommy import mommy
    mommy.make('blog.Article', _quantity=20)
    return redirect('blog')
