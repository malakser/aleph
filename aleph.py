import os
import time
import re
from openai import OpenAI
from prompt import prompt

MEM_SIZE = 65536

buf = bytearray(MEM_SIZE)  # Initialize with spaces
buf[:] = b' ' * MEM_SIZE

def gettag(t, s):
  return re.findall(f'<{t}\\b.*?>.*?</{t}>', s, re.DOTALL)

client = OpenAI(
    base_url="https://api.studio.nebius.ai/v1/",
    api_key=os.environ.get("NEBIUS_API_KEY"),
)

def write(a, s):
  buf[a:a + len(s.encode('utf-8'))] = s.encode('utf-8')


def read(a, n):
  return buf[a:a + n].decode('utf-8', errors='replace')




def ask(p):
  comp_res = client.chat.completions.create(
      #model="meta-llama/Meta-Llama-3.1-405B-Instruct",
      #model="meta-llama/Meta-Llama-3.1-70B-Instruct",
      #model="meta-llama/Meta-Llama-3.1-8B-Instruct",
      #model="google/gemma-2-2b-it",
      model="google/gemma-2-9b-it",
      #model="Qwen/Qwen2.5-Coder-7B-Instruct",
      #model="Qwen/Qwen2.5-Coder-32B-Instruct",
      messages=[{'role': 'user', 'content': p}],
      temperature=0,
      max_tokens=1000
  )
  return comp_res.choices[0].message.content
#q = 'No actions were performed'

"""
with open("alice.txt", "r") as file:
    alice_content = file.read()
    write(8888, alice_content)
"""

q = """
<prev>
  <action read 100 100></action>
  <result>
  address 8888 - Alice's Adventures in Wonderland by Lewis Carroll
  </result>
</prev>
"""
q = ""


def genprev(ac, r):
  return f"""\
<prev>
  {ac}
  <result>
    {r}
  </result>
</prev>
"""

READ_MAX = 2000

def aa(a):
  res = ''
  read_tot = 0
  for ac in gettag('action', a):
    try:
      _, com, *args = re.search(r'<([^>]+)>', ac)[1].split()
      args = list(map(int, args))
      if com == 'read':
        if  args[0] > MEM_SIZE:
          res += genprev(ac, 'ERROR: MEMORY ADDRESS OUT OF BOUNDS')
        elif args[1] + read_tot <= READ_MAX:
          read_tot += args[1]
          res += genprev(ac, read(*args))
        else:
          res += genprev(ac, 'ERROR: READ_MAX EXCEEDED')
      elif com == 'write':
        if args[0] > MEM_SIZE:
          res += genprev(ac, 'ERROR: MEMORY ADDRESS OUT OF BOUNDS')
        else:
          content = re.search(r'>([^<]+)<', ac)[1]
          write(args[0], content)
          res += genprev(ac, 'WRITE OK')
      else:
        res += genprev(ac, 'ERROR: WRONG COMMAND')
    except Exception:
      res += genprev(ac, "ERROR: MALFORMED ACTION")
  return res


try:
  while True:
    print(q)
    q = prompt(q)
    a = ask(q)
    print(a)
    #write(0, q+a)
    print('='*10)
    q = aa(a)
    #input('Press Enter to continue...')
    print('='*10)
    time.sleep(3)
except Exception:
  with open("dump.txt", "wb") as file:
    file.write(buf)
  raise
except KeyboardInterrupt:
  with open("dump.txt", "wb") as file:
    file.write(buf)
  raise

