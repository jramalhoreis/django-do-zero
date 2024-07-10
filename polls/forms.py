

from django import forms 
from django.core.files.temp import NamedTemporaryFile

from polls.models import Question


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('question_text', 'pub_date', 'categoria', 'end_date')
        widgets= {
            'pub_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type':'date'}
            ),
            'end_date': forms.DateTimeInput(
                format='%Y-%m-%d %H:%M;%S',
                attrs={'type':'datetime-local'}
            ),
        }




class QuestionImportForm(forms.Form):
    import_file = forms.FileField(label='Arquivo para importacao CSV')

    def clean(self):
        cleaned_data = super().clean()
        import_data = cleaned_data.get('import_file')

        if not self.has_error('import_file'):
            csv_temp_file = NamedTemporaryFile(delete=False)

        with csv_temp_file as uploaded_file:
            for chunk in import_data.chunks():
                uploaded_file.write(chunk)

        cleaned_data['tmp_file_name'] = csv_temp_file.name

        return cleaned_data


