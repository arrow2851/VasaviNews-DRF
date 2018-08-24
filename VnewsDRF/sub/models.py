from django.db import models
#from django.contrib.auth import get_user_model
from userlist.models import Vser
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.


class Subgroup(models.Model):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(Vser, on_delete=models.CASCADE, related_name='%(class)s_owner')
    moderators = models.ManyToManyField(Vser, related_name='%(class)s_modlist', blank=True)

    banned_list = models.ManyToManyField(Vser, default=None, related_name='%(class)s_bannedlist', blank=True)
    subscribers = models.ManyToManyField(Vser, related_name='%(class)s_subslist', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    # Can be of different types I guess?

    class Meta:
        abstract = True

class Clubs(Subgroup):
    class Meta:
        abstract = False

    def __str__(self):
        return self.name


class Class(Subgroup):

    class Meta:
        abstract = False

    def __str__(self):
        return self.name


class News(Subgroup):

    class Meta:
        abstract = False

    def __str__(self):
        return self.name

class Post(models.Model):
    # subgroup = models.ForeignKey(Subgroup, on_delete=models.CASCADE)
    classgroup = models.ForeignKey(Class, on_delete=models.CASCADE, blank=True, null=True)
    newsgroup = models.ForeignKey(News, on_delete=models.CASCADE, blank=True, null=True)
    clubsgroup = models.ForeignKey(Clubs, on_delete=models.CASCADE, blank=True, null=True)

    author = models.ForeignKey(Vser, on_delete=models.CASCADE)
    author_name = author.name
    title = models.CharField(max_length=150)

    text = models.TextField(max_length=5000, blank=True)
    url = models.URLField(null=True, blank=True)

    comment_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=1)

    locked = models.BooleanField(default=False)
    removed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        x = self.classgroup
        y = self.newsgroup
        z = self.clubsgroup

        if (x and not (y or z)) or (y and not (x or z)) or (z and not (x or y)) :
            super(Post, self).save(*args, **kwargs)
        else:
            raise ValueError('Only one of three must be true')

    def __str__(self):
        return self.title
    #flair =
    #add tags using flairs


class Comment(MPTTModel):
    author = models.ForeignKey(Vser, on_delete=models.CASCADE)
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', related_name='children',
                            null=True, blank=True,
                            db_index=True,
                            on_delete=models.CASCADE)
    removed = models.BooleanField(default=False)

    timestamp = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=1)

    class MPTTMeta:
        order_insertion_by = ['-score']

    @classmethod
    def create(cls, author, text, parent):
        """
        Create a new comment instance. If the parent is post
        update comment_count field and save it.
        If parent is comment post it as child comment
        :param author: Vser instance
        :type author: Vser
        :param text: Raw comment text
        :type text: str
        :param parent: Comment or Submission that this comment is child of
        :type parent: Comment | Post
        :return: New Comment instance
        :rtype: Comment
        """

        # todo: any exceptions possible?
        comment = cls(author=author,
                      author_name=author.user.username,
                      text=text
                      )

        if isinstance(parent, Post):
            post = parent
            comment.post = post
        elif isinstance(parent, Comment):
            post = parent.post
            comment.post = post
            comment.parent = parent
        else:
            return
        post.comment_count += 1
        post.save()

        return comment

# class Vote(models.Model):
#     user = models.ForeignKey('users.Vser', on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     vote_object_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     vote_object_id = models.PositiveIntegerField()
#     vote_object = GenericForeignKey('vote_object_type', 'vote_object_id')
#     value = models.IntegerField(default=0)
#
#     @classmethod
#     def create(cls, user, vote_object, vote_value):
#         """
#         Create a new vote object and return it.
#         It will also update the ups/downs/score fields in the
#         vote_object instance and save it.
#
#         :param user: Vser instance
#         :type user: Vser
#         :param vote_object: Instance of the object the vote is cast on
#         :type vote_object: Comment | Post
#         :param vote_value: Value of the vote
#         :type vote_value: int
#         :return: new Vote instance
#         :rtype: Vote
#         """
#
#         if isinstance(vote_object, Post):
#             post = vote_object
#             vote_object.author.link_karma += vote_value
#         else:
#             post = vote_object.post
#             vote_object.author.karma += vote_value
#
#         vote = cls(user=user,
#                    vote_object=vote_object,
#                    value=vote_value)
#
#         vote.post = post
#         # the value for new vote will never be 0
#         # that can happen only when removing upvote.
#         vote_object.score += vote_value
#         if vote_value == 1:
#             vote_object.score += 1
#
#         vote_object.save()
#         vote_object.author.save()
#
#         return vote
#
#     def change_vote(self, new_vote_value):
#         if self.value == 1 and new_vote_value == 0:  # down to up
#             vote_diff = -1
#             self.vote_object.score += -1
#             self.vote_object.ups += 1
#             self.vote_object.downs -= 1
#         elif self.value == 1 and new_vote_value == -1:  # up to down
#             vote_diff = -2
#             self.vote_object.score -= 2
#             self.vote_object.ups -= 1
#             self.vote_object.downs += 1
#         elif self.value == 0 and new_vote_value == 1:  # canceled vote to up
#             vote_diff = 1
#             self.vote_object.ups += 1
#             self.vote_object.score += 1
#         elif self.value == 0 and new_vote_value == -1:  # canceled vote to down
#             vote_diff = -1
#             self.vote_object.downs += 1
#             self.vote_object.score -= 1
#         else:
#             return None
#
#         if isinstance(self.vote_object, Post):
#             self.vote_object.author.link_karma += vote_diff
#         else:
#             self.vote_object.author.comment_karma += vote_diff
#
#         self.value = new_vote_value
#         self.vote_object.save()
#         self.vote_object.author.save()
#         self.save()
#
#         return vote_diff
#
#     def cancel_vote(self):
#         if self.value == 1:
#             vote_diff = -1
#             self.vote_object.ups -= 1
#             self.vote_object.score -= 1
#         elif self.value == -1:
#             vote_diff = 1
#             self.vote_object.downs -= 1
#             self.vote_object.score += 1
#         else:
#             return None
#
#         if isinstance(self.vote_object, Post):
#             self.vote_object.author.link_karma += vote_diff
#         else:
#             self.vote_object.author.comment_karma += vote_diff
#
#         self.value = 0
#         self.save()
#         self.vote_object.save()
#         self.vote_object.author.save()
#         return vote_diff
