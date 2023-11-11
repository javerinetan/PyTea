from wtforms import Form, StringField, EmailField, SelectField, validators, PasswordField, DateField, RadioField
import datetime


class CreateUserForm(Form):
    name = StringField('Name',[validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.DataRequired()])
    birth_month_choices = [
        ('', 'Month'), ('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('July', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')
    ]
    birth_month = SelectField('Birthday Month', [validators.AnyOf(values=[choice[0] for choice in birth_month_choices[1:]]),
                                            validators.DataRequired()], choices=birth_month_choices, default='')
    
    password = PasswordField('Password', [validators.DataRequired(),validators.Regexp('^(?=.*[A-Z].*[A-Z])(?=.*[!@#$&*])(?=.*[0-9].*[0-9])(?=.*[a-z].*[a-z].*[a-z]).{8,20}$',message='Password must have at least: \n • 8 Characters \n • 1 Special Character \n • 2 Numerials \n • 2 Letters in Upper Case \n • 3 Letters in Lower Case')])
    confirm_password=PasswordField('Confirm Password', [validators.DataRequired(message='*Required'),validators.EqualTo('password', message='Both password fields must be equal!')])



class CreateStaffForm(Form):
    name = StringField('Name',[validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired(),validators.Regexp('^(?=.*[A-Z].*[A-Z])(?=.*[!@#$&*])(?=.*[0-9].*[0-9])(?=.*[a-z].*[a-z].*[a-z]).{8,20}$',message='Password must have at least: \n • 8 Characters \n • 1 Special Character \n • 2 Numerials \n • 2 Letters in Upper Case \n • 3 Letters in Lower Case')])
    confirm_password=PasswordField('Confirm Password', [validators.DataRequired(message='*Required'),validators.EqualTo('password', message='Both password fields must be equal!')])

class CreateLoginForm(Form):
    email = EmailField('Email', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])


# fix validation for dates
# class CreateLeaveForm(Form):
#     start_date=DateField('Start Date', [validators.DataRequired()] )
#     end_date=DateField('End Date',[validators.DataRequired()] )
#     type=RadioField('Leave Type', [validators.DataRequired()],choices=[('Full Day', 'Full Day'), ('Half Day', 'Half Day')], default='Full Day')

        
class ChangePasswordForm(Form):
    password = PasswordField('Password',[validators.DataRequired(),validators.Regexp('^(?=.*[A-Z].*[A-Z])(?=.*[!@#$&*])(?=.*[0-9].*[0-9])(?=.*[a-z].*[a-z].*[a-z]).{8,20}$',message='Password must have at least: \n • 8 Characters \n • 1 Special Character \n • 2 Numerials \n • 2 Letters in Upper Case \n • 3 Letters in Lower Case')])
    confirm_password=PasswordField('Confirm Password',[validators.DataRequired(message='*Required'),validators.EqualTo('password', message='Both password fields must be equal!')])


class ForgotPasswordForm(Form):
    password = PasswordField('Password',[validators.DataRequired(),validators.Regexp('^(?=.*[A-Z].*[A-Z])(?=.*[!@#$&*])(?=.*[0-9].*[0-9])(?=.*[a-z].*[a-z].*[a-z]).{8,20}$',message='Password must have at least: \n • 8 Characters \n • 1 Special Character \n • 2 Numerials \n • 2 Letters in Upper Case \n • 3 Letters in Lower Case')])
    confirm_password=PasswordField('Confirm Password',[validators.DataRequired(message='*Required'),validators.EqualTo('password', message='Both password fields must be equal!')])
