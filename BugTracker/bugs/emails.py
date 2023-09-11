from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse


def send_forget_password_mail(email, token):
    subject = 'Your forget password link'
    reset_form_url = reverse('reset_password', args=[token])
    reset_link = f"{settings.BASE_URL}{reset_form_url}"
    message = f'Hi, Click on the link to reset your password {reset_link}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    print("forgot email goes to: ", recipient_list)
    send_mail(
        subject,
        message,
        email_from,
        recipient_list
    )
    return True


def send_password_change_ack(user):
    subject = 'Your password has been reset'
    login_url = reverse('login')
    login_link = f'{settings.BASE_URL}{login_url}'
    message = (f'Hi, You have changed your password successfully. Please go to the link for login to the application '
               f'{login_link}')
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    print("inbox comes in: ", recipient_list)
    send_mail(
        subject,
        message,
        email_from,
        recipient_list
    )
    return True


def send_bug_assigned_email(bug):
    bug_list_url = reverse('bug_list', kwargs={'project_id': bug.project_id})
    bug_link = f"{settings.BASE_URL}{bug_list_url}?bug_id={bug.id}"
    subject = "{} assigned a new bug: {}".format(bug.reporter, bug.title)

    template_name = 'email_templates/bug_email.html'
    context = {
        'bug_link': bug_link,
        'created_user': bug.reporter,  # Pass the creator user to the template
        'assigned_user': bug.assigned,  # Pass the user to the template
        'bug': bug,  # Pass the bug instance to the template
    }

    message = render_to_string(template_name, context)

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [bug.assigned.email]
    send_mail(
        subject,
        "",
        from_email,
        recipient_list,
        html_message=message
    )


def send_project_invitation_email(project, user):
    login_url = reverse('login')  # Replace 'login' with your actual login URL name
    login_link = f'{settings.BASE_URL}{login_url}'
    subject = 'Invitation to Project access'

    template_name = 'email_templates/project_invitation.html'
    context = {
        'login_link': login_link,
        'user': user.username,
        'project_created_user': project.created_user,  # Pass the creator user to the template
        'project_name': project.name,  # Pass the user to the template
    }

    message = render_to_string(template_name, context)

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(
        subject,
        "",
        from_email,
        recipient_list,
        html_message=message,
        fail_silently=False
    )


def send_registration_invitation_email(project, email):
    signup_url = reverse('signup')
    signup_link = f'{settings.BASE_URL}{signup_url}'
    subject = 'Invitation to Project Access Registration'

    template_name = 'email_templates/project_access_registration.html'
    context = {
        'signup_link': signup_link,
        'project_created_user': project.created_user,  # Pass the creator user to the template
        'project_name': project.name,  # Pass the user to the template
    }

    message = render_to_string(template_name, context)

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        html_message=message,
        fail_silently=False
    )
