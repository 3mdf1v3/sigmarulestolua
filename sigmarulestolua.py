#!/bin/python3
import yaml
import glob
from pathlib import Path

def luaPatterm(value):

    value = value.replace('%', '%%')
    value = value.replace('\\', '\\\\')  
    value = value.replace(r"'", r"\'")
    value = value.replace(r'"', r'\"')  
    value = value.replace('#', '%#')  
    value = value.replace('.', '%.')
    value = value.replace(',', '%,')
    value = value.replace(';', '%;')
    value = value.replace('<', '%<')
    value = value.replace('>', '%>')
    value = value.replace('|', '%|')
    value = value.replace('=', '%=')
    value = value.replace('?', '%?')
    value = value.replace('[', '\[')
    value = value.replace(']', '\]')
    value = value.replace('(', '%(')
    value = value.replace(')', '%)')
    value = value.replace('&', '%&')
    value = value.replace('$', '%$')
    value = value.replace('+', '%+')
    value = value.replace('-', '%-')
    value = value.replace(':', '%:')    

    if not value.endswith('*'): 
        value = value + '$'
    if not value.startswith('*'): 
        value = '^' + value 

    value = value.replace('*', '.+')
    value = '"' + value + '",'

    return value

def main():

    home = str(Path.home())
    sourcePathRules = home + '/Documents/sigma/rules/'
    source = {
        'apt': 'CommandLine',
        'proxy': 'UserAgent',
        'windows/process_creation': 'CommandLine'
    }

    for directory,extractField in source.items():

        path = sourcePathRules + directory
        filesSrc = [f for f in glob.glob(path + "**/*.yml", recursive=True)]
        directory = directory.replace('/', '_')
        fileDstName = directory + '_' + extractField + '.txt'
        fileDst = open(fileDstName,'w') 

        for fileSrc in filesSrc:    
            with open(fileSrc, 'r') as yamlFile:
                dictionaries = yaml.load_all(yamlFile, Loader=yaml.SafeLoader)
                for dictionary in dictionaries:
                    detection = dictionary.get('detection')
                    if detection is not None:
                        for k1,v1 in detection.items():
                            if type(v1) == dict:
                               for k2,v2 in v1.items():
                                  if k2 == extractField: 
                                    if type(v2) == list:
                                        for i in v2:
                                            fileDst.write(luaPatterm(i))
                                    else:   
                                            fileDst.write(luaPatterm(v2))
        fileDst.close

if __name__== "__main__":
  main()
