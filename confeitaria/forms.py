from django import forms
import requests
import re

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

    def clean_cep(self):
        cep = self.cleaned_data.get("cep")
        if not cep:
            raise forms.ValidationError("CEP não enviado!")
        cep = cep.strip().replace("-", "")
        resposta = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
        
        print(resposta.json())
        if not "cep" in resposta.text:
            raise forms.ValidationError("CEP inválido!")

        return resposta.json()['cep']

    def clean_contato(self):
        contato = self.cleaned_data.get("contato")
        regex = "([0-9]{2})?( )?9[0-9]{4}(-)?[0-9]{4}"

        if not re.match(regex, contato):
            raise forms.ValidationError('Número de contato inválido! Lembre-se de usar o padrão 11 91234-5678')

        return contato