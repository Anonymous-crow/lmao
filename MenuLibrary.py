import lmao, os
from cursesmenu import CursesMenu
from cursesmenu.items import FunctionItem, SubmenuItem, CommandItem, MenuItem

def main():
    menu = CursesMenu("Lmao", "It is what it be")
    item1 = MenuItem("Item 1", menu)

    submenu = CursesMenu("Typetext", "")
    typetext1 = FunctionItem("typetext", lmao.typetext, [])
    typetext2 = FunctionItem("typetext2", lmao.typetext2, [])
    submenu.append_item(typetext1)
    submenu.append_item(typetext2)
    submenu_item = SubmenuItem("TypeText", submenu=submenu)
    menu.items.append(submenu_item)

    ytmenu = CursesMenu("YT", "Download using youtube-dl")
    yt1 = CommandItem("YT MP3", 'python lmao.py -yt')
    yt2 = CommandItem("YT PLAYLIST MP3", 'python lmao.py -yp')
    yt3 = CommandItem("YT LIVE", 'python lmao.py -yl')
    ytmenu.append_item(yt1)
    ytmenu.append_item(yt2)
    ytmenu.append_item(yt3)
    ytmenu_item = SubmenuItem("YT", submenu=ytmenu)
    menu.items.append(ytmenu_item)

    playermenu = CursesMenu("Music Player", "Play Music")
    player1 = CommandItem("Playlist Player", 'python lmao.py -pp')
    playermenu.append_item(player1)
    playermenu_item = SubmenuItem("Music Player", submenu=playermenu)
    menu.items.append(playermenu_item)

    optmenu = CursesMenu("OPTIONS", "")
    install_dependencies = CommandItem("INSTALL DEPENDENCIES", 'pip install -Ur requirements.txt')
    optmenu.append_item(install_dependencies)
    optmenu_item = SubmenuItem("OPTIONS", submenu=optmenu)
    menu.items.append(optmenu_item)

    # menu.start()
    # menu.join()
    menu.show()

def makemenu(list, title='Please Select One'):
    return list[CursesMenu.get_selection(list, title)]


if __name__ == "__main__":
    os.system('color a')
    main()
