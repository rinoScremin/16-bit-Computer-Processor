def instructionParse(instruction):
	if instruction:
		operand = ""
		opCode = ""
		label = ""
		isLabel = False
		isOperand = False
		if instruction.find(' ;'):
			TEMP1 = instruction.split(" ;")
			instruction = str(TEMP1[0])
		spliteInstruc = instruction.split(" ")
		for i in range(0,len(spliteInstruc[0])):
			if ":" in spliteInstruc[0][i]:
				label = spliteInstruc[0]
				opCode = spliteInstruc[1]
				isLabel = True
				if len(spliteInstruc) >= 3:
					operand = spliteInstruc[2]
		if not isLabel:
			if len(spliteInstruc) == 1:
				opCode = spliteInstruc[0]
			if len(spliteInstruc) == 2:
				opCode = spliteInstruc[0]
				operand = spliteInstruc[1]		
		parsedCode = [label,opCode,operand]
		return parsedCode
	return ""
def GetMachineCode(instruction=[], instructions=[]):
	fullInstruction = "".join(instruction[1]) + " "+ "".join(instruction[2])
	temp2 = "".join(instruction[2]).split(",")
	halfInstr = "".join(instruction[1]) + " "+ "".join(temp2[0])
	spliteIn = []
	temp = [] 		
	for i in range(0,len(instructions)):		
		if instructions[i][1]:
			spliteIn = "".join(instructions[i][1]).split(" ")
			if "".join(instructions[i][1]).upper() in fullInstruction.upper():
				return [instruction[0],instruction[1],instruction[2],instructions[i][0],"","","",instructions[i][1],"",""]
	for i in range(0,len(instructions)):
		if instructions[i][1]:
			spliteIn = "".join(instructions[i][1]).split(" ")		
			if len(spliteIn) >= 2:
				#print(2)
				temp = "".join(spliteIn[1]).split(",")
				CMPhalf = "".join(spliteIn[0]) +" " +"".join(temp[0])
				if CMPhalf.upper() in halfInstr.upper():
					return [instruction[0],instruction[1],instruction[2],instructions[i][0],temp[1],temp2[1],"",instructions[i][1],"",""]
	return [[],[],[],[],[],[],[]]
def printInstruction(parsedInstruction=[]):
	for i in range(0, len(parsedInstruction)):
		print (parsedInstruction[i])
def link(instruction=[]):
	for i in range(0,len(instruction)):
		if instruction[i][0] and not DW(i,instruction):
			temp = "".join(instruction[i][0])
			temp=temp[0:len(temp)-1]
			if temp:
				for x in range(0,len(instruction)):
					temp2 = "".join(instruction[x][2])
					if temp in temp2:
						instruction[x][5] = instruction[i][6]		
def getNumberOfBitInInstruction(instruction=[]):	
	for i in range(0,len(instruction)):
		temp1 = str(instruction[i][7]).split(" ")
		if len(temp1) <= 1 and "".join(instruction[i][2]) and not DW(i,instruction):
			instruction[i][5]=instruction[i][2]
		if instruction[i][5]:
			if len(instruction[i][5]) <= 4:
				instruction[i][8] = 2
			if len(instruction[i][5]) == 8:
				instruction[i][8] = 3
		else:
			instruction[i][8] = 1
		if str(instruction[i][9]) and not DW(i,instruction):
			instruction[i][8] = 2
		if DW(i,instruction):
			instruction[i][8] = DW(i,instruction)[1]			
def assignMemoryAddress(instruction=[]):
	programCounter = 0
	for i in range(0,len(instruction)):
		if instruction[i][8] and not DW(i,instruction):
			if int(instruction[i][8]) == 1 and not DW(i,instruction):
				instruction[i][6] = hex(programCounter)[2:]
				programCounter+=1
			if int(instruction[i][8]) == 2 and not DW(i,instruction):
				instruction[i][6] = hex(programCounter)[2:]
				programCounter+=2
			if int(instruction[i][8]) == 3 and not DW(i,instruction):
				instruction[i][6] = hex(programCounter)[2:]
				programCounter+=3
		if DW(i,instruction):
			DWData = DW(i,instruction)
			instruction[i][6] = hex(programCounter)
			programCounter += DWData[1]			
def checkForMatchingLabel(instruction=[]):
	for i in range(0,len(instruction)):
		if instruction[i][0]:
			temp = "".join(instruction[i][0])
			temp=temp[0:len(temp)-1]
			if temp:
				for x in range(0,len(instruction)):
					temp2 = "".join(instruction[x][2])
					if temp in temp2:
						instruction[x][9] = 1
def assemble(instruction=[]):
	outPut = ""
	for i in range(0,len(instruction)):
		if instruction[i][8] and not DW(i,instruction):
			if int(instruction[i][8]) == 1:
				outPut += "".join(instruction[i][3]) + " " 
			if int(instruction[i][8]) == 2:
				outPut += "".join(instruction[i][3]) + " " + str(instruction[i][5]) + " "
			if int(instruction[i][8]) == 3:
				outPut += "".join(instruction[i][3]) + " " + str(instruction[i][5])[0:4]+ " " + str(instruction[i][5])[4:8]+" "
		if DW(i,instruction):
			outPut += DW(i,instruction)[0]
	return outPut
def DW(index,instruction=[]):
	count=0
	tempstr=""
	pc=0
	if "DW" in str(instruction[index][1]).upper():
		if str(instruction[index][0]):
			instruction[index][9] = 1
		operand = instruction[index][2]
		for x in range(0,len(operand)):
			tempstr+=operand[x]
			count+=1
			if count == 4:
				tempstr+=" "
				count=0
				pc+=1
		if count > 0:
			tempstr+=" "
			pc+=1
		return [tempstr,pc]
	return ""
def linkDW(instruction,outBits):
	ParsedBits = outBits.split(" ")
	returnStr = "" 
	for i in range(0,len(ParsedBits)):
		bit = ParsedBits[i]
		for x in range(0,len(instruction)):
			ParsedLabel = str(instruction[x][0])[:-1]
			ParsedOpCode = str(instruction[x][1])
			if ParsedLabel and ParsedLabel in bit and "DW" in ParsedOpCode.upper():
				ParsedBits[i] = str(instruction[x][6])[2:]
	for i in range(0,len(ParsedBits)):
		returnStr += str(ParsedBits[i])+" "
	return returnStr
opCodes = [
		[["6"],["MOV A,A"]],[["8"],["MOV A,B"]],[["a"],["MOV A,C"]],
		[["c"],["MOV A,D"]],[["e"],["MOV A,E"]],[["10"],["MOV A,H"]],
		[["12"],["MOV A,L"]],[["14"],["MOV A,M"]],[["17"],["MOV B,A"]],
		[["19"],["MOV B,B"]],[["1b"],["MOV B,C"]],[["1d"],["MOV B,D"]],
		[["1f"],["MOV B,E"]],[["21"],["MOV B,H"]],[["23"],["MOV B,L"]],
		[["25"],["MOV B,M"]],[["28"],["MOV C,A"]],[["2a"],["MOV C,B"]],
		[["2c"],["MOV C,C"]],[["2e"],["MOV C,D"]],[["30"],["MOV C,E"]],
		[["32"],["MOV C,L"]],[["34"],["MOV C,H"]],[["36"],["MOV C,M"]],
		[["39"],["MOV D,A"]],[["3b"],["MOV D,B"]],[["3d"],["MOV D,C"]],
		[["3f"],["MOV D,D"]],[["41"],["MOV D,E"]],[["43"],["MOV D,L"]],
		[["45"],["MOV D,H"]],[["47"],["MOV D,M"]],[["4a"],["MOV E,A"]],
		[["4c"],["MOV E,B"]],[["4e"],["MOV E,C"]],[["50"],["MOV E,D"]],
		[["52"],["MOV E,E"]],[["54"],["MOV E,L"]],[["56"],["MOV E,H"]],
		[["58"],["MOV E,M"]],[["5b"],["MOV L,A"]],[["5d"],["MOV L,B"]],
		[["5f"],["MOV L,C"]],[["61"],["MOV L,D"]],[["63"],["MOV L,E"]],
		[["65"],["MOV L,H"]],[["67"],["MOV L,L"]],[["69"],["MOV L,M"]],
		[["6c"],["MOV H,A"]],[["6e"],["MOV H,B"]],[["70"],["MOV H,C"]],
		[["72"],["MOV H,D"]],[["74"],["MOV H,E"]],[["76"],["MOV H,L"]],
		[["78"],["MOV H,H"]],[["7a"],["MOV H,M"]],[["7d"],["MOV M,A"]],
		[["80"],["MOV M,B"]],[["83"],["MOV M,C"]],[["86"],["MOV M,D"]],
		[["89"],["MOV M,E"]],[["8c"],["MOV M,L"]],[["8f"],["MOV M,H"]],
		[["92"],["MVI A,dd"]],[["95"],["MVI B,dd"]],[["98"],["MVI C,dd"]],
		[["301"],["MVI D,dd"]],[["9e"],["MVI E,dd"]],[["a1"],["MVI H,dd"]],
		[["a4"],["MVI L,dd"]],[["a7"],["LXI B,dddd"]],[["ac"],["LXI D,dddd"]],
		[["b6"],["LDAX B"]],[["b9"],["LDAX D"]],[["bc"],["LHLD"]],
		[["b1"],["LXI H,dddd"]],[["c3"],["LD A,aa"]],[["c6"],["ST A,aa"]],
		[["cb"],["ATAX B"]],[["c7"],["ATAX D"]],[["ce"],["SHLD"]],
		[["e1"],["XCHG"]],[["de"],["ADD A"]],[["e1"],["ADD B"]],
		[["e4"],["ADD C"]],[["e7"],["ADD D"]],[["ea"],["ADD E"]],
		[["ed"],["ADD H"]],[["f0"],["ADD L"]],[["f3"],["ADD M"]],
		[["03"],["NOP"]],[["05"],["HULT"]],[["da"],["STC"]],[["dc"],["CMC"]],
		[["f7"],["ADC A"]],[["fb"],["ADC B"]],[["ff"],["ADC C"]],[["103"],["ADC D"]],
		[["107"],["ADC E"]],[["10b"],["ADC H"]],[["10f"],["ADC L"]],[["113"],["ADC M"]],
		[["11b"],["SUB B"]],[["11e"],["SUB C"]],[["121"],["SUB D"]],[["124"],["SUB E"]],
		[["127"],["SUB H"]],[["12a"],["SUB L"]],[["12d"],["SUB M"]],[["131"],["SBB A"]],
		[["135"],["SBB B"]],[["139"],["SBB C"]],[["13d"],["SBB D"]],[["141"],["SBB E"]],
		[["145"],["SBB H"]],[["149"],["SBB L"]],[["14d"],["DAD M"]],[["118"],["SUB A"]],
		[["152"],["DAD B"]],[["159"],["DAD D"]],[["160"],["DAD H"]],[["167"],["ADI"]],
		[["16b"],["ACI"]],[["170"],["SUI"]],[["174"],["SBI"]],[["179"],["DAA"]],
		[["194"],["XRA A"]],[["197"],["XRA B"]],[["19a"],["XRA C"]],[["19d"],["XRA D"]],
		[["1a0"],["XRA E"]],[["13a"],["XRA H"]],[["1a6"],["XRA L"]],[["1a9"],["XRA M"]],
		[["1ad"],["ORA A"]],[["1b0"],["ORA B"]],[["1b3"],["ORA C"]],[["1b6"],["ORA D"]],
		[["1b9"],["ORA E"]],[["1bc"],["ORA H"]],[["1bf"],["ORA L"]],[["1c2"],["ORA M"]],
		[["17b"],["AND A"]],[["17e"],["AND B"]],[["181"],["AND C"]],[["184"],["AND D"]],
		[["187"],["AND E"]],[["18a"],["AND H"]],[["18d"],["AND L"]],[["190"],["AND M"]],
		[["1c6"],["ANI"]],[["1ca"],["XRI"]],[["1ce"],["ORI"]],[["1d2"],["CMA"]],
		[["1d4"],["RLC"]],[["1d8"],["RRC"]],[["1dc"],["RAR"]],[["1de"],["RAL"]],
		[["1e0"],["INR A"]],[["1e2"],["INR B"]],[["1e4"],["INR C"]],[["1e6"],["INR D"]],
		[["1e8"],["INR E"]],[["1ea"],["INR H"]],[["1ec"],["INR L"]],[["1fc"],["INR M"]],
		[["1ee"],["DCR A"]],[["1f0"],["DCR B"]],[["1f2"],["DCR C"]],[["1f4"],["DCR D"]],
		[["1f6"],["DCR E"]],[["1f8"],["DCR H"]],[["1fa"],["DCR L"]],[["201"],["DCR M"]],
		[["206"],["INX B"]],[["209"],["INX D"]],[["20c"],["INX H"]],[["20f"],["DCX B"]],
		[["212"],["DCX D"]],[["215"],["DCX H"]],[["218"],["JMP"]],[["21a"],["PCHL"]],
		[["21d"],["CMP A"]],[["220"],["CMP B"]],[["223"],["CMP C"]],[["226"],["CMP D"]],
		[["229"],["CMP E"]],[["22c"],["CMP H"]],[["22f"],["CMP L"]],[["232"],["CMP M"]],[["236"],["CPI"]],
		[["23d"],["JNZ"]],[["23a"],["JZ"]],[["240"],["JNC"]],[["243"],["JC"]],
		[["246"],["JPO"]],[["249"],["JPE"]],[["24c"],["JP"]],[["24f"],["JM"]],
		[["252"],["CALL"]],[["258"],["CNZ"]],[["25f"],["CZ"]],[["266"],["CC"]],
		[["26d"],["CNC"]],[["274"],["CPE"]],[["27b"],["CPO"]],[["282"],["CP"]],[["281"],["CM"]],		
		[["290"],["RET"]],[["293"],["RNZ"]],[["297"],["RZ"]],[["29b"],["RC"]],
		[["29f"],["RNC"]],[["2a3"],["RPE"]],[["2a7"],["RPO"]],[["2ab"],["RP"]],[["2af"],["RM"]],
		[["2b3"],["LXI SP,dddd"]],[["2b6"],["DAD SP"]],[["2b9"],["INX SP"]],[["2bb"],["DCX SP"]],
		[["2bd"],["PUSH B"]],[["2c4"],["PUSH D"]],[["2cb"],["PUSH H"]],[["2d3"],["PUSH PSW"]],[["2da"],["POP B"]],
		[["2df"],["POP D"]],[["2e4"],["POP H"]],[["2e9"],["POP PSW"]],[["2ee"],["XTHL"]],
		[["2f7"],["SPHL"]],[["2f9"],["IN1"]],[["2fb"],["IN2"]],[["2fd"],["OUT1"]],[["2ff"],["OUT2"]],[["301"],["ORG"]],[[""],["DW"]],
		]				

file = open("/Users/Rino/Desktop/8080test.txt")
parsedInstruction = []
finalOut = ""
programCodeString = file.read()
Codes = programCodeString.split("\n")
refindProgramCode = []

for i in range(0, len(Codes)):
	if Codes[i]:
		refindProgramCode.append(Codes[i].strip())
for i in range(0, len(refindProgramCode)):
	if instructionParse(refindProgramCode[i]):
		parsedInstruction.append(GetMachineCode(instructionParse(refindProgramCode[i]),opCodes))
		
checkForMatchingLabel(parsedInstruction)
getNumberOfBitInInstruction(parsedInstruction)
assignMemoryAddress(parsedInstruction)
link(parsedInstruction)
finalOut=assemble(parsedInstruction)
finalOut=linkDW(parsedInstruction,finalOut)
printInstruction(parsedInstruction)	
finalOut="v2.0 raw\n"+finalOut
print(finalOut)

f= open("output.txt","w+")
f.write(finalOut)
f.close() 