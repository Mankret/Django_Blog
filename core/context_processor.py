from blog.forms import ContactUsForm


def get_context_data(request):
    context = {
        'form': ContactUsForm()
    }
    return context