 # main.py
from flet import *
from screens.screens import *
from myaction import  create_tables
from mystorage import *
import asyncio


def main(page: Page):
    page.title = "Gestion des ouvrages EA"
    page.scroll = True
    page.window.width=450
    theme=get_value('theme')
    if theme=="ThemeMode.LIGHT":
        theme=ThemeMode.LIGHT
    else:
        theme=ThemeMode.DARK
    if theme:
        page.theme_mode = theme
    else:
        page.theme_mode = ThemeMode.LIGHT
    theme = Theme()
    theme.page_transitions.android = PageTransitionsTheme.android
    
    def route_change(route):
        if page.route == "/":
            page.views.append(AcceuilView(page))
        elif page.route == "/project":
            page.views.append(ProjectView(page))
        elif page.route == "/list-local":
            page.views.append(LocalisationView(page))
        elif page.route == "/recap-ouvrage":
            page.views.append(RecapOuvrageView(page))
        elif page.route == "/filtrer-ouvrage":
            page.views.append(FiltreOuvrageView(page))
        elif page.route == "/stats":
            page.views.append(StatView(page))
        elif page.route == "/statgeneral":
            page.views.append(StatGeneralView(page))
        elif page.route == "/statcommune":
            page.views.append(StatCommuneView(page))
        elif page.route == "/statcanton":
            page.views.append(StatCantonView(page))
        elif page.route == "/apropos":
            page.views.append(ApropoView(page))
        elif page.route == "/settings":
            page.views.append(SettingView(page))
        # elif page.route == "/statics":
        #     page.views.append(StaticView(page))
        page.update()

    def on_view_pop(e: ViewPopEvent):
        # 🔙 Cette fonction est appelée quand l'utilisateur appuie sur le bouton retour Android
        # print(page.views)
        if len(page.views) > 1:
            page.views.pop()
            page.go(page.views[-1].route)
        else:
            # Si on est sur la première page, quitter l'app
            page.window.close()

    
    page.views.append(AcceuilView(page))
    page.on_route_change = lambda e: route_change(page)
    page.on_view_pop = lambda e: on_view_pop(page)
    page.update()

if __name__=="__main__":
    asyncio.run(create_tables())
    app(main)
