import neologdn

def format_text(text):
    text = neologdn.normalize(text)

    with open('./merged_file/normalized.txt', 'a+') as f:
        f.write(text)
        f.close()

with open('./merged_file/cleaned.txt') as f:
    text = f.read()
    format_text(text)
    f.close()