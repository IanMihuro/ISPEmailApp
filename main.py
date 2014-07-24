# coding: utf-8
#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import webapp2
import os
import logging
import csv

from google.appengine.api import rdbms
from google.appengine.ext import webapp
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google. appengine.ext import db
from google.appengine.api import mail

import jinja2

template_path = os.path.join(os.path.dirname(__file__)) 

jinja2_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_path))

template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))


class MainHandler(webapp.RequestHandler):
	def get(self):
		users = db.GqlQuery("SELECT * FROM EntriesDB2")
		template_values = {"users": users}
		template = jinja2_env.get_template('index.html')
		self.response.out.write(template.render(template_values))
				
		
class GuestBook(webapp.RequestHandler):
	def post(self):
		#posting a new guestbook entry
		conn = get_connection()
		cursor = conn.cursor()
		cursor.execute('INSERT INTO entries (guest_name, content) VALUES (%s, %s)', 
		(self.request.get('guest_name'), self.request.get("content")))
		
		conn.commit()
		conn.close()
		self.redirect("/")

html = '''
		<html>
		<head>

		<title>Search Email Details</title>

		<!-- Load the Style sheet -->

		<link type "text/css" rel="stylesheet" href="css/bootstrap.css" />
		<link rel="stylesheet" href="css/style.css" />

		<script src = "js/bootstrap.js"></script>
		<script src = "js/jquery-1.9.1.js"></script>
		<script src = "js/validate.js" type="text/javascript" ></script>



	    <link rel="stylesheet" href="css/bootstrap.css"/>
	    <link rel="stylesheet" href="css/bootstrapValidator.css"/>

	    <script type="text/javascript" src="jquery/jquery-1.10.2.min.js"></script>
	    <script type="text/javascript" src="js/bootstrap.min.js"></script>
	    <script type="text/javascript" src="js/bootstrapValidator.js"></script>



		<!-- End -->

		</head>

		<body>

		<!-- fixed navigation bar -->
		<div class="navbar navbar-default navbar-fixed-top">
			<div class="container" >
				<div class="navbar-header">
					<button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
						<span class="icon-bar"></span>
						<span class="icon-bar"></span>
						<span class="icon-bar"></span>
					</button>
					<a href="#" class="navbar-brand">KCA University</a>
				</div>

				<div class="navbar-collapse collapse">
					<ul class="nav navbar-nav">
					<li><a href="/">Home</a></li>
					<li><a href="/help">Help</a></li>
					<li><a href="/about">About Us</a></li>
					<li><a href="/contact">Contact Us</a></li>
					</ul>
				</div>
			</div>
		</div>

		<br />

		<br />

		<br />

		<!-- Grid -->
		<div class="container">

			<div class="row">

				<div class="col-md-2">
				</div>
				<div class="col-md-10">
					<p>
						Welcome to the KCA university student email activation portal.
					</p>
					<p>
						Type in your Admission Number below to retrieve your official email address.
					</p>
				</div>

			</div>

			<br />
			<br />

			<div class="row">

				<div class="col-md-2">
				</div>
				<div class="col-md-8">
					<form action="/" method="post"  class="well form-search span8" id="emailActivation" 
						data-bv-message="This value is not valid"
                      data-bv-feedbackicons-valid="glyphicon glyphicon-ok"
                      data-bv-feedbackicons-invalid="glyphicon glyphicon-remove"
                      data-bv-feedbackicons-validating="glyphicon glyphicon-refresh"

						 >
					
				  		<label>Enter Admission Number:</label>
				  		<input name="password" type="text" class="span7 search-query" placeholder = "ie 01/12345 " required data-bv-notempty-message="*The Admission Number is required and cannot be empty"  />
					   	<input type="submit" value="Click To Get My Email" class = "btn btn-primary">
				    	<br />
				    	<br />
				    	<br />
				    	 
				    		<p class="text-right">Powered by: <img src="https://lh5.googleusercontent.com/-AEBsZLrSc38/UUgznsFOOLI/AAAAAAAAAJ8/tBfNuGm6w-M/s912/intellisoftplus_logo-final.png" width="100" height="20"> </p>
				    	
					</form>
				</div>
			</div>

			<script type="text/javascript">
			    $(document).ready(function() {
			        $('#emailActivation').bootstrapValidator();
			    });
				
			    $('#emailActivation').bootstrapValidator({
			        message: 'This value is not valid',
			        feedbackIcons: {
			            valid: 'glyphicon glyphicon-ok',
			            invalid: 'glyphicon glyphicon-remove',
			            validating: 'glyphicon glyphicon-refresh'
			        },
			        fields: {
			            password: {
			                validators: {
			                    regexp: {
			                    	regexp:  /\d{2}\/\d{5}/,
                        			message: 'The Admission Number is not in the correct format'
			                        
			                    }
			                }
			            }
			        }
			    });
			   
			</script>
						
				    	
		'''




class Search(webapp.RequestHandler):
	def get(self):
		
		self.response.write(html)
	def post(self):
		self.response.write(html)
		
		adm= self.request.get('password')
		adm2 = adm.strip()
		
		if adm == "":
			self.redirect("/error")		
		elif '07/' in adm2:
			adm2 = adm2.replace('07/','7')
		elif '08/' in adm2:
			adm2 = adm2.replace('08/','8')
		elif '09/' in adm2:
			adm2 = adm2.replace('09/','9')
		else:
			adm2 = adm2.replace('/','')
			
		
		
		rows = db.GqlQuery("SELECT * FROM EntriesDB2 WHERE password = :1",adm2).get()
		
		if rows is None:
			self.redirect("/error")
		else:
			
			newpassword = list(rows.password)
			
			if not newpassword:
				self.redirect("/error")
			elif '7' in newpassword[0]:
				newpassword[0] = '07/'
			elif '8' in newpassword[0]:
				newpassword[0] = '08/'
			elif '9' in newpassword[0]:
				newpassword[0] = '09/'
			else:
				newpassword.insert(2, '/')			
						
			newpassword = ''.join(map(str, newpassword))



			
			
			self.response.write('''

				<div class="row">

					<div class="col-md-2">
					</div>
					<div class="col-md-6">			
				
				''')
			self.response.write('<p>Welcome <b>%s</b> your student email details are as follows</p>'%rows.firstname)
			self.response.write('<p>Follow the below steps to access your account:</p>')
			self.response.write('<ol>')
			self.response.write('<li>Open <a href="http://www.gmail.com/">www.gmail.com</a> on your browser</li>')
			self.response.write('<li>In the email field type in your full email address:<b> %s</b></li>'% rows.emailaddress )
			self.response.write('<li>In the password field type in your temporary password:<b> %s</b></li>' %newpassword)
			self.response.write('<li>Click on the blue “I accept. Continue to my account” button</li> ')
			self.response.write('<li>Please change your password (Put a password that only you will have access to)</li>')
			self.response.write('<li>Congratulations<b> %s</b> you now have an official KCA University email address</li>'%rows.firstname)
			
			output = '''
					</ol> 
					</div>
				</div>
			</div>

		    </div>
					
							
							
						</body>
						</html>
					'''
			self.response.write(output)
			#Housekeeping assigning global variables their values
			global first_name, last_name, email_add, password_temp 
			first_name = rows.firstname
			last_name = rows.lastname
			email_add 	= rows.emailaddress
			password_temp = newpassword

			
			
						
		
	
		
html_error = '''
		
			<html>
				<head>

					<title>
						Error Page
				</title>


					<!-- Load the Style sheet -->

					<link type "text/css" rel="stylesheet" href="css/bootstrap.css" />
					<link rel="stylesheet" href="css/style.css" />



					<link rel="stylesheet" href="css/bootstrap.css"/>
				    <link rel="stylesheet" href="css/bootstrapValidator.css"/>

				    <script type="text/javascript" src="jquery/jquery-1.10.2.min.js"></script>
				    <script type="text/javascript" src="js/bootstrap.min.js"></script>
				    <script type="text/javascript" src="js/bootstrapValidator.js"></script>


					<!-- End -->



					
				</head>



				<body>

				<script src = "js/bootstrap.js"></script>
				<script src = "js/jquery-1.9.1.js"></script>


				<!-- fixed navigation bar -->
				<div class="navbar navbar-default navbar-fixed-top">
					<div class="container" >
						<div class="navbar-header">
							<button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
								<span class="icon-bar"></span>
								<span class="icon-bar"></span>
								<span class="icon-bar"></span>
							</button>
							<a href="#" class="navbar-brand">KCA University</a>
						</div>

						<div class="navbar-collapse collapse">
							<ul class="nav navbar-nav">
								<li><a href="/">Home</a></li>
								<li><a href="/help">Help</a></li>
								<li><a href="/about">About Us</a></li>
								<li><a href="/contact">Contact Us</a></li>
							</ul>
						</div>
					</div>
				</div>

				<br />

				<br />

				<br />
						
				<!-- Grid -->
				<div class="container">

					<div class="row">

						<div class="col-md-2">
						</div>
						<div class="col-md-10">
						<h3>
						Sorry, we can't seem to find your details.
						</h3>
						<p>Please note:</p>
						<ol>
						<li>Ensure your admission number is the correct format i.e. 07/0987</li>
						
						</ol>
						</div>
					</div>
				
'''
		
class ErrorHandler(webapp2.RequestHandler):
	
	def get(self):		
		self.response.out.write(html_error)
		self.response.out.write('''
					<div class="row">
								<div class="col-md-2">
								</div>
								<div class="col-md-10">


			''')
		self.response.out.write('<form action="/" class="well">')
		self.response.out.write(' <input type="submit" value="Try Again" class="btn btn-primary"></p>	</form>  ')
		
		html_cont = '''
		
							</div>
						</div>
						<div class="row">

							<div class="col-md-2">
							</div>
							<div class="col-md-10">
							<h3> OR </h3>
							<h3> Still can't find your details? Fill the form details below to help us get you a new account</h3>
							
							<form class=" well form-horizontal"  action="/email" method="post" id="errorForm" 
						
							data-bv-message="This value is not valid"
	                      	data-bv-feedbackicons-valid="glyphicon glyphicon-ok"
	                      	data-bv-feedbackicons-invalid="glyphicon glyphicon-remove"
	                      	data-bv-feedbackicons-validating="glyphicon glyphicon-refresh" >

								<div class="form-group">
  								<label class="form-sm-2 control-label" >Full Name<font color="red">*</font></label><br />
  								<div class="col-sm-6">
  								<input name="fname" type="text" id="fname" class="form-control" placeholder="Enter Name"  required data-bv-notempty-message="Your full name is required and cannot be empty" > 
  								</div>
  								</div>
  								
  								 <div class="form-group"> 		
	  								<label class="form-sm-2 control-label">Admission<font color="red">*</font></label><br />
	  								<div class="col-sm-6">
	  								<input name="adm" type="text" id="adm" class="form-control" placeholder="Enter Admission"  required data-bv-notempty-message="Your Admission number is required and cannot be empty">
	  							</div>
	  							</div>
  								  		
  								 <div class="form-group"> 
	  								<label class="form-sm-2 control-label" >Alternate Email<font color="red">*</font></label><br /> 
	  								<div class="col-sm-6">
	  								<input name="email" type="email" id="email" class="form-control" placeholder="Enter Alternate Email"  data-bv-emailaddress-message="The input is not a valid email address">
  								</div>
  								</div>
  								  		
  								<div class="form-group">
  								<div class="col-sm-6">	
    							<input type="submit" value="Send Email" class="btn btn-primary">
    							</div>
    							</div>
							</form>
							</div>
						</div>
							
				</div>
				<script type="text/javascript">
				    $(document).ready(function() {
				        $('#errorForm').bootstrapValidator();
				    });
				</script>

				<br />
				<!-- Footer -->
				<br />
				<br />
				<br />
				<div class="navbar navbar-default navbar-fixed-bottom">
					
					<div class="container">
						<p class="navbar-text pull-right">
							Powered by: <img src="https://lh5.googleusercontent.com/-AEBsZLrSc38/UUgznsFOOLI/AAAAAAAAAJ8/tBfNuGm6w-M/s912/intellisoftplus_logo-final.png" width="100" height="20">

						</p>

					</div>

				</div>
				<!-- end -->
				</body>				
			
				</html>
				
		'''
		
		self.response.out.write(html_cont)
	
	
		
		

class UploadFormHandler(webapp2.RequestHandler):
	def get(self):
		upload_url = blobstore.create_upload_url('/upload')
		
		self.response.out.write("""<html>
									<head>
										<title>Upload files </title>
											
										<!-- Load the Style sheet -->

										<link type "text/css" rel="stylesheet" href="css/bootstrap.css" />
										<link rel="stylesheet" href="css/style.css" />
					
									</head>
									<body>


										<!-- fixed navigation bar -->
										<div class="navbar navbar-default navbar-fixed-top">
											<div class="container" >
												<div class="navbar-header">
													<button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
														<span class="icon-bar"></span>
														<span class="icon-bar"></span>
														<span class="icon-bar"></span>
													</button>
													<a href="#" class="navbar-brand">KCA University</a>
												</div>

												<div class="navbar-collapse collapse">
													<ul class="nav navbar-nav">
														<li><a href="/">Home</a></li>
														<li><a href="/help">Help</a></li>
														<li><a href="/about">About Us</a></li>
														<li><a href="/contact">Contact Us</a></li>
													</ul>
												</div>
											</div>
										</div>

										<br />

										<br />

										<br />

										<div class="container">
										<div class="row">

											<div class="col-md-2">
											</div>
											<div class="col-md-10">
											<h2>Upload Spreedsheet</h2>
											</div>
										</div>
										<div class="row">
											<div class="col-md-2">
												</div>
												<div class="col-md-8">

									""")
		
		self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data" class="well form-horizontal">' % upload_url)
		self.response.out.write("""

			<div class="form-group"> 		
	  								<label class="form-sm-2 control-label">Upload SpreedSheet*</label><br />
	  								<div class="col-sm-6">
	  								<input type="file" name="file" class="form-control">
	  							</div>
	  							</div>		 
		
		<input type="submit" name="submit" value="Submit" class="btn btn-primary"> 
		</form>	
		</div>
		</div>
		</div>

		<!-- Footer -->
				<br />
				<br />
				<br />
				<div class="navbar navbar-default navbar-fixed-bottom">
					
					<div class="container">
						<p class="navbar-text pull-right">
							Powered by: <img src="https://lh5.googleusercontent.com/-AEBsZLrSc38/UUgznsFOOLI/AAAAAAAAAJ8/tBfNuGm6w-M/s912/intellisoftplus_logo-final.png" width="100" height="20">

						</p>

					</div>

				</div>
				<!-- end -->
		
		
		</body>
		
        
        <style>
        
        
        </html>""")

			
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		upload_files = self.get_uploads('file') # 'file' is file upload upload field un the form
		blob_info = upload_files[0]
		process_csv(blob_info)
		
		blobstore.delete(blob_info.key()) # optional: delete file after import
		self.redirect("/")
		
def process_csv(blob_info):
	blob_reader = blobstore.BlobReader(blob_info.key())
	reader = csv.reader(blob_reader, delimiter=',')
	for row in reader:
		emailaddress, firstname, lastname, password  = row
		entry = EntriesDB2(emailaddress=emailaddress, firstname=firstname, lastname = lastname, password=password)
		entry.put()
		
class SendEmail(webapp2.RequestHandler):
	def post(self):
		user_add = (" You can contact me at my alternate email address which is %s." %self.request.get("email"))
		user_name =("Hi, My names are %s, " % self.request.get("fname"))
		user_adm = ("and my admission number is %s. Please assist me to find my student email address on the student portal. " % self.request.get("adm"))
		recipient_add = "support@kca.ac.ke" #changeo to KCA support email add.
		sender_add = "support@intellisoftplus.com" #change this to a KCA developer email add.
		
		subject = "I cannot find my details in the email student portal"
		
		body = (user_name + user_adm + user_add)
		
		mail.send_mail(sender_add, recipient_add, subject, body)
		self.redirect("/")

class AboutUs(webapp2.RequestHandler):
	def get(self):


				self.response.out.write("""<html>
									<head>
										<title>About Us </title>
											
										<!-- Load the Style sheet -->

										<link type "text/css" rel="stylesheet" href="css/bootstrap.css" />
										<link rel="stylesheet" href="css/style.css" />


										<!-- End -->
					
									</head>
									<body>


										<!-- fixed navigation bar -->
										<div class="navbar navbar-default navbar-fixed-top">
											<div class="container" >
												<div class="navbar-header">
													<button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
														<span class="icon-bar"></span>
														<span class="icon-bar"></span>
														<span class="icon-bar"></span>
													</button>
													<a href="#" class="navbar-brand">KCA University</a>
												</div>

												<div class="navbar-collapse collapse">
													<ul class="nav navbar-nav">
														<li><a href="/">Home</a></li>
														<li><a href="/help">Help</a></li>
														<li><a href="/about">About Us</a></li>
														<li><a href="/contact">Contact Us</a></li>
													</ul>
												</div>
											</div>
										</div>

										<br />

										<br />

										<br />

										<div class="container">
										<div class="row">

											<div class="col-md-2">
											</div>
											<div class="col-md-10">
											<h3>About Intellisoftplus</h3>
											<p>
												Intellisoftplus is an authorized Google partner that has helped over 10,000 users in many organizations to "go Google."
												As masters of cloud computing, our team helps small and large businesses, educational institutions and government agencies discover the wonders of "the cloud" and work smarter through Google Apps. 
												Our technical and sales teams design and implement solutions for these organizations with custom features, security and support - all with our strong philosophy of innovation and customer service. 
												Feel free to apply <a href="http://www.intellisoftplus.com/careers/internships.html">here</a></li>.
											</p>
											<h3>Benefits of your Official KCA Email Address </h3>

											<div class="list-group">
											
												<a href="#" class="list-group-item active">
												<h4 class="list-group-item-heading">Get stuff done faster</h4>
												<p class="list-group-item-text">
												Google Apps for Education can help streamline academic tasks such as  essay writing and class scheduling.
												Students can work together in real time on group work and assignments in  via Google Docs and see changes as they are made. 
												This does away with students and professors waiting for versions to be sent via email ensuring timely submissions and version control. 
												Students can also have access to information on professors availability, and vice versa, with Google Calendar. 
												By removing reducing these time-consuming bottlenecks, Google Apps frees you up to spend more time on learning and teaching.
												</p>
												</a>

												<a href="#" class="list-group-item active">
												<h4 class="list-group-item-heading">Get a Professional Image when Applying for a Job</h4>
												<p class="list-group-item-text">
												Maintain a professional image when sending emails and CVs to people external to the University using an official email account.
												Schedule your time better by accessing Calendar to view class timetables and availability of your professor.
												</p>
												</a>

												<a href="#" class="list-group-item active">
												<h4 class="list-group-item-heading">All your information in one place</h4>
												<p class="list-group-item-text">
												Google Apps will provide you with unlimited storage space via Drive for all your individual and group assignments, coursework, research material and past papers. 
												Get your exam results sent directly to your email account. 
												</p>
												</a>


											</div>


											</div>
										</div>
									</div>

									<!-- Footer -->
									<br />
									<br />
									<br />
									<div class="navbar navbar-default navbar-fixed-bottom">
										<div class="container">
											<p class="navbar-text pull-right">
												Powered by: <img src="https://lh5.googleusercontent.com/-AEBsZLrSc38/UUgznsFOOLI/AAAAAAAAAJ8/tBfNuGm6w-M/s912/intellisoftplus_logo-final.png" width="100" height="20">

											</p>

										</div>

									</div>
									<!-- end -->
								</body>
							</html>


									""")

class Help(webapp2.RequestHandler):
	def get(self):

		global first_name, last_name, email_add, password_temp 
		try:
			first_name
		except NameError:
			first_name = None
		if first_name is None:
			first_name = "N/A"
			last_name = "N/A"
			email_add = "N/A"
			password_temp = "N/A"


		self.response.out.write("""<html>
									<head>
										<title>Help </title>
											
										<!-- Load the Style sheet -->

										<link type "text/css" rel="stylesheet" href="css/bootstrap.css" />
										<link rel="stylesheet" href="css/style.css" />
					
									</head>
									<body>


										<!-- fixed navigation bar -->
										<div class="navbar navbar-default navbar-fixed-top">
											<div class="container" >
												<div class="navbar-header">
													<button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
														<span class="icon-bar"></span>
														<span class="icon-bar"></span>
														<span class="icon-bar"></span>
													</button>
													<a href="#" class="navbar-brand">KCA University</a>
												</div>

												<div class="navbar-collapse collapse">
													<ul class="nav navbar-nav">
														<li><a href="/">Home</a></li>
														<li><a href="/help">Help</a></li>
														<li><a href="/about">About Us</a></li>
														<li><a href="/contact">Contact Us</a></li>
													</ul>
												</div>
											</div>
										</div>

										<br />

										<br />

										<br />

										<div class="container">
										<div class="row">

											<div class="col-md-2">
											</div>
											<div class="col-md-10"> """)

		

		self.response.out.write('<p> Your Email Address is:<b> %s </b></p>'%email_add)
		self.response.out.write('<p> Your temporary password address is:<b> %s </b></p>'%password_temp)
		self.response.out.write('''<p> Follow the bellow steps to access your account</p>


			<ol>
				<li>Log-in to <a href="https://mail.google.com">www.gmail.com</a></li>
				<br />
				<img src="/images/gmail_log_in.png" alt="S" width="300" height="300">
				<br />

			''')
		self.response.out.write('<li>In the email field type in your full email address: %s</li>' %email_add)
		self.response.out.write('<li>In the password field type in your temporary password: %s</li>'%password_temp)
		self.response.out.write(""" <li>Click on the blue “I accept. Continue to my account” button  </li>
				<br />
				<img src="/images/gmail_new_account.png" alt="S" width="300" height="300">
				<br />
				<li>Please change your password (Put a password that only you will have access to)</li>
				<br />
				<img src="/images/gmail_change_password.png" alt="S" width="300" height="300">
				<br />
				<br />
			""")
		self.response.out.write('<li>Congratulations <b>%s !!</b> you now have an official KCA University email address</li>'%first_name)


		self.response.out.write("""</ol></div>
										</div>
									</div>
									<!-- Footer -->
										<br />
										<br />
										<br />
										<div class="navbar navbar-default navbar-fixed-bottom">
											<div class="container">
												<p class="navbar-text pull-right">
													Powered by: <img src="https://lh5.googleusercontent.com/-AEBsZLrSc38/UUgznsFOOLI/AAAAAAAAAJ8/tBfNuGm6w-M/s912/intellisoftplus_logo-final.png" width="100" height="20">

												</p>

											</div>

										</div>
										<!-- end -->

								</body>
							</html>


									""")


class ContactUs(webapp2.RequestHandler):
	def get(self):
		self.response.out.write('''

				<html>
				<head>

					<title>
						Contact Us
				</title>


					<!-- Load the Style sheet -->

					<link type "text/css" rel="stylesheet" href="css/bootstrap.css" />
					<link rel="stylesheet" href="css/style.css" />


					<link rel="stylesheet" href="css/bootstrap.css"/>
				    <link rel="stylesheet" href="css/bootstrapValidator.css"/>

				    <script type="text/javascript" src="jquery/jquery-1.10.2.min.js"></script>
				    <script type="text/javascript" src="js/bootstrap.min.js"></script>
				    <script type="text/javascript" src="js/bootstrapValidator.js"></script>

					<!-- End -->
					
				</head>

				<body>

				<script src = "js/bootstrap.js"></script>
				<script src = "js/jquery-1.9.1.js"></script>


				<!-- fixed navigation bar -->
				<div class="navbar navbar-default navbar-fixed-top">
					<div class="container" >
						<div class="navbar-header">
							<button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
								<span class="icon-bar"></span>
								<span class="icon-bar"></span>
								<span class="icon-bar"></span>
							</button>
							<a href="#" class="navbar-brand">KCA University</a>
						</div>

						<div class="navbar-collapse collapse">
							<ul class="nav navbar-nav">
								<li><a href="/">Home</a></li>
								<li><a href="/help">Help</a></li>
								<li><a href="/about">About Us</a></li>
								<li><a href="/contact">Contact Us</a></li>
							</ul>
						</div>
					</div>
				</div>

				<br />
				<br /> 
				<br />
						
				<!-- Grid -->
				<div class="container">

					<div class="row">

						<div class="col-md-2">
						</div>
						<div class="col-md-10">
						<h3>
						Reach out to intellisoftplus
						</h3>
						<p>Our Contact Info:</p>
						<p><b>Address:</b> NHC Langata Road Nairobi, Kenya </p>
						<p><b>Email:</b> support@intellisoftplus.com </p>
						<p><b>Phone:</b> 020 6009999/8 </p>					
						</div>
					</div> 		
						<div class="row">

							<div class="col-md-2">
							</div>
							<div class="col-md-7">
							<h3> Contact Form </h3>							
							
							<form class=" well form-horizontal"  action="/email" method="post"  id="contactForm" 
						
							data-bv-message="This value is not valid"
	                      	data-bv-feedbackicons-valid="glyphicon glyphicon-ok"
	                      	data-bv-feedbackicons-invalid="glyphicon glyphicon-remove"
	                      	data-bv-feedbackicons-validating="glyphicon glyphicon-refresh" >

								<div class="form-group">
								<div class="col-sm-6">
  								<label class="form-sm-2 control-label" >Full Name<font color="red">*</font></label>  								
  								<input name="fname" type="text" id="fname" class="form-control" placeholder="Enter Name"  required data-bv-notempty-message="Your Full Name is required and cannot be empty" > 
  								</div>
  								</div> 								  								 
  								  		
  								 <div class="form-group"> 
  								 	<div class="col-sm-6">
	  								<label class="form-sm-2 control-label">Email<font color="red">*</font></label>
	  								
	  								<input name="email" type="email" id="email" class="form-control" placeholder="Enter Email"
	  								  data-bv-emailaddress-message="The input is not a valid email address" >
  								</div>
  								</div>

  								<div class="form-group">
  									<div class="col-sm-6"> 		
	  								<label class="form-sm-2 control-label">Subject<font color="red">*</font></label><br />
	  								
	  								<input name="subj" type="text" id="subj" class="form-control" placeholder="Subject"  required data-bv-notempty-message="The Subject of the email is required and cannot be empty" >
	  							</div>
	  							</div>

	  							<div class="form-group"> 
	  								<div class="col-sm-6">		
	  								<label class="form-sm-2 control-label">Message<font color="red">*</font></label><br />
	  								
	  								<textarea name="msg" type="text" id="msg" class="form-control" placeholder="Enter message"  required data-bv-notempty-message="Your Body is required and cannot be empty" ></textarea>
	  							</div>
	  							</div>
  								  		
  								<div class="form-group">
  								<div class="col-sm-6">	
    							<input type="submit" value="Send Email" class="btn btn-primary">
    							</div>
    							</div>
							</form>
							</div>
						</div>
							
				</div>
				<script type="text/javascript">
				    $(document).ready(function() {
				        $('#contactForm').bootstrapValidator();
				    });
				</script>

				<!-- Footer -->
				<br />
				<br />
				<br />
				<div class="navbar navbar-default navbar-fixed-bottom">					
					<div class="container">
						<p class="navbar-text pull-right">
							Powered by: <img src="https://lh5.googleusercontent.com/-AEBsZLrSc38/UUgznsFOOLI/AAAAAAAAAJ8/tBfNuGm6w-M/s912/intellisoftplus_logo-final.png" width="100" height="20">

						</p>

					</div>

				</div>
				<!-- end -->

				</body>				
			
				</html>




			''')
		

		
			
			
class EntriesDB2(db.Model):
	emailaddress = db.TextProperty(required = False)
	firstname = db.TextProperty(required = False)
	lastname = db.TextProperty(required = False)
	password = db.StringProperty(required = False)
 
		

app = webapp2.WSGIApplication([
    ("/main", MainHandler),
	("/sign", GuestBook),
	("/", Search),
	("/upload", UploadHandler),
	("/uploadform", UploadFormHandler),
	("/error",ErrorHandler),
	("/email",SendEmail),
	("/about",AboutUs),
	("/help",Help),
	("/contact",ContactUs)
], debug=True)
