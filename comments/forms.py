from django import forms
from comments.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'placeholder': 'Write your comment here...',
                'rows': 10,
                'required': True
            }),
        }
        labels = {
            'content': 'Comment',
        }
    
    def clean_content(self):
        content = self.cleaned_data.get('content')

        if len(content) < 1:
            raise forms.ValidationError("Comment must be at least 1 character long.")
        
        if len(content) > 700:
            raise forms.ValidationError("Comment cannot exceed 700 characters.")
        return content