import os
from openai import OpenAI
from prompt import prompt

buf = bytearray(1024 * 1024)  # Initialize with spaces


client = OpenAI(
    base_url="https://api.studio.nebius.ai/v1/",
    api_key=os.environ.get("NEBIUS_API_KEY"),
)

def write(a, s):
  buf[a:a + len(s.encode('utf-8'))] = s.encode('utf-8')


def read(a, n):
  return buf[a:a + n].decode('utf-8')




def ask(p):
  comp_res = client.chat.completions.create(
      #model="meta-llama/Meta-Llama-3.1-405B-Instruct",
      #model="meta-llama/Meta-Llama-3.1-70B-Instruct",
      #model="meta-llama/Meta-Llama-3.1-8B-Instruct",
      #model="google/gemma-2-2b-it",
      #model="google/gemma-2-9b-it",
      model="Qwen/Qwen2.5-Coder-7B-Instruct",
      #model="Qwen/Qwen2.5-Coder-32B-Instruct",
      messages=[{'role': 'user', 'content': p}],
      temperature=0.0001
  )
  return comp_res.choices[0].message.content
#q = 'No actions were performed'

write(100, "Hello, Marvin!")
with open("alice.txt", "r") as file:
    alice_content = file.read()
    write(8888, alice_content)

q= """
<prev>
  <action write 100>Hello, World!</action>
  <result>WRITE OK</result>
</prev>
  <action read 107 5></action>
  <result>World</result>
<prev>
  <action write 107 7>Marvin!</action>
  <result>WRITE OK</result>
</prev>
<prev>
  <action read 100 14></action>
  <result>Hello, Marvin</result>
</prev>
"""
q = """
<prev>
  <action read 100 100></action>
  <result>
  address 8888 - Alice's Adventures in Wonderland by Lewis Carroll
  </result>
</prev>
"""
a = ask(prompt(q))
print(a)



