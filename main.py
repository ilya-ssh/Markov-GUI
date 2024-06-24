import rustimport.import_hook
import somecode
import io
from nicegui import run, ui, app


def generate(text, sent, labeladr):
    global genlabel1
    global genlabel2
    generated = somecode.rebuild_and_generate(text, int(sent))
    if labeladr == 0:
        genlabel1.text = generated
    else:
        genlabel2.text = generated

async def switchmode():
    if dark.value == True:
        dark.disable()
    elif dark.value == False:
        dark.enable()

async def choose_file():
    global content
    file_types = ('Text Files (*.txt)', 'All files (*.*)')
    try:
        files = await app.native.main_window.create_file_dialog(allow_multiple=False, file_types=file_types)
        for file in files:
            ui.notify(file)
            with open(file, 'r', encoding='utf-8') as txt:
                content = txt.read()
    except TypeError:
        ui.notify('No file was provided!')

def settext(text,sent, labeladr):
    punctuation_marks = ['.', '!', '?']
    if text and len(text.split()) >= 2 and any(char in punctuation_marks for char in text):
        if sent is not None:
            text = generate(text,sent, labeladr) 
        else:
            ui.notify('Number of sentences should not be empty')
    else:
        ui.notify('Text should not be empty, contain at least two words separated by spaces and contain punctuation marks like . or ! or ?')
        
def tab1():
    global genlabel1
    text = ui.textarea(label='Text', placeholder='start typing').style('width: 100%;')
    sent = ui.number(label='Number of sentences to generate', min=1)
    with ui.grid(columns=1).style('justify-content: center;font-size: 200%; margin-top: 10px;'):
        ui.button('Generate!', on_click=lambda e: settext(text.value, sent.value, 0))
        genlabel1 = ui.label('')
        
def tab2():
    global content
    global genlabel2
    with ui.grid(columns=1).style('justify-content: center;font-size: 200%; margin-bottom: 10px;'):
        ui.button('Choose file', on_click=choose_file)
    sent2 = ui.number(label='Number of sentences to generate', min=1)
    with ui.grid(columns=1).style('justify-content: center;font-size: 200%; margin-top: 112px;'):
        ui.button('Generate!', on_click=lambda e: settext(content, sent2.value, 1))
        genlabel2 = ui.label('')
        
def header():
    with ui.grid(columns=2).style('justify-content: start;font-size: 200%;'):
        ui.button(icon="light_mode", on_click=lambda e: switchmode(), color=" ").classes('rounded-lg w-4 h-4 ml-4')
        ui.label('Markovbot').style("font-family: 'Montserrat';")
    ui.label('Powered by Rust 🦀').style("font-family: 'Montserrat'; font-size: 100%;")
    ui.label('Get the source text for Markovbot from:').style("font-family: 'Montserrat';font-size: 200%;")
    with ui.tabs().classes('w-full') as tabs:
        one = ui.tab('Input')
        two = ui.tab('.txt File')
    with ui.tab_panels(tabs, value=one).classes('w-full'):
        with ui.tab_panel(one):
            tab1()
        with ui.tab_panel(two):
            tab2()
            
def loadwebsite():
    header()
    
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(native='True', window_size=(600, 900))
    dark = ui.dark_mode()
    dark.enable()
    loadwebsite()
