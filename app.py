from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_mail import Mail, Message
from account_form import (
    CreateUserForm,
    CreateLoginForm,
    ChangePasswordForm,
    ForgotPasswordForm,
)
from classes.contactUs import contactUs
from contact_form import CreateCustomerContactForm
import shelve, uuid
from classes.customer import Customer
from chat import get_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    login_user,
    LoginManager,
    login_required,
    current_user,
    logout_user,
)
import random
from staff_pages import staff_blueprint
from datetime import datetime
from classes.shoppingBag import shoppingBag, ThaiMilkTea, BlackPearlTea, ThaiBubbleTea
from checkout_form import CreateCheckoutForm
import smtplib, ssl


app = Flask(__name__)
app.config["SECRET_KEY"] = "thisisakey"

app.register_blueprint(staff_blueprint)


# Header
@app.route("/")
def home():
    if current_user.is_authenticated:
        if current_user.get_user_type()=='staff':
            return redirect(url_for('staff.staff_home'))
    return render_template("home.html")


# @app.get("/")
# def index_get():
#     return render_template("base.html")


# Javerine: Term and Condition Page
@app.route("/termsandcondition")
def tandc():
    return render_template("termsandcondition.html")


# Javerine Feedback Main Page
@app.route("/feedback")
def feedback():
    return render_template("Feedback.html")


# Javerine Generic Feedback Form
@app.route("/generic-feedback", methods=["GET", "POST"])
def generic_feedback():
    return render_template("GenericFeedback.html")


# Javerine: Contact us form
# Javerine: Send the mail server
mail = Mail(app)
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "buyfrompytea@gmail.com"
app.config["MAIL_PASSWORD"] = "wqwivbbqjrqkhlkf"  # this is auto-generated. it can check your IP address if you use it, so do not use it!
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True

mail = Mail(app)

@app.route("/contact-us", methods=["GET", "POST"])
def contact():
    create_contactUs_form = CreateCustomerContactForm(request.form)
    if request.method == "POST" and create_contactUs_form.validate():
        feedback_dict = {}  # just incase the feedback dictionary is empty
        db = shelve.open("storage.db", "c")
        try:
            feedback_dict = db["Feedback"]
        except:
            print("Error in retrieving Users from storage.db")

        first_name = create_contactUs_form.first_name.data
        last_name = create_contactUs_form.last_name.data
        email = create_contactUs_form.email.data
        salutation = create_contactUs_form.salutation.data
        comment = create_contactUs_form.feedback.data
        # submission_time = create_contactUs_form.date.data
        submission_time = datetime.today()

        feedback = contactUs(
            first_name, last_name, email, salutation, comment
        )  # create feedback object
        print(submission_time)
        feedback.set_time(submission_time)

        # give unique id
        feedback_id = random.randint(5000, 9999)
        for sent in feedback_dict.values():
            if sent.get_user_id() == str(feedback_id):
                feedback_id = random.randint(5000, 9999)
        feedback.set_user_id(feedback_id)

        # store back the feedback into the shelve
        feedback_dict[feedback.get_user_id()] = feedback
        db["Feedback"] = feedback_dict

        db.close()
        # test code
        # feedback_contactus_dict = db['Feedback']
        # feedback = feedback_contactus_dict[feedback_id]
        # print(feedback.get_first_name(), feedback.get_last_name(), "was stored in storage.db successfully wit user_id ==", feedback.get_user_id(), " feedback", feedback.get_feedback())

        # send confirmation email
        with app.open_resource("static/images/logo-clear.png", "rb") as img:
            image_data = img.read()

        msg = Message(
            f"PyTea Feedback Form, Case No {feedback_id} ",
            sender="buyfrompytea@gmail.com",
            recipients=[email],
        )
        msg.attach(
            filename="static/images/logo-clear.png",
            content_type="image/png",
            data=image_data,
        )
        msg.body = (
            f"Dear {salutation} {first_name},\n"
            f"\nOn behalf of the entire PyTea team, I wanted to extend our heartfelt thanks for taking the time to submit the feedback form."
            f"Our staff will get back to you in 1-2 days regarding your feedback.\n"
            f"\nYou have asked about:\n"
            f"{comment}\n"
            f"\nBest Regards,\n"
            f"Javerine\n"
            f"PyTea Customer Support"
        )

        mail.send(msg)

        return redirect(url_for("submitted"))

    return render_template("contact_us.html", form=create_contactUs_form)



# Javerine: Confirmation page and sending email
@app.route("/thankyoupage")
def submitted():
    return render_template("thankyoupage.html")


# Javerine:  Chatbot
@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    # TODO: check if text is valid
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)


@app.route("/submitted", methods=["POST"])
def submit():
    # Handle form submission here, you can process the form data if needed
    # Then redirect to the thank you page
    return render_template("thankyoupage.html")


# Amber : login and Sign up

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    db = shelve.open("storage.db", "c")
    user_dict = db["Users"]
    account = None
    for user in user_dict.values():
        account = user
        if user.get_id() == user_id:
            break
    return account


@app.route("/login", methods=["GET", "POST"])
def login():
    # can remove this but this is to stop ppl from going in after logging in
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    else:
        create_login_form = CreateLoginForm(request.form)
        if request.method == "POST" and create_login_form.validate():
            db = shelve.open("storage.db", "r")

            try:
                users_dict = db["Users"]
            except:
                print("Error in retrieving Users from storage.db.")

            if create_login_form.email.data.lower() not in users_dict:
                flash("Unregistered Email. Please sign up first !")
                return redirect(url_for("signup"))

            else:
                user = users_dict[create_login_form.email.data.lower()]
                if check_password_hash(
                    user.get_password(), create_login_form.password.data
                ):
                    "sucessful"
                    login_user(user, remember=True)
                    if current_user.get_user_type() == "customer":
                        return redirect(url_for("home"))
                    else:
                        return redirect(url_for("staff.staff_home"))
                else:
                    "unsuccessful"
                    flash("Incorrect password! Try Again")

                db.close()
    return render_template("login.html", form=create_login_form)


@app.route("/sign-up", methods=["GET", "POST"])
def signup():
    create_user_form = CreateUserForm(request.form)
    if request.method == "POST" and create_user_form.validate():
        users_dict = {}
        db = shelve.open("storage.db", "c")
        try:
            if "Users" in db:
                users_dict = db["Users"]
            else:
                db["Users"] = users_dict
        except:
            print("Error in retrieving Users from storage.db.")

        if create_user_form.email.data.lower() in users_dict:
            flash("You have entered a registed email.")

        else:
            user = Customer(
                create_user_form.name.data,
                create_user_form.email.data.lower(),
                create_user_form.birth_month.data,
                generate_password_hash(create_user_form.password.data),
            )

            customer_id = random.randint(10, 4999)
            for customer in users_dict.values():
                if customer.get_id() == str(customer_id):
                    customer_id = random.randint(10, 4999)
            user.set_user_id(str(customer_id))

            users_dict[user.get_email()] = user
            db["Users"] = users_dict

            db.close()
            return redirect(url_for("login"))
    return render_template("signup.html", form=create_user_form)


@app.route("/user-settings")
@login_required
def u_settings():
    if current_user.get_user_type() == "customer":
        update_password_form = ChangePasswordForm(request.form)
        order_dict={}
        db = shelve.open("storage.db", "w")
        try:
            order_dict = db["Orders"]
        except:
            print("Error opening database!")
        order_list=[]
        points=0
        for order in order_dict.values():
            if order.get_user_email()==current_user.get_email():
                order_list.append(order)
                for drink in order.get_order().values():
                    points+=drink.get_total_cost()
                    
        sorting_key = lambda obj: datetime.strptime(str(obj.get_date()), "%Y-%m-%d %H:%M:%S.%f")
        order_list.sort(key=sorting_key, reverse=True)
        
        user_dict = db["Users"]
        user=user_dict[current_user.get_email()]
        if user.get_points != points:
            user.set_points(points)
            db["Users"]=user_dict
        

        db.close()

        return render_template("customersettings.html", form=update_password_form, order_list=order_list, count=len(order_list))

    return redirect(url_for("home"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error404.html"), 404


# @app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
# def update_user(id):
#     update_user_form = ChangePasswordForm(request.form)
#     if request.method == 'POST' and update_user_form.validate():
#         email = current_user.get_email()
#         users_dict = {}
#         db = shelve.open('storage.db', 'w')
#         users_dict = db['Users']

#         user = users_dict.get(email)
#         user.set_password(generate_password_hash(update_user_form.password.data))
#         print(update_user_form.password.data)

#         db['Users'] = users_dict
#         db.close()

#         return redirect(url_for('home'))

#     return render_template('change_password.html', form=update_user_form)


@app.route("/edit-settings/<int:id>/", methods=["GET", "POST"])
def edit_settings(id):
    update_settings = request.form
    if request.method == "POST":
        email = current_user.get_email()
        users_dict = {}
        db = shelve.open("storage.db", "w")
        users_dict = db["Users"]
        user = users_dict.get(email)
        if id == 1:
            try:
                user.set_name(update_settings.get("name"))
                flash('Name Changed', category='success')
            except:
                flash('Error changing name', category='error')
        if id == 2:
            try:
                user.set_address(update_settings.get("address"))
                flash('Address Changed', category='success')
            except:
                flash('Error changing address', category='error')
        if id == 3:
            try:
                user.set_postal_code(update_settings.get("postal_code"))
                flash('Postal Code Changed', category='success')
            except:
                flash('Error changing postal code', category='error')
        elif id == 4:
            try:
                user.set_password(generate_password_hash(update_settings.get("password")))
                flash('Password Changed', category='success')
            except:
                flash('Error changing password', category='error')

        db["Users"] = users_dict
        db.close()
        if current_user.get_user_type() == "customer":
            return redirect(url_for("u_settings"))
        else:
            return redirect(url_for("staff.s_settings"))

    return render_template("customersettings.html")


@app.route("/forgot-password/<int:id>/", methods=["GET", "POST"])
def forgot_password(id):
    forgot_password_form = ForgotPasswordForm(request.form)
    users_dict = {}
    db = shelve.open("storage.db", "w")
    try:
        users_dict = db["Users"]
    except:
        pass
    
    for users in users_dict.values():
        if int(users.get_id())==id:
            email=users.get_email()
            break

    user=users_dict[email]
    if request.method == "POST" and forgot_password_form.validate():
        user.set_password(generate_password_hash(forgot_password_form.password.data))
        print(forgot_password_form.password.data)

        db["Users"] = users_dict
        db.close()
        flash('Password changed', category='success')
        return redirect(url_for("login"))

    return render_template("forget_password.html", form=forgot_password_form, email=email)

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password_email():
    forgot_password_form = request.form
    users_dict = {}
    db = shelve.open("storage.db", "w")
    try:
        users_dict=db['Users']
    except:
        print('Error retrieving Users storage')
    
    if (
        request.method == "POST"
        and forgot_password_form.get("email").lower() not in users_dict
    ):
        flash("Unregistered Email. Please sign up first !")
        return redirect(url_for("signup"))

    elif request.method == "POST":
        mail = Mail(app)
        with app.open_resource("static/images/logo-clear.png", "rb") as img:
            image_data = img.read()
        user = users_dict[forgot_password_form.get("email").lower()]
        msg = Message(
            f"PyTea Forget Password",
            sender="buyfrompytea@gmail.com",
            recipients=[forgot_password_form.get("email").lower()],
        )
        msg.attach(
            filename="static/images/logo-clear.png",
            content_type="image/png",
            data=image_data,
        )
        msg.body = (
            f"Dear {user.get_name().title()},\n"
            f"You have sent a forget password form\n"
            f"This is the link to change your password: \n"
            f"http://127.0.0.1:5000/forgot-password/{user.get_id()}/\n"
            f"Please run the application before going to this link \n"
            f"\nBest Regards,\n"
            f"PyTea\n"
        )

        mail.send(msg)
        flash('Email has been sent', category='success') 
    return render_template("forget_password_email.html", form=forgot_password_form)


@app.route("/delete-user/<int:id>", methods=["POST"])
def delete_user(id):
    email = current_user.get_email()
    users_dict = {}
    db = shelve.open("storage.db", "w")
    users_dict = db["Users"]
    users_dict.pop(email)
    print(email)
    db["Users"] = users_dict
    db.close()
    logout_user()
    return redirect(url_for("home"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


# Natelie : menu / transaction
@app.route("/menu")
def menu():
    return render_template("menu.html")


@app.route("/thaimilktea-customisation", methods=["GET", "POST"])
def thaimilktea_customisation():
    if current_user.is_authenticated:
        create_drink = request.form
        if request.method == "POST":
            user_dict = {}
            db = shelve.open("storage.db", "c")

            try:
                user_dict = db["Users"]
            except:
                print("Error in retrieving User from storage.db.")

            drink = ThaiMilkTea(
                (create_drink.get("quantity")[-1]),
                (create_drink.get("size")),
                (create_drink.get("sugar_level")),
            )

            for t in create_drink.getlist("topping"):
                drink.set_topping(t)

            user = user_dict[current_user.get_email()]

            if user.get_shopping_bag() == None:
                shopping_bag = shoppingBag()
            else:
                shopping_bag = user.get_shopping_bag()

            drink_id = random.randint(10, 100)
            while drink_id in shopping_bag.get_order():
                drink_id = random.randint(10, 100)

            drink.set_drink_id(drink_id)

            shopping_bag.add_order(drink_id, drink)

            user.set_shopping_bag(shopping_bag)
            db["Users"] = user_dict

            db.close()

            return redirect(url_for("menu"))
        return render_template("thaimilktea_customisation.html", form=create_drink)
    else:
        flash("Please login before ordering", category='error')
        return redirect(url_for("login"))


@app.route("/blackpearltea-customisation", methods=["GET", "POST"])
def blackpearltea_customisation():
    if current_user.is_authenticated:
        create_drink = request.form
        if request.method == "POST":
            user_dict = {}
            db = shelve.open("storage.db", "c")
            try:
                user_dict = db["Users"]
            except:
                print("Error in retrieving Users from storage.db.")

            drink = BlackPearlTea(
                (create_drink.get("quantity")[-1]),
                (create_drink.get("size")),
                (create_drink.get("sugar_level")),
            )

            for t in create_drink.getlist("topping"):
                drink.set_topping(t)
            print(drink.get_drink_id())

            user = user_dict[current_user.get_email()]

            if user.get_shopping_bag() == None:
                shopping_bag = shoppingBag()
            else:
                shopping_bag = user.get_shopping_bag()

            drink_id = random.randint(10, 100)
            while drink_id in shopping_bag.get_order():
                drink_id = random.randint(10, 100)

            drink.set_drink_id(drink_id)

            drink.set_drink_id(drink_id)

            shopping_bag.add_order(drink_id, drink)

            user.set_shopping_bag(shopping_bag)
            db["Users"] = user_dict

            db.close()

            return redirect(url_for("menu"))
        return render_template("blackpearltea_customisation.html", form=create_drink)
    else:
        flash("Please login before ordering", category='error')
        return redirect(url_for("login"))


@app.route("/thaibubbletea-customisation", methods=["GET", "POST"])
def thaibubbletea_customisation():
    if current_user.is_authenticated:
        create_drink = request.form
        if request.method == "POST":
            user_dict = {}
            db = shelve.open("storage.db", "c")

            try:
                user_dict = db["Users"]
            except:
                print("Error in retrieving User from storage.db.")

            drink = ThaiBubbleTea(
                (create_drink.get("quantity")[-1]),
                (create_drink.get("size")),
                (create_drink.get("sugar_level")),
            )

            for t in create_drink.getlist("topping"):
                drink.set_topping(t)

            user = user_dict[current_user.get_email()]

            if user.get_shopping_bag() == None:
                shopping_bag = shoppingBag()
            else:
                shopping_bag = user.get_shopping_bag()

            drink_id = random.randint(10, 100)
            while drink_id in shopping_bag.get_order():
                drink_id = random.randint(10, 100)

            drink.set_drink_id(drink_id)

            shopping_bag.add_order(drink_id, drink)

            user.set_shopping_bag(shopping_bag)
            db["Users"] = user_dict

            db.close()

            return redirect(url_for("menu"))
        return render_template("thaibubbletea_customisation.html", form=create_drink)
    else:
        flash("Please login before ordering", category='error')
        return redirect(url_for("login"))


@app.route("/shopping-bag")
def shopping_bag():
    if current_user.is_authenticated:
        db = shelve.open("storage.db", "w")
        users_dict = db["Users"]
        user = users_dict[current_user.get_email()]
        shopping_bag = []  # stores the individual drink orders
        total_cost = 0
        if user.get_shopping_bag() is not None:
            for drink in user.get_shopping_bag().get_order().values():
                shopping_bag.append(drink)
                total_cost += drink.get_total_cost()
            user.get_shopping_bag().set_total_cost(round(total_cost, 2))
        
        db["Users"] = users_dict
        
        return render_template(
            "shopping_bag.html",
            count=len(shopping_bag),
            shoppingbag=shopping_bag,
            total=round(total_cost, 2),
        )
    else:
        flash("Please login before ordering", category='error')
        return redirect(url_for("login"))


@app.route("/shopping-bag/delete-drink/<int:id>/", methods=["GET", "POST"])
def delete_drink(id):
    if current_user.is_authenticated:
        if request.method == "POST":
            users_dict = {}
            db = shelve.open("storage.db", "w")
            users_dict = db["Users"]
            user = users_dict[current_user.get_email()]
            order = user.get_shopping_bag()
            drink_name = order.get_order().get(id).get_name()
            print(drink_name)
            order.delete_order(id)
            print(id)
            db["Users"] = users_dict
            db.close()
            # stuff
            # after done:
            sentence = drink_name + " was removed"
            flash(sentence)
            return redirect(url_for("shopping_bag"))
    else:
        flash("Please login before checking out", category='error')
        return redirect(url_for("login"))


@app.route("/checkout", methods=["GET", "POST"])
def create_checkout_form():
    if current_user.is_authenticated:
        checkout_form = CreateCheckoutForm(request.form)
        db = shelve.open("storage.db", "r")
        users_dict = db["Users"]
        user = users_dict[current_user.get_email()]
        shopping_bag = []

        if user.get_shopping_bag() is not None:
            for drink in user.get_shopping_bag().get_order().values():
                shopping_bag.append(drink)

        total_cost = sum(drink.get_total_cost() for drink in shopping_bag)

        if request.method == "POST" and checkout_form.validate():
            orders_dict = {}

            db = shelve.open("storage.db", "c")
            try:
                orders_dict = db["Orders"]
            except:
                print("Error in retrieving Orders from storage.db.")

            # add order in shelve
            order_id = random.randint(10, 1000)
            while order_id in orders_dict:
                order_id = random.randint(10, 1000)

            orders = current_user.get_shopping_bag()
            orders.set_date(datetime.today())
            orders.set_order_id(order_id)
            orders.set_user_email(current_user.get_email())
            orders_dict[order_id] = orders
            db["Orders"] = orders_dict

            # update shopping bag
            user_dict = db["Users"]
            user = user_dict[current_user.get_email()]
            user.reset_shopping_bag()
            # user.set_past_order(order_id, orders)

            # update user address & postal code if they checked the checkbox
            try:
                checked = request.form.get("save-info")
                if checked:
                    user.set_address(checkout_form.address.data)
                    user.set_postal_code(checkout_form.postal_code.data)
                db["Users"] = user_dict
            except:
                pass
            
            # update inventory
            stocks = db["Inventory"]
            for drink in orders.get_order().values():
                for quantity in range(1, int(drink.get_quantity()) + 1):
                    stocks.used_cup()
                    stocks.used_tea()
                    stocks.used_milk()
                    for toppings in drink.get_topping():
                        if toppings == "Classic Black Pearls":
                            stocks.used_bubble()
                        elif toppings == "Signature Pearls":
                            stocks.used_signature_pearls()
                        elif toppings == "Jelly":
                            stocks.used_jelly()
            db["Inventory"] = stocks

            db.close()

            return redirect(url_for("home"))

        db.close()

        return render_template(
            "checkout.html",
            form=checkout_form,
            shoppingbag=shopping_bag,
            total=total_cost,
        )
    else:
        flash("Please login before checking out", category='error')
        return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
