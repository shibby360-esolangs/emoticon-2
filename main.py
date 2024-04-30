# Tasklist:
import math, re, random, os, json, sys
math.round = round
def lnlog(b):
  return math.log(b)
math.ln = lnlog
from simpleeval import simple_eval
f = open('main')
# sourcecode = f.read()
sourcecode = sys.argv[1]
f.close()
def emoticon2(code, variables, curvar, ifs, loops, functions):
  def number(st):
    try:
      return int(st)
    except ValueError:
      return float(st)
  def seval(expr):
    return simple_eval(expr, names=variables)
  def value(v):
    if '${' in v:
      return variables[v[2:-1]]
    else:
      try:
        return number(v)
      except ValueError:
        return v
  def upsertVar(val, var):
    if type(variables[var]) == list:
      variables[var].append(val)
    else:
      variables[var] = val
  ncode = code.split()
  while variables['_counter'] < len(ncode):
    inccounter = True
    cmd = ncode[variables['_counter']]
    if cmd.startswith(':'):
      ncmd = cmd[1:cmd.find('-')]
      prms = cmd[cmd.find('-'):].split('-')[1:]
      if ncmd == '<':
        opt = value(prms[0])
        if opt == 's':
          print(' ', end='')
        elif opt == 'n':
          print('\n', end='')
        elif opt == 'c':
          os.system('clear')
        else:
          print(variables[curvar], end='')
      elif ncmd == '>':
        w = {'n':number,'s':str}[value(prms[1])]
        upsertVar(w(input(variables[curvar])), prms[0])
      elif ncmd == '#':
        curvar = prms[0]
        if curvar not in variables:
          variables[curvar] = ''
      elif ncmd == 'M':
        upsertVar(seval(prms[0] + value(prms[1]).replace('~','-').replace('^','**') + prms[2]), curvar)
      elif ncmd == 'm':
        upsertVar(seval('_math.'+value(prms[0])+'('+prms[1]+')'), curvar)
      elif ncmd == '(':
        loops[prms[0]] = variables['_counter']
        if not variables[prms[1]]:
          variables['_counter'] = ncode.index(':)-' + prms[0], variables['_counter'])
      elif ncmd == ')' or ncmd == '(^)':
        variables['_counter'] = loops[prms[0]]
        inccounter = False
      elif ncmd == '?':
        upsertVar(seval(prms[0] + value(prms[1]) + prms[2]), curvar)
      elif ncmd == '?<':
        if not seval(prms[0] + value(prms[1]) + prms[2]):
          r = re.compile(r":<\?>.*?"+prms[3])
          nxtcondl = list(filter(r.match, ncode[variables['_counter']+1:]))
          if len(nxtcondl) == 0:
            if ':>?-'+prms[3] in ncode:
              variables['_counter'] = ncode.index(':>?-' + prms[3])
            else:
              variables['_counter'] = ncode.index(':?|-'+prms[3])
          elif nxtcondl[0] in ncode:
            variables['_counter'] = ncode.index(nxtcondl[0], variables['_counter']) - 1
          else:
            if ':>?-'+prms[3] in ncode:
              variables['_counter'] = ncode.index(':>?-' + prms[3])
            else:
              variables['_counter'] = ncode.index(':?|-'+prms[3])
        else:
          ifs[prms[3]] = True
      elif ncmd == '<?>':
        if prms[3] in ifs:
          variables['_counter'] = ncode.index(':?|-'+prms[3])
          continue
        if not seval(prms[0] + value(prms[1]) + prms[2]):
          r = re.compile(r":<\?>.*?"+prms[3])
          nxtcondl = list(filter(r.match, ncode[variables['_counter']+1:]))
          if len(nxtcondl) == 0:
            if ':>?-'+prms[3] in ncode:
              variables['_counter'] = ncode.index(':>?-' + prms[3])
            else:
              variables['_counter'] = ncode.index(':?|-'+prms[3])
          elif nxtcondl[0] in ncode:
            variables['_counter'] = ncode.index(nxtcondl[0], variables['_counter']) - 1
          else:
            if ':>?-'+prms[3] in ncode:
              variables['_counter'] = ncode.index(':>?-' + prms[3])
            else:
              variables['_counter'] = ncode.index(':?|-'+prms[3])
        else:
          ifs[prms[3]] = True
      elif ncmd == '>?':
        if prms[0] in ifs:
          variables['_counter'] = ncode.index(':?|-'+prms[0])
          continue
      elif ncmd == '?|':
        if prms[0] in ifs:
          del ifs[prms[0]]
      elif ncmd == 'v~v':
        if value(prms[0]) == 'n':
          variables[curvar] = number(variables[curvar])
        elif prms[0] == 's':
          variables[curvar] = str(variables[curvar])
      elif ncmd == '||':
        variables[curvar] = variables[curvar][value(prms[0])]
      elif ncmd == '>=>':
        if type(variables[curvar]) == list:
          variables[prms[0]] = variables[curvar].copy()
        else:
          variables[prms[0]] = variables[curvar]
      elif ncmd == '`/':
        del variables[curvar]
        curvar = '_'
      elif ncmd == 'XX':
        return
      elif ncmd == '??':
        upsertVar(random.uniform(0,1), curvar)
      elif ncmd == '[]<':
        if len(prms) == 1:
          variables[curvar].append(variables[prms[0]])
        else:
          variables[curvar].insert(value(prms[1]), variables[prms[0]])
      elif ncmd == '[]v^':
        variables[curvar][value(prms[1])] = variables[prms[0]]
      elif ncmd == '</>{':
        endind = ncode.index(':}<>/-' + prms[0], variables['_counter'])
        functions[prms[0]] = ' '.join(ncode[variables['_counter']+1:endind])
        variables['_counter'] = endind
      elif ncmd == '}<>/':
        pass
      elif ncmd.startswith('<') and ncmd.endswith('>'):
        vars = variables.copy()
        vars['_counter'] = 0
        for i in range(0, len(prms)):
          vars['_' + str(i)] = value(prms[i])
        vars['_return'] = ''
        emoticon2(functions[ncmd[1:-1]], vars, curvar, ifs.copy(), loops.copy(), functions.copy())
        upsertVar(vars['_return'], curvar)
      elif ncmd == '{@}':
        print('\n=>\nprogram info:')
        print('current variable: ' + curvar)
        print('value: ' + str(variables[curvar]))
        vars = variables.copy()
        vars['_math'] = str(vars['_math'])
        print('variables: ' + json.dumps(vars,indent=2))
        print('loops: ' + json.dumps(loops,indent=2))
        print('ifs: ' + json.dumps(ifs,indent=2))
      else:
        print('\ni don\'t know what to do with a ' + cmd)
        return
    elif cmd.startswith('*'):
      pass
    else:
      try:
        upsertVar(number(cmd), curvar)
      except ValueError:
        upsertVar(cmd, curvar)
    if inccounter:
      variables['_counter'] += 1
emoticon2(sourcecode, {'_': '', '_counter':0, '_true':True, '_false':False, '_math':math, '_list':[], '_math_pi':math.pi, '_math_e':math.e}, '_', {}, {}, {})