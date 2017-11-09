# coding=UTF-8

from datetime import date, timedelta

from django import forms

from vol.models import AreaTrabalho, AreaAtuacao, Voluntario, Entidade, UFS_SIGLA, AreaInteresse

class FormVoluntario(forms.ModelForm):
    "Formulário para cadastro de voluntário"
    nome = forms.RegexField(regex=r'^[^\s]+\s[^\s]+',
                            max_length=100,
                            label=u'Nome completo',
                            error_messages={'invalid': u'Favor digitar nome e sobrenome.'},
                            help_text="(não utilize abreviações)",
                            widget=forms.TextInput(attrs={'class':'form-control', 'size':35}))
    email = forms.EmailField(label=u'E-mail',
                             widget=forms.TextInput(attrs={'class':'form-control', 'size':25}),
                             error_messages={'invalid': u'Digite um e-mail válido.'})
    data_aniversario = forms.DateField(label=u'Data de nascimento',
                                       widget=forms.SelectDateWidget(years=[y for y in range(date.today().year-105, date.today().year-5)], empty_label=(u'ano', u'mês', u'dia'),attrs={'class':'form-control'}),
                                       #input_date_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],
                                       #initial=date(date.today().year-36, 5, 22),
                                       help_text="",
                                       required=False)
    estado = forms.ChoiceField(label=u'Estado',
                               choices=UFS_SIGLA,
                               initial=u'SP',
                               widget=forms.Select(attrs={'class':'form-control'}),
                               help_text="")
    cidade = forms.CharField(label=u'Cidade',
                             max_length=100,
                             widget=forms.TextInput(attrs={'class':'form-control', 'size':25}),
                             error_messages={'invalid': u'Digite a cidade onde mora.'},
                             help_text="")
    profissao = forms.CharField(label=u'Profissão',
                                max_length=100,
                                widget=forms.TextInput(attrs={'class':'form-control', 'size':25}),
                                help_text="",
                                required=False)
    area_trabalho = forms.ModelChoiceField(label=u'Área de Trabalho',
                                           empty_label=u'-- Escolha a área de trabalho --',
                                           queryset=AreaTrabalho.objects.all().order_by('nome'),
                                           widget=forms.Select(attrs={'class':'form-control'}),
                                           help_text="",
                                           required=False)
    ddd = forms.CharField(label=u'Telefone (ddd)',
                          max_length=4,
                          widget=forms.TextInput(attrs={'class':'form-control', 'size':4}),
                          help_text="",
                          required=False)
    telefone = forms.CharField(label=u'número',
                               max_length=60,
                               widget=forms.TextInput(attrs={'class':'form-control', 'size':25}),
                               help_text="",
                               required=False)
    empresa = forms.CharField(label=u'Empresa onde trabalha',
                              max_length=60,
                              widget=forms.TextInput(attrs={'class':'form-control', 'size':40}),
                              help_text="",
                              required=False)
    foi_voluntario = forms.BooleanField(label=u'sim',
                                     help_text="",
                                     required=False)
    entidade_que_ajudou = forms.CharField(label=u'Entidade que ajudou',
                                          max_length=100,
                                          widget=forms.TextInput(attrs={'class':'form-control', 'size':40}),
                                          help_text="",
                                          required=False)
    area_interesse = forms.ModelChoiceField(label=u'Área de Interesse',
                                            empty_label=u'-- Escolha a área de atuação --',
                                            queryset=AreaAtuacao.objects.all().order_by('nome'),
                                            widget=forms.Select(attrs={'class':'form-control'}),
                                            help_text="",
                                            required=False)
    descricao = forms.CharField(label=u'Descrição',
                                max_length=7000,
                                widget=forms.Textarea(attrs={'class':'form-control', 'rows':5, 'cols':30}),
                                help_text="",
                                required=False)

    class Meta:
        model = Voluntario
        fields = ("nome", "email", "data_aniversario", "estado", "cidade", "profissao", "ddd", "telefone",
                  "empresa", "foi_voluntario", "entidade_que_ajudou", "descricao", "area_trabalho", "area_interesse")

    def clean_nome(self):
        """
        Garante apenas caracteres alfanuméricos e pelo menos duas palavras.
        
        """
        nome = self.cleaned_data['nome']
        partes = nome.split(' ')
        
        if len(partes) < 2:
            raise forms.ValidationError(u'Favor digitar nome e sobrenome.')
        else:
            return self.cleaned_data['nome']

    def clean_email(self):
        # Email PRECISA estar em caixa baixa para o procedimento de login.
        val = self.cleaned_data['email'].strip().lower()
##         if self.instance and self.instance.pk:
##             existing = User.objects.filter(email__exact=val).exclude(pk=self.instance.pk)
##         else:
##             existing = User.objects.filter(email__exact=val)
##         if existing.exists():
##             raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        return val

    def clean_data_aniversario(self):
        val = self.cleaned_data['data_aniversario']
        if val == '':
            return None
        return val

    def clean_estado(self):
        val = self.cleaned_data['estado'].strip().upper()
        ufs = dict(UFS_SIGLA)
        if val not in ufs.keys():
            raise forms.ValidationError(u'Estado inexistente')
        return val

    def clean_cidade(self):
        return self.cleaned_data['cidade'].strip()

    def clean_profissao(self):
        return self.cleaned_data['profissao'].strip()

    def clean_ddd(self):
        return self.cleaned_data['ddd'].strip()

    def clean_telefone(self):
        return self.cleaned_data['telefone'].strip()

    def clean_empresa(self):
        return self.cleaned_data['empresa'].strip()

    def clean_entidade_que_ajudou(self):
        return self.cleaned_data['entidade_que_ajudou'].strip()

    def clean_descricao(self):
        return self.cleaned_data['descricao'].strip()

    def clean(self):
        cleaned_data = super(FormVoluntario, self).clean()
        # Se tem erro em algum campo mas não tem erro geral de formulário
        if self.errors and not self.non_field_errors():
            self.add_error(None, u'Por favor, verifique as pendências abaixo')
        return cleaned_data


class FormEntidade(forms.ModelForm):
    "Formulário para cadastro de entidade"
    nome_fantasia = forms.CharField(label=u'Nome fantasia',
                                    max_length=100,
                                    help_text=u'(apelido)',
                                    widget=forms.TextInput(attrs={'class':'form-control', 'size':30}))
    razao_social = forms.CharField(label=u'Razão social',
                                   max_length=120,
                                   widget=forms.TextInput(attrs={'class':'form-control', 'size':30}))
    cnpj = forms.CharField(label=u'CNPJ',
                           max_length=36,
                           help_text=u'Exemplo: 99.999.999/9999-99',
                           widget=forms.TextInput(attrs={'class':'form-control', 'size':18}))
    area_atuacao = forms.ModelChoiceField(label=u'Área de Atuação',
                                          empty_label=u'-- Escolha a área de atuação --',
                                          queryset=AreaAtuacao.objects.all().order_by('nome'),
                                          widget=forms.Select(attrs={'class':'form-control'}),
                                          help_text="")
    nome_resp = forms.CharField(label=u'Primeiro nome',
                                max_length=50,
                                widget=forms.TextInput(attrs={'class':'form-control', 'size':30}),
                                help_text="")
    sobrenome_resp = forms.CharField(label=u'Sobrenome',
                                     max_length=70,
                                     widget=forms.TextInput(attrs={'class':'form-control', 'size':30}),
                                     help_text="")
    cargo_resp = forms.CharField(label=u'Cargo',
                                 max_length=50,
                                 widget=forms.TextInput(attrs={'class':'form-control', 'size':30}),
                                 help_text="")
    cep = forms.CharField(label=u'CEP',
                          max_length=10,
                          widget=forms.TextInput(attrs={'class':'form-control', 'size':10}))
    logradouro = forms.CharField(label=u'Logradouro',
                                 max_length=100,
                                 widget=forms.TextInput(attrs={'class':'form-control', 'size':35}),
                                 error_messages={'invalid': u'Digite o logradouro (rua) onde fica a entidade.'},
                                 help_text="")
    bairro = forms.CharField(label=u'Bairro',
                             max_length=40,
                             widget=forms.TextInput(attrs={'class':'form-control', 'size':30}),
                             error_messages={'invalid': u'Digite o bairro.'},
                             help_text="")
    cidade = forms.CharField(label=u'Cidade',
                             max_length=60,
                             widget=forms.TextInput(attrs={'class':'form-control', 'size':30}),
                             error_messages={'invalid': u'Digite a cidade.'},
                             help_text="")
    estado = forms.ChoiceField(label=u'Estado',
                               initial=None,
                               choices=UFS_SIGLA,
                               widget=forms.Select(attrs={'class':'form-control'}),
                               help_text="")
    ddd = forms.CharField(label=u'DDD',
                          max_length=4,
                          widget=forms.TextInput(attrs={'class':'form-control', 'size':3}),
                          help_text="",
                          required=False)
    telefone = forms.CharField(label=u'Telefone',
                               max_length=100,
                               widget=forms.TextInput(attrs={'class':'form-control', 'size':20}),
                               help_text="",
                               required=False)
    email = forms.EmailField(label=u'E-mail',
                             widget=forms.TextInput(attrs={'class':'form-control', 'size':30}),
                             error_messages={'invalid': u'Digite um e-mail válido.'})
    nome_contato = forms.CharField(label=u'Falar com',
                                   max_length=100,
                                   widget=forms.TextInput(attrs={'class':'form-control', 'size':30}),
                                   help_text="",
                                   required=False)
    website = forms.CharField(label=u'Website',
                              max_length=110,
                              widget=forms.TextInput(attrs={'class':'form-control', 'size':30}),
                              help_text="",
                              required=False)

    class Meta:
        model = Entidade
        fields = ("nome_fantasia", "razao_social", "cnpj", "area_atuacao",
                  "nome_resp", "sobrenome_resp", "cargo_resp", "cep", "logradouro", "bairro",
                  "cidade", "estado", "ddd", "telefone", "email", "nome_contato", "website")

    def clean_email(self):
        # Email PRECISA estar em caixa baixa para o procedimento de login.
        val = self.cleaned_data['email'].strip().lower()
##         if self.instance and self.instance.pk:
##             existing = User.objects.filter(email__exact=val).exclude(pk=self.instance.pk)
##         else:
##             existing = User.objects.filter(email__exact=val)
##         if existing.exists():
##             raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        return val

    def clean_estado(self):
        val = self.cleaned_data['estado'].strip().upper()
        ufs = dict(UFS_SIGLA)
        if val not in ufs.keys():
            raise forms.ValidationError(u'Estado inexistente')
        return val

    def clean_cidade(self):
        return self.cleaned_data['cidade'].strip()

    def clean_ddd(self):
        return self.cleaned_data['ddd'].strip()

    def clean_telefone(self):
        return self.cleaned_data['telefone'].strip()

    def clean(self):
        cleaned_data = super(FormEntidade, self).clean()
        # Se tem erro em algum campo mas não tem erro geral de formulário
        if self.errors and not self.non_field_errors():
            self.add_error(None, u'Por favor, verifique as pendências abaixo')
        return cleaned_data

class FormAreaInteresse(forms.ModelForm):
    "Formulário de áreas de interesse de voluntário"
    area_atuacao = forms.ModelChoiceField(label=u'Área de Interesse',
                                          empty_label=u'-- Escolha uma opção --',
                                          queryset=AreaAtuacao.objects.all().order_by('nome'),
                                          widget=forms.Select(attrs={'class':'form-control combo-area-interesse'}),
                                          help_text="")

    class Meta:
        model = AreaInteresse
        fields = ("area_atuacao",)