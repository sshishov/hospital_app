class ProjectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.get('project'):
            project = request.user.userprofile.projects.first()
            if project:
                request.session['project'] = str(project.id)
        response = self.get_response(request)
        return response
