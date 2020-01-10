# Create the form class.
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Div
from django import forms

from tokbox.models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'time_end', 'days', 'description', 'what_you_will_learn', 'requirements']

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(
                    Div('name'),
                    Div('time_end'),
                    Div("days"),
                    Div("description"),
                    Div("what_you_will_learn"),
                    Div("requirements"),
                    css_class="col-6 offset-3"),
                css_class="row"),
            Div(
                Div(
                    Submit('submit', 'Submit', css_class='button white'),
                    css_class="col-4 offset-8"),
                css_class="row"),
        )
