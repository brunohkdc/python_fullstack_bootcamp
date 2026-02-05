from django import forms
from posts.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'post']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Enter post title',
                'required': True
            }),
            'post': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'placeholder': 'Write your post content here...',
                'rows': 10,
                'required': True
            }),
        }
        labels = {
            'title': 'Post Title',
            'post': 'Post Content',
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Post title must be at least 5 characters long.")
        
        if len(title) > 100:
            raise forms.ValidationError("Post title cannot exceed 100 characters.")
        return title
    
    def clean_post(self):
        content = self.cleaned_data.get('post')
        if len(content) < 30:
            raise forms.ValidationError("Post content must be at least 30 characters long.")
        return content