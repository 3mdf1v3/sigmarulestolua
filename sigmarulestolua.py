#!/bin/python3
import yaml
import glob

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

    sourcePAthRules = '~/Documents/sigma/'
    source = {
        'apt': 'CommandLine',
        'proxy': 'UserAgent',
        'windows/process_creation': 'CommandLine'
    }

    for directory,extractField in source.items():

        path = sourcePAthRules + directory
        files = [f for f in glob.glob(path + "**/*.yml", recursive=True)]
        fileDstName = directory.replace('/', '_') + '_' + extractField + '.txt'
        fileDst = open(fileDstName,'w') 

        for file in files:        
            with open(file, 'r') as yamlFile:
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
