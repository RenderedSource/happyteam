from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.utils.html import escape, conditional_escape
from itertools import chain
from django.forms.widgets import Select

class ButtonGroup(Select):

    def __init__(self, attrs=None, choices=()):
        super(Select, self).__init__(attrs)
        self.choices = list(choices)

    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = ''
        if attrs is None: attrs = dict()
        attrs.update({ 'class': 'btn-group', 'data-toggle': 'buttons-radio' })
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<div%s>' % flatatt(final_attrs)]
        options = self.render_options(choices, [value])
        if options:
            output.append(options)
        output.append(u'</div>')

        return mark_safe(u'\n'.join(output))

    def render_options(self, choices, selected_choices):
        # Normalize to strings.
        selected_choices = set(force_unicode(v) for v in selected_choices)
        output = []
        for option_value, option_label in chain(self.choices, choices):
            css_class = 'btn btn-primary active' if option_value in selected_choices else 'btn btn-primary'
            output.append(u'<button type="button" data-toggle="button" class="%s">%s</button>' % (css_class, escape(option_label)))
        return u'\n'.join(output)