# -*- coding: utf-8 -*-
"""
    __init__.py
    :copyright: (c) 2019 by Joe Paul.
    :license: see LICENSE for details.
"""
import re
import json
import argparse

from colorama import init
from colorama import Fore, Style
from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import HTTPException, NotFound, abort
from werkzeug.routing import Map, Rule
from werkzeug.serving import run_simple


init()
endpoint_regex = re.compile("[^A-Za-z0-9]+")

class Interceptor(object):

    def __init__(self, rules):
        rule_objs = []
        for rule in rules:
            endpoint_name = endpoint_regex.sub('', rule["path"])

            rule_objs.append(Rule(
                '/%s' % rule["path"],
                methods=rule["methods"],
                endpoint=endpoint_name
            ))

            # Add function into the local context
            code = compile("""def %s(request):
                print(Fore.GREEN)
                print("URL\\n----\\n{0}\\n".format(str(request.url)))
                print("Method\\n----\\n{0}\\n".format(str(request.method)))
                print("Args\\n----\\n{0}\\n".format(str(request.args)))
                print("Headers\\n-------\\n{0}\\n".format(str(request.headers)))
                print("Files\\n-----\\n{0}\\n".format(str(request.files)))
                print("Form\\n-----\\n{0}\\n".format(str(request.form)))
                print("Data\\n-----\\n{0}\\n".format(str(request.data)))
                print(Style.RESET_ALL)

                try:
                    resp = json.loads(json.dumps('%s'))
                except ValueError:
                    resp = str('%s')

                return Response(**{"mimetype": "application/json", "response": resp})
            """ % (endpoint_name, rule["response"], rule["response"]), "<string>", "exec")

            ns = {
                "json": json,
                "Fore": Fore,
                "Style": Style,
                "Response": Response,
            }
            exec(code, ns)

            self.__setattr__(endpoint_name, ns[endpoint_name])

        self.url_map = Map(rule_objs)

    def dispatch_request(self, request):
        """Match and dispatch request"""
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, endpoint)(request, **values)
        except NotFound as e:
            return abort(404)
        except HTTPException as e:
            return e

    def wsgi_app(self, environ, start_response):
        """Build request context, route and respond"""
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


class HTTPInterceptorCLI(argparse.ArgumentParser):
    info = ({
        'prog': 'HTTP interceptors',
        'description': 'Simple HTTP interceptor',
    })

    def __init__(self):
        super(HTTPInterceptorCLI, self).__init__(**self.info)

        self.add_argument(
            'rules', type=json.loads, help='List of dicts representing url rules'
        )
        self.add_argument(
            '-p', '--port', type=int,
            default=8080, dest='port', help='HTTP port'
        )

    def run(self, args=None):
        """Runs the interceptor with the specified rules"""
        app = Interceptor(args.rules)
        run_simple('localhost', args.port, app)


def execute():
    cli = HTTPInterceptorCLI()
    cli.run(cli.parse_args())


if __name__ == "__main__":
    execute()
