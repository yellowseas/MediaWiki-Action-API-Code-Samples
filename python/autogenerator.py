#!/usr/bin/python3

"""
    autogenerator.py

    MediaWiki Action API Code Samples
    Generates python and javascript files for all demos of MediaWiki API supported
    actions that support GET Requests only and can be easily built
    from a JSON Schema.

    MIT License
"""
import pathlib
import json

class CodeGeneratorBackend:
    """ A python code generator backend. Code borrowed from
    http://effbot.org/zone/python-code-generator.htm """

    def __init__(self, tab="\t"):
        """ Declare variables """
        self.code = []
        self.tab = tab
        self.level = 0

    def end(self):
        """ Get the complete code string """
        return "".join(self.code)

    def write(self, string):
        """ Append code line to a string """
        self.code.append(self.tab * self.level + string)

    def indent(self):
        """ Indent a line of code """
        self.level = self.level + 1

    def dedent(self):
        """ Dedent a line of code """
        self.level = self.level - 1

def make_file():
    """ Generate a file... """
    code = CodeGeneratorBackend(tab="    ")

    file = open('../modules.json', 'r')
    modules = json.load(file)
    file.close()

    for module in modules:
        python_file_name = module['filename'] + '.py'
        file = pathlib.Path(python_file_name)

        if file.exists():
            print('`' + python_file_name + "`: already exists, cannot re-write!")
        else:
            code.code = []
            code.write('#This file is auto-generated. See modules.json and '\
                'autogenerator.py for details\n\n')
            code.write('#!/usr/bin/python3\n\n')
            code.write('"""\n')
            code.indent()
            code.write(python_file_name + '\n\n')
            code.write('MediaWiki Action API Code Samples\n')
            code.write(module['docstring'] + '\n\n')
            code.write('MIT License\n')
            code.dedent()
            code.write('"""\n\n')
            code.write('import requests\n\n')
            code.write('S = requests.Session()\n\n')
            code.write('URL = "' + module['endpoint'] + '"\n\n')
            code.write('PARAMS = {\n')
            code.indent()

            for i, param in enumerate(module['params']):
                param_str = '"' + param + '": "' + module['params'][param]
                if i < (len(module['params'])-1):
                    code.write(param_str + '",\n')
                else:
                    code.write(param_str + '"\n')

            code.dedent()
            code.write('}\n\n')
            code.write('R = S.get(url=URL, params=PARAMS)\n')
            code.write('DATA = R.json()\n\n')
            code.write('print(DATA)\n')

            file = open(python_file_name, 'w')
            file.write(code.end())
            file.close()

            print('`' + python_file_name + "`: generated")

def make_javascript_file():
    """ Generate a file... """
    code = CodeGeneratorBackend(tab="    ")

    file = open('../modules.json', 'r')
    modules = json.load(file)
    file.close()

    for module in modules:
        javascript_file_name = module['filename'].split('.',1)
        javascript_file_name = javascript_file_name[0] + '.js'
        file = pathlib.Path(javascript_file_name)

        if file.exists():
            print('`' + javascript_file_name + "`: already exists, cannot re-write!")
        else:
            code.code = []
            code.write('//This file is autogenerated\n\n')
            code.write('let URL = "' + module['endpoint'] + '"; \n\n')
            code.write('const params = {\n')
            code.indent()

            for i, param in enumerate(module['params']):
                param_str =  param + ': "' + module['params'][param]
                if i < (len(module['params'])-1):
                    code.write(param_str + '",\n')
                else:
                    code.write(param_str + '"\n')

            code.dedent()
            code.write('}\n\n')
            code.write('URL = URL + "?origin=*";\n')
            code.write('Object.keys(params).forEach(key => URL = URL + "&" + key + "=" + params[key]);\n\n')
            code.write('fetch(URL)\n')
            code.indent()
            code.write('.then(response => response.json())\n')
            code.write('.then(response => console.log(response))\n')
            code.write('.catch(error=>console.log(error))\n')
            code.dedent()

            file = open(javascript_file_name, 'w')
            file.write(code.end())
            file.close()

            print('`' + javascript_file_name + "`: generated")

if __name__ == '__main__':
    make_file()
    make_javascript_file()
