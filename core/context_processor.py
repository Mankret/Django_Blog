from blog.forms import ContactUsForm

# Contact us context processor
def get_context_data(request):
    context = {
        'form': ContactUsForm()
    }
    return context