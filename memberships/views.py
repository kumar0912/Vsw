from django.shortcuts import render

from django.views.generic import ListView

from .models import Membership,UserMembership,Subscription

def get_user_membership(request):
        user_membership_qs = UserMembership.objects.filter(user = request.user)
        if user_membership_qs.exists():
            return user_membership_qs.first()
        return None

def get_user_subscription(request):
    user_subscription_qs = Subscription.objects.filter(
        user_membership = get_user_membership(request))
    if user_subscription_qs.exists():
        return user_subscription_qs.first()
    return None


class MembershipSelectView(ListView):
    model = Membership

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data( **kwargs)
        current_membership = get_user_membership(self.request)
        context['current_membership'] = str(current_membership.membership)
        return context

    def post(self,request,**kwargs):
        selected_membership_type = request.POST.get('membership_type')
        user_membership = get_user_membership(self.request)
        user_subscription = get_user_subscription(self.request)

        selected_membership_qs = Membership.objects.filter(
                membership_type = selected_membership_type)
        if selected_membership_qs.exists():
            selected_membership = selected_membership_qs.first()

        #'''
        #=======
        #VALIDATION
        #=======
        #'''

        if user_membership.membership == selected_membership:
            if user_subscription != None:
                messages.info(request,"You already have this memberships your \
                    next payment is due {}".format('get this value from stripe'))
            # this automatically returns it to the URL it came from
                return HttpResponseRedirect(request.META.get('HTTP-REFERER'))

        # assign to the session
        request.session['selected_membership_type']= selected_membership.membership_type
        return HttpResponseRedirect(reverse('memberships:payment'))
