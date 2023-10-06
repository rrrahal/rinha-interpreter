from context import Context

def interpret(node, ctx = Context()):
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
    case 'Let':
      return interpret_let(node, ctx)
    case 'Function':
      return interpret_function(node, ctx)
    case 'Call':
      return interpret_call(node, ctx)
    case 'Var':
      return interpret_var(node, ctx)
    case 'If':
      return interpret_if(node, ctx)
    case 'Binary':
      return interpret_binary(node, ctx)
    case 'Int':
      return int(node['value'])
    case _: raise Exception('Invalid node')

def interpret_print(node, ctx):
  # Exemplos que devem ser válidos: print(a), print("a"), print(2), print(true), print((1, 2))
  # TODO: Testar todos os exemplos
  value = interpret_term(node['value'], ctx)
  print(str(value))
  return value


def interpret_let(node, ctx):
  name = interpret_parameter(node['name'], ctx)

  value = interpret_term(node['value'], ctx)

  ctx.add(name, value)

  return interpret_term(node['next'], ctx)


def interpret_parameter(node, ctx):
  text = node['text']

  return text


def interpret_function(node, ctx):
  parameters = list(map(lambda parameter: interpret_parameter(parameter, ctx), node['parameters']))

  return {
    "parameters": parameters,
    "source": node['value']
  }


def interpret_call(node, ctx):
  callee = interpret_term(node['callee'], ctx)
  # Callee has to be a function oject

  parameters = callee['parameters']

  # TODO: Conferir se é assim que se lança erro
  #if len(node['arguments']) != len(parameters):
  #  raise Exception('Invalid number of arguments')
  new_ctx = Context(ctx)
  for (idx, argument) in enumerate(node['arguments']):

    value = interpret_term(argument, new_ctx)
    name = parameters[idx]
    # TODO: Criar um context novo dentro da função, podendo olhar pro contexto de fora
    # Contexto precisa morrer depois de ser usado
    new_ctx.add(name, value)

  return interpret_term(callee['source'], new_ctx)


def interpret_var(node, ctx):
  return ctx.get(node['text'])

def interpret_if(node, ctx):
  # TODO: isso aqui talvez de problema, rever, onde lança exceção?
  condition = interpret_term(node['condition'], ctx)

  if condition:
    return interpret_term(node['then'], ctx)
  else:
    return interpret_term(node['otherwise'], ctx)


def interpret_binary(node, ctx):
  # TODO: isso aqui talvez de problema, rever, onde lança exceção?
  left = interpret_term(node['lhs'], ctx)
  right = interpret_term(node['rhs'], ctx)
  op = node['op']

  match op:
    case 'Eq': return left == right
    case 'Add': return left + right
    case 'Sub': return left - right
    case 'Lt': return left < right
    case 'Or': return left or right
    case _: raise Exception('Invalid operator', op)
