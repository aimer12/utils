import json
from functools import wraps
from django.http import HttpResponse


def check_required_args(*keys):
    """
    @params: accept position arguments, example:
        @check_required_args(arg1, arg2, arg3, .., argn)
        def index(request):
            return HttpResponse(args_dict)
    @response:
        if there any argument check failure,
        a error response will be returned
    """

    def wrapper(func):
        @wraps(func)
        def new_func(request, *args, **kwargs):
            check_rst = dict(code=0)
            data = dict()
            for arg in keys:
                value = request.REQUEST.get(arg, None)
                if not value:
                    check_rst = {'code': 101,
                                 'msg': '{0} is required.'.format(arg)}
                    return HttpResponse(json.dumps(check_rst))
                    break
                if value.count(',') >= 1:
                    data["{}__in".format(arg)] = value.split(',')
                else:
                    data[arg] = value
            check_rst['data'] = data
            rsp = func(request, *args, **kwargs)
            return rsp
        return new_func
    return wrapper
