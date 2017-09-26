from django import template
from django.template import Context
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType

register = template.Library()

class AllListNode(template.Node):
    def __init__(self, keyword):        
        self.keyword = template.Variable(keyword)        
        
    def render(self, context):
        keyword = self.keyword.resolve(context)    
        t = context.template.engine.get_template('shower/components/all.html')
        return t.render(Context({'keyword':keyword}, autoescape=context.autoescape))

class ModelListNode(template.Node):
    def __init__(self, model, keyword, quantity):
        self.model = model        
        self.keyword = keyword
        self.quantity = quantity
        self.template_name = 'shower/components/object_list.html'        
        
    def render(self, context):
        for c in context:
            if self.model in c.keys():
                self.model = template.Variable(self.model).resolve(context)
            if self.keyword in c.keys():
                self.keyword = template.Variable(self.keyword).resolve(context)

        if self.model == 'profile':
            self.template_name = 'shower/components/profile_list.html'        
                                
        ctype = ContentType.objects.get(model=self.model)
        object_list = ctype.model_class().objects.filter_by_keyword(self.keyword)
             
        context_dict = {
            'title': ctype.model_class()._meta.verbose_name_plural,
            'object_list':object_list[:self.quantity] if self.quantity is not None else object_list,
            'show_all': len(object_list) > self.quantity if self.quantity is not None else False,
            'all_link': '/shower/%s/?keyword=%s' % (ctype.model_class().__name__.lower(), self.keyword),
        } 

        print self.template_name       

        t = context.template.engine.get_template(self.template_name)
        return t.render(Context(context_dict, autoescape=context.autoescape))

@register.tag(name='shower_list')
def shower_list(parser, token):
    """
    Syntax:
        {% shower_list '[model]' [keyword] %}
        {% shower_list '[model]' [keyword] '[number]'%}
    """
    try:
        tokens = token.split_contents() 
        quantity = None
        if len(tokens) == 4:
            quantity = int(quit_quotes(tokens.pop(3)))
    except ValueError:
        raise template.TemplateSyntaxError("The last argument of %r tag must be a number" % token.contents.split()[0])

    try:
        tag_name, model, keyword = tokens
        model = quit_quotes(model)
        keyword = quit_quotes(keyword)
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires two or three arguments" % token.contents.split()[0])

    return ModelListNode(model, keyword, quantity)

@register.tag(name='shower_all')
def shower_all(parser, token):
    """
    Syntax:
        {% shower_all [keyword] %}        
    """
    try:
        tag_name, keyword = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])    

    return AllListNode(keyword)


def quit_quotes(_str):
    if _str.startswith("'") and _str.endswith("'") or \
        _str.startswith("\"") and _str.endswith("\""):
        return _str[1:-1]

    return _str