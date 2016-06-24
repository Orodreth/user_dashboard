from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        
        self.load_model("User")
        self.load_model("Message")
        self.load_model("Comment")
   
    def index(self):
        return self.load_view('index.html')

    def signin(self):
        return self.load_view("signin.html")

    def signin_process(self):
        info = {
            "email": request.form["email"],
            "pwd": request.form["pwd"]
        }
        result = self.models["User"].login_user(info)

        if not result["status"]:
            return redirect("/signin")

        session["user"] = result["user"]

        if result["user"]["is_admin"] == 1:
            return redirect("/dashboard/admin")
        
        return redirect("/dashboard")

    def register(self):
        return self.load_view("reg.html", from_admin = 0)

    def new(self):
        return self.load_view("reg.html", from_admin = 1)

    def register_process(self):
        user = {
            "email": request.form["email"],
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "pwd": request.form["pwd"],
            "pwd_confirm": request.form["pwd_confirm"]
        }
        result = self.models["User"].create_user(user)

        if not result["status"]:
            return redirect("/register")

        session["user"] = result["user"]

        if result["user"]["is_admin"] == 1:
            return redirect("/dashboard/admin")
        
        return redirect("/dashboard")

    def dashboard_admin(self):
        return self.load_view("dashboard.html", is_admin = 1, users = self.models["User"].get_all_users())

    def dashboard(self):
        return self.load_view("dashboard.html", is_admin = 0, users = self.models["User"].get_all_users())

    def remove(self, user_id):
        return redirect("/remove.html")

    def remove_process(self, user_id):
        self.models["Comment"].delete_comments_by_user_id(user_id)
        self.models["Message"].delete_messages_by_receiver_id(user_id)
        self.models["Message"].delete_messages_by_Sender_id(user_id)
        self.models["User"].delete_user_by_id(user_id)

        return redirect("/dashboard/admin")

    def edit_profile(self):
        return self.load_view("edit.html", user_id = 0, info = session["user"])

    def edit(self, user_id):
        info = self.models["User"].get_user_info(user_id)
        return self.load_view("edit.html", user_id = user_id, info = info)

    def edit_user_info(self, user_id):
        user_info = {
            "email": request.form["email"],
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "is_admin": request.form["is_admin"],
            "user_id": user_id
        }
        self.models["User"].update_user_info(user_info)

        return redirect("/")

    def edit_user_password(self, user_id):
        user_password = {
            "pwd": request.form["pwd"],
            "pwd_confirm": request.form["pwd_confirm"],
            "user_id": request.form["user_id"]
        }
        result = self.models["User"].update_user_password(user_password)

        return redirect("/")

    def edit_user_desc(self, user_id):
        user_desc = {
            "desc": request.form["desc"],
            "user_id": user_id
        }
        result = self.models["User"].update_user_desc(user_desc)

        return redirect("/")

    def show(self, user_id):
        receiver = self.models["User"].get_user_info(user_id)
        if receiver:
            messages = self.models["Message"].get_messages_by_receiver_id(receiver["id"])
            comments = self.models["Comment"].get_comments_by_messages(messages)

        return self.load_view("show.html", user = session["user"], receiver = receiver, messages = messages, comments = comments)

    def post_message(self, sender_id, receiver_id):
        message = {
            "message": request.form["message"],
            "sender_id": sender_id,
            "receiver_id": receiver_id
        }
        result = self.models["Message"].add_message(message)

        return redirect("/users/show/" + receiver_id)

    def post_comment(self, message_id, user_id):
        comment = {
            "comment": request.form["comment"],
            "user_id": user_id,
            "message_id": message_id
        }
        result = self.models["Comment"].add_comment(comment)

        return redirect("/users/show/" + user_id)

    