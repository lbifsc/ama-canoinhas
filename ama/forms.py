from . import models
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import PrependedText
from crispy_forms.layout import ButtonHolder, Layout, Row, Column, HTML, Submit


class MensagemForm(forms.ModelForm):
    nome = forms.CharField(
        required=True,
        max_length=150,
        label='Nome:',
    )

    email = forms.EmailField(
        required=True,
        max_length=200,
        label='E-mail:',
    )

    telefone = forms.CharField(
        required=False,
        max_length=20,
        label='Telefone:',
    )

    assunto = forms.CharField(
        required=True,
        max_length=150,
        label='Assunto:',
    )

    mensagem = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'rows': 6}),
        label='Mensagem',
    )

    class Meta:
        model = models.Mensagem
        fields = ['nome', 'email', 'telefone', 'assunto', 'mensagem']

    def __init__(self, *args, **kwargs):
        super(MensagemForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Row(
                Column('nome', css_class='col-lg-12'),
            ),
            Row(
                Column('email', css_class='col-lg-6'),
                Column('telefone', css_class='col-lg-6'),
            ),
            Row(
                Column('assunto', css_class='col-lg-12'),
            ),
            Row(
                Column('mensagem', css_class='col-lg-12'),
            ),
            ButtonHolder(
                Submit('submit', 'enviar', css_class='mb-2'),
            ),
        )
