#decorators.py
from django.shortcuts import redirect

def activeproject(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if not 'project_id' in request.session:
            return redirect('viewProject')

        return view_func(request, *args, **kwargs)
    return _wrapped_view_func
    
def activeexp(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if not 'project_id' in request.session:
            return redirect('viewProject')
        if not 'exp_id' in request.session:
            return redirect('viewExperiment')

        return view_func(request, *args, **kwargs)
    return _wrapped_view_func