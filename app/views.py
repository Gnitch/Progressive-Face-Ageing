from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect, get_list_or_404
from django.contrib.auth.decorators import login_required

from app.forms import FamilyForm, MissingForm
from app.models import Family, Missing
from utils.choices import choices_gender, choices_state
from utils.util import calculateAge

def home(request):     
    return render(request,'app/home.html')

def personDetail(request, person_id):   
    person_detail = get_object_or_404(Missing, pk=person_id)    
    age = calculateAge(person_detail.dob)
    family_detail = get_object_or_404(Family, pk=person_detail.family_id)
    context = {"person_detail":person_detail, 
                "family_detail":family_detail,
                "state":choices_state[person_detail.state],
                "gender":choices_gender[person_detail.gender],
                "age":age}
    return render(request, 'app/person_deatil.html', context)

def find(request):     
    people_list = get_list_or_404(Missing, status=False)
    context = {"people_list":people_list}    
    return render(request,'app/find.html',context)    

def searchPerson(request):
    query = request.GET.get("q")
    people_list = list(Missing.objects.filter(firstname=query).filter(status=False))
    context = {"people_list":people_list}        
    if len(people_list) < 1 :
        context['error'] = "No Missing Person found"
        print(context)
    return render(request,'app/find.html',context)    

@login_required()
def statusUpdate(request, person_id):
    person_detail = get_object_or_404(Missing, pk=person_id)    
    person_detail.status = True
    person_detail.save()
    return personDetail(request, person_id)

@login_required()
def familyForm(request):      
    if request.method == "POST" :
        family_form = FamilyForm(request.POST)
        if family_form.is_valid():
            form_obj = family_form.save()
            request.session['family_pk'] = form_obj.id      
            return render(request, 'app/person.html')

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
        missing_form = MissingForm(request.POST, request.FILES)
        if missing_form.is_valid():
            if 'family_pk' in request.session :
                form_obj = missing_form.save(commit=False)
                family_pk = request.session['family_pk']                
                family_obj = get_object_or_404(Family, pk=family_pk)
                del request.session['family_pk']                
                form_obj.family_id = family_obj.id 
                form_obj.user_id = request.user.id
                form_obj.save()            
                return render(request,'app/family.html')    
            
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

