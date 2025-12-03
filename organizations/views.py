from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Company, Cooperative
from .forms import CompanyForm, CooperativeForm


# ===== COMPANY VIEWS =====

@login_required
def company_list(request):
    """Lista de todas las empresas"""
    companies = Company.objects.all().order_by('-created_at')
    return render(request, 'organizations/company_list.html', {'companies': companies})


@login_required
def company_create(request):
    """Crear una nueva empresa"""
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.created_by = request.user
            company.save()
            
            # Asignar la empresa al perfil del usuario
            request.user.profile.company = company
            request.user.profile.save()
            
            messages.success(request, f'¡Empresa "{company.name}" creada exitosamente!')
            return redirect('organizations:company_detail', company.id)
    else:
        form = CompanyForm()
    
    return render(request, 'organizations/company_form.html', {'form': form, 'action': 'Crear'})


@login_required
def company_detail(request, pk):
    """Detalle de una empresa"""
    company = get_object_or_404(Company, pk=pk)
    members = company.members.all()
    cooperatives = company.cooperatives.all()
    
    is_member = request.user.profile.company == company
    can_join = not request.user.profile.company
    
    context = {
        'company': company,
        'members': members,
        'cooperatives': cooperatives,
        'is_member': is_member,
        'can_join': can_join,
    }
    return render(request, 'organizations/company_detail.html', context)


@login_required
def company_join(request, pk):
    """Unirse a una empresa"""
    company = get_object_or_404(Company, pk=pk)
    
    if request.user.profile.company:
        messages.warning(request, 'Ya perteneces a una empresa.')
    else:
        request.user.profile.company = company
        request.user.profile.save()
        messages.success(request, f'¡Te has unido a {company.name}!')
    
    return redirect('organizations:company_detail', company.id)


@login_required
def company_leave(request, pk):
    """Salir de una empresa"""
    company = get_object_or_404(Company, pk=pk)
    
    if request.user.profile.company == company:
        request.user.profile.company = None
        request.user.profile.save()
        messages.success(request, f'Has salido de {company.name}.')
    
    return redirect('organizations:company_list')


# ===== COOPERATIVE VIEWS =====

@login_required
def cooperative_list(request):
    """Lista de todas las cooperativas"""
    cooperatives = Cooperative.objects.all().order_by('-created_at')
    return render(request, 'organizations/cooperative_list.html', {'cooperatives': cooperatives})


@login_required
def cooperative_create(request):
    """Crear una nueva cooperativa"""
    if request.method == 'POST':
        form = CooperativeForm(request.POST)
        if form.is_valid():
            cooperative = form.save(commit=False)
            cooperative.created_by = request.user
            cooperative.save()
            messages.success(request, f'¡Cooperativa "{cooperative.name}" creada exitosamente!')
            return redirect('organizations:cooperative_detail', cooperative.id)
    else:
        form = CooperativeForm()
    
    return render(request, 'organizations/cooperative_form.html', {'form': form, 'action': 'Crear'})


@login_required
def cooperative_detail(request, pk):
    """Detalle de una cooperativa"""
    cooperative = get_object_or_404(Cooperative, pk=pk)
    companies = cooperative.companies.all()
    
    user_company = request.user.profile.company
    is_member = user_company and user_company in companies
    can_join = user_company and cooperative.can_join(user_company) and not is_member
    
    context = {
        'cooperative': cooperative,
        'companies': companies,
        'is_member': is_member,
        'can_join': can_join,
    }
    return render(request, 'organizations/cooperative_detail.html', context)


@login_required
def cooperative_join(request, pk):
    """Unir la empresa del usuario a una cooperativa"""
    cooperative = get_object_or_404(Cooperative, pk=pk)
    user_company = request.user.profile.company
    
    if not user_company:
        messages.warning(request, 'Debes pertenecer a una empresa para unirte a una cooperativa.')
    elif not cooperative.can_join(user_company):
        messages.error(request, 'Tu empresa no puede unirse a esta cooperativa (sectores diferentes).')
    else:
        cooperative.companies.add(user_company)
        messages.success(request, f'¡Tu empresa se ha unido a {cooperative.name}!')
    
    return redirect('organizations:cooperative_detail', cooperative.id)


@login_required
def cooperative_leave(request, pk):
    """Salir de una cooperativa"""
    cooperative = get_object_or_404(Cooperative, pk=pk)
    user_company = request.user.profile.company
    
    if user_company and user_company in cooperative.companies.all():
        cooperative.companies.remove(user_company)
        messages.success(request, f'Tu empresa ha salido de {cooperative.name}.')
    
    return redirect('organizations:cooperative_list')

