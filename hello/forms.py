from django import forms
from .models import Foo, Application, JAVA, PHP, NODE

class FooForm(forms.ModelForm):
    class Meta:
        model = Foo
        fields = ['bar']

class ApplicationForm(forms.ModelForm):
    LANGUAGE_CHOICES = (
        ('java', 'JAVA'),
        ('php', 'PHP'),
        ('node', 'NODE')
    )

    language = forms.ChoiceField(choices=LANGUAGE_CHOICES, required=True)
    class Meta:
        model = Application
        fields = ['name', 'description', 'repository']

    def get_language(self):
        return self.instance.get_language()

class JAVAForm(forms.ModelForm):
    class Meta:
        model = JAVA
        fields = ['jdk_version']

class PHPForm(forms.ModelForm):
    class Meta:
        model = PHP
        fields = ['php_version']

class NODEForm(forms.ModelForm):
    class Meta:
        model = NODE
        fields = ['node_version']
