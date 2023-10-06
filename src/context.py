class Context:
  def __init__(self, upper_ctx = None) -> None:
    self.ctx = {}
    if upper_ctx:
      self.upper_ctx = upper_ctx


  def get(self, value):
    if value in self.ctx:
      return self.ctx[value]

    if hasattr(self, 'upper_ctx'):
      return self.upper_ctx.get(value)

    raise Exception(f'Variable {value} not found')
  

  def add(self, key, value):
    self.ctx[key] = value

