

def interpret(node, ctx):
  if not node.get('kind'):
    return interpret_file(node, ctx)


def interpret_file(node, ctx):
  term = node['expression']
  return interpret_term(term, ctx)


def interpret_term(node, ctx):
  match node['kind']:
    case 'Print':
      return interpret_print(node, ctx)
    case 'Str':
      return node['value']

def interpret_print(node, ctx):
  # Exemplos que devem ser válidos: print(a), print("a"), print(2), print(true), print((1, 2))
  # TODO: Testar todos os exemplos
  value = interpret_term(node['value'], ctx)
  print(str(value))
  return value
