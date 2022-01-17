from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.contrib.auth.decorators import login_required

from app.forms import FamilyForm, MissingForm
from app.models import Family, Missing

def home(request):     
    return render(request,'app/home.html')

@login_required()
def familyForm(request):      
    if request.method == "POST" :
        family_form = FamilyForm(request.POST)
        if family_form.is_valid():
            form_obj = family_form.save()
            request.session['family_pk'] = form_obj.id
            print(f'Family object created with pk={form_obj.id}')
            return render(request,'app/person.html')

        else :            
            errors = family_form.errors.as_data()             
            errors = list(errors.values())        
            err = ''
            for error in errors :
                err = str(list(error[0])[0]) + ' '
            context = {'error':err}           
            return render(request, 'app/family.html', context)             

    return render(request,'app/family.html')

@login_required()
def missingPersonForm(request):       
    if request.method == "POST" :
        missing_form = MissingForm(request.POST)
        if missing_form.is_valid():
            if 'family_pk' in request.session :
                form_obj = missing_form.save(commit=False)
                family_pk = request.session['family_pk']                
                family_obj = get_object_or_404(Family, pk=family_pk)
                del request.session['family_pk']                
                form_obj.family_id = family_obj.id 
                form_obj.user_id = request.user.id
                form_obj.save()            
                print(f'Missing object created with pk={form_obj.id}')    
            
            else :
                context = {'error':'Some error occured with the session variable'}           
                return render(request, 'app/person.html', context)                    

        else :            
            errors = missing_form.errors.as_data()                         
            errors = list(errors.values())        
            print(errors)            
            err = ''
            for error in errors :
                err = str(list(error[0])[0]) + ' '
            context = {'error':err}           
            return render(request, 'app/person.html', context)                                

    return render(request,'app/person.html')

