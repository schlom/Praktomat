from django.db import models
from django.conf import settings
from tasks.models import Task
from solutions.models import Solution, SolutionFile
from django.utils.translation import ugettext_lazy as _
from django.core.mail import EmailMessage
from django.template import Context, loader
from django.contrib.sites.requests import RequestSite
from datetime import datetime
from utilities.nub import nub
import difflib

from accounts.models import User
from configuration import get_settings


class Attestation(models.Model):
	""""""
	class Meta:
		verbose_name = _('Attestation')
		verbose_name_plural = _('Attestations')

	created = models.DateTimeField(auto_now_add=True)
	solution = models.ForeignKey(Solution)
	author = models.ForeignKey(User, verbose_name="attestation author", limit_choices_to = {'groups__name': 'Tutor'})

	public_comment = models.TextField(blank=True, help_text = _('Comment which is shown to the user.'))
	private_comment = models.TextField(blank=True, help_text = _('Comment which is only visible to tutors'))
	final_grade = models.ForeignKey('RatingScaleItem', null=True, help_text = _('The mark for the whole solution.'))
	
	final = models.BooleanField(default = False, help_text = _('Indicates whether the attestation is ready to be published'))
	published = models.BooleanField(default = False, help_text = _('Indicates whether the user can see the attestation.'))
	published_on = models.DateTimeField(blank=True,null=True,help_text = _('The Date/Time the attestation was published.'))
	
	def publish(self, request, by):
		""" Set attestation to published and send email to user """
		self.published = True
		self.published_on = datetime.now()
		self.save()

                email = self.solution.author.email
                if not email:
                    return

		# Send confirmation email
                t = loader.get_template('attestation/attestation_email.html')
                c = {
                        'attest': self,
                        'protocol': request.is_secure() and "https" or "http",
                        'domain': RequestSite(request).domain,
                        'site_name': settings.SITE_NAME,
                        'by': by,
                        'invisible_attestor' : get_settings().invisible_attestor,
                        }
                subject = _("New attestation for your solution of the task '%s'") % self.solution.task
                body = t.render(Context(c))
                reply_to = ([self.author.email]                    if self.author.email and (not get_settings().invisible_attestor) else []) \
                         + ([get_settings().attestation_reply_to]  if get_settings().attestation_reply_to else [])
                headers = {'Reply-To': ', '.join(reply_to)} if reply_to else None
                email = EmailMessage(subject, body, None, (email,), headers = headers)
                email.send()

        def withdraw(self, request, by):
		self.published = False
                self.final = False
		self.published_on = datetime.now()
		self.save()

                recps = nub([
                    self.solution.author, # student
                    self.author,          # attestation writer
                    by,                   # usually attestation writer, may be trainer
                    ] + list(User.objects.filter(groups__name="Trainer"))  # and, for withdrawals, all trainers
                    )
                emails = [u.email for u in recps if u.email]

                if not emails:
                    return

		# Send confirmation email
                t = loader.get_template('attestation/attestation_withdraw_email.html')
                c = {
                        'attest': self,
                        'protocol': request.is_secure() and "https" or "http",
                        'domain': RequestSite(request).domain,
                        'site_name': settings.SITE_NAME,
                        'by': by,
                        }
                subject = _("Attestation for your solution of the task '%s' withdrawn") % self.solution.task
                body = t.render(Context(c))
                recipients = emails[0:1]
                bcc_recipients = emails[1:]
                email = EmailMessage(subject, body, None, recipients, bcc_recipients)
                email.send()

class AnnotatedSolutionFile(models.Model):
	""""""
	attestation = models.ForeignKey(Attestation)
	solution_file = models.ForeignKey(SolutionFile)
	content = models.TextField(help_text = _('The content of the solution file annotated by the tutor.'), blank = True)
	
	def has_anotations(self):
		original = self.solution_file.content().replace("\r\n","\n").replace("\r","\n")
		anotated = self.content.replace("\r\n","\n").replace("\r","\n")
		return not original == anotated
	
	def content_diff(self):
		d = difflib.Differ()
		original = self.solution_file.content().replace("\r\n","\n").replace("\r","\n").splitlines(0)
		anotated = self.content.replace("\r\n","\n").replace("\r","\n").splitlines(0)
		result = list(d.compare(original, anotated))
		return "\n".join(map(lambda l: l.strip("\n"), result))
	
	def __unicode__(self):
		return self.solution_file.__unicode__()
	
class RatingAspect(models.Model):
	""" describes an review aspect which the reviewer has to evaluate """	
	class Meta:
		verbose_name = _('Rating Aspect')
		verbose_name_plural = _('Rating Aspects')
		
	name = models.CharField(max_length=100, help_text = _('The Name of the Aspect to be rated. E.g.: "Readabylity"'))
	description = models.TextField(help_text = _('Description of the Aspect and how it should be rated. E.w.: "How well is the code structured?"'))
	
	def __unicode__(self):
		return self.name

class RatingScale(models.Model):
	""" describes a scale upone which the reviewer rates the aspect """
	class Meta:
		verbose_name = _('Rating Scale')
		verbose_name_plural = _('Rating Scales')
	name = models.CharField(max_length=100, help_text = _('The Name of the rating scale for the aspects. E.g.: "School marks"'))
	
	def __unicode__(self):
		return self.name
	
class RatingScaleItem(models.Model):
	""" lists all items(marks) of an rating scale"""	
	class Meta:
		verbose_name = _('Rating Scale Item')
		verbose_name_plural = _('Rating Scale Items')
	scale = models.ForeignKey(RatingScale)
	name = models.CharField(max_length=100, help_text = _('The Name of the item(mark) in the rating scale. E.g.: "A" or "very good" '))
	position = models.PositiveSmallIntegerField(help_text = _('Defines the order in which the items are sorted. Lowest is best.'))
	
	class Meta:
		ordering = ['position']
	
	def __unicode__(self):
		return self.name

class Rating(models.Model):
	""" intermediate model to assign a rating aspect and a rating scale to a task """
	task = models.ForeignKey(Task)
	aspect = models.ForeignKey(RatingAspect)
	scale = models.ForeignKey(RatingScale)
	
	def __unicode__(self):
		return "%s - %s - %s" % (self.task.title, self.aspect.name, self.scale.name)
		
class RatingResult(models.Model):
	""" the rating of particular aspect of a specific solution """
	attestation = models.ForeignKey(Attestation)
	rating = models.ForeignKey(Rating)
	mark = models.ForeignKey(RatingScaleItem, null=True) # allow for db-null so that rating results can be created programaticly without mark (blank = False !)

	def __unicode__(self):
		return unicode(self.rating.aspect) 
	
class Script(models.Model):
	""" save java script function of the rating overview page """
	script = models.TextField(blank=True, help_text = _("This JavaScript will calculate a recommend end note for every user based on final grade of every task."), default="""var sum = 0.0;\nfor (x = 0; x != grades.length; ++x) {\n    grade = parseFloat(grades[x]);\n    if (!isNaN(grade)) {\n        sum += grade;\n    }\n}\nresult=sum;""")
	
	
