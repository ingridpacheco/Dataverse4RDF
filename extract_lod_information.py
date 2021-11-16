import re

content = '<dataDscr>'

count = 1

def create_DDI_file(file):
    global content
    prefixes = get_prefixes(file)
    insert_prefixes(prefixes,file)
    content = content + '</dataDscr>'
    return content

def get_variables(prefix, data):
    lines = data.split('\n')
    lines = list(filter(lambda line: '@prefix' not in line and prefix in line, lines))
    p = re.compile(rf'{prefix}\w+')
    result = []
    
    for line in lines:
        match = p.findall(line)
        if len(match) != 0 and match[0] not in result:
            result.append(match[0])

    return result

def insert_variables(variables, prefixes):
    global content, count

    for variable in variables:
        variableParts = variable.split(':')
        variablePrefix = variableParts[0] + ':'
        variableUri = prefixes[variablePrefix]
        variableUri = variableUri[1:len(variableUri) - 2]
        variableUri = variableUri + "/" + variableParts[1]

        content = content + f'''
            <var ID="v{count}" name="{variable}">
                <labl level="variable">{variableUri}</labl>
                <varFormat type="character"/>
            </var>
        '''
        count = count + 1

def insert_prefixes(prefixes, data):
    global content, count

    identifiers = ''
    group_count = 2
    prefix_keys = prefixes.keys()
    for i in range(1, len(prefix_keys) + 1):
        if (i == len(prefix_keys)):
            identifiers = identifiers + f'v{i}'
        else:
            identifiers = identifiers + f'v{i} '

    content = content + f'''
        <varGrp ID="VG1" var={identifiers}>
            <labl>Prefixes</labl>
        </varGrp>
    '''
    
    for prefix in prefixes.items():
        prefix = list(prefix)
        prefix[1] = prefix[1][1:len(prefix[1]) - 2]
        content = content + f'''
            <var ID="v{count}" name="{prefix[0]}">
                <labl level"variable">{prefix[1]}</labl>
                <varFormat type="character"/>
            </var>
        '''
        count = count + 1
        variables = get_variables(prefix[0], data)
        identifiers = ''
        
        for i in range(count, len(variables) + count):
            if (i == len(variables) + count - 1):
                identifiers = identifiers + f'v{i}'
            else:
                identifiers = identifiers + f'v{i} '

        content = content + f'''
            <varGrp ID="VG{group_count}" var="{identifiers}">
                <labl>{prefix[0]}</labl>
            </varGrp>
        '''

        group_count = group_count + 1

        insert_variables(variables, prefixes)

def get_prefixes(data):
    lines = data.split('\n')
    lines = list(filter(lambda line: '@prefix' in line, lines))
    prefixes = {}

    for line in lines:
        prefix = line.split(': ')
        prefix_key = prefix[0].split('@prefix ')[1] + ':'
        prefix_value = prefix[1].split(' .')[0]
        prefixes[prefix_key] = prefix_value

    return prefixes