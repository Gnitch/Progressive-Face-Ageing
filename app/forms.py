from django import forms

from app.models import Missing, Family

class FamilyForm(forms.ModelForm):  
    error_messages = {        
        'contact_check': 'Enter 10 digit contact. Number should start from 7,8 or 9'
    }    
    class Meta :
        model = Family
        fields = ['father', 'mother', 'sibling', 'guardian', 'contact1', 'contact2']

    def clean(self):
        contact1 = str(self.cleaned_data.get('contact1'))
        contact2 = str(self.cleaned_data.get('contact2'))
        check = lambda x : len(x) != 10 and x[0] not in ['7', '8', '9']            
        if check(contact1) and check(contact2):
            raise forms.ValidationError(
                self.error_messages['contact_check'],
                code='contact_check'
            )  

        return self.cleaned_data

class MissingForm(forms.ModelForm):  
    error_messages = {       
        'adhar_check': 'Enter 12 digit adhar number',         
        'adhar_exist':'Adhar number exists'
    }    
    class Meta :
        model = Missing
        fields = ['gender', 'img_person','state', 'firstname', 'lastname', 'weight', 'height', 'city', 'dob', 'adhar', 'last_sighted']

    def clean(self):
        adhar = self.cleaned_data.get('adhar')
        if len(str(adhar)) != 12 :
            raise forms.ValidationError(
                self.error_messages['adhar_check'],
                code='adhar_check'
            )         

        if Missing.objects.filter(adhar=adhar).exists():
            raise forms.ValidationError(
                self.error_messages['adhar_exist'],
                code='adhar_exist'
            )         

        return self.cleaned_data

