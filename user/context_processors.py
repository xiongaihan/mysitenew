from mysite.forms import LoginForm

def login_form(request):
    return {'login_modal_form':LoginForm()}
