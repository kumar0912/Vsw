from django.db import models

from django.urls import reverse

from memberships.models import Membership

class Course(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length =250)
    description = models.TextField()
    allowed_memberships = models.ManyToManyField(Membership)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:detail', kwargs={'slug':self.slug})

    # Now we had this property since Lesson class has a foreign Key to
    #this class self.lesson_set.all() returns all those lessons which are
    #given the foreign key to this course
    #self.lesson_set.all() is just a syntax it could be anything
    #Like self.lecture_set.all()
    #lesson or lecture or phalana/dhimkana doesn't really matter

    @property
    def lessons(self):
        return self.lesson_set.all().order_by('position')

class Lesson(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length = 120)
    course = models.ForeignKey(Course,on_delete = models.SET_NULL,null = True)
    position = models.IntegerField()
    video_url = models.CharField(max_length = 200)
    thumbnail = models.ImageField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:lesson-detail',
        kwargs = {
            'course_slug':self.course.slug,
            'lesson_slug':self.slug,
        })
