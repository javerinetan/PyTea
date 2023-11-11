from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, EmailField, DateTimeLocalField, DateField
from datetime import datetime,date

class CreateCheckoutForm(Form):
    address = StringField('Address',[validators.Length(min=3, max=150), validators.DataRequired()])
    postal_code = StringField('Postal Code',[validators.Length(min=2, max=150), validators.DataRequired()])
    payment_method = RadioField(choices=[('Credit card', 'Credit card'), ('Dedit card', 'Dedit card'), ('Paypal', 'Paypal')], default='Credit card')
    card_name = StringField('Name on Card',[validators.Length(min=2, max=150), validators.DataRequired()])
    card_number = StringField('Credit Card Number',[validators.Length(min=2, max=150), validators.DataRequired()])
    card_expiration = StringField('Card Expiration',[validators.Length(min=2, max=150), validators.DataRequired()])
    card_cvv = StringField('Card CVV',[validators.Length(min=2, max=150), validators.DataRequired()])


