from flask import render_template, request, redirect, url_for, flash, Blueprint, session
from account_form import CreateStaffForm, ChangePasswordForm
import shelve
from classes.staff_leave import StaffLeave
from classes.staff import Staff
from classes.contactUs import contactUs
from contact_form import CreateCustomerContactForm
from werkzeug.security import generate_password_hash
from flask_login import (
    login_user,
    LoginManager,
    login_required,
    current_user,
    logout_user,
)
import random
from datetime import date, datetime
from operator import attrgetter
import math
from order_form import UpdateOrderForm
import ast  # for converting string to list

staff_blueprint = Blueprint(name="staff", import_name=__name__, url_prefix="/staff/")
staff_blueprint.secret_key = "any_random_string"


@staff_blueprint.route("/")
@login_required
def staff_home():
    if current_user.get_user_type() == "staff":
        orders_dict = {}
        db = shelve.open("storage.db", "c")
        try:
            orders_dict = db["Orders"]
        except:
            print("Error in retrieving Orders from storage.db.")

        order_list = []  # stores the individual drink orders

        for (
            order
        ) in (
            orders_dict.values()
        ):  # one order is one shoppingbag object which contains multiple drink objects
            order_list.append(order)

        sorting_key = lambda obj: datetime.strptime(
            str(obj.get_date()), "%Y-%m-%d %H:%M:%S.%f"
        )
        order_list.sort(key=sorting_key, reverse=True)

        return render_template(
            "staff_home.html", today=date.today(), order_list=order_list
        )
    else:
        return redirect(url_for("home"))


@staff_blueprint.route(
    "/update-order/<int:id>/<int:drink_id>/", methods=["GET", "POST"]
)
@login_required
def update_order(id, drink_id):  # id is the order id
    update_form = UpdateOrderForm(request.form)
    if request.method == "POST" and update_form.validate():
        print(update_form.topping.data)
        # Fetch the order from the database based on the id
        db = shelve.open("storage.db", "w")
        orders_dict = db.get("Orders")

        order = orders_dict.get(id)  # gets the shopping bag object

        if order:
            # Update the order fields with the form data
            drink = order.get_order().get(drink_id)
            drink.set_quantity(update_form.quantity.data)
            drink.set_size(update_form.size.data)
            drink.set_sugar_level(update_form.sugar_level.data)
            drink.reset_topping()

            for t in request.form.getlist("topping"):
                drink.set_topping(t)

            # Save the updated order back to the database
            orders_dict[id] = order
            db["Orders"] = orders_dict

            # Update the user side as well
            # user_dict=db['Users']
            # user=user_dict[order.get_user_email()]
            # past_order=user.get_past_orders().get(id).get_order()
            # past_order[drink_id]=drink
            # db['Users']=user_dict
            db.close()

            return redirect(url_for("staff.staff_home"))
        else:
            db.close()
            flash("Order not found.", "danger")
            return redirect(url_for("staff.staff_home"))
    else:
        order_dict = {}
        db = shelve.open("storage.db", "r")
        order_dict = db.get("Orders", {})
        db.close()

        order = order_dict.get(id)

        if not order:
            flash("Order not found.", "danger")
            return redirect(url_for("staff.staff_home"))

        # Populate the form fields with the existing order data
        drink = order.get_order().get(drink_id)
        update_form.quantity.data = drink.get_quantity()
        update_form.size.data = drink.get_size()
        update_form.sugar_level.data = drink.get_sugar_level()
        if len(drink.get_topping())!=0:
            update_form.topping.data = drink.get_topping()
        # else:
        #     update_form.topping.data = ['None']
        # update_form.process()

        return render_template(
            "staff_updateorder.html", form=update_form, drink_name=drink.get_name()
        )


@staff_blueprint.route("/delete-order/<int:id>/<int:drink_id>/", methods=["GET", "POST"])
@login_required
def delete_order(id, drink_id):
    # remb to check if the drink is the last one , if it is the last one delete the whole shopping bag object
    order_dict = {}
    db = shelve.open("storage.db", "w")
    order_dict = db["Orders"]
    order=order_dict.get(id) # get the individual shopping bag
    # order = order_dict.pop(id) # this deletes the whole order before it even delete the drink
    print(1)
    print(order.get_order())
    print(drink_id)
    if len(order.get_order()) == 1:
        # Delete the whole shopping bag object
        order_dict.pop(id)
    else:
        # Only delete the drink
        print(drink_id)
        order.get_order().pop(drink_id)
        print('after: ',order.get_order())
    print(4)
    db["Orders"] = order_dict
    db.close()
    return redirect(url_for("staff.staff_home"))


@staff_blueprint.route("/signup", methods=["GET", "POST"])
def staff_signup():
    create_staff_form = CreateStaffForm(request.form)
    if request.method == "POST" and create_staff_form.validate():
        users_dict = {}
        db = shelve.open("storage.db", "c")

        try:
            if "Users" in db:
                users_dict = db["Users"]
            else:
                db["Users"] = users_dict
        except:
            print("Error in retrieving Users from storage.db.")

        if create_staff_form.email.data.lower() in users_dict:
            "email already exist"
            flash("Email already exists.")

        else:
            user = Staff(
                create_staff_form.name.data,
                create_staff_form.email.data.lower(),
                generate_password_hash(create_staff_form.password.data),
            )

            staff_id = random.randint(1, 9)
            for staff in users_dict.values():
                if staff.get_id() == str(staff_id):
                    staff_id = random.randint(1, 9)
            user.set_user_id(str(staff_id))

            users_dict[user.get_email()] = user
            db["Users"] = users_dict

        db.close()
        return redirect(url_for("login"))
    return render_template("staff_signup.html", form=create_staff_form)


@staff_blueprint.route("/users")
@login_required
def retrieve_users():
    if current_user.get_user_type() == "staff":
        db = shelve.open("storage.db", "r")
        users_dict = {}
        try:
            users_dict = db["Users"]
        except:
            print("no Users")
        db.close()

        users_list = []
        for key in users_dict:
            user = users_dict.get(key)
            users_list.append(user)

        return render_template("retrieve_user.html", users_list=users_list)
    else:
        return redirect(url_for("home"))


@staff_blueprint.route("/delete-user/<int:id>", methods=["GET", "POST"])
@login_required
def staff_delete_user(id):
    if current_user.get_user_type() == "staff":
        db = shelve.open("storage.db", "w")
        users_dict = db["Users"]
        for u in users_dict.values():
            if u.get_id() == str(id):
                user_email = u.get_email()
                user_name=u.get_name()
        try:
            users_dict.pop(user_email)
            db["Users"] = users_dict
            message= "User: " + user_email + ' (' + user_name + ') was deleted'
            flash(message, category='success')
        except:
            flash('Error deleting user', category='error')
        
        db.close()
        return redirect(url_for("staff.retrieve_users"))

    else:
        return redirect(url_for("home"))


@staff_blueprint.route("/inventory")
@login_required
def inventory():
    if current_user.get_user_type() == "staff":
        db = shelve.open("storage.db", "r")
        product_inventory = db["Inventory"]
        db.close()

        return render_template("staff_inventory.html", inventory=product_inventory)
    else:
        return redirect(url_for("home"))


@staff_blueprint.route("/restocked/<int:id>", methods=["GET", "POST"])
@login_required
def restock(id):
    if current_user.get_user_type() == "staff":
        if request.method == "POST":
            db = shelve.open("storage.db", "w")
            product_inventory = db["Inventory"]
            print(1)
            if id == 1:
                print(2)
                try:
                    print(request.form.get('cup'))
                    product_inventory.restock_cup(int(request.form.get('cup')))
                    flash('Cup Inventory Updated', category='success')
                except:
                    flash('Error updating cup inventory', category='error')
            if id == 2:
                try:
                    product_inventory.restock_milk(int(request.form.get('milk')))
                    flash('Milk Inventory Updated', category='success')
                except:
                    flash('Error updating milk inventory', category='error')
            elif id == 3:
                try:
                    product_inventory.restock_tea(int(request.form.get('tea')))
                    flash('Tea Inventory Updated', category='success')
                except:
                    flash('Error updating tea inventory', category='error')
            elif id == 4:
                try:
                    product_inventory.restock_signature_pearls(int(request.form.get('signature_pearls')))
                    flash('Signature Pearls Inventory Updated', category='success')
                except:
                    flash('Error updating signature pearls inventory', category='error')

            elif id == 5:
                try:
                    product_inventory.restock_bubble(int(request.form.get('bubble')))
                    flash('Bubbles Inventory Updated', category='success')
                except:
                    flash('Error updating bubble inventory', category='error')
            elif id == 6:
                try:
                    product_inventory.restock_jelly(int(request.form.get('jelly')))
                    flash('Jelly Inventory Updated', category='success')
                except:
                    flash('Error updating jelly inventory', category='error')
            db["Inventory"] = product_inventory
            db.close()

        return redirect(url_for("staff.inventory"))
    else:
        return redirect(url_for("home"))


@staff_blueprint.route("/leave", methods=["GET", "POST"])
@login_required
def leave():
    if current_user.get_user_type() == "staff":
        # create_leave_form = request.form
        # print('ok 1')
        if request.method == "POST":
            leave = StaffLeave(
                request.form.get("start_date"),
                request.form.get("end_date"),
                request.form.get("type"),
                request.form.get("reason"),
            )
            print(request.form)
            # print(leave)
            # print(request.form.get("start_date"))
            # print(create_leave_form.get("end_date"))
            # print('ok 3')
            db = shelve.open("storage.db", "w")
            user_dict = db["Users"]
            user = user_dict.get(current_user.get_email())
            user.set_leave(leave)
            db["Users"] = user_dict
            db.close()
        return redirect(url_for("staff.staff_home"))


@staff_blueprint.route("/user-settings")
@login_required
def s_settings():
    if current_user.get_user_type() == "staff":
        update_password_form = ChangePasswordForm(request.form)
        return render_template("staffsettings.html", form=update_password_form)

    return redirect(url_for("home"))


# Javerine's portion


def custom_sort_key(feedback):
    status_priority = {
        "Redirect to Manager": 0,
        "Open (2+ days)": 1,
        "Open": 2,
        "In Progress": 3,
        "Closed": 4,
    }
    # Sort by status first (Open status will be at the top, followed by Issue, In Progress, and then Closed)
    status = feedback.get_status()
    priority = status_priority.get(
        status, 5
    )  # Default priority is 4 for unknown statuses (will be sorted last)

    if status == "Closed":
        # Sort by the date in ascending order for Closed items
        return (priority, feedback.get_time())
    else:
        # Sort by the date in descending order for other statuses
        return (priority, feedback.get_time())


@staff_blueprint.route("/feedback", methods=["GET", "POST"])
@login_required
def staff_feedback():
    if current_user.get_user_type() == "staff":
        db = shelve.open("storage.db", "r")
        feedback_dict = {}
        try:
            feedback_dict = db["Feedback"]
        except:
            print("no Feedback")
        db.close()

        if request.method == "POST":
            feedback_id = request.form["feedback_id"]
            status = request.form["status"]

            if feedback_id in feedback_dict:
                feedback = feedback_dict[feedback_id]
                feedback.set_status(status)
                db = shelve.open("storage.db", "w")
                db["Feedback"] = feedback_dict
                db.close()
                flash("Feedback status updated successfully.")

        current_datetime = date.today()
        feedback_list = []

        for key in feedback_dict:
            user = feedback_dict.get(key)
            feedback_list.append(user)

        # Sort the feedback_list using the custom_sort_key function
        feedback_list.sort(key=custom_sort_key)

        # Check if the feedback is still "Open" and more than 2 days old
        for feedback in feedback_list:
            if feedback.get_status() == "Open":
                submission_date = feedback.get_time().date()
                days_diff = (current_datetime - submission_date).days
                if days_diff >= 2:
                    feedback.set_status("Open (2+ days)")

                # elif days_diff >= 2:
                #     feedback.set_status(f'Open ({days_diff}+ days)')

        return render_template(
            "staff_feedback.html",
            count=len(feedback_list),
            feedback_list=feedback_list,
            current_datetime=current_datetime,
        )

    return redirect(url_for("home"))


@staff_blueprint.route("/update-customer-feedback/<int:id>", methods=["GET", "POST"])
@login_required
def update_customer_feedback(id):
    update_feedback = CreateCustomerContactForm(request.form)
    if request.method == "POST" and update_feedback.validate():
        feedback_dict = {}
        db = shelve.open("storage.db", "w")
        feedback_dict = db["Feedback"]

        customer = feedback_dict.get(id)
        customer.set_first_name(update_feedback.first_name.data)
        customer.set_last_name(update_feedback.last_name.data)
        customer.set_email(update_feedback.email.data)
        customer.set_saluation(update_feedback.salutation.data)
        customer.set_feedback(update_feedback.feedback.data)
        customer.set_status(update_feedback.status.data)

        db["Feedback"] = feedback_dict
        db.close()

        session["user_updated"] = (
            customer.get_first_name() + " " + customer.get_last_name()
        )

        return redirect(url_for("staff.staff_feedback"))
    else:
        feedback_dict = {}
        db = shelve.open("storage.db", "r")
        feedback_dict = db["Feedback"]
        db.close()

        customer = feedback_dict.get(id)
        update_feedback.first_name.data = customer.get_first_name()
        update_feedback.last_name.data = customer.get_last_name()
        update_feedback.salutation.data = customer.get_salutation()
        update_feedback.email.data = customer.get_email()
        update_feedback.feedback.data = customer.get_feedback()
        update_feedback.status.data = customer.get_status()

        return render_template("staff_updatefeedback.html", form=update_feedback)


@staff_blueprint.route("/delete-customer-feedback/<int:id>", methods=["POST"])
@login_required
def delete_customer_feedback(id):
    feedback_dict = {}
    db = shelve.open("storage.db", "w")
    feedback_dict = db["Feedback"]
    customer = feedback_dict.pop(id)
    db["Feedback"] = feedback_dict
    db.close()

    session["user_deleted"] = customer.get_first_name() + " " + customer.get_last_name()

    return redirect(url_for("staff.staff_feedback"))


@staff_blueprint.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")
