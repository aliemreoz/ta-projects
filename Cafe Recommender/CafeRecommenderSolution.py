__author__ = "aliemre"

from Tkinter import *
import ttk
from xlrd import *
import anydbm
import pickle
from recommendations import *
import tkFileDialog

class Rating:
    def __init__(self,cafe,score):
        self.cafe = cafe
        self.score = score

class User:
    def __init__(self,username):
        self.username = username
        self.ratings = {}


class CafeRecommender(Frame):

    """
    Main Class for program.
    Has method for GUI and Functionality.
    """

    def __init__(self, parent):

        Frame.__init__(self, parent)
        self.parent = parent

        self.main_user = User("user")
        self.user_rated_cafe_dict = self.main_user.ratings


        self.color_for_recommend = "red"
        self.color_for_rating = "pink"

        self.init_ui()


    def init_ui(self):

        #################################################################################################

        # First Part of the top of the GUI
        # 1 widget : App Name Label

        self.frame_top1 = Frame(self,
                                bg="light green",
                                highlightbackground="black",
                                highlightthickness=2)

        self.frame_top1.pack(side=TOP,
                             fill=BOTH)


        self.app_label = Label(text="CAFE RECOMMENDER",
                               bg='light green',
                               fg='red',
                               font='helvetica 25',
                               height=2)

        self.app_label.pack(in_=self.frame_top1,
                            fill=X)

        #################################################################################################

        # Second Part of the top of the GUI
        # 2 widget : Upload Cafe Button, Upload Rating Button

        self.frame_top2 = Frame(self,
                               bg="light green",
                               highlightbackground="black",
                               highlightthickness=2)

        self.frame_top2.pack(side=TOP,
                            fill=BOTH,
                            ipady=15)


        self.upload_cafe_data = Button(text="Upload Cafe Data",
                                       height=3,
                                       width=20,
                                       bg="red",
                                       font="Helvetica 10 bold",
                                       fg="white")

        self.upload_cafe_data.configure(command=self.get_cafe_list_func)

        self.upload_cafe_data.pack(in_=self.frame_top2,
                                   side=LEFT,
                                   padx=160)


        self.upload_rating_data = Button(text="Upload Ratings",
                                         height=3,
                                         width=20,
                                         bg="red",
                                         font="Helvetica 10 bold",
                                         fg="white")

        self.upload_rating_data.configure(command=self.get_rating_dict_func)

        self.upload_rating_data.pack(in_=self.frame_top2,
                                     side=RIGHT,
                                     padx=160)

        #################################################################################################

        # Left side of the GUI
        # 2 widget : Rating Button, Recommend Button

        self.frame_bottom_left = Frame(self,
                                       bg="light green",
                                       highlightbackground="black",
                                       highlightthickness=2)

        self.frame_bottom_left.pack(side=LEFT,
                                    fill=BOTH,
                                    ipadx=15)


        self.rating_button = Button(text="RATING",
                                    wraplength=1,
                                    width=6,
                                    height=10,
                                    bg="pink",
                                    font="Helvetica 8 bold",
                                    fg="white",
                                    relief=SUNKEN)

        self.rating_button.configure(command=self.switch_rating)

        self.rating_button.pack(in_=self.frame_bottom_left,
                                side=TOP,
                                pady=10)


        self.recommend_button = Button(text="RECOMMEND",
                                       wraplength=1,
                                       width=6,
                                       height=10,
                                       bg="red",
                                       font="Helvetica 8 bold",
                                       fg="white",
                                       relief=RAISED)

        self.recommend_button.configure(command=self.switch_recommendation)

        self.recommend_button.pack(in_=self.frame_bottom_left,
                                   side=BOTTOM,
                                   pady=10)

        #################################################################################################

        # Left Part of the Main GUI, for Rating
        # 5 widget : Choose Cafe Label, Cafe Combobox, Choose Rating Label, Slider, Add Button

        self.frame_rate_left = Frame(self,
                                     bg="light green",
                                     highlightbackground="black",
                                     highlightthickness=2)

        self.frame_rate_left.pack(side=LEFT,
                                  fill=BOTH,
                                  ipadx=20)


        self.choose_cafe_label = Label(text="Choose Cafe",
                                       bg="light green",
                                       fg='black',
                                       font="Helvetica 25")

        self.choose_cafe_label.pack(in_=self.frame_rate_left,
                                    side=TOP,
                                    pady=30)


        self.cafe_list = StringVar()

        self.cafe_combobox = ttk.Combobox(width=45,
                                          font="Helvetica 10",
                                          textvariable=self.cafe_list,
                                          state="readonly")

        self.cafe_combobox.bind("<FocusIn>", self.defocus) ### Not Necessary, just for visualisation

        self.cafe_combobox.pack(in_=self.frame_rate_left,
                                side=TOP)


        self.choose_rating_label = Label(text="Choose Rating",
                                         bg="light green",
                                         fg='black',
                                         font="Helvetica 25")

        self.choose_rating_label.pack(in_=self.frame_rate_left,
                                      side=TOP,
                                      pady=30)


        self.slider = Scale(from_=1,
                            to=10,
                            length=350,
                            orient=HORIZONTAL,
                            font="Helvetica 15",
                            bg="light green",
                            highlightbackground="light green",
                            troughcolor = "white")

        self.slider.pack(in_=self.frame_rate_left,
                         side=TOP)


        self.add_cafe_button = Button(text="ADD",
                                      height=5,
                                      width=15,
                                      bg="red",
                                      font="Helvetica 10 bold",
                                      fg="white")

        self.add_cafe_button.configure(command=self.add_rating_func)

        self.add_cafe_button.pack(in_=self.frame_rate_left,
                                  side=TOP,
                                  pady=40)

        #################################################################################################

        # Right Part of the Main GUI, for Rating
        # 2 widget : User-Rated Cafes TreeView, Remove Button

        self.frame_rate_right = Frame(self,
                                      bg="light green",
                                      width=738,
                                      highlightbackground="black",
                                      highlightthickness=2)

        self.frame_rate_right.pack(side=LEFT,
                                   fill=BOTH)


        self.user_rated_cafe_widget = ttk.Treeview(height=25)
        self.user_rated_cafe_widget["columns"] = ("n", "s")
        self.user_rated_cafe_widget.column("n", width=200)
        self.user_rated_cafe_widget.column("s", width=100)
        self.user_rated_cafe_widget.heading("n", text="Cafe")
        self.user_rated_cafe_widget.heading("s", text="Rating")
        self.user_rated_cafe_widget['show'] = 'headings'

        self.user_rated_cafe_widget.pack(in_=self.frame_rate_right,
                                         padx=25,
                                         pady=20,
                                         side=LEFT)


        self.remove_cafe_button = Button(text="REMOVE",
                                         height=3,
                                         width=25,
                                         bg="red",
                                         font="Helvetica 10 bold",
                                         fg="white")

        self.remove_cafe_button.configure(command=self.remove_rating_func)

        self.remove_cafe_button.pack(in_=self.frame_rate_right,
                                     side=LEFT,
                                     padx=10)

        #################################################################################################

        # Left Part of the Main GUI, for Recommendation
        # Divided Into two Frame for Better Layout : frame_recommend_left1, frame_recommend_left2
        # 9 widget : Settings Label, Num. of Recommendation Label, Num. of Recommendation Entry,
        #            Similarity Metrics Label, Euclidean CheckButton, Pearson CheckButton,
        #            Jaccard CheckButton, Recommend Similar User Button, Recommend Similar Cafe Button

        self.frame_recommend_left = Frame(self,
                                          bg="light green",
                                          highlightbackground="black",
                                          highlightthickness=2)

        self.frame_recommend_left.pack(in_=self,
                                       side=LEFT,
                                       fill=BOTH)


        self.frame_recommend_left1 = Frame(self,
                                           bg="light green")

        self.frame_recommend_left1.pack(in_=self.frame_recommend_left,
                                        side=LEFT,
                                        fill=BOTH,
                                        padx=5)


        self.frame_recommend_left2 = Frame(self,
                                           bg="light green")

        self.frame_recommend_left2.pack(in_=self.frame_recommend_left,
                                        side=LEFT,
                                        fill=BOTH)


        self.settings_label = Label(text=" Settings ",
                                    bg="light green",
                                    fg='black',
                                    font="Helvetica 25 underline")

        self.settings_label.pack(in_=self.frame_recommend_left1,
                                 side=TOP,
                                 pady=10)


        self.number_of_rec_label = Label(text="Number of Recommendation",
                                         bg="light green",
                                         fg='black',
                                         font="Helvetica 15")

        self.number_of_rec_label.pack(in_=self.frame_recommend_left1,
                                      side=TOP,
                                      pady=10)


        self.number_of_rec_entry = Entry(width=5,
                                         font="Helvetica 15")

        self.number_of_rec_entry.pack(in_=self.frame_recommend_left1,
                                      side=TOP)


        self.empty_label = Label(text="", bg="light green")

        self.empty_label.pack(in_=self.frame_recommend_left1,
                              side=TOP,
                              pady=30)


        self.similarity_metrics_label = Label(text="Similarity Metrics",
                                              bg="light green",
                                              fg='black',
                                              font="Helvetica 15")

        self.similarity_metrics_label.pack(in_=self.frame_recommend_left1,
                                           side=TOP,
                                           pady=10)

        self.var = StringVar()
        self.var.set('None')


        self.euclidean_button = Checkbutton(bg="light green",
                                            text='Euclidean',
                                            font="Helvetica 11",
                                            variable=self.var,
                                            onvalue='Euclidean')

        self.euclidean_button.pack(in_=self.frame_recommend_left1,
                                   side=TOP)


        self.pearson_button = Checkbutton(bg="light green",
                                          text='Pearson',
                                          font="Helvetica 11",
                                          variable=self.var,
                                          onvalue='Pearson')

        self.pearson_button.pack(in_=self.frame_recommend_left1,
                                 side=TOP)


        self.jaccard_button = Checkbutton(bg="light green",
                                          text='Jaccard',
                                          font="Helvetica 11",
                                          variable=self.var,
                                          onvalue='Jaccard')

        self.jaccard_button.pack(in_=self.frame_recommend_left1,
                                 side=TOP)

        self.empty_label3 = Label(text="",
                                  bg="light green")

        self.empty_label3.pack(in_=self.frame_recommend_left1,
                               side=TOP,
                               pady=25)

        self.empty_label2 = Label(text="",
                                  bg="light green")

        self.empty_label2.pack(in_=self.frame_recommend_left2,
                               side=TOP,
                               pady=50)


        self.recommend_user_button = Button(text="Recommend Similar User",
                                            wraplength=120,
                                            font="Helvetica 12",
                                            bg="red",
                                            fg="white")

        self.recommend_user_button.configure(command=self.recommend_similar_user_func)

        self.recommend_user_button.pack(in_=self.frame_recommend_left2,
                                        side=TOP,
                                        pady=20)


        self.recommend_cafe_button = Button(text="Recommend Cafe",
                                            wraplength=120,
                                            font="Helvetica 12",
                                            bg="red",
                                            fg="white")

        self.recommend_cafe_button.configure(command=self.recommend_similar_cafe_func)

        self.recommend_cafe_button.pack(in_=self.frame_recommend_left2,
                                        side=TOP)

        #################################################################################################

        # Right Part of the Main GUI, for Recommendation
        # Divided Into two Frame for Button Functionality : frame_recommend_right_cafe, frame_recommend_right_user
        # 2 widget in Similiar Cafe: Similiar Cafes Label, Similiar Cafes TreeView
        # 5 widget in Similiar User: Similiar User Label, Similiar User TreeView, Get User's Rating Button
        #                            Username Label, User's Ratings TreeView

        self.frame_recommend_right = Frame(self,
                                           bg="light green",
                                           width=750,
                                           highlightbackground="black",
                                           highlightthickness=2)

        self.frame_recommend_right.pack(side=LEFT,
                                        fill=BOTH)


        self.frame_recommend_right_cafe = Frame(self,
                                                bg="light green")


        self.similiar_cafe_label = Label(text="Similiar Cafes",
                                         bg="light green",
                                         fg='black',
                                         font="Helvetica 15")

        self.similiar_cafe_label.pack(in_=self.frame_recommend_right_cafe,
                                      side=TOP,
                                      pady=10)


        self.similiar_cafe_widget = ttk.Treeview(height=15)
        self.similiar_cafe_widget["columns"] = ('n', "s",)
        self.similiar_cafe_widget.column("n", width=175)
        self.similiar_cafe_widget.column("s", width=125)
        self.similiar_cafe_widget.heading("n", text="Cafe")
        self.similiar_cafe_widget.heading("s", text="Similarity")
        self.similiar_cafe_widget['show'] = 'headings'

        self.similiar_cafe_widget.pack(in_=self.frame_recommend_right_cafe,
                                       side=TOP)


        self.frame_recommend_right_user = Frame(self,
                                                bg="light green")


        self.similiar_user_label = Label(text="Similiar User",
                                         bg="light green",
                                         fg='black',
                                         font="Helvetica 15")

        self.similiar_user_label.pack(in_=self.frame_recommend_right_user,
                                      side=TOP,
                                      pady=10)


        self.similiar_user_widget = ttk.Treeview(height=6)
        self.similiar_user_widget["columns"] = ('n', "s",)
        self.similiar_user_widget.column("n", width=175)
        self.similiar_user_widget.column("s", width=125)
        self.similiar_user_widget.heading("n", text="User")
        self.similiar_user_widget.heading("s", text="Similarity")
        self.similiar_user_widget['show'] = 'headings'

        self.similiar_user_widget.pack(in_=self.frame_recommend_right_user,
                                       side=TOP)


        self.get_user_rating_button = Button(text="Get User's Rating",
                                             font="Helvetica 9")

        self.get_user_rating_button.configure(command=self.get_users_rating_func)

        self.get_user_rating_button.pack(in_=self.frame_recommend_right_user,
                                         side=TOP,
                                         pady=10)


        self.username_label = Label(text="Select user the see him/her rating.",
                                    bg="light green",
                                    fg='black',
                                    font="Helvetica 9")

        self.username_label.pack(in_=self.frame_recommend_right_user,
                                 side=TOP)


        self.similiar_user_rating_widget = ttk.Treeview(height=6)
        self.similiar_user_rating_widget["columns"] = ('n', "s",)
        self.similiar_user_rating_widget.column("n", width=175)
        self.similiar_user_rating_widget.column("s", width=125)
        self.similiar_user_rating_widget.heading("n", text="Cafe")
        self.similiar_user_rating_widget.heading("s", text="Rating")
        self.similiar_user_rating_widget['show'] = 'headings'


        self.similiar_user_rating_widget.pack(in_=self.frame_recommend_right_user, side=TOP)

        #################################################################################################

        self.rating_button.bind("<Enter>", self.on_enter_rating)
        self.rating_button.bind("<Leave>", self.on_leave_rating)

        self.recommend_button.bind("<Enter>", self.on_enter_recommend)
        self.recommend_button.bind("<Leave>", self.on_leave_recommend)

        #################################################################################################

        self.pack(fill=BOTH)


    def get_cafe_list_func(self):
        """
        Import Cafe List button command. Opens file dialogue and calls excel loading functions.
        :return: None
        """
        fname = tkFileDialog.askopenfilename(filetypes=(("Template files", "*.xlsx"), ("All files", "*")))
        try:
            cafes = open_workbook(fname, "rb").sheet_by_index(0)
            cafe_list = []
            for column in range(1):
                for row in range(37):
                    a = cafes.cell(row + 1, column).value
                    cafe_list.append(a)
            self.cafe_combobox["values"] = cafe_list

        except:
            raise Exception('Please select a file.')


    def get_rating_dict_func(self):
        """
        Import Rating Database button command. Opens file dialogue and calls db loading functions.
        :return: None
        """
        fname = tkFileDialog.askopenfilename(filetypes=(("Template files", "*.db"), ("All files", "*")))

        try:
            self.users_rating_dict = {}
            self.cafe_rating_db = anydbm.open(fname, "c")
            for i,j in self.cafe_rating_db.items():
                self.users_rating_dict[i]=pickle.loads(j)
        except:
            raise Exception('Please select a file.')


    def switch_rating(self):
        """
        This function for switching between frames.
        Changes the color for buttons.
        Forget recommedation frames.
        Change the style of buttons.
        Calls rating frame.
        :return: None
        """
        self.color_for_rating = "pink"
        self.color_for_recommend = "red"
        self.frame_recommend_left.pack_forget()
        self.frame_recommend_right.pack_forget()
        self.rating_button.configure(bg=self.color_for_rating,relief=SUNKEN)
        self.recommend_button.configure(bg=self.color_for_recommend,relief=RAISED)
        self.frame_rate_left.pack(side=LEFT, fill=BOTH, ipadx=48)
        self.frame_rate_right.pack(side=LEFT, fill=BOTH)


    def switch_recommendation(self):
        """
        This function for switching between frames.
        Changes the color for buttons.
        Forget rating frames.
        Change the style of buttons.
        Calls recommendation frame.
        :return: None
        """
        self.color_for_recommend = "pink"
        self.color_for_rating = "red"
        self.frame_rate_left.pack_forget()
        self.frame_rate_right.pack_forget()
        self.recommend_button.configure(bg=self.color_for_recommend, relief=SUNKEN)
        self.rating_button.configure(bg=self.color_for_rating, relief=RAISED)
        self.frame_recommend_left.pack(side=LEFT, fill=BOTH, ipadx=48)
        self.frame_recommend_right.pack(side=LEFT, fill=BOTH)


    def add_rating_func(self):
        """
        This function for adding cafe and rating to TreeView.
        Get the selected cafe from ComboBox widget
        Get the rating from slider
        Add them in TreeView
        Add them in dict
        :return: None
        """
        self.selected_cafe = self.cafe_combobox.get()
        self.selected_rating = self.slider.get()
        self.rating_object = Rating(self.selected_cafe,self.selected_rating)
        if self.selected_cafe != "":
            self.user_rated_cafe_widget.insert('', "end", text='Line 1', values=(self.rating_object.cafe, self.rating_object.score))
            self.user_rated_cafe_dict[self.rating_object.cafe] = self.rating_object.score
        else:
            raise Exception("Please select a cafe.")


    def remove_rating_func(self):
        """
        This function for removing cafe and rating from TreeView.
        Get the selected rated cafe from TreeView widget
        Delete it from widget by index
        Delete it from dict by item
        :return: None
        """
        try:
            self.selected_rated_cafe_index = self.user_rated_cafe_widget.focus()
            self.selected_rated_cafe = self.user_rated_cafe_widget.item(self.selected_rated_cafe_index)["values"][0]
            self.user_rated_cafe_widget.delete(self.selected_rated_cafe_index)
            del self.user_rated_cafe_dict[self.selected_rated_cafe]
        except:
            raise Exception("Please select a cafe for deletion.")


    def recommend_similar_cafe_func(self):
        """
        This function for recommending similiar cafe based on user's ratings about cafes. Uses recommendation functions.
        First delete the previous data if exist.
        Then layout the proper frame.
        Get the num. of recommendation from entry widget.
        Get similarity metrics from checkbutton widget.
        Create dict and add main user's rating to that dict.
        Concatenate that dict and db_dict
        Based on metric selection and that last dict do some computation and creates recommendation
        Add recommendation to TreeView
        :return: None
        """
        try:
            self.username_label.configure(text="Select user the see him/her rating.")
            self.number_of_recommendation = int(self.number_of_rec_entry.get())
            self.similarity_metrics = self.var.get()
            self.similiar_cafe_widget.delete(*self.similiar_cafe_widget.get_children())
            self.frame_recommend_right_user.pack_forget()
            self.frame_recommend_right_cafe.pack(in_=self.frame_recommend_right, fill=BOTH ,ipadx=170)
            self.user_ratings_dict = {}
            self.user_ratings_dict[self.main_user.username] = self.user_rated_cafe_dict

            self.all_rating_dict = dict(self.user_ratings_dict.items() + self.users_rating_dict.items())

            if self.similarity_metrics == "Euclidean":
                self.similiar_cafe_list = getRecommendations(self.all_rating_dict, self.main_user.username,
                                                  similarity=sim_distance)
            elif self.similarity_metrics == "Pearson":
                self.similiar_cafe_list = getRecommendations(self.all_rating_dict, self.main_user.username,
                                                  similarity=sim_pearson)
            elif self.similarity_metrics == "Jaccard":
                self.similiar_cafe_list = getRecommendations(self.all_rating_dict, self.main_user.username,
                                                  similarity=sim_jaccard)
            else:
                print "Select similarity metric."

            for i in self.similiar_cafe_list[0:self.number_of_recommendation]:
                self.similiar_cafe_widget.insert("","end",text="Line 1",values=(i[1],i[0]))
        except:
            raise Exception("Please select number of recommendations/metrics")

    def recommend_similar_user_func(self):
        """
        This function for recommending similiar users based on user's ratings about cafes. Uses recommendation functions.
        First delete the previous data if exist.
        Then layout the proper frame.
        Get the num. of recommendation from entry widget.
        Get similarity metrics from checkbutton widget.
        Create dict and add main user's rating to that dict.
        Concatenate that dict and db_dict
        Based on metric selection and that last dict do some computation and creates recommendation
        Add recommendation to TreeView
        :return: None
        """
        try:
            self.number_of_recommendation = int(self.number_of_rec_entry.get())
            self.similarity_metrics = self.var.get()
            self.similiar_user_rating_widget.delete(*self.similiar_user_rating_widget.get_children())
            self.similiar_user_widget.delete(*self.similiar_user_widget.get_children())
            self.frame_recommend_right_cafe.pack_forget()
            self.frame_recommend_right_user.pack(in_=self.frame_recommend_right, fill=BOTH, ipadx=170)

            self.number_of_recommendation = int(self.number_of_rec_entry.get())
            self.similarity_metrics = self.var.get()
            self.user_ratings_dict = {}
            self.user_ratings_dict[self.main_user.username] = self.user_rated_cafe_dict

            self.all_rating_dict = dict(self.user_ratings_dict.items() + self.users_rating_dict.items())

            if self.similarity_metrics == "Euclidean":
                self.similiar_user_list = topMatches(self.all_rating_dict, self.main_user.username,
                                                     n=self.number_of_recommendation, similarity=sim_distance)
            elif self.similarity_metrics == "Pearson":
                self.similiar_user_list = topMatches(self.all_rating_dict, self.main_user.username,
                                                     n=self.number_of_recommendation, similarity=sim_pearson)
            elif self.similarity_metrics == "Jaccard":
                self.similiar_user_list = topMatches(self.all_rating_dict, self.main_user.username,
                                                     n=self.number_of_recommendation, similarity=sim_jaccard)
            else:
                print "Select similarity metric."

            for i in self.similiar_user_list:
                self.similiar_user_widget.insert("", "end", text="Line 1", values=(i[1], i[0]))
        except:
            raise Exception("Please select number of recommendations/metrics")




    def get_users_rating_func(self):
        """
        This function for getting similiar user's ratings about cafes. Uses recommendation functions.
        First delete the previous data if exist on widget.
        Then get the selected user and find that user's rating from dictionary.
        Set the label with selected user's name
        Add rated cafes of selected user's to the widget
        :return: None
        """
        self.similiar_user_rating_widget.delete(*self.similiar_user_rating_widget.get_children())
        self.selected_user_index = self.similiar_user_widget.focus()
        self.selected_user = self.similiar_user_widget.item(self.selected_user_index)["values"][0]
        self.selected_user_rating = self.all_rating_dict[self.selected_user]
        self.username_label.configure(text=str(self.selected_user)+"'s Rating")
        for i,j in self.selected_user_rating.items():
            self.similiar_user_rating_widget.insert("", "end", text="Line 1", values=(i, j))


    def on_enter_rating(self, e):
        """
        This function for catching mouse event on Switch Rating Button.
        :param event: To catch mouse event.
        :return: None
        """
        self.rating_button['background'] = 'orange'


    def on_leave_rating(self, e):
        """
        This function for catching mouse event on Switch Rating Button.
        :param event: To catch mouse event.
        :return: None
        """
        self.rating_button['background'] = self.color_for_rating


    def on_enter_recommend(self, e):
        """
        This function for catching mouse event on Switch Recommend Button.
        :param event: To catch mouse event.
        :return: None
        """
        self.recommend_button['background'] = 'orange'


    def on_leave_recommend(self, e):
        """
        This function for catching mouse event on Switch Recommend Button.
        :param event: To catch mouse event.
        :return: None
        """
        self.recommend_button['background'] = self.color_for_recommend


    ### Not Necessary, just for visualisation about ComboBox
    def defocus(self,event):
        event.widget.master.focus_set()

def main():
    root = Tk()
    root.title("Cafe Recommender 1.0")
    root.geometry("1000x600")
    root.resizable(width=FALSE, height=FALSE)
    app = CafeRecommender(root)
    root.mainloop()

main()