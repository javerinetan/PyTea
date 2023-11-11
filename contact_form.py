from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, EmailField, DateTimeLocalField, DateField
from datetime import datetime,date


class CreateCustomerContactForm(Form):
    first_name = StringField('First Name',[validators.Length(min=3, max=150), validators.DataRequired()])
    last_name = StringField('Last Name',[validators.Length(min=2, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.DataRequired()])
    salutation_choices = [
        ('', 'Choose your Saluatation..'),
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Madam', 'Madam'),
        ('Miss', 'Miss')
    ]
    salutation = SelectField('Salutation', [validators.AnyOf(values=[choice[0] for choice in salutation_choices[1:]]),
                                            validators.DataRequired()], choices=salutation_choices, default='')
    feedback = StringField('Feedback',[validators.Length(min=1, max=1000000), validators.DataRequired()])
    status = RadioField('Status', choices=[('Open', 'Open'), ('Redirect to Manager', 'Redirect to Manager'), ('In Progress', 'In Progress'), ('Closed', 'Closed')], default='Open')

class FeedbackStatusForm(Form):
    status_choices = [
        ('open', 'Open'),
        ('closed', 'Closed')
    ]
    status = SelectField('Feedback Status', [validators.AnyOf(values=[choice[0] for choice in status_choices]),
                                             validators.DataRequired()], choices=status_choices)