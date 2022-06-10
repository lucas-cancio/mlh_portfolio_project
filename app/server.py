import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

class Person:
    def __init__(self, _name, _hobbies, _workExperience, _education, _aboutMe, _travelMapURL, _profileImageURL="./static/img/logo.jpg"):
        self.name = _name
        self.hobbies = _hobbies
        self.workExperience = _workExperience
        self.education = _education
        self.aboutMe = _aboutMe
        self.travelMapURL = _travelMapURL
        self.profileImageURL = _profileImageURL

class WorkExperience:
    def __init__(self, _startDate, _endDate, _organization, _role, _roleDescriptions = ""):
        self.startDate = _startDate
        self.endDate = _endDate
        self.organization = _organization
        self.role = _role
        self.roleDescription = _roleDescriptions

class Education:
    def __init__(self, _institution, _completionDate, _degree):
        self.institution = _institution
        self.completionDate = _completionDate
        self.degree = _degree

class Hobby:
    def __init__(self, _name, _pictureURLs = "", _description = ""):
        self.name = _name
        self.pictureURLs = _pictureURLs
        self.description = _description

class Project:
    def __init__(self, _title = "Project #", _pictureURLS = [], _description = "", _siteURL = "", _githubURL = ""):
        self.title = _title
        self.pictureURLs = _pictureURLS
        self.description = _description
        self.siteURL = _siteURL
        self.githubURL = _githubURL

def GetPeople():
    Lucas = Person("Lucas Cancio"
                , [Hobby("game development", ["./static/img/lucas/gameDev02.PNG", "./static/img/lucas/gameDev03.PNG"], "I enjoy making games, mainly the programming aspect since I am not the best artist. You can check out some of the things I have made on my Itch.io page.")
                    , Hobby("martial arts", ["./static/img/lucas/tkd.PNG"], "I like doing different forms of martial arts, including Taekwondo, Brazilian Jiu Jitsu, and kick boxing.")
                    , Hobby("outdoors stuff", ["./static/img/lucas/outdoors01.jpg", "./static/img/lucas/outdoors02.jpg", "./static/img/lucas/outdoors03.jpg"], "I enjoy biking and hiking in a nature park near my home.")]
                , [WorkExperience("May 2020", "August 2020", "TheCoderSchool", "Programming Tutor", "I tutored kids on how to program using C++, Python, and Scratch.")
                    , WorkExperience("June 2021", "September 2021", "Machine Intelligence Lab @ UF", "Undergraduate Researcher", "I mainly focused on documenting an autonomous submarine's simulation software.")]
                , [Education("University of Florida", "May 2023", "Bachelor's of Science in Computer Science")]
                , "Hello everyone! I am a 4th year CS major at University of Florida in the USA. I am pursuing becoming a professional software developer with a focus on web development. From what I have learned so far from this program, I am now also considering being a production engineer. I love programming and the power it gives me to create things like games and what ever cool app ideas I can imagine."
                , ""
                , "./static/img/lucas/lucas.jpg")
                
    return Lucas

@app.route('/')
def index():
    return render_template('home.html', title="Home", url=os.getenv("URL"))

@app.route('/my-work')
def my_work():
    return render_template('my-work.html', title="My Work", url=os.getenv("URL"))

@app.route('/about')
def about():
    return render_template('about.html', title="About", url=os.getenv("URL"))

@app.route('/contact')
def contact():
    return render_template('contact.html', title="Contact", url=os.getenv("URL"))