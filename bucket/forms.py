from django import forms

from multiuploader.forms import MultiUploadForm

from .models import BucketFile

class BucketUploadForm(forms.ModelForm):
    class Meta:
        model = BucketFile
        exclude = ['thumbnail_url', 'being_edited_by']
    # bucket = forms.ModelChoiceField(queryset=Bucket.objects.all(), empty_label=None)
