import os
from flask import Flask, jsonify, render_template, request
import requests
from dotenv import load_dotenv
from itsdangerous import json
from peewee import *
from playhouse.shortcuts import model_to_dict
import datetime


load_dotenv()
app = Flask(__name__)

#db connection
mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306)

# db timeline model
class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

print(mydb)
mydb.connect()
mydb.create_tables([TimelinePost])


class Experience:
    def __init__(self, _startDate, _endDate, _organization, _role, _roleDescription = ""):
        self.startDate = _startDate
        self.endDate = _endDate
        self.organization = _organization
        self.role = _role
        self.roleDescription = _roleDescription

class Education:
    def __init__(self, _institution, _completionDate, _degree):
        self.institution = _institution
        self.completionDate = _completionDate
        self.degree = _degree
        
class Project:
    def __init__(self, _title = "Project #", _id = "Project#", _descriptions = [], _siteURL = "", _githubURL = "", _pictureURLs = [], _miscURLs = [{"linkName": "", "url": ""}]):
        self.title = _title
        self.id = _id
        self.descriptions = _descriptions
        self.siteURL = _siteURL
        self.githubURL = _githubURL
        self.pictureURLs = _pictureURLs
        self.miscURLs = _miscURLs

class ContactMethod:
    def __init__(self, _name, _value = "", _linkURL = "", _iconName = ""):
        self.name = _name
        self.value = _value
        self.linkURL = _linkURL
        self.iconName = _iconName


projects = [Project(
            _title = "ShadowMe Web App",
            _id = "ShadowMe",
            _descriptions = [{"title": "What is it?", "content": "So far, it is a web app I created with account creation and login authorization functionalities. Its ultimate purpose is to connect students with shadowing opportunites."},
                            {"title": "What I Used?", "content": "I used a JavaScript tech stack with React.js and Node.js for the front and back end, and MySQL for the database."}],
            _siteURL = "https://shadowme-app.herokuapp.com/",
            _githubURL = "https://github.com/lucas-cancio/ShadowMe",
            _pictureURLs = ["./static/img/projects/ShadowMe/LoginPage.PNG",
                            "./static/img/projects/ShadowMe/CreateAccountPage.PNG"],
            _miscURLs = [{"linkName": "" ,"url": ""}]),
            Project(
            _title = "CaffeineCulator Web App",
            _id = "CaffeineCulator",
            _descriptions = [{"title": "What is it?", "content": "A web app that tracks your daily caffeine consumption. I collaborated in a group of three for a MLH hackathon."},
                            {"title": "How I contributed?", "content": "I constructed the backend and frontend by routing the webcam data to the server's barcode scanner and decoder, and forwarding the corresponding nutrition information back to the frontend for display by using JavaScript, Python, and Flask"}],
            _siteURL = "https://caffeineculator.pythonanywhere.com/",
            _githubURL = "https://github.com/chisafukutome/caffeine-detector-project",
            _pictureURLs = ["./static/img/projects/CaffeineCulator/HomePage.PNG",
                            "./static/img/projects/CaffeineCulator/ScanningPage.PNG",
                            "./static/img/projects/CaffeineCulator/ReceiptPage.PNG"],
            _miscURLs = [{"linkName": "Devpost" ,"url": "https://devpost.com/software/caffeineculator"}]),
            Project(
            _title = "Game Development Projects",
            _id = "GameDev",
            _descriptions = [{"title": "What I do?", "content": "I am a hobbyist game developer with a particular affinity for the programming aspect of making games."},
                            {"title": "What I use?", "content": "I primarily use the Unity engine, which uses C# for scripting."},
                            {"title": "What I have made?", "content": "I have made games for both personal projects and school projects. I have also published Unity packages to the Unity Asset Store for other creators to use."}],
            _siteURL = "",
            _githubURL = "",
            _pictureURLs = ["./static/img/projects/GameDev/CarnageContainment05.PNG",
                            "./static/img/projects/GameDev/UnityPackage.PNG",
                            "./static/img/projects/GameDev/Skator02.PNG",
                            "./static/img/projects/GameDev/CarnageContainment04.PNG"],
            _miscURLs = [{"linkName": "my Itch.io page" ,"url": "https://lucascancio.itch.io/"},
                        {"linkName": "my Unity package" ,"url": "https://assetstore.unity.com/packages/tools/ai/navmesh-link-placer-223521"}]),
            Project(
            _title = "Portfolio Site",
            _id = "PortfolioSite",
            _descriptions = [{"title": "What is it?", "content": "This is my portfolio website, which exhibits information about my work experience, education, projects, and more."},
                            {"title": "How I made it?", "content": "I used Python's Flask framework for the backend, and Jinja templates and bootstrap styling for the frontend."},
                            {"title": "Why I made it?", "content": "I was prompted to make this site for MLH's production engineering fellowship program. I also wanted to make this site before the program, because it made for good practice and elegantly displayed important information about me and my qualifications."}],
            _siteURL = "http://lucas-cancio.duckdns.org:5000/",
            _githubURL = "https://github.com/lucas-cancio/mlh_portfolio_project",
            _pictureURLs = ["./static/img/projects/PortfolioSite/HomePagePNG.PNG",
                            "./static/img/projects/PortfolioSite/MyWorkPage.PNG"],
            _miscURLs = [])]

experiences = [Experience(_startDate = "June 2021",
                        _endDate = "September 2021",
                        _organization = "Machine Intelligence Lab @ UF",
                        _role = "Undergraduate Researcher", 
                        _roleDescription = "I documented the functionalities of an autonomous submarine's simulation software that used Python, XML, ROS, and Gazebo. I also implemented different launch options for toggling the submarine's simulated or real cameras during the simulation."),
                Experience(_startDate = "May 2020",
                        _endDate = "August 2020",
                        _organization = "TheCoderSchool",
                        _role = "Programming Tutor",
                        _roleDescription = "I tutored kids, ages 8 to 17, on how to program using C++, Python, and Scratch. I also taught and led kids during programming-oriented summer camps.")]

contactMethods = [ContactMethod("E-mail", "lucas.canciox1@gmail.com", "", "fa fa-envelope-open-o"),
                    ContactMethod("LinkedIn", "lucas-cancio-b24581216", "https://www.linkedin.com/in/lucas-cancio-b24581216/", "fa fa-linkedin-square "),
                    ContactMethod("GitHub", "lucas-cancio", "https://github.com/lucas-cancio", "fa fa-github"),
                    ContactMethod("Discord", "Lucas Cancio#3138", "", "bi bi-discord ")]  

educations = [Education("University of Florida", "May 2023", "Bachelor's of Science in Computer Science")]        

skills = ["JavaScript", "Flask", "Python", "React", "NodeJS", "MySQL", "C++", "HTML", "CSS", "Git", "Linux"]

def fetch_time_line_posts():
    timeline_posts = requests.get("http://localhost:5000/api/timeline_post")
    return timeline_posts

@app.route('/')
def index():
    return render_template('home.html', title="Home", url=os.getenv("URL"))

@app.route('/my-work')
def my_work():
    return render_template('my-work.html', title="My Work", projects=projects, experiences=experiences, url=os.getenv("URL"))

@app.route('/about')
def about():
    return render_template('about.html', title="About", educations=educations, skills=skills, url=os.getenv("URL"))

@app.route('/contact')
def contact():
    return render_template('contact.html', title="Contact", contactMethods = contactMethods, url=os.getenv("URL"))

@app.route('/timeline')
def timeline():
    timeline_posts = fetch_time_line_posts()
    # print(str(timeline_posts))
    timeline_posts = json.loads(timeline_posts.text)['timeline_posts']
    print(str(timeline_posts))

    return render_template('timeline.html', title="Timeline", timeline_posts=timeline_posts)

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    print("Creating new timeline post")
    name = request.form.get("fname")
    email = request.form.get("femail")
    content = request.form.get("fcontent")
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    timeline_posts = json.loads(fetch_time_line_posts().text)['timeline_posts']    

    return render_template('timeline.html', title="Timeline", timeline_posts=timeline_posts)


@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/api/timeline_post', methods=['DELETE'])
def delete_time_line_post():
    id = request.form['id']

    post = TimelinePost.get_by_id(id)
    TimelinePost.delete_by_id(id)
    
    return model_to_dict(post)