from django.shortcuts import render,redirect,get_object_or_404
from .models import Profile, Relationship
from .forms import ProfileModelForm
from django.views.generic import ListView,DetailView
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.



@login_required
def my_profile_view(request):
    profile=Profile.objects.get(user=request.user)
    form=ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    confirm=False
    if request.method == 'POST':
        if form.is_valid():
            confirm=True
    return render(request,'profiles/my_profile.html',{
        'profile':profile,
        'form':form,
        'confirm':confirm
    })


@login_required
def invites_received_view(request):
    profile=Profile.objects.get(user=request.user)
    # الحصول علي جميع طلبات الصداقه الخاصه بتلك الصفحه
    qs=Relationship.objects.invatations_received(profile)
    results=list(map(lambda x:x.sender,qs))
    is_empty=False
    if len(results) == 0:
        is_empty = True
    return render(request,'profiles/my_invites.html',{
        'is_empty':is_empty,
        'qs':results
    })


@login_required
def accept_invitation(request):
    if request.method == 'POST':
        pk=request.POST.get('profile_pk')
        sender=Profile.objects.get(pk=pk)
        receiver=Profile.objects.get(user=request.user)
        rel= get_object_or_404(Relationship,sender=sender,receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('my_invites_view')


@login_required
def reject_invitation(request):
    if request.method == 'POST':
        pk=request.POST.get('profile_pk')
        sender=Profile.objects.get(pk=pk)
        receiver=Profile.objects.get(user=request.user)
        rel= get_object_or_404(Relationship,sender=sender,receiver=receiver)
        if rel.status == 'send':
            rel.delete()
    return redirect('invites_received_view')

@login_required
def invite_profiles_list_view(request):
    user=request.user
    qs=Profile.objects.get_all_profiles_to_invite(user)
    return render(request,'profiles/to_invite_list.html',{
        'qs':qs
    })

class ProfileDetailView(LoginRequiredMixin,DetailView):
    model=Profile
    template_name='profiles/detail.html'
    
    # get the profile
    def get_object(self, slug=None):
        slug=self.kwargs.get('slug')
        profile=Profile.objects.get(slug=slug)
        return profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=User.objects.get(username__iexact = self.request.user)
        profile = Profile.objects.get(user=user)
        # user is sender
        rel_r=Relationship.objects.filter(sender=profile)
        # user is receiver
        rel_s=Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context['rel_receiver']=rel_receiver
        context['rel_sender']=rel_sender
        #  get_all_author_posts() ==> from models
        context['posts']=self.get_object().get_all_author_posts()
        context['len_posts']=True if len(self.get_object().get_all_author_posts()) > 0 else False
        return context



class ProfileListView(LoginRequiredMixin,ListView):
    model=Profile
    template_name='profiles/profile_list.html'
    context_object_name='qs'
    
    def get_queryset(self):
        search_friends = self.request.GET.get('q')
        if search_friends:
            qs=Profile.objects.filter(Q(first_name__contains=search_friends) )
        else:
            qs = Profile.objects.get_all_profiles(self.request.user)
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=User.objects.get(username__iexact = self.request.user)
        profile = Profile.objects.get(user=user)
        # user is sender
        rel_r=Relationship.objects.filter(sender=profile)
        print(rel_r)
        # user is receiver
        rel_s=Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context['rel_receiver']=rel_receiver
        context['rel_sender']=rel_sender
        context['is_empty']=False
        if len(self.get_queryset()) == 0:
            context['is_empty']=True
        return context


@login_required
def sender_invatation(request):
    if request.method == 'POST':
        pk=request.POST.get('profile_pk')
        user=request.user
        sender=Profile.objects.get(user=user)
        receiver=Profile.objects.get(pk=pk)
        rel=Relationship.objects.create(sender=sender,receiver=receiver,status='send')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('my_profile_view')


@login_required
def remove_form_friends(request):
    if request.method == 'POST':
        pk=request.POST.get('profile_pk')
        user=request.user
        sender=Profile.objects.get(user=user)
        receiver=Profile.objects.get(pk=pk)
        rel=Relationship.objects.filter((Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender)))
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('my_profile_view')

