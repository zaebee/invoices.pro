from django import template

register = template.Library()


@register.inclusion_tag('patty/tags/dummy.html', takes_context=True)
def dynamic_tabs(context, template='patty/tags/patty.html'):
    models = {}

    return {'template': template,
            'models': models,
            }


class VerbatimNode(template.Node):

    def __init__(self, text):
        self.text = text

    def render(self, context):
        return self.text


@register.tag
def verbatim(parser, token):
    text = []
    while 1:
        token = parser.tokens.pop(0)
        if token.contents == 'endverbatim':
            break
        if token.token_type == template.TOKEN_VAR:
            text.append('{{')
        elif token.token_type == template.TOKEN_BLOCK:
            text.append('{%')
        text.append(token.contents)
        if token.token_type == template.TOKEN_VAR:
            text.append('}}')
        elif token.token_type == template.TOKEN_BLOCK:
            text.append('%}')
    return VerbatimNode(''.join(text))
