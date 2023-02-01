from django import forms
import requests
import re
from django.utils import timezone


class PedidoForms(forms.Form):
    nome=forms.CharField(max_length=60, required=True, label="Nome", widget=forms.TextInput(
        attrs={
            "class": "form__nome",
            "placeholder": "Exemplo: Breno Morim"
        }
    ))
    contato=forms.CharField(max_length=20, required=True, label="Número de Telefone", widget=forms.TextInput(
        attrs={
            "class": "form__contato",
            "placeholder": "Exemplo: 11 91234-5678"
        }
    ))
    cep=forms.CharField(max_length=20, required=True, label="CEP para entrega", widget=forms.TextInput(
        attrs={
            "class": "form__cep",
            "placeholder": "Exemplo: 01234-567"
        }
    ))
    numero_endereco=forms.IntegerField(min_value=1, required=True, label="Número do endereço", widget=forms.NumberInput(
        attrs={
            "class": "form__numero-endereco",
            "placeholder": "Exemplo: 9"
        }
    ))
    data_entrega=forms.DateField(
        input_formats=["%d/%m/%Y"],
        required=True,
        label="Data para realizarmos a entrega",
        widget=forms.DateInput(attrs={"class": "form__data-entrega", "placeholder": "Exemplo: 20/02/2023"},format=["%d/%m/%Y"])
    )
    mensagem=forms.CharField(required=False, max_length=255, label="Deixe uma mensagem para nossa equipe (Opcional)", widget=forms.Textarea(
        attrs={
            "class": "form__mensagem",
            "placeholder": "Pode ser uma recomendação ou detalhe sobre o pedido, por exemplo"
        }
    ))

    def clean_cep(self):
        cep = self.cleaned_data.get("cep")
        if not cep:
            raise forms.ValidationError("CEP não enviado!")
        cep = cep.strip().replace("-", "")

        # Usa o web service viacep para pegar os dados do endereço
        resposta = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
        
        # A resposta quando encontra um endereço válido retorna um json contendo também o cep já formatado
        if not "cep" in resposta.text:
            raise forms.ValidationError("CEP inválido!")

        return resposta.json()['cep']

    def clean_contato(self):
        contato = self.cleaned_data.get("contato")

        # Garante que o telefone de contato siga o padrão:
        # 11 91234-5678, podendo ou não conter o espaço separando o DDD ou o hífen no número
        regex = "([0-9]{2})( )?9[0-9]{4}(-)?[0-9]{4}"

        if not re.match(regex, contato):
            raise forms.ValidationError('Número de contato inválido! Lembre-se de usar o padrão 11 91234-5678')

        return contato

    def clean_data_entrega(self):
        data_entrega = self.cleaned_data.get("data_entrega")
        if not data_entrega:
            raise forms.ValidationError("Data de entrega não enviada")
        
        data_atual = timezone.datetime.now().date()

        if data_entrega > data_atual:
            return data_entrega
        else:
            raise forms.ValidationError("A data de entrega deve ser no minínimo um dia depois de hoje")
        