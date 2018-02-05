import gi
import requests
import signal

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import GObject as gobject


APPINDICATOR_ID = 'ethPriceIndicator'
ETH_PRICE_LABEL = "ethPrice"

class EthereumIndicator():
    def main(self):
        indicator = appindicator.Indicator.new(APPINDICATOR_ID, "/home/tiit/ethereum.png", appindicator.IndicatorCategory.SYSTEM_SERVICES)
        indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        indicator.set_menu(self.build_menu())
        indicator.set_label("default", ETH_PRICE_LABEL) # Find and check documentation what are these args
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        gobject.timeout_add(1000 * 30, self.update, indicator)
        self.update(indicator)
        gtk.main()

    def build_menu(self):
        menu = gtk.Menu()
        item_quit = gtk.MenuItem('Quit')
        item_quit.connect('activate', quit)
        menu.append(item_quit)
        menu.show_all()
        return menu

    def quit(self):
        gtk.main_quit()


    def update(self, indicator):
        ethPrice = self.getEthPrice()
        indicator.set_label(str(ethPrice), ETH_PRICE_LABEL)
        return True

    def getEthPrice(self):
        ethJson = requests.get('https://v2.ethereumprice.org:8080/snapshot/eth/usd/waex/24h/?_=1517815371190').json()
        return ethJson["data"]["price"]


if __name__ == "__main__":
    ethIndicator = EthereumIndicator()
    ethIndicator.main()

