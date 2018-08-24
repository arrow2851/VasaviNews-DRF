from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
#from sub.models import Subgroup



class Vser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    emailid = models.EmailField(null=True, blank=True, default=None)
    karma = models.IntegerField(default=0)
    flair = models.CharField(max_length=30, null=True, blank=True)
    subscribed_list = None
    # try:
    #     subscribed_list = Subgroup.objects.filter(subscribers=user)
    # except:
    #     subscribed_list = None
    banned = models.BooleanField(default=False)
    about = models.TextField(null=True, blank=True,default=None)
    cakeday = models.DateTimeField(auto_now_add=True)

    #Post List try getting only the ones that belong to specific Vser

    #comment list

    #Modlist = [] instead of making it a list, make it a one to many relation to the Subs
    # model

    # def is_Mod(self,sub):
    #     if sub in self.Modlist:
    #         return True
    #     else:
    #         return False

    #Registration

    #Login

    #Email confirmation

    #Forgot password

    #Change Password

    #Create Group

    #Comment

    #Post

    #Delete Comment

    #Mod delete other comment (Add in the previous one? )

    #Upvote

    #Subscribe to sub

    #Moderator stuff (Add as different type of VnewsUser?)



    def __str__(self):
        return self.name

class Moderator(models.Model):
    mod = models.OneToOneField(Vser, on_delete=models.CASCADE)