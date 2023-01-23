from django.db import models

# Create your models here.
from oscar.core.compat import get_user_model
from oscar.apps.customer.abstract_models import AbstractUser

from django.template.loader import get_template
from django.db import models
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from fastcart import settings

# from apps.customer.helpers import generate_unique_invite_code


User = get_user_model()


class UserInvitation(models.Model):
    invite_code = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


# class CustomUser(AbstractUser):
#     invite_code = models.CharField(max_length=50, blank=True)


class Invitation(models.Model):

    email = models.EmailField()  # friend's email to invite
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    sender_invite_model = models.ForeignKey(UserInvitation, on_delete=models.CASCADE)

    def send(self, hostname):

        subject = u"Hey Friend, here’s your link to join Fastcart"
        template = get_template('oscar/customer/referal_email_new.html')
        domain = hostname

        # sender_id = self.sender_id
        # sender= User.objects.get(pk=sender_id.user_id)

        context = {
            'sender_fname': self.sender.first_name,
            'sender_lname': self.sender.last_name,
            'sender': self.sender.email,
            'invite_code': self.sender_invite_model.invite_code,
            'domain': domain,

        }
        message = template.render(context)
        msg = EmailMessage(subject,
                           message,
                           settings.DEFAULT_FROM_EMAIL,
                           [self.email])
        msg.content_subtype = "html"
        return msg.send()


class Referrals(models.Model):
    user = models.ForeignKey(User, related_name='referee_referrals', on_delete=models.CASCADE)
    referred_by = models.ForeignKey(User, related_name='referrer_referrals', on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Referrals'
        verbose_name_plural = 'Referrals'
        unique_together = ('user', 'referred_by')

    def __str__(self):
        return "%s <- %s" % (self.user, self.referred_by)



from oscar.apps.customer.models import *  # noqa isort:skip
