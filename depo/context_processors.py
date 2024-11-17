from django.conf import settings

def project_version(request):
    return {
        'project_version': settings.PROJECT_VERSION
    }
