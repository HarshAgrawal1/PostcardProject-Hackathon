from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import PostcardForm
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from xhtml2pdf import pisa
from .forms import ChristmasForm
from django.template.loader import get_template

def inputform(request):
    template = loader.get_template('inputform.html')
    return HttpResponse(template.render())
    
def samplepostcard(request):
    template = loader.get_template('christmas.html')
    return HttpResponse(template.render())
    # return HttpResponse(request,'christmas.html')

@csrf_exempt
def postcard_view(request):
    if request.method == 'POST':
        form = PostcardForm(request.POST)
        if form.is_valid():
            paragraph = form.cleaned_data['paragraph']
            return render(request, 'christmas.html', {
                'form': form,
                'paragraph': paragraph,
            })
    else:
        form = PostcardForm()

    return render(request, 'inputform.html', {'form': form})

def christmas_card(request):
    if request.method == 'POST':
        form = ChristmasForm(request.POST)
        if form.is_valid():
            num_people = form.cleaned_data['num_people']

            # Generate a PDF card for each person
            for i in range(num_people):
                receiver_name = form.cleaned_data[f'receiver_name_{i+1}']
                email = form.cleaned_data[f'email_{i+1}']

                # Create a PDF using the HTML template for each person
                template_path = 'your_template_path/christmas.html'  # Update the path accordingly
                template = get_template(template_path)
                context = {'receiver_name': receiver_name}
                html = template.render(context)

                # Generate PDF
                pdf = HttpResponse(content_type='application/pdf')
                pdf['Content-Disposition'] = f'attachment; filename="christmas_card_{i+1}.pdf"'
                pisa.CreatePDF(html, dest=pdf)

                # Send the generated PDF to the provided email for each person
                email_subject = 'Your Christmas Card'
                email_body = 'Please find the attached Christmas card.'
                email_message = EmailMessage(email_subject, email_body, to=[email])
                email_message.attach(f'christmas_card_{i+1}.pdf', pdf.getvalue(), 'application/pdf')
                email_message.send()

            return HttpResponse('Emails sent successfully!')
    else:
        form = ChristmasForm()

    return render(request, 'your_template.html', {'form': form})