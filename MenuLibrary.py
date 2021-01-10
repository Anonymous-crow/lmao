import lmao, os
from cursesmenu import *
from cursesmenu.items import *

def testexit(menu):
    menu.exit()

def main():
    menu = CursesMenu("Lmao", "It is what it be")
    item1 = MenuItem("Item 1", menu)
    command_item = CommandItem("Command", "lmao.py")
    submenu = CursesMenu("Typetext", "")
    typetext1 = FunctionItem("typetext", lmao.typetext, [])
    typetext2 = FunctionItem("typetext2", lmao.typetext2, [])
    submenu.append_item(typetext1)
    submenu.append_item(typetext2)
    submenu_item = SubmenuItem("TypeText", submenu=submenu)
    submenu_item.set_menu(menu)
    ytmenu = CursesMenu("YT", "Download using youtube-dl")
    yt1 = CommandItem("YT MP3", 'lmao.py -yt')
    yt2 = CommandItem("YT PLAYLIST MP3", 'lmao.py -yt')
    ytmenu.append_item(yt1)
    ytmenu.append_item(yt2)
    ytmenu_item = SubmenuItem("YT", submenu=ytmenu)
    ytmenu_item.set_menu(menu)
    menu.append_item(command_item)
    menu.append_item(submenu_item)
    menu.append_item(ytmenu_item)
    menu.start()
    menu.join()
    #menu.show()

if __name__ == "__main__":
    os.system('color a')
    main()
    print('lmaoooooo')
