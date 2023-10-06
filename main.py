import json
from interpreter import interpret

def main():
  # read the file from souce/print.json
  source_code = open('source/combination.json', 'r').read()
  AST = json.loads(source_code)
  interpret(AST)

main()
