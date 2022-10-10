from PIL import Image
import os
from datetime import datetime

IMG_WIDTH = 83 # 各牌の幅
IMG_HEIGHT = 120 # 各牌の高さ

def check_hai_code(code):
    img_path = f'./tiles/{code}.png'
    return os.path.isfile(img_path)

def hai_img_generate(code):
    file_name = datetime.now().strftime('%Y%m%d-%H%M%S')
    next_furo = False
    tsumo_margin = IMG_WIDTH // 4
    code_list = code.split('/')
    img_width = len(code_list) * IMG_WIDTH * 2
    left_corner = 0
    if '@t' in code_list:
        img_width -= IMG_WIDTH - tsumo_margin
    if '@f' in code_list:
        img_width += IMG_WIDTH // 4
    if '@l' in code_list:
        img_width += IMG_HEIGHT - IMG_WIDTH
    img = Image.new('RGBA', (img_width, IMG_HEIGHT))
    for tile in code_list:
        if tile == '@t':
            left_corner += tsumo_margin
        elif tile == '@l':
            left_corner += IMG_WIDTH
        elif tile == '@f':
            next_furo =True
        elif tile == '@b':
            img.paste(Image.open(f'./tiles/b.png').convert('RGBA'), (left_corner, 0))
            left_corner += IMG_WIDTH
        elif check_hai_code(tile):
            if next_furo:
                img.paste(Image.open(f'./tiles/{tile}.png').convert('RGBA').rotate(90, expand=True), (left_corner, IMG_HEIGHT - IMG_WIDTH))
                left_corner += IMG_HEIGHT
                next_furo = False
            else:
                img.paste(Image.open(f'./tiles/{tile}.png').convert('RGBA'), (left_corner, 0))
                left_corner += IMG_WIDTH
        else:
            return False
    img.crop((0, 0, left_corner, IMG_HEIGHT)).save(f'./tmp/{file_name}.png')
    return f'./tmp/{file_name}.png'

def easy_hai_img_generate(man: int = '', pin: int = '', sou: int = '', honors: int = '', tsumo: str = ''):
    tiles_items = {'m':man, 'p':pin, 's':sou, 'z':honors}
    code = ''
    for k, v in tiles_items.items():
        for i in str(v):
            if i == '0':
                code += f'r5{k}/'
            else:
                code += f'{i}{k}/'
    if tsumo != '':
        code += f'@t/{tsumo}'
    else:
        code = code.rstrip('/')
    file_path = hai_img_generate(code)
    return file_path

if __name__ == '__main__':
    print(hai_img_generate('1m/2m/3m/5m/5m/2z/2z/@t/5m/@l/@b/1s/1s/@b/@f/2m/1m/3m'))