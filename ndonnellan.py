import webapp2
import jinja2
import cgi, os, re
import shutil
from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), 'templates')


jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def blog_key(name="default"):
	return db.Key.from_path('blogs',name)

class BlogEntry(db.Model):
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

	def render(self):
		self._render_text = self.content.replace('\n','<br>')
		return render_str("post.html", p = self)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class NewPost(Handler):
	def get(self):
		self.render("blog_post_new.html")

	def post(self):
		subject = self.request.get("subject")
		content = self.request.get("content")

		if subject and content:
			entry = BlogEntry(parent=blog_key(), subject=subject, content=content)
			entry.put()
			self.redirect("/unit2/blog/posts/" + str(entry.key().id()))
		else:
			self.render("blog_post_new.html", 
				subject=subject,
				content=content,
				error="Both subject and content are required")


class Blog(Handler):
	def get(self):
		entries = db.GqlQuery("SELECT * FROM BlogEntry ORDER BY created DESC")
		self.render("blog.html", entries = entries)

class PermaPost(Handler):
	def get(self, post_id):
		post_key = db.Key.from_path("BlogEntry", int(post_id), parent=blog_key())
		entry = db.get(post_key)

		if entry:
			self.render("blog_post.html", entry=entry, post_id = post_id)
		else:
			self.error(404)
			return

def rot13(mystr):
	newStr = ""
	capStrRange = (65, 90)
	lowStrRange = (97, 122)

	# Rotate chars
	for s in range(len(mystr)):
		if mystr[s].isalpha():
			sNum = ord(mystr[s])
			if sNum <= capStrRange[1]:
				R = capStrRange
			else:
				R = lowStrRange

			sNumShift = ((sNum - R[0] + 13) % (R[1]-R[0]+1)) + R[0]
			newStr += chr(sNumShift)
		else:
			newStr += mystr[s]
	return newStr

class Rot13(Handler):
    def write_form(self, text=""):
        self.render("rot13.html", text=text)
        
    def get(self):
        self.render("rot13.html")

    def post(self):
    	mytext = self.request.get("text")

    	# Rotate characters
    	mytext = rot13(mytext)
        self.write_form(cgi.escape(mytext, quote = True))

class CarCulator(Handler):
	def get(self):
		self.render('car-form.html')

class World(Handler):
	def get(self):
		self.render('world.html')

class HomePage(Handler):
	def get(self):
		self.render('home.html')

app = webapp2.WSGIApplication([('/unit2/rot13', Rot13),
							   ('/carculator',CarCulator),
							   ('/unit2/blog',Blog),
							   ('/unit2/blog/newpost',NewPost),
							   (r'/unit2/blog/posts/([0-9]+)',PermaPost),
							   ('/world',World),
							   ('/',HomePage)],
                              debug=True)







