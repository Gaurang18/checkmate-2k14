from django.shortcuts import render_to_response,render
from django.template import RequestContext
from django.http import HttpResponseRedirect,Http404,HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from checkmate.main.models import *
from django.contrib.auth.decorators import login_required
from checkmate.main.forms import *
from django.db import IntegrityError
from django.utils import simplejson

@login_required
def question(request) :
	if request.POST:
		no = int(request.POST['no'])
	if request.GET:
		no=int(request.GET['no'])
	u=request.user
	cflip=1
	try:
		up=UserProfile.objects.get(user=u)
	except ObjectDoesNotExist:	
		raise Http404
	level=up.level
	if level!=1 and level != 2:#(11) send request from transition
		raise Http404
	if level == 1:#(6) manually uses flip in question
		try:
			q=Question.objects.get(no=no,level=1)#(12)ensuring doesnt attempt level 2 question in level 1
		except :
			raise Http404
	else :
		if up.fqs.filter(no=no).exists(): #(5)& (4) check if viewing a question after flip
			try:
				q=Question.objects.get(no=no,flip = True,level=2)#(12)ensuring doesnt attemp level 1 question in level 2
				cflip = 0
			except :
				raise Http404
		else:
			q=Question.objects.get(no=no,flip = False,level=2)#(12)ensuring doesnt attemp level 1 question in level 2
	if up.qs.filter(pk=q.no).exists():#(10) security for manual entry of question
		raise Http404
	if request.POST and 'answer' in request.POST:
		data=request.POST
		
		if data['dd']=='True' and up.ddqs.filter(pk=q.id).exists():#(3) security for double dd
			raise Http404
		if data['dd']=='True':
			if up.dd < 1 :#(1) checking if not giving manual command for dd even if he doesnt have the power up
				raise Http404
		if data['answer']==q.answer:
			up.score += q.price
			up.qs.add(q)
			up.save()
			resp={}
			resp['status']=1
			resp['score']=up.score
			resp['qno']=q.no
			json = simplejson.dumps(resp)
			return HttpResponse(json, mimetype='application/json')
			#return HttpResponseRedirect('/main/')
		elif data['answer'] is not q.answer :	
			if data['dd']=='True' :
				up.ddqs.add(q)
				up.dd -= 1
				up.save()
				resp={}
				resp['status']=2
				resp['score']=up.score
				json = simplejson.dumps(resp)
				return HttpResponse(json, mimetype='application/json')
				#return HttpResponseRedirect('/question/'+str(no)+'/')#return question for w/o dd
			up.score -= q.price /2 #<check & confirm>this is for -ve marking can be removed if needed
			up.qs.add(q)
			up.save()
			resp={}
			resp['status']=0
			resp['score']=up.score
			resp['qno']=q.no
			json = simplejson.dumps(resp)
			return HttpResponse(json, mimetype='application/json')

		#	return HttpResponseRedirect('/main/')
	if request.POST and 'flip' in request.POST:
		if up.flip == 0 or q.flip is True :#(2) & (6)checking if not giving manual command for flip even if he doesnt have the power up
			raise Http404

		up.fqs.add(q)#(4) manually enters flip for smae question
		up.flip -=1
		up.save()
		resp={}
		resp['status']=1
		resp['qno']=q.no
		#resp['score']=up.score
		json = simplejson.dumps(resp)
		return HttpResponse(json, mimetype='application/json')
		#return HttpResponseRedirect('/question/'+str(no)+'/')#redirect to same page with same question no.
		'''else:
			if level==1 or up.ddqs.filter(pk=q.id).exists() or up.dd==0:
				form.fields.pop('dd')
			return render_to_response('question.html', {'form':form,'q':q,'u':u,'up':up},context_instance=RequestContext(request))#display question again'''
	elif request.POST:
		raise Http404
	else :
		cdd = 1
		if level==1 or up.ddqs.filter(pk=q.id).exists() :
			cdd=0
		resp={}
		resp['status']=1
		resp['content']=q.content
		resp['cdd']=cdd
		resp['cflip']=cflip
		resp['price']=q.price
		json = simplejson.dumps(resp)
		return HttpResponse(json, mimetype='application/json')
		#return render_to_response('question.html', {'form':form,'q':q,'u':u,'up':up},context_instance=RequestContext(request))

@login_required
def transition(request):
	u=request.user
	up=UserProfile.objects.get(user=u)
	minscore=200#<check or complete> min score required to make transtion from one level to another
	level=up.level
	if up.score >= minscore and level==1:#(7)ensuring this is not a manual post request and hes sending it only to access from level 1
		up.level=3#(8)to make sure he doesnt manual request to transition market place
		up.save()
		resp={}
		resp['status']=1
		json = simplejson.dumps(resp)
		return HttpResponse(json, mimetype='application/json')
		#return HttpResponseRedirect('/market/')
	else :
		raise Http404

@login_required
def market(request):
	u=request.user
	try :
		up=UserProfile.objects.get(user=u)
	except :
		raise Http404
	level=up.level
	if level != 2 and level != 3:#(8)&(9)ensuring no manual request to marketplace from level 1
		raise Http404
	if level==3:
		flipcost=20#<complete> price of power subject to change
		ddcost=20#<complete>price of power subject to change
	elif level==2:
		flipcost=30#<complete>price of power subject to change
		ddcost=30#<complete>price of power subject to change
	if request.POST and 'buy' in request.POST:
		data=request.POST
		if up.score < (int(data['flip'])*flipcost + int(data['dd'])*ddcost) :
			resp ={}
			resp['status']=0
			json=simplejson.dumps(resp)
			return HttpResponse(json, mimetype='application/json')
		up.score = up.score - (int(data['flip'])*flipcost + int(data['dd'])*ddcost)
		up.flip=up.flip + int(data['flip'])
		up.dd =up.dd + int(data['dd'])
		up.level=2
		up.save()
		resp={}
		resp['status']=1
		resp['score']=up.score
		resp['dd']=up.dd
		resp['flip']=up.flip
		json = simplejson.dumps(resp)
		return HttpResponse(json, mimetype='application/json')
		#if request.session['prev_url']:
		#	request.session.clear_expired()
		#	return HttpResponseRedirect(request.session['prev_url'])
		#else:
		#return HttpResponseRedirect('/')
	'''else:
		resp={}
		resp['status']=1
		resp['flipcost']=flipcost
		resp['ddcost']=ddcost
		resp['score']=up.score
		json = simplejson.dumps(resp)
		return HttpResponse(json, mimetype='application/json')
		form=MarketForm()
		form.fields['flip'].help_text='(Cost ' + str(flipcost)+' Points)'
		form.fields['dd'].help_text='(Cost ' + str(ddcost)+' Points)'
		return render_to_response('market.html', {'form':form,'u':u,'up':up},context_instance=RequestContext(request))'''

def login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	if request.POST:
		form=LoginForm(request.POST)
		if form.is_valid():	
			data=form.cleaned_data
			username = data['username']
			password = data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					auth.login(request, user)
					return HttpResponseRedirect('/')
					
				else:
					state = "Your account is not active, please contact the site admin."
					return render_to_response('LOGINhtml.html', {'form':form,'state':state},context_instance=RequestContext(request))
					
			else:
				state = "Your username and/or password were incorrect."
				return render_to_response('LOGINhtml.html', {'form':form,'state':state},context_instance=RequestContext(request))
		else:
			return render_to_response('LOGINhtml.html', {'form':form},context_instance=RequestContext(request))
			
	else:
		form=LoginForm()
		return render_to_response('LOGINhtml.html', {'form':form},context_instance=RequestContext(request))

@login_required
def main(request):
	u=request.user
	up=UserProfile.objects.get(user=u)
	level=up.level
	'''if level == 3:
		return HttpResponseRedirect('/market/')'''
	eqset=up.qs.filter(level=level).order_by('no')
	elist=eqset.values('no')
	qset=Question.objects.filter(level=level,flip=False).exclude(no__in=elist).order_by('no')
	return render_to_response('index.html', {'qset':qset,'eqset':eqset,'u':u,'up':up},context_instance=RequestContext(request))

def rulebook(request):
	 return render_to_response('rulebook.html',context_instance=RequestContext(request))


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")

def register(request):
	m=''
	if request.user.is_authenticated():
		return HttpResponseRedirect('/main/')
	if request.POST:

		form=RegistrationForm(request.POST)
		if form.is_valid():
			
			data=form.cleaned_data
			u=User()
			up=UserProfile()
			u.username=data['username']
			u.set_password(data['password'])
			u.email=data['email1']
			try:
				u.save()
			except IntegrityError:
				m='Username already exists'
				return render_to_response('REGIShtml.html',{'message':m},context_instance=RequestContext(request))
			up.name1=data['name1']
			up.name2=data['name2']
			up.phone1=data['phone1']
			up.phone2=data['phone2']
			up.email1=data['email1']
			up.email2=data['email2']
			up.user=u
			up.save()
			return HttpResponseRedirect('/login/')
		else:
			return render_to_response('REGIShtml.html',{'message':m},context_instance=RequestContext(request))
	else:
		form=RegistrationForm()
		return render_to_response('REGIShtml.html',{'form':form},context_instance=RequestContext(request))