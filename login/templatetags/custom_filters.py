from django import template
from bs4 import BeautifulSoup

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def solo_parrafos(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    paragraphs = soup.find_all('p')
    return ' '.join([p.get_text() for p in paragraphs])

