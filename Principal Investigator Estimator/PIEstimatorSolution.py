__author__ = "aliemre"

from Tkinter import *
import urllib2
from bs4 import BeautifulSoup
import re
import docclass

class FacultyMember():

    def __init__(self,name,webpage):
	
        self.name = name
        self.webpage = webpage
        self.publication = []

class Project():

    def __init__(self,title,summary,investigator):
	
        self.title = title
        self.summary = summary
        self.investigator = investigator

    def merge(self):
	
        self.document = " ".join([self.title,self.summary])
        return self.document

class FetchData():

    def __init__(self):
	
        self.members = {}
        self.projects = {}

    def fetch_members(self):
	
        response = urllib2.urlopen("http://cs.sehir.edu.tr/en/people/")
        html_doc = response.read()
        soup = BeautifulSoup(html_doc, "html.parser")
        member_soup = soup.find_all(class_="member")
		
        for a in member_soup:
            member_tokens = " ".join(re.findall("\S+", a.find("h4").text.strip().encode("utf-8")))
            member_tokens = [name for name in member_tokens.split() if len(name) > 0]
            member_name = member_tokens[0] + ' ' + member_tokens[-1]
            link = "http://cs.sehir.edu.tr" + a.find_all("a")[0]["href"].encode("utf-8")
            self.members[member_name] = FacultyMember(member_name,link)

    def fetch_member_publications(self):
	
        for name, obj in self.members.items():
            response = urllib2.urlopen(obj.webpage)
            html_doc = response.read()
            soup = BeautifulSoup(html_doc, "html.parser")
            pub_soup = soup.find_all(class_="tab-pane")
            for j in pub_soup[0].find_all("li"):
                pub = " ".join(re.findall("\S+", j.text.encode("utf-8"))[1:])
                obj.publication.append(pub)
        return self.members

    def fetch_projects(self):
	
        self.all_member = self.members.keys()
        response = urllib2.urlopen("http://cs.sehir.edu.tr/en/research/")
        html_doc = response.read()
        soup = BeautifulSoup(html_doc, "html.parser")
        project_soup = soup.find_all(class_="list-group-item")
		
        for a in project_soup:
            title = a.find("h4").text.strip().encode("utf-8")
            member = " ".join(a.find_all("p")[2].text.strip().encode("utf-8").split(" ")[-2:])
            summary = a.find_all("p")[4].text.strip().encode("utf-8")
            if member in self.members or member.startswith("Mehmet"):
                self.projects[title] = Project(title, summary, member)
        return self.projects

class Gui(Frame):
    def __init__(self,parent):
	
        self.parent = parent
        Frame.__init__(self,parent)
        self.fetcher = FetchData()
        self.initUI()

    def initUI(self):
	
        self.frame1 = Frame(self)
        self.frame1.pack(side=TOP, fill=BOTH, expand=TRUE)

        self.top_label = Label(self.frame1, text="PI Estimator Tool for SEHIR CS Projects", bg="#00A0AF", fg="white", font=("", "20", "bold"))
        self.top_label.pack(fill=BOTH,expand=TRUE)


        self.frame2 = Frame(self)
        self.frame2.pack(side=TOP, pady=15)

        self.url_entry1 = Entry(self.frame2, width=100,justify="center", font=("Helvetica", "10"))
        self.url_entry1.grid(row=0,column=0,padx=10)
        self.url_entry1.insert(END, "http://cs.sehir.edu.tr/en/people/")

        self.url_entry2 = Entry(self.frame2, width=100,justify="center", font=("Helvetica", "10"))
        self.url_entry2.grid(row=1, column=0,padx=10, pady=10)
        self.url_entry2.insert(END,"http://cs.sehir.edu.tr/en/research/")

        self.fetch_button = Button(self.frame2, text="    Fetch    ", font=("Helvetica", "10", "bold"))
        self.fetch_button.grid(row=2, column=0)
        self.fetch_button.configure(command=self.fetch)


        self.frame3 = Frame(self)
        self.frame3.pack(side=TOP)

        self.project_label = Label(self.frame3, text="Projects", font=("Helvetica", "18",))
        self.project_label.grid(row=0, column=0)

        self.project_listbox = Listbox(self.frame3, width=100, height=10)
        self.project_listbox.grid(row=1,column=0,pady=(0,50))
        self.project_listbox.bind("<<ListboxSelect>>", self.classify_member)

        self.scrollbar = Scrollbar(self.frame3, orient="vertical")
        self.scrollbar.config(command=self.project_listbox.yview)
        self.scrollbar.grid(row=1, column=1, sticky="NWES",pady=(0,50))

        self.project_listbox.config(yscrollcommand=self.scrollbar.set)

        self.prediction_text_label = Label(self.frame3, text="Prediction", font=("Helvetica", "18",))
        self.prediction_text_label.grid(row=0, column=2, padx=(50,0))

        self.prediction_label = Label(self.frame3, text="", font=("Helvetica", "18",))
        self.prediction_label.grid(row=1,column=2,padx=(50,0),pady=(0,50))

        self.pack(fill=BOTH, expand=TRUE)

    def fetch(self):
	
        self.fetcher.fetch_members()
        self.members = self.fetcher.fetch_member_publications()
        self.cl = docclass.naivebayes(docclass.getwords)
		
        for mem,obj in self.members.items():
            for pub in obj.publication:
                self.cl.train(pub, mem)
        self.projects = self.fetcher.fetch_projects()
		
        projects = self.projects.keys()
        projects.sort()
		
        for i in projects:
            self.project_listbox.insert(END, i)

    def classify_member(self, event):
	
        widget = event.widget
        index = int(widget.curselection()[0])
        title = widget.get(index)
        full_text = self.projects[title].merge()
        prediction = self.cl.classify(full_text)
        self.prediction_label.configure(text = prediction)
		
        if prediction == self.projects[title].investigator:
            #print "Prediction: " + prediction, "/ True: " + self.projects[title].investigator
            self.prediction_label.configure(bg="green")
        
        else:
            #print "Prediction: " + prediction, "/ True: "+ self.projects[title].investigator
            self.prediction_label.configure(bg="red")

def main():
    root = Tk()
    app = Gui(root)
    root.title("Classifier/Analysis Tool")
    root.geometry("1000x400+50+50")
    app.mainloop()

main()
