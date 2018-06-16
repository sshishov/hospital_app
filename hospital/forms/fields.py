from django import forms

from . import widgets


class HospitalBaseMixin(object):

    @staticmethod
    def add_class(attrs, class_name):
        if 'class' in attrs:
            attrs['class'] = '{old_classes} {new_class}'.format(old_classes=attrs['class'], new_class=class_name)
        else:
            attrs['class'] = class_name
        return attrs

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs.update({
            'data-toggle': 'popover',
            'title': self.label,
            'data-content': self.help_text,
        })
        attrs = self.add_class(attrs, 'col-8')
        return attrs


class HospitalSelectMixin(HospitalBaseMixin):

    def __init__(self, *args, **kwargs):
        self.search_support = kwargs.pop('search_support', False)
        super().__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs = self.add_class(attrs, 'selectpicker')
        if self.search_support:
            attrs['data-live-search'] = 'true'
        return attrs


class HospitalIntegerField(HospitalBaseMixin, forms.IntegerField):
    pass


class HospitalDecimalField(HospitalBaseMixin, forms.DecimalField):
    pass


class HospitalCharField(HospitalBaseMixin, forms.CharField):
    pass


class HospitalTextField(HospitalBaseMixin, forms.CharField):
    widget = forms.Textarea


class HospitalBooleanField(HospitalBaseMixin, forms.BooleanField):
    widget = widgets.HospitalCheckboxInput


class HospitalDateField(HospitalBaseMixin, forms.DateField):
    input_formats = ('%d.%m.%Y',)
    widget = widgets.HospitalDateInput


class HospitalDateTimeField(HospitalBaseMixin, forms.DateTimeField):
    input_formats = ('%d.%m.%Y H:i:s',)
    widget = widgets.HospitalDateTimeInput


class HospitalSelectField(HospitalSelectMixin, forms.ChoiceField):
    widget = widgets.HospitalSelect


class HospitalSelectMultipleField(HospitalSelectMixin, forms.MultipleChoiceField):
    widget = widgets.HospitalMultiSelect
