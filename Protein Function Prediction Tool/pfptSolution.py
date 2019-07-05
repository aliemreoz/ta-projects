from Tkinter import *
import tkFileDialog
from recommendations import *

class GO():
    """
        This class holds GO Term attributes.
    """
    def __init__(self, id, name=None):
        """
            :param id: String; GO Term ID
            :param name: String; GO Term Name
            :return: None
        """
        self.id = id
        self.name = name

class EvidenceCode():
    """
        This class holds Evidence Code attributes.
    """
    def __init__(self, acronym, numeric_value=0.0):
        """
            :param acronym: String; Evidence Code acronym
            :param numeric_value: Float; vidence Code numeric value
            :return: None
        """
        self.acronym = acronym
        self.numeric_value = numeric_value

class Annotation():
    """
        This class holds annotation of a protein attributes.
    """
    def __init__(self, functionality, evidence_code):
        """
            :param functionality : Object; GO term
            :param evidence_code: Object; Evidence Code Object
            :return: None
        """
        self.functionality = functionality
        self.evidence_code = evidence_code

class Protein():
    """
        This class holds protein attributes.
    """
    def __init__(self, id, name):
        """
            :param id: String; Protein ID
            :param name: String; Protein Name
            :param annotation: Dictionary; Protein's Annotation; {GO_id:evidence_code}
            :return: None
        """
        self.id = id
        self.name = name
        self.annotation = {}

class DataCenter():
    """
        This class is a container for data loading and manipulation.
    """

    def __init__(self):
        """
            :param proteins: Dictionary; a dictionary of all protein objects
            :param evidence_codes: Dictionary; a dictionary of all evidence code objects
            :param go_dict: Dictionary; a dictionary of all go attributes as id and name
            :param protein_map_dict: Dictionary; a dictionary of all protein attributes as id and name
            :param protein_map_reversed_dict: Dictionary; reversed version of protein_map_dict
            :param prefs: Dictionary; a nested dictionary for recommendations methods
            :return: None
        """
        self.proteins = {}
        self.evidence_codes = {}
        self.go_dict = {}
        self.protein_map_dict = {}
        self.protein_map_reversed_dict = {}
        self.prefs = {}

    def read_annotation_file(self, filename):
        """
            This function gets an annotation file path and process it.
            :param filename: String; Path to Annotation File.
            :return: None
        """
        read_file = open(filename, "r")

        lines = read_file.readlines()
        for i in lines:
            if i.startswith("!"):
                continue
            else:
                id = i.split("\t")[1]
                name = i.split("\t")[2]
                protein_object = Protein(id, name)
                self.proteins[protein_object.id] = protein_object
        for i in lines:
            if i.startswith("!"):
                continue
            else:
                id = i.split("\t")[1]
                annotation = i.split("\t")[4]
                experimental_code = i.split("\t")[6]
                annotation_object = Annotation(GO(annotation),EvidenceCode(experimental_code))

                temp_dict = {annotation_object.functionality.id : annotation_object}
                if annotation_object.functionality.id in self.proteins[id].annotation:
                    continue
                else:
                    self.proteins[id].annotation = dict(self.proteins[id].annotation.items() + temp_dict.items())

        #print self.proteins["CPX-1120"].annotation["GO:1902951"].evidence_code.acronym
    def read_go_file(self,filename):
        """
            This function gets an protein function file path and process it.
            :param filename: String; Path to go file.
            :return: None
        """
        read_file = open(filename, "r")

        lines = read_file.readlines()
        i = 0
        id = None
        name = None
        while i < len(lines):
            if i % 2 == 0:
                id = lines[i][4:].strip()
                name = lines[i+1][6:].strip()
            self.go_dict[id] = name
            i = i + 2
        for i in self.proteins.values():
            for j in i.annotation.values():
                j.functionality.name = self.go_dict[j.functionality.id]

    def read_ecv_file(self, filename):
        """
            This function gets an evidence code value file path and process it.
            :param filename: String; Path to evidence code value file.
            :return: None
        """
        read_file = open(filename, "r")

        lines = read_file.readlines()
        for i in lines:
            acronym = i.split("\t")[0]
            numeric_value = float(i.split("\t")[1].split("\n")[0])
            evidence_code_object = EvidenceCode(acronym, numeric_value)
            self.evidence_codes[acronym] = evidence_code_object

        for i in self.proteins.values():
            for j in i.annotation.values():
                j.evidence_code.numeric_value = self.evidence_codes[j.evidence_code.acronym].numeric_value

    def create_protein_map_dict(self,proteins):
        """
            This function gets an protein list and process it. Creates dictionary for protein id/name mapping.
            :param proteins: Dictionary; protein objects dictionary.
            :return: Dictionary; {'CPX-2544' : 'tgfb3-tgfbr1-tgfbr2_human'}
        """
        for i in proteins.values():
            self.protein_map_dict[i.id] = i.name
        return  self.protein_map_dict

    def create_protein_map_reversed_dict(self, proteins):
        """
            This function gets an protein list and process it. Creates dictionary for protein name/id mapping.
            :param proteins: Dictionary; protein objects dictionary.
            :return: Dictionary; {'tgfb3-tgfbr1-tgfbr2_human': 'CPX-2544'}
        """
        for i in proteins.values():
            self.protein_map_reversed_dict[i.name] = i.id
        return self.protein_map_reversed_dict

    def create_prefs_dict(self,proteins):
        """
           This function gets an protein list and process it.
           Creates dictionary for protein id/function/evidence code numeric value.
           :param proteins: Dictionary; protein objects dictionary.
           :return: Dictionary; ie. {'CPX-2544': {'GO:0007179': '5.0', 'GO:0005025': '5.0'}}
       """
        for i,j in proteins.items():
            temp_dict = j.annotation
            self.prefs.setdefault(j.id,{})
            for k,l in temp_dict.items():
                self.prefs[j.id][k] = l.evidence_code.numeric_value
        return self.prefs

class Gui(Frame):
    """
        This class is a container of GUI functions and widgets.
    """
    def __init__(self,parent):
        self.parent = parent
        Frame.__init__(self,parent)
        self.readData = DataCenter()
        self.initUI()

    def initUI(self):
        """
            Initialize user interface and place widgets here.
            :return: None
        """
        ### Frame 1 ###
        self.frame1 = Frame(self)
        self.frame1.pack(side=TOP, fill=BOTH, expand=TRUE)

        # Header Label #
        self.top_label = Label(self.frame1, text="Protein Function Prediction Tool", bg="lightgreen", fg="white", font=("", "20", "bold"))
        self.top_label.pack(fill=BOTH,expand=TRUE)

        ### Frame 2 ###
        self.frame2 = Frame(self)
        self.frame2.pack(side=TOP)

        # Upload Buttons #
        self.button_left = Button(self.frame2,text="Upload\nAnnotations",font=("Helvetica", "10", "bold"))
        self.button_left.pack(side=LEFT, pady=25)
        self.button_left.configure(command = self.upload_button_left)

        self.button_middle = Button(self.frame2, text="Upload Evidence\nCode Values", font=("Helvetica", "10", "bold"))
        self.button_middle.pack(side=LEFT, pady=25, padx=50)
        self.button_middle.configure(command= self.upload_button_middle)

        self.button_right = Button(self.frame2, text="Upload GO File", font=("Helvetica", "10", "bold"))
        self.button_right.pack(side=LEFT, pady=25)
        self.button_right.configure(command=self.upload_button_right)

        ### Frame 3
        self.frame3 = Frame(self)
        self.frame3.pack(side=TOP)

        # Frame3/Left - Label/Listbox #
        self.protein_label = Label(self.frame3, text="Proteins", font=("Helvetica", "10", "bold"))
        self.protein_label.grid(row=0,column=0)

        self.protein_listbox = Listbox(self.frame3, width=30, height=15)
        self.protein_listbox.grid(row=1, column=0, rowspan=4, sticky="NWES", pady=(0,25))
        self.protein_listbox.bind("<<ListboxSelect>>", self.calculate_score_listbox)

        self.scrollbar1 = Scrollbar(self.frame3, orient="vertical")
        self.scrollbar1.config(command=self.protein_listbox.yview)
        self.scrollbar1.grid(row=1, column=1, rowspan=4, sticky="NWES", pady=(0,25))

        self.protein_listbox.config(yscrollcommand=self.scrollbar1.set)

        # Frame3/Middle - Label/Frame/Radiobuttons #
        self.metric_label = Label(self.frame3, text="Similarity Metric", font=("Helvetica", "10", "bold"))
        self.metric_label.grid(row=0,column=2, padx=50)

        self.metric_frame= Frame(self.frame3, highlightbackground="black", highlightthickness=2)
        self.metric_frame.grid(row=1,column=2,rowspan=4,sticky="NWES", padx=50, pady=(0,25))

        self.var = StringVar()
        self.var.set("euclidean")

        self.pearson_checkbutton = Checkbutton(self.metric_frame,text="Pearson",width=15,variable=self.var,onvalue="pearson")
        self.pearson_checkbutton.pack(side=TOP,pady=(20,0))
        self.pearson_checkbutton.configure(command=self.calculate_score_checkbutton)

        self.euclidean_checkbutton = Checkbutton(self.metric_frame,text="Euclidean",width=15,variable=self.var,onvalue="euclidean")
        self.euclidean_checkbutton.pack(side=TOP)
        self.euclidean_checkbutton.configure(command=self.calculate_score_checkbutton)

        # Frame3/Right - Label/Listboxes #
        self.similar_label = Label(self.frame3, text="Similar Protein", font=("Helvetica", "10", "bold"))
        self.similar_label.grid(row=0, column=3)

        self.prediction_label = Label(self.frame3, text="Predicted Function", font=("Helvetica", "10", "bold"))
        self.prediction_label.grid(row=0,column=5)

        self.similar_listbox = Listbox(self.frame3, width=40, height=15)
        self.similar_listbox.grid(row=1, column=3, rowspan=4, sticky="NWES", pady=(0, 25))

        self.scrollbar2 = Scrollbar(self.frame3, orient="vertical")
        self.scrollbar2.config(command=self.similar_listbox.yview)
        self.scrollbar2.grid(row=1, column=4, rowspan=4, sticky="NWES", pady=(0, 25), padx= (0,15))

        self.similar_listbox.config(yscrollcommand=self.scrollbar2.set)

        self.prediction_listbox = Listbox(self.frame3, width=75, height=15)
        self.prediction_listbox.grid(row=1, column=5, rowspan=4, sticky="NWES", pady=(0, 25))

        self.scrollbar3 = Scrollbar(self.frame3, orient="vertical")
        self.scrollbar3.config(command=self.prediction_listbox.yview)
        self.scrollbar3.grid(row=1, column=6, rowspan=4, sticky="NWES", pady=(0, 25))

        self.prediction_listbox.config(yscrollcommand=self.scrollbar3.set)

        self.pack(fill=BOTH, expand=TRUE)

    def upload_button_left(self):
        """
            Upload Annotation button command. Opens file dialogue and calls data loading functions from ReadFile class.
            :return: None
        """

        self.annotation_file = tkFileDialog.askopenfilename(title="Select Annotation File",
                                                            filetypes = (("gaf files","*.gaf"),("All Files","*.*")))

        self.readData.read_annotation_file(self.annotation_file)

        self.protein_map_reversed_dict = self.readData.create_protein_map_reversed_dict(self.readData.proteins)
        self.protein_map_dict = self.readData.create_protein_map_dict(self.readData.proteins)

        for i in self.protein_map_reversed_dict.keys():
            self.protein_listbox.insert(END,i)

    def upload_button_middle(self):
        """
            Upload Evidence Code Values button command. Opens file dialogue and calls data loading functions from ReadFile class.
            :return: None
        """
        self.ecv_file = tkFileDialog.askopenfilename(title="Select Evidence Code Values File",
                                                     filetypes=(("txt files", "*.txt"), ("All Files", "*.*")))
        self.readData.read_ecv_file(self.ecv_file)

    def upload_button_right(self):
        """
            Upload GO File button command. Opens file dialogue and calls data loading functions from ReadFile class.
            :return: None
        """
        self.go_file = tkFileDialog.askopenfilename(title="Select GO File",
                                                    filetypes=(("obo files", "*.obo"), ("All Files", "*.*")))

        self.readData.read_go_file(self.go_file)
        self.prefs = self.readData.create_prefs_dict(self.readData.proteins)
        print self.prefs["CPX-1012"]
        # {"CPX-1012":{'GO:0030155': 5.0, 'GO:0030334': 5.0, 'GO:1903672': 5.0, 'GO:0062023': 5.0}}
    def calculate_score_listbox(self, event):
        """
            This function is for displaying data for listbox event.
            :param event: To catch listbox event.
            :return: None
        """

        self.prediction_listbox.delete(0,END)
        self.similar_listbox.delete(0, END)


        widget = event.widget
        index = int(widget.curselection()[0])
        protein = widget.get(index)
        protein_id = self.protein_map_reversed_dict[protein]
        score_list, similar_protein_list = self.metric(self.prefs, protein_id, 25)

        self.fill_listboxes(score_list, similar_protein_list)

    def calculate_score_checkbutton(self):
        """
            This function is for displaying data for checkbuttons. Data display on list boxes also handled here.
            :return: None
        """

        self.prediction_listbox.delete(0, END)
        self.similar_listbox.delete(0, END)


        widget = self.protein_listbox
        index = int(widget.curselection()[0])
        protein = widget.get(index)
        protein_id = self.protein_map_reversed_dict[protein]

        score_list, similar_protein_list = self.metric(self.prefs,protein_id,25)

        self.fill_listboxes(score_list, similar_protein_list)

    def metric(self, dict, id, n):
        """
            This function is calculation similar proteins and scores/functions. Calls recommendation methods.
            :param dict: Dictionary; prefs dict
            :param id: String; Protein ID
            :param n: Integer; Number of similar items
            :return: score_list; List; Functions/Score list
            :return: similar_proteins; List; Similar Protein list
        """
        if self.var.get() == "euclidean":
            self.score_list = getRecommendations(dict, id, sim_distance)
            self.similar_proteins = topMatches(dict, id, n, similarity=sim_distance)

        elif self.var.get() == "pearson":
            self.score_list = getRecommendations(dict, id, sim_pearson)
            self.similar_proteins = topMatches(dict, id, n, similarity=sim_pearson)

        else:
            raise Exception("Select metric!")

        return self.score_list, self.similar_proteins

    def fill_listboxes(self,score_list,similar_protein_list):
        """
            This function is for filling listboxes with final results.
            :param: score_list; List; Functions/Score list
            :param: similar_protein_list; List; Similar Protein list
            :return: None
        """

        for (score, id) in score_list:
            temp_str = str(score) + " - " + id + " - " + self.readData.go_dict[id]
            self.prediction_listbox.insert(END, temp_str)

        for (score, protein_id) in similar_protein_list:
            if score > 0.0:
                temp_str = str(score) + " - " + protein_id + " - " + self.protein_map_dict[protein_id]
                self.similar_listbox.insert(END, temp_str)

def main():
    root = Tk()
    App = Gui(root)
    root.title("Protein Function Prediction Tool")
    root.geometry("1200x450+50+50")
    App.mainloop()

main()