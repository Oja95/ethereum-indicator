from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import GObject as gobject

import requests
import signal

APPINDICATOR_ID = 'ethPriceIndicator'
ETH_PRICE_LABEL = "ethprice"

def build_menu():
    menu = gtk.Menu()
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu

def quit(source):
    gtk.main_quit()

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, "/home/tiit/ethereum.png", appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    indicator.set_label("default", ETH_PRICE_LABEL) # Find and check documentation what are these args
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    gobject.timeout_add(1000 * 30, update, indicator)
    update(indicator)
    gtk.main()

def update(indicator):
    ethPrice = getEthPrice()
    print(ethPrice)
    indicator.set_label(str(ethPrice), ETH_PRICE_LABEL)
    return True # Gobject will call until it receives True as callback

def getEthPrice():
    ethJson = requests.get('https://v2.ethereumprice.org:8080/snapshot/eth/usd/waex/24h/?_=1517815371190').json()
    return ethJson["data"]["price"]

#def updateLabel():


if __name__ == "__main__":
    main()


