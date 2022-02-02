from dataclasses import field
from django import forms
from django.contrib.auth import get_user_model


class UserCreationForm(forms.ModelForm):
    password = forms.CharField() #なんでパスだけ再定義するんだろ

    class Meta:
        model = get_user_model() #この使い方便利よな
        fields = ('username', 'email', 'password',)

        def clean_password(self):
            password = self.clean_data.get("password")
            return password
        
        def save(self, commit=True):
            user = super().save(commit=False)
            user.set_password(self.cleand_data["password"])
            if commit:
                user.save()
            return user