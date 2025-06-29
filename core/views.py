import os
import hashlib
import time
import datetime
import random
import string
import requests
import urllib
import base64
import qrcode
import json
import calendar
from io import BytesIO
from collections import Counter
from openpyxl import Workbook
from Crypto.Cipher import AES
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from cryptography import x509
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from core.models import Paper
from mysite import settings
# 移除付费验证
def download(request):
    return FileResponse(open('data.zip', 'rb'))




def get_paginated_reviews(reviews, page_number):
    if page_number is None:
        page_number = 1

    p = Paginator(reviews, 20)
    try:
        reviews = p.get_page(page_number)
    except PageNotAnInteger:
        page_number = 1
        reviews = p.page(1)
    except EmptyPage:
        page_number = p.num_pages
        reviews = p.page(p.num_pages)

    items = list(reviews)
    indices = list(range((reviews.number - 1) * p.per_page + 1, reviews.number * p.per_page + 1))

    return reviews, zip(items, indices)

def format_impact_factor(impact_factor):
    if impact_factor is None:
        return None
    if impact_factor < 0.1:
        return "<0.1"
    return f"{impact_factor:.1f}"

def to_number(s):
    try:
        return float(s)
    except ValueError:
        return ''

from core.query import tokenize, parse

def build_query(parsed_query):
    if not parsed_query:
        return Q()

    query = Q()
    current_operator = None

    for token in parsed_query:
        if isinstance(token, list):
            # 递归处理嵌套表达式
            subquery = build_query(token)
            if current_operator == 'AND' or current_operator is None:
                query &= subquery
            elif current_operator == 'OR':
                query |= subquery
        elif token in {'AND', 'OR', 'NOT'}:
            current_operator = token
        else:
            # 构建单个字段查询的Q对象
            q_obj = (
                Q(title__icontains=token) |
                Q(journal__icontains=token) |
                Q(doi=token) |
                Q(pmid=token) |
                Q(article_type__icontains=token) |
                Q(description__icontains=token) |
                Q(novelty__icontains=token) |
                Q(limitation__icontains=token) |
                Q(research_goal__icontains=token) |
                Q(research_objects__icontains=token) |
                Q(field_category__icontains=token) |
                Q(disease_category__icontains=token) |
                Q(technique__icontains=token) |
                Q(model_type__icontains=token) |
                Q(data_type__icontains=token) |
                Q(sample_size__icontains=token)
            )
            if current_operator == 'NOT':
                q_obj = ~q_obj

            if current_operator == 'AND' or current_operator is None:
                query &= q_obj
            elif current_operator == 'OR':
                query |= q_obj

    return query

def home(request):
    papers = Paper.objects.all()

    filter_quantile = request.GET.get('fq') or ''
    if filter_quantile == '1':
        papers = papers.filter(journal_impact_factor_quartile='1')
    elif filter_quantile == '2':
        papers = papers.filter(journal_impact_factor_quartile__lte='2')
    elif filter_quantile == '3':
        papers = papers.filter(journal_impact_factor_quartile__lte='3')
    else:
        filter_quantile = ''

    filter_impact_factor = request.GET.get('fi') or ''
    impact_factor_min, impact_factor_max = '', ''
    if filter_impact_factor:
        values = (filter_impact_factor.split('-') + [''])[:2]
        impact_factor_min = to_number(values[0])
        impact_factor_max = to_number(values[1])
    if impact_factor_min != '':
        papers = papers.filter(journal_impact_factor__gte=impact_factor_min)
    if impact_factor_max != '':
        papers = papers.filter(journal_impact_factor__lte=impact_factor_max)

    filter_pub_date = request.GET.get('fd') or ''
    pub_date_start, pub_date_end = None, None
    if filter_pub_date:
        values = (filter_pub_date.split('-') + [''])[:2]
        if values[0] != '':
            if len(values[0]) == 4:
                pub_date_start = datetime.datetime.strptime(values[0] + '0101', '%Y%m%d')
            elif len(values[0]) == 6:
                pub_date_start = datetime.datetime.strptime(values[0] + '01', '%Y%m%d')
        if values[1] != '':
            if len(values[1]) == 4:
                pub_date_end = datetime.datetime.strptime(values[1] + '1231', '%Y%m%d')
            elif len(values[1]) == 6:
                year_month = values[1]
                year = int(year_month[:4])
                month = int(year_month[4:])
                last_day = calendar.monthrange(year, month)[1]
                pub_date_end = datetime.datetime(year, month, last_day)
    if pub_date_start is not None and pub_date_end is not None:
        if pub_date_start > pub_date_end:
            pub_date_start, pub_date_end = pub_date_end, pub_date_start
    if pub_date_start is not None:
        papers = papers.filter(pub_date_dt__gte=pub_date_start)
    if pub_date_end is not None:
        papers = papers.filter(pub_date_dt__lte=pub_date_end)

    query = request.GET.get('q') or ''
    if query:
        tokens = tokenize(query)
        parsed_query = parse(tokens)
        q_obj = build_query(parsed_query)
        papers = papers.filter(q_obj)

    papers = papers.order_by('-source', '-pub_date_dt')

    page_number = request.GET.get('page')
    papers, items = get_paginated_reviews(papers, page_number)

    get_params = request.GET.copy()
    if 'page' in get_params:
        del get_params['page']

    for index, paper in enumerate(papers):
        paper.index = index + papers.start_index()
        if paper.parse_time is None:
            paper.parse_time = paper.created
        if paper.article_type is None or paper.article_type == '':
            paper.article_type = 'NA'
        if paper.description is None or paper.description == '':
            paper.description = 'NA'
        if paper.novelty is None or paper.novelty == '':
            paper.novelty = 'NA'
        if paper.limitation is None or paper.limitation == '':
            paper.limitation = 'NA'
        if paper.research_goal is None or paper.research_goal == '':
            paper.research_goal = 'NA'
        if paper.research_objects is None or paper.research_objects == '':
            paper.research_objects = 'NA'
        if not getattr(paper, 'field_category', None):
            paper.field_category = 'NA'
        if paper.disease_category is None or paper.disease_category == '':
            paper.disease_category = 'NA'
        if paper.technique is None or paper.technique == '':
            paper.technique = 'NA'
        if paper.model_type is None or paper.model_type == '':
            paper.model_type = 'NA'
        if paper.data_type is None or paper.data_type == '':
            paper.data_type = 'NA'
        if paper.sample_size is None or paper.sample_size == '':
            paper.sample_size = 'NA'
        paper.journal_impact_factor = format_impact_factor(paper.journal_impact_factor)

    return render(request, 'core/home.html', {
        'query': query,
        'filter_quantile': filter_quantile,
        'impact_factor_min': impact_factor_min,
        'impact_factor_max': impact_factor_max,
        'pub_date_start': pub_date_start.strftime('%Y%m') if pub_date_start else '',
        'pub_date_end': pub_date_end.strftime('%Y%m') if pub_date_end else '',
        'get_params': get_params,
        'papers': papers,
        'items': items,
    })

def stat(request):
    papers = Paper.objects.all().order_by('-pub_date_dt')
    year_counts = Counter([paper.pub_date_dt.year for paper in papers])
    month_counts = Counter([f"{paper.pub_date_dt.year}-{paper.pub_date_dt.month:02}" for paper in papers])

    years = sorted(year_counts.keys(), reverse=True)  # 获取所有年份并按倒序排列
    months = [f"{i:02d}" for i in range(1, 13)]  # 生成月份列表

    # 构造一个包含所有数据的二级列表
    data = []
    for year in years:
        year_data = {'year': year, 'total': year_counts[year], 'months': []}
        for month in months:
            count = month_counts.get(f"{year}-{month}", 0)
            year_data['months'].append({'month': month, 'count': count})
        data.append(year_data)

    context = {
        'data': data,
        'months': months,
    }
    return render(request, 'core/stat.html', context)

def all_papers_to_excel():
    wb = Workbook()
    ws = wb.active
    ws.title = "Papers"
    ws.append([
        "标题", "杂志", "影响因子", "分区", "发表日期", "DOI", "PMID",
        "类型", "简述", "创新点", "不足", "研究目的", "研究对象",
        "领域", "病种", "技术", "模型", "数据类型", "样本量"
    ])
    for papers in Paper.objects.all():
        quartile_info = '-'
        if papers.journal_impact_factor_quartile:
            quartile_info = 'Q' + papers.journal_impact_factor_quartile
        ws.append([
            papers.title,
            papers.journal,
            format_impact_factor(papers.journal_impact_factor),
            quartile_info,
            papers.pub_date,
            papers.doi,
            papers.pmid,
            papers.article_type,
            papers.description,
            papers.novelty,
            papers.limitation,
            papers.research_goal,
            papers.research_objects,
            papers.field_category,
            papers.disease_category,
            papers.technique,
            papers.model_type,
            papers.data_type,
            papers.sample_size
            ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="papers.xlsx"'
    wb.save(response)
    return response



def download(request):
    return all_papers_to_excel()

    return render(request, 'core/download.html')

def do_logout(request):
    logout(request)
    return redirect('home')
