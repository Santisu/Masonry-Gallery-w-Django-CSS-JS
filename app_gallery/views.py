from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import Picture, Hashtag
from .forms import HashtagForm, PictureForm, PictureDataForm

class GaleryView(View):
    template_name = 'gallery.html'
    hashtag_form = HashtagForm
    picture_form = PictureForm
    picture_data_form = PictureDataForm

    def get(self, request):

        """Get all the pictures marked as visible"""

        pictures = Picture.objects.filter(is_visible=True)
        context = {
            'pictures': pictures,
            'hashtag_form': self.hashtag_form(),
            'picture_form': self.picture_form(), 
            'picture_data_form': self.picture_data_form()
        }
        return render(request, self.template_name, context)
    
    def post(self, request):

        
        if request.POST.get('upload'):
            
            """Upload multiple pictures using the form created with 
            django-multiupload library"""

            picture_form = self.picture_form(request.POST, request.FILES)
            if picture_form.is_valid():
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
                image_id = request.POST.get('image_id') #Get the image_id value added with JS
                picture = Picture.objects.get(id = image_id)    #Search for the image using the id
                picture.title = form.title
                picture.description = form.description
                picture.is_visible = form.is_visible
                hashtags_selected = request.POST.getlist('hashtags')
                #If there is any hashtag selected, it will replace the current tags 
                if hashtags_selected:
                    picture.hashtags.set(hashtags_selected)
                #If the clear tags checkbox is marked it will erase all the tags from the picture
                if request.POST.get('clear_hashtags'):
                    picture.hashtags.clear()
                picture.save()
                return redirect('gallery')
            
        return redirect('404') 
            

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
                'hashtags': hashtags_list,
                'url': self.picture.image.url,
                'id': self.picture.id,
                'description' : self.picture.description,
                'is_visible' : self.picture.is_visible,
                'uploaded_at' : self.picture.uploaded_at,
                }
        return JsonResponse(data)