print("Booting Up Python")
import builtins
import micropip
from pyodide import to_js

async def install_deps():
    await micropip.install('setuptools')
    import setuptools
    # await micropip.install('https://softwareprocess.es/2022/ttwl_cli_saveedit-0.0.5-py3-none-any.whl')
    await micropip.install('Pillow')
    import PIL
    print("Done deps")

async def get_binary_url(url):
    from js import fetch
    from io import BytesIO
    response = await fetch(url)
    js_buffer = await response.arrayBuffer()
    return BytesIO(js_buffer.to_py()).read()

async def save_binary_url(url, filename):
    data = await get_binary_url(url)
    with open(filename,"wb") as fd:
        fd.write(data)

def get_image_info(pic_name):
    from PIL import Image
    image = Image.open(pic_name)
    return f"{image.format} {image.size} {image.mode}"

def get_image_info_dict(pic_name):
    from PIL import Image
    image = Image.open(pic_name)
    info = {
        "format":image.format,
        "size":image.size,
        "mode":image.mode
    }
    return to_js( info )


def resize_image(input_file, width, height, output_file):
    from PIL import Image
    image = Image.open(input_file)
    small_image = image.resize((width, height))
    small_image.save(output_file)

def wrap_io(f):
    import io
    import sys
    out = io.StringIO()
    oldout = sys.stdout
    olderr = sys.stderr
    sys.stdout = sys.stderr = out
    try:
        f()
    except:
        traceback.print_exc()
    sys.stdout = oldout
    sys.stderr = olderr
    res =  out.getvalue()
    out.close()
    return res

#  josephernest  https://github.com/pyodide/pyodide/issues/679#issuecomment-637519913
def load_file_from_browser(output_filename):
    ''' saves the browser content as output_filename '''
    from js import content
    with open(output_filename,"wb") as fd:
        return fd.write(content.to_bytes())

def get_file(filename):
    return file_to_buffer(filename)

def file_to_buffer(filename):
    from js import Uint8Array
    with open(filename,"rb") as fd:
        chunk = fd.read()
        x = Uint8Array.new(range(len(chunk)))
        x.assign(chunk)
        return x
    

