from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """辞書からキーに対応する値を取得するカスタムフィルタ"""
    return dictionary.get(key)

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    return value.as_widget(attrs={'class': arg})