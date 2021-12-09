from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField
import uuid
from users.models import Profile
# Create your models here.
class Project(models.Model):
    owner = models.ForeignKey(Profile, verbose_name="project_owner", on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField("title", max_length=200)
    description = models.TextField("description", null=True, blank=True)
    featured_image = models.ImageField(default='default.jpg', blank=True, null=True)
    demo_link = models.CharField("demo_link", max_length=2000, null=True, blank=True)
    source_link = models.CharField("source_link", max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag')
    vote_total = models.IntegerField("vote-count", default=0, null=True, blank=True)
    vote_ratio = models.IntegerField("vote-ratio", default=0, null=True, blank=True)
    created_at = models.DateTimeField("created_at", auto_now_add=True)
    id = models.UUIDField("id", default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    def __str__(self) -> str:
        return self.title

    class Meta:
        # ordering = ['-created_at']
        ordering = ['-vote_ratio', '-vote_total', 'title', '-created_at']

    @property
    def reviewers(self):
        query_set = self.review_set.all().values_list('owner__id', flat=True)
        return query_set


    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        up_votes = reviews.filter(value='up').count()
        total_votes = reviews.count()
        ratio = (up_votes/total_votes)*100
        self.vote_total = total_votes
        self.vote_ratio = ratio
        self.save()

# review model
class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField("body", blank=True, null=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    create_at = models.DateTimeField("created_at", auto_now_add=True)
    id = models.UUIDField("id", default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    def __str__(self) -> str:
        return self.value

    class Meta:
        unique_together = [
            ['owner', 'project']
        ] 

# Tag model
class Tag(models.Model):
    name = models.CharField("tag-name", max_length=200)
    created_at = models.DateTimeField("created_at", auto_now_add=True)
    id = models.UUIDField("id", primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    def __str__(self) -> str:
        return self.name

