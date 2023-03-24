import re

def semantic_analyzer(code):
    variables = {}
    count_lines = 0
    verify_integrity = 0
    
    # Regex
    declarationPattern = re.compile(r"(int|char) (\w+)(\[[0-9]*\])?;")
    findVarPattern = r"\b([a-zA-Z_][a-zA-Z0-9_]*(?:\[[0-9]+\])?)\b"
    complexDeclarationPattern = re.compile(r"(int|char) ((\w+)(\[\w+])?, )+((\w+)(\[\w+])?;)")
    mathPattern = r"([a-zA-Z]+\d*)\s*=\s*([a-zA-Z]+\d*)\s*([-+*/])\s*([a-zA-Z]+\d*)\s*([-+*/])\s*([a-zA-Z]+\d*);"
    assignmentMathPattern = re.compile(mathPattern)
    functionCallPattern = re.compile(r"(\w+)\s*\((.*?)\);")
    printPattern = re.compile(r'print\("([^"]+)"\s*,\s*(.*)\)')
    simplePrintPattern = re.compile(r'print\(\"\w*\"\);')
    simpleAtribPattern = re.compile(r"(\w+)\s*=\s*(\w+);")
    varToVarPattern = re.compile(r"([a-zA-Z]+) = ([a-zA-Z]+);")
    varToNumber = re.compile(r"([a-zA-Z]+) = ([0-9]+);")
    varToString = re.compile(r"([a-zA-Z]+)\s*=\s*\"\w*\";")
    lines = code.splitlines()

    for line in lines:
        verify_integrity = -1
        count_lines += 1

        declarationMatcher = declarationPattern.search(line)
        if declarationMatcher:
            verify_integrity = 0
            varType = declarationMatcher.group(1)
            varName = declarationMatcher.group(2)
            variables[varName] = varType
        
        complexDeclarationMatcher = complexDeclarationPattern.search(line)
        if complexDeclarationMatcher:
            verify_integrity = 0
            getVariables = re.findall(findVarPattern, complexDeclarationMatcher.group())
            varType = getVariables[0]
            for index, var in enumerate(getVariables):
                if index != 0:
                    variables[var] = varType
        
        assignmentMathMatcher = assignmentMathPattern.search(line)
        if assignmentMathMatcher:
            verify_integrity = 0
            varType1 = variables.get(assignmentMathMatcher.group(1))
            varType2 = variables.get(assignmentMathMatcher.group(2))
            varType3 = variables.get(assignmentMathMatcher.group(4))
            varType4 = variables.get(assignmentMathMatcher.group(6))
            if varType1 != "int" or varType2 != "int":
                print(f"Erro semântico: variável não declarada. Linha {count_lines}")
                return -1, count_lines 
            if varType3 != "int" or varType4 != "int":
                print(f"Erro semântico: variável não declarada. Linha {count_lines}")
                return -1, count_lines 

        functionCallMatcher = functionCallPattern.search(line)
        if functionCallMatcher:
            verify_integrity = 0
            functionName = functionCallMatcher.group(1)
            if functionName == "fie":
                try:
                    params = functionCallMatcher.group(2).split(",")
                    for param in params:
                        var = param.strip()
                        varType = variables.get(var)
                        if var[0] == '"' and var[len(var) - 1] == '"':
                            continue 
                        if not varType:
                            print(f"Erro semântico: chamada inválida da função fie. Linha {count_lines}")
                            return -1, count_lines 
                except Exception as e:
                    print(f"Erro semântico: chamada inválida da função fie. Linha {count_lines}")
                    return -1, count_lines 
            elif functionName == "print":
                printMatcher = printPattern.search(line)
                simplePrintMatcher = simplePrintPattern.search(line)
                if not printMatcher and not simplePrintMatcher:
                    print("entrei aq")
                    print(f"Erro semântico: chamada inválida da função print. Linha {count_lines}")
                    return -1, count_lines
                
                if printMatcher:
                    string = printMatcher.group(1)
                    if string.find("%"):
                        vars = printMatcher.group(2).split(",")
                        for var in vars:
                            param = var.strip()
                            varType = variables.get(param)
                            if not varType:
                                print(f"Erro semântico: chamada inválida da função print. Linha {count_lines}")
                                print("Variável {} não declarada".format(var))
                                return -1, count_lines 

        simpleAtribMatcher = simpleAtribPattern.search(line)
        if simpleAtribMatcher:
            verify_integrity = 0
            isVarToVar = varToVarPattern.search(line)
            if isVarToVar:
                var1 = isVarToVar.group(1)
                var2 = isVarToVar.group(2)
                varType1 = variables.get(var1)
                varType2 = variables.get(var2)
                if not varType1:
                    print(f"Variável {var1} não declarada. Linha {count_lines}")
                    return -1, count_lines 
                if not varType2:
                    print(f"Variável {var2} não declarada. Linha {count_lines}")
                    return -1, count_lines 
                continue
            isVarToNumber = varToNumber.search(line)
            if isVarToNumber:
                var = isVarToNumber.group(1)
                varType = variables.get(var)
                if not varType:
                    print(f"Variável {var} não declarada. Linha {count_lines}")
                    return -1, count_lines
                continue
            isVarToString = varToString.search(line)
            if isVarToString:
                var = isVarToNumber.group(1)
                print(var)
                varType = variables.get(var)
                if not varType:
                    print(f"Variável {var} não declarada. Linha {count_lines}")
                    return -1, count_lines 
        if verify_integrity == -1:
            return verify_integrity, count_lines
    return verify_integrity, count_lines
                
def readCodeFile():
    file = open('teste.txt', 'r')
    code = file.read()
    file.close()
    return code

code_test = readCodeFile()

verify, count_lines = semantic_analyzer(code_test)

if verify != -1:
    print("Compilado com sucesso!")
else:
    print(f"Erro, não foi possível compilar. Linha {count_lines}")