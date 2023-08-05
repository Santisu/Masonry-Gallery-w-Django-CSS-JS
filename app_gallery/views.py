import json
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import Picture, Hashtag
from .forms import CreateHashtagForm, HashtagForm, PictureForm, MultiPictureForm, PictureDataForm
from django.middleware.csrf import get_token
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})

class GaleryView(View):
    template_name = 'gallery.html'
    hashtag_form = HashtagForm
    picture_form = PictureForm
    multi_picture_form = MultiPictureForm
    picture_data_form = PictureDataForm

    def get(self, request):

        """Get all the pictures marked as visible, if user is auth shows everything"""

        if request.user.is_authenticated:
            if request.GET.get('non-visible'):
                pictures = Picture.objects.filter(is_visible=False)
            elif request.GET.get('show-visible'):
                pictures = Picture.objects.filter(is_visible=True)
            else:
                pictures = Picture.objects.all()
        else:
                pictures = Picture.objects.filter(is_visible=True)
                
        context = {
            'pictures': pictures,
            'hashtag_form': self.hashtag_form(),
            'multi_picture_form': self.multi_picture_form(), 
            'picture_data_form': self.picture_data_form(),
            'picture_form' : self.picture_form(),
        }
        return render(request, self.template_name, context)
    
    def post(self, request):

        if request.user.is_authenticated:  
            """Methods only available if user is auth"""

            if request.POST.get('single-picture'):
                """Upload unique picture"""

                picture_form = self.picture_form(request.POST, request.FILES)
                if picture_form.is_valid():
                    picture = picture_form.save()
                    return redirect('gallery')
            
            if request.POST.get('upload'):
                
                """Upload multiple pictures using the form created with 
                django-multiupload library"""

                multi_picture_form = self.multi_picture_form(request.POST, request.FILES)
                if multi_picture_form.is_valid():
                    images = request.FILES.getlist('multi_pictures')
                    for image in images:
                        image_ins = Picture(image=image)
                        image_ins.save()
                    return redirect('gallery')
                
            if request.POST.get('update'):

                """Updates picture """

                picture_data_form = self.picture_data_form(request.POST)
                if picture_data_form.is_valid():
                    form = picture_data_form.save(commit=False)
                    image_id = request.POST.get('image_id')
                    
                    try:
                        picture = Picture.objects.get(id=image_id)
                    except Picture.DoesNotExist:
                        return HttpResponseBadRequest("Image not found")
                    picture.title = form.title
                    picture.description = form.description
                    picture.is_visible = form.is_visible
                    
                    if request.POST.get('clear_hashtags'):
                        picture.hashtags.clear()
                    else:
                        hashtags_selected = request.POST.getlist('hashtags')
                        current_hashtags = picture.hashtags.all()
                        union_hashtags = list(set(current_hashtags) | set(hashtags_selected))
                        picture.hashtags.set(union_hashtags)
                    
                    picture.save()
                    return redirect('gallery')
                
            if request.POST.get('delete'):
                """Delete the selected picture"""
                image_id = request.POST.get('image_id')
                try:
                    picture = Picture.objects.get(id=image_id)
                except Picture.DoesNotExist:
                    return HttpResponseBadRequest("Image not found")
                picture.delete()
                return redirect('gallery')
                    
        if request.POST.get('hashtag'):
            
            """Return pictures filtered by hashtag"""

            hashtag_form = self.hashtag_form(request.POST)
            if hashtag_form.is_valid():
                hashtag = hashtag_form.cleaned_data['hashtag']
                pictures = Picture.objects.filter(hashtags=hashtag, is_visible=True)
                context = {
                    'pictures': pictures,
                    'hashtag_form': self.hashtag_form(),
                    'multi_picture_form': self.multi_picture_form(),
                    'picture_data_form': self.picture_data_form(),
                    'picture_form' : self.picture_form(),
                }
                return render(request, self.template_name, context)
        
        return redirect('gallery')

class GetPicture(View):
    
    """Send picture to modal"""

    def dispatch(self, request, pk, *args, **kwargs):

        """Handle the request and checks if the picture exists and is available"""
        
        try:
            self.picture = Picture.objects.get(id=pk)
        except Picture.DoesNotExist:
            data = {
            'data':"Picture isn't available"
                    }   
            return JsonResponse(data, status=404)
        if request.user.is_authenticated:
            pass
        else:
            if self.picture.is_visible == False:
                data = {
                'data':"Picture isn't available"
                        }   
                return JsonResponse(data, status=404)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):

        """Sends full quality picture url and their data"""

        hashtags_list = list(self.picture.hashtags.values_list('hashtag', flat=True))
        data = {'title': self.picture.title,
                'url': self.picture.image.url,
                'hashtags': hashtags_list,
                'uploaded_at' : self.picture.uploaded_at,
                'description' : self.picture.description,
                'id': self.picture.id,
                'is_visible' : self.picture.is_visible,
                }
        return JsonResponse(data)


class CreateHashtagView(View):
    @method_decorator(login_required)
    def post(self, request):
        data = json.loads(request.body)
        form = CreateHashtagForm(data)

        if form.is_valid():
            hashtag = form.cleaned_data['hashtag']
            new_hashtag = Hashtag.objects.create(hashtag=hashtag.lower())
            return JsonResponse({'message': 'Hashtag created successfully.',
                                'hashtag': str(new_hashtag)})
        else:
            return JsonResponse({'error': 'Form error.', 'errors': form.errors}, status=400)