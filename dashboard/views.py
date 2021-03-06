
import requests
import json
import time
import datetime

from django.conf import settings
from django.utils import timezone
from django.shortcuts import render,HttpResponse,redirect,get_object_or_404,HttpResponseRedirect,reverse
from django.urls import reverse_lazy,reverse
from django.utils.http import is_safe_url
from django.http import JsonResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import resolve_url
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout, REDIRECT_FIELD_NAME
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView,
    PasswordResetConfirmView, LoginView
)

# local imports
from dashboard.models import User, Image, ImageAlbum, SiteContent, EventData
from dashboard.forms import (
    RegisterForm, LoginForm, ProfileForm,
    PasswordResetEmailForm, UserEditForm,
    ImageForm, ImageAlbumForm, SiteContentForm,
    EventDataForm
)


class Home(TemplateView):
    """To display landing(home) page for website
    """
    template_name = "home.html"


class RegisterView(CreateView):
    """create new account for user
    """
    template_name = "authentication/register.html"
    form_class = RegisterForm

    def get_success_url(self):
        return reverse_lazy("thank_you")

    def dispatch(self, request, *args, **kwargs):
        """If your already logged In Redirect To Dashboard
        """
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("home"))
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        user = User.objects.create_user(
            email=form.cleaned_data.get('email'),
            password=form.cleaned_data.get('password'),
            first_name=form.cleaned_data.get('first_name'),
            last_name=form.cleaned_data.get('last_name'),
            date_of_birth=form.cleaned_data.get('date_of_birth'),
            contact=form.cleaned_data.get('contact'),
            emergency_contact_no=form.cleaned_data.get('emergency_contact_no'),
            photo=form.cleaned_data.get('photo'),
        )
        # ToDo: Do not activate user directly. impliment email confirmation by sending emails.
        user.is_active = True
        user.save()
        if self.request.is_ajax():
            data = {'success_url': str(self.get_success_url()), 'error': False}
            return JsonResponse(data)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        response = super(RegisterView, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return response


class RegistrationSuccess(TemplateView):
    """Registration thank you template
    """
    template_name = "authentication/thank_you.html"


class LogInView(LoginView):
    """Login user
    """
    template_name = "authentication/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())
        if self.request.is_ajax():
            return JsonResponse({'error': False, 'success_url': self.get_success_url()})
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("dashboard")


    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return super(LogInView, self).form_invalid(form)


class DashboardView(LoginRequiredMixin, TemplateView):
    """Landing page after user logIn are register
    """
    template_name = "user_dashboard/dashboard.html"


class LogOutView(View):
    """Logout User and redirect to site home page
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("home_page"))


class ProfileEdit(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = "user_dashboard/profile_edit.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("dashboard")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return super(ProfileEdit, self).form_invalid(form)

    def form_valid(self, form):
        form.save()
        if self.redate_of_birth == form.cleaned_data.get(self.request.is_ajax()):
            data = {'error': False, 'success_url': 3(self.get_success_url())}
            return JsonResponse(data)
        return HttpResponseRedirect(self.get_success_url())

class ForgotPassword(PasswordResetView):
    """form with email field to get reset password link
    """
    template_name = 'authentication/password_reset.html'
    form_class = PasswordResetEmailForm
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'authentication/password_reset_email.html'


class PasswordResetSuccessView(PasswordResetDoneView):
    """confirmation to sent email with reset link
    """
    template_name = 'authentication/password_reset_done.html'
    title = 'Password reset email sent!'
    success_url = reverse_lazy('password_reset_done')


class PasswordResetConfirmationEmail(PasswordResetConfirmView):
    """form with new password and confirm password to set new passeord
    """
    template_name = 'authentication/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class PasswordResetCompleteView(PasswordResetCompleteView):
    """after succeesfully change of password
    """
    template_name = 'authentication/password_reset_complete.html'
    title = 'Password reset complete'


@staff_member_required
def staff_inactive(request, id):
    u = User.objects.get(pk=id)
    u.is_active = False
    u.save()
    result = User.objects.all().exclude(id=request.user.id)
    return render(request, 'staff_list.html', {'result':result})


@staff_member_required
def staff_active(request, id):
    u = User.objects.get(pk=id)
    u.is_active = True
    u.save()
    result = User.objects.all().exclude(id=request.user.id)
    return render(request, 'staff_list.html', {'result':result})


@staff_member_required
def staff_add(request,id):
    u = User.objects.get(pk=id)
    u.is_staff = True
    u.save()
    result = User.objects.all().exclude(id=request.user.id)
    return render(request, 'staff_list.html', {'result':result})


@staff_member_required
def staff_remove(request,id):
    u = User.objects.get(pk=id)
    u.is_staff = False
    u.save()
    result = User.objects.all().exclude(id=request.user.id)
    return render(request, 'staff_list.html', {'result':result})


class StaffList(LoginRequiredMixin, ListView):
    model = User
    template_name = 'staff_list.html'
    paginate_by = 10
    paginate_orphans = 1
    context_object_name = 'result'

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@staff_member_required
def staff_edit(request, id):
    user = get_object_or_404(User,id=id)
    user = User.objects.get(id=id)
    if request.method == "GET":
        form = UserEditForm(instance=user)
        return render(request,'staffedit.html', {'form':form})

    if request.method == "POST":
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            result = User.objects.all().exclude(id=request.user.id)
            return redirect('staff_list')
        else:
            return render(request, 'staffedit.html', {'form':form})


class StaffDelete(LoginRequiredMixin, DeleteView):
    model = User
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('staff_list')
    template_name = 'staffdelete.html'

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(StaffDelete,self).dispatch(*args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs['pk'])
        return render(request, 'staffdelete.html',{'user':user})




class HomePage(TemplateView):
    template_name = "frontend/index.html"



class SiteContentCreateView(LoginRequiredMixin, CreateView):
    model = SiteContent
    template_name = 'sitecontent_create.html'
    form_class = SiteContentForm

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        site_content = form.save(commit=False)
        site_content.created_by = self.request.user
        site_content.index = SiteContent.objects.count()
        if site_content.index == SiteContent.objects.count():
            site_content.index=site_content.index+1
            site_content.save()
        return redirect('sitecontent_list')


class SiteContentList(LoginRequiredMixin, ListView):
    model = SiteContent
    template_name = 'sitecontent_list.html'
    success_url = reverse_lazy('dashboard')
    paginate_by = 10
    paginate_orphans=1
    queryset = SiteContent.objects.order_by('index')
    context_object_name = 'sitelist'


    def get_ordering(self):
        return self.ordering


class SiteContentUpdate(LoginRequiredMixin, UpdateView):
    model = SiteContent
    template_name = 'sitecontent_update.html'
    form_class = SiteContentForm
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('sitecontent_list')


class SiteContentDelete(LoginRequiredMixin, DeleteView):
    model = SiteContent
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('sitecontent_list')

    def dispatch(self, *args, **kwargs):
        return super(SiteContentDelete,self).dispatch(*args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        site_name = SiteContent.objects.get(pk=kwargs['pk'])
        site_name = site_name.name
        return render(request, 'staffdelete.html',{'user':site_name})

    def post(self, request, *args, **kwargs):
        index = SiteContent.objects.all()
        index_present = SiteContent.objects.get(pk=kwargs['pk'])
        for i in index:
            if i.index > index_present.index:
                i.index = i.index-1
                i.save()
        return self.delete(request, *args, **kwargs)

        
def up(request,id):
    if request.method == "GET":
        all_obj = list(SiteContent.objects.all().values_list('index', flat=True))
        count=SiteContent.objects.count()
        content_id = SiteContent.objects.get(id=id)
        if content_id.index == min(all_obj):
            pass
        else:
            content_index = SiteContent.objects.get(index=content_id.index-1)
            content_id.index = content_id.index-1
            content_index.index = content_index.index+1
            content_id.save()
            content_index.save()
    return redirect('sitecontent_list')


def down(request,id):
    if request.method == "GET":
        all_obj = list(SiteContent.objects.all().values_list('index', flat=True))
        content_id = SiteContent.objects.get(id=id)
        count=SiteContent.objects.count()
        if content_id.index == max(all_obj):
            pass
        else:
            content_index = SiteContent.objects.get(index=content_id.index+1)
            content_id.index = content_id.index+1
            content_index.index = content_index.index-1
            content_id.save()
            content_index.save()
    return redirect('sitecontent_list')
    

class HomePage(TemplateView):
    template_name = 'frontend/index.html'
    

    def get_context_data(self, **kwargs):
        data = super(HomePage,self).get_context_data(**kwargs)
        data['sitelist'] = SiteContent.objects.filter(active=True).order_by('index')
        return data


class Upcoming_Eventdata(CreateView):
    model = EventData
    form_class = EventDataForm
    template_name = 'eventdata.html'
    success_url = reverse_lazy('sitecontent_list')


    def get(self, request, *args, **kwargs):
        groupname = settings.GROUP_NAME
        key = settings.API_KEY
        url = 'https://api.meetup.com/'+groupname+'/events?&sign=true&photo-host=public&page=20&key='+key
        context = requests.get(url)
        if context.status_code == 200:
            events= context.json()
            for context in events:
                up_date = context.get('updated')
                up_date = int(str(up_date)[:10])
                up_date = time.strftime("%Y-%m-%d %H:%M", time.localtime(up_date))
                up_date_date = datetime.datetime.strptime(up_date, '%Y-%m-%d %H:%M')
                if EventData.objects.filter(created_id=context['id']).exists():
                    ev_obj = EventData.objects.filter(created_id=context['id']).first()
                    if not ev_obj.updated_date.replace(tzinfo=timezone.utc)< up_date_date.replace(tzinfo=timezone.utc):
                        continue
                else:
                    ev_obj = EventData()
                date_feild = context.get('local_date')
                date_feild = datetime.datetime.strptime(date_feild, "%Y-%m-%d")
                time_feild = context.get('local_time')
                time_feild = datetime.datetime.strptime(time_feild, '%H:%M').time()
                ev_obj.created = context.get('created')
                ev_obj.name = context.get('name')
                ev_obj.created_id = context.get('id')
                ev_obj.event_datetime = datetime.datetime.combine(date_feild, time_feild)
                ev_obj.status = context.get('status')
                ev_obj.updated = context.get('updated')
                ev_obj.updated_date = up_date
                ev_obj.venue_name = context.get('venue', {}).get('name', "")
                ev_obj.venue_address = context.get('venue', {}).get('address_1', "")
                ev_obj.venue_city = context.get('venue', {}).get('city',"")
                ev_obj.venue_country = context.get('venue', {}).get('country', "")
                ev_obj.link = context.get('link')
                ev_obj.Contact_Us = context.get('how_to_find_us')
                ev_obj.description = context.get('description')
                ev_obj.save()
            message = "data created sucessfully"
        else:
            message = "your url page is not loaded"
        return render(request, 'eventdata.html',{'message':message}) 


class Past_Eventdata(CreateView):
    model = EventData
    form_class = EventDataForm
    template_name = 'eventdata.html'
    success_url = reverse_lazy('sitecontent_list')


    def get(self, request, *args, **kwargs):
        groupname = settings.GROUP_NAME
        key = settings.API_KEY
        url = 'https://api.meetup.com/'+groupname+'/events?&sign=true&photo-host=public&status=past&key='+key
        context = requests.get(url)
        if context.status_code == 200:
            events = context.json()
            for context in events:
                if EventData.objects.filter(created_id=context['id']).exists():
                    message = "the data is already saved"
                else:
                    date_feild = context.get('local_date')
                    date_feild = datetime.datetime.strptime(date_feild, "%Y-%m-%d")
                    time_feild = context.get('local_time')
                    time_feild = datetime.datetime.strptime(time_feild, '%H:%M').time()
                    up_date = context.get('updated')
                    up_date = int(str(up_date)[:10])
                    up_date = time.strftime("%Y-%m-%d %H:%M", time.localtime(up_date))
                    event = EventData.objects.create(
                       created=context.get('created'),
                       name=context.get('name'),
                       created_id=context.get('id'),
                       event_datetime=datetime.datetime.combine(date_feild,time_feild),
                       status=context.get('status'),
                       updated=context.get('updated'),
                       updated_date=up_date,
                       venue_name=context.get('venue', {}).get('name', ""),
                       venue_address=context.get('venue', {}).get('address_1',""),
                       venue_city=context.get('venue', {}).get('city',""),
                       venue_country=context.get('venue', {}).get('country',""),
                       link=context.get('link'),
                       Contact_Us=context.get('how_to_find_us'),
                       description=context.get('description'))
                    message = "data created sucessfully"
        else:
            message = "your url page is not loaded"
        return render(request, 'eventdata.html',{'message':message}) 



class EventDataList(ListView):
    model = EventData
    template_name = 'events_list.html'
    success_url = reverse_lazy('dashboard')
    paginate_by = 10
    context_object_name = 'eventsdata'

    def get_queryset(self):
        events = EventData.objects.all()
        if self.request.GET.get('status') == "past":
            return events.filter(status='past')
        else:
            return events.filter(status='upcoming')

    def get_context_data(self, **kwargs):
        data = super(EventDataList,self).get_context_data(**kwargs)
        data['status'] = self.request.GET.get('status')
        return data

    def post(self, request, *args, **kwargs):
        event_name = request.POST.get("event_name")
        if not event_name == "":
            eventsdata = EventData.objects.filter(name__icontains=event_name)
            if eventsdata.exists():
                return render(request,'events_list.html',{'eventsdata':eventsdata})
            else:
                error = 'search results not found.............'
                return render(request,'events_list.html',{'eventsdata':eventsdata,'error':error})
        else:
            error = "please enter event name to search"
            
        return render(request,'events_list.html',{'error':error})

