import codecs

with codecs.open('index.html', 'r', 'utf-8') as f:
    lines = f.readlines()

# The duplicate is exactly at lines 2844-2847 (indices 2843-2846). 
# Let's verify by checking the content.
if "function initDandelions()" in lines[2844] and "function initDandelions()" in lines[2848]:
    del lines[2843:2847]
    with codecs.open('index.html', 'w', 'utf-8') as f:
        f.writelines(lines)
    print("Deleted duplicate lines exactly!")
else:
    # Fallback to finding it dynamically
    for i in range(len(lines)):
        if "function initDandelions()" in lines[i]:
            if "function initDandelions()" in lines[i+4]:
                del lines[i-1:i+3]
                with codecs.open('index.html', 'w', 'utf-8') as f:
                    f.writelines(lines)
                print("Deleted duplicate lines dynamically!")
                break
    else:
        print("Could not find duplicate to delete.")
