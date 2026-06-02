import codecs

lines = codecs.open('index_old.html', 'r', 'utf-8').readlines()
start = 0
end = 0

for i, l in enumerate(lines):
    if 'const fxCanvas = document.createElement' in l: 
        start = i - 2
    if 'function fxLoop()' in l: 
        end = i + 10

old_block = "".join(lines[start:end])

with codecs.open('old_block.txt', 'w', 'utf-8') as f:
    f.write(old_block)

print("Extracted to old_block.txt")
