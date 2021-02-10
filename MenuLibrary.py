import lmao, os
from cursesmenu import *
from cursesmenu.items import *

def main():
    menu = CursesMenu("Lmao", "It is what it be")
    item1 = MenuItem("Item 1", menu)

    submenu = CursesMenu("Typetext", "")
    typetext1 = FunctionItem("typetext", lmao.typetext, [])
    typetext2 = FunctionItem("typetext2", lmao.typetext2, [])
    submenu.append_item(typetext1)
    submenu.append_item(typetext2)
    submenu_item = SubmenuItem("TypeText", submenu=submenu)
    submenu_item.set_menu(menu)

    ytmenu = CursesMenu("YT", "Download using youtube-dl")
    yt1 = CommandItem("YT MP3", 'lmao.py -yt')
    yt2 = CommandItem("YT PLAYLIST MP3", 'lmao.py -yp')
    yt3 = CommandItem("YT LIVE", 'lmao.py -yl')
    ytmenu.append_item(yt1)
    ytmenu.append_item(yt2)
    ytmenu.append_item(yt3)
    ytmenu_item = SubmenuItem("YT", submenu=ytmenu)
    ytmenu_item.set_menu(menu)

    playermenu = CursesMenu("Music Player", "Play Music")
    player1 = CommandItem("Playlist Player", 'lmao.py -pp')
    playermenu.append_item(player1)
    playermenu_item = SubmenuItem("Music Player", submenu=playermenu)
    playermenu_item.set_menu(menu)

    optmenu = CursesMenu("OPTIONS", "")
    install_dependencies = CommandItem("INSTALL DEPENDENCIES", 'lmao.py -i')
    optmenu.append_item(install_dependencies)
    optmenu_item = SubmenuItem("OPTIONS", submenu=optmenu)
    optmenu_item.set_menu(menu)

    menu.append_item(submenu_item)
    menu.append_item(ytmenu_item)
    menu.append_item(playermenu_item)
    menu.append_item(optmenu_item)

    # menu.start()
    # menu.join()
    menu.show()

def makemenu(list, title='Please Select One'):
    menu = SelectionMenu(list, title=title, show_exit_option=False)
    # try:
    #     rtnvalue=
    # except:
    #     return None
    return list[menu.get_selection(list, title=title, exit_option=False)]


if __name__ == "__main__":
    os.system('color a')
    main()
