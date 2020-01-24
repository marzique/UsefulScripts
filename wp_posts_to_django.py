"""
Get all posts from WordPress website using embedded REST API
and add them as ORM objects. Also downloads images.

# models.py:
class Article(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', null=True)
    date = models.DateTimeField(default=datetime.datetime.now)


class Paragraph(models.Model):
    subtitle = models.CharField(max_length=100)
    content = models.TextField(max_length=10000)
    article = models.ForeignKey(Article, related_name='paragraphs', on_delete=models.CASCADE)


# show article for each paragraph in admin
class ParagraphAdmin(admin.ModelAdmin):
    list_display = ('subtitle', 'article')


Usage:
python3 manage.py shell
from appname.helpers import *
parse_posts_info(get_posts_json(website='https://any_wordpress.website', limit=<int:how many posts to parse>))

"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse
from django.core.files.base import ContentFile
from .models import Article, Paragraph


def parse_posts_info(posts_list):
    for post in posts_list:
        content = post['content']['rendered'].replace('\n', '')
        image_url = post['_embedded']['wp:featuredmedia'][0]['source_url']

        title = post['title']['rendered'].replace('\n', '')

        if '&#' in title:
            continue
        paragraphs = split_to_paragraphs(content)
        print(type(paragraphs))
        if not paragraphs:
            continue
        else:
            if not paragraphs[0][0]:
                paragraphs = [ (title, paragraphs[0][1]) ]
        
        a = Article(title=title)
        add_image(image_url, a)
        a.save()
        for paragraph in paragraphs:
            p = Paragraph(subtitle=paragraph[0], content=paragraph[1], article=a)
            p.save()


def get_posts_json(website='https://cement.ua', limit=50):
    """Get """
    url = website + f'/wp-json/wp/v2/posts?per_page={limit}&_embed'
    r = requests.get(url)
    posts_list = r.json()
    return posts_list


def split_to_paragraphs(html_content):
    paragraphs = []
    soup = BeautifulSoup(html_content, 'html.parser')
    h2tags = soup.find_all('h2')
    tables = soup.find_all('table')

    if tables:
        return None
    if not h2tags:
        return [(None, soup.get_text())]

    for h2tag in h2tags:
        subtitle = h2tag.get_text()
        text = ''
        elem = next_element(h2tag)
        while elem and elem.name != 'h2':
            text += elem.get_text().replace(';', '. ')
            if '&#' in text:
                return None
            elem = next_element(elem)
        paragraphs.append((subtitle, text))
    return paragraphs


def next_element(elem):
    while elem is not None:
        # Find next element, skip NavigableString objects
        elem = elem.next_sibling
        if hasattr(elem, 'name'):
            return elem

def add_image(url, article):
    name = urlparse(url).path.split('/')[-1]
    response = requests.get(url)
    if response.status_code == 200:
        article.image.save(name, ContentFile(response.content), save=True)


