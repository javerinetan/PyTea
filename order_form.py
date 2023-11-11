from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, EmailField, widgets, SelectMultipleField
from markupsafe import Markup
 
 
class BootstrapListWidget(widgets.ListWidget):
 
    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        html = [f"<{self.html_tag} {widgets.html_params(**kwargs)}>"]
        for subfield in field:
            if self.prefix_label:
                html.append(f"<li class='list-group-item'>{subfield.label} {subfield(class_='form-check-input ms-1')}</li>")
            else:
                html.append(f"<li class='list-group-item'>{subfield(class_='form-check-input me-1')} {subfield.label}</li>")
        html.append("</%s>" % self.html_tag)
        return Markup("".join(html))
 
 
class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.
 
    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = BootstrapListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class UpdateOrderForm(Form):
    quantity = StringField('Quantity', [validators.Length(min=1, max=150), validators.DataRequired()])
    size_choices = [
        ('', 'Choose your Size..'),
        ('Medium', 'Medium'),
        ('Large', 'Large')
    ]
    size = SelectField('Size', [validators.AnyOf(values=[choice[0] for choice in size_choices[1:]]),
                                            validators.DataRequired()], choices=size_choices, default='')
    
    sugar_level_choices = [
        ('', 'Choose your Sugar Level..'),
        ('0%', '0%'),
        ('25%', '25%'),
        ('50%', '50%'),
        ('75%', '75%'),
        ('100%', '100%')
    ]
    sugar_level = SelectField('Sugar Level', [validators.AnyOf(values=[choice[0] for choice in sugar_level_choices[1:]]),
                                            validators.DataRequired()], choices=sugar_level_choices, default='')
    
    topping_choices = [('Signature Pearls', 'Signature Pearls'), ('Classic Black Pearls', 'Classic Black Pearls'), ('Jelly', 'Jelly')]

    topping = MultiCheckboxField('Topping',choices=topping_choices)
