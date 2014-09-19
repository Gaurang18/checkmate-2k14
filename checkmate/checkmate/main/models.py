from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
	no=models.PositiveSmallIntegerField()
	price=models.PositiveSmallIntegerField()
	content=models.CharField(max_length=5000)
	level=models.PositiveSmallIntegerField(default=1)
	answer=models.CharField(max_length=50)
	flip=models.BooleanField(default=False)#indicates if this question for flipped questions or an original one
	class Meta:
		unique_together=('no','flip',)
	def __unicode__(self):
		if self.level == 2:
			return str(self.no) + ' level - ' + str(self.level) + ' flip - ' + str(self.flip)
		return str(self.no) + ' level - ' + str(self.level) 


class UserProfile(models.Model):
	user=models.ForeignKey(User,unique=True)#extending user model
	score=models.IntegerField(default=0)
	name1=models.CharField(max_length=200)
	name2=models.CharField(max_length=200,blank=True,null=True)
	phone1=models.BigIntegerField(null=True)
	phone2=models.BigIntegerField(blank=True,null=True)
	email1=models.EmailField()
	email2=models.EmailField(blank=True,null=True)
	qs=models.ManyToManyField('Question',related_name='qs')#storing list of questions attempted
	fqs=models.ManyToManyField('Question',related_name='fqs')#storing list of questions on which flip has been used
	ddqs=models.ManyToManyField('Question',related_name='ddqs')#storing list of questions on which dd has been used
	level=models.PositiveSmallIntegerField(default=1)#storing current level
	dd=models.PositiveSmallIntegerField(default=0)#storing amount of dd power ups
	flip=models.PositiveSmallIntegerField(default=0)#storing amopunt of flip power ups

	def __unicode__(self):
		return self.user.username