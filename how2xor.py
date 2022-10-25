import sys
from typing import Iterable, Union


class XORConstructor:
  def __init__(self, table: Union[str, bytes]):
    self.table = table.encode() if isinstance(table, str) else table

  def find(self, goal: Union[str, bytes], num: int, result_type: str='bytes', byteorder: str='little'):
    if result_type not in ['bytes', 'int', 'hex']:
      raise ValueError(f"result_type must 'bytes' or 'int' or 'hex'")
    if isinstance(goal, str):
      goal = str.encode(goal)
    result = [b'' for _ in range(num)]
    for c in goal:
      self._result = []
      self._dfs(c, num)
      result = [a + b for a, b in zip(result, self._result)]
      if len(self._result) == 0:
        print(f"Warning: could not find a way to get {c.to_bytes(1, 'little')}. Returns None", file=sys.stderr)
        return
    if result_type == 'bytes':
      return result
    result = [int.from_bytes(entry, byteorder) for entry in result]
    if result_type == 'int':
      return result
    return [hex(entry) for entry in result]

  def _dfs(self, goal, num, cur=0):
    if num == 0:
      return cur == goal
    for x in self.table:
      self._result.append(x.to_bytes(1, 'little'))
      if self._dfs(goal, num - 1, cur ^ x):
        return True
      self._result.pop()
    return False


if __name__ == '__main__':
  ctor = XORConstructor(sys.argv[1])
  print(ctor.find(sys.argv[2], int(sys.argv[3]), 'hex'))
