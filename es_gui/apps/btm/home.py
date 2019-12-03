from __future__ import absolute_import

import os
from functools import partial

from kivy.uix.screenmanager import Screen
from kivy.app import App

# from es_gui.tools.valuation.valuation_dms import ValuationDMS
from es_gui.resources.widgets.common import WarningPopup, NavigationButton
from es_gui.tools.btm.btm_dms import BtmDMS
from es_gui.proving_grounds.help_carousel import HelpCarouselModalView
from .op_handler import BtmOptimizerHandler


class BehindTheMeterHomeScreen(Screen):
    """
    The home screen for doing behind-the-meter energy storage analysis.
    """
    def __init__(self, **kwargs):
        super(BehindTheMeterHomeScreen, self).__init__(**kwargs)

        # Initialize data management system.
        self.dms = BtmDMS(
            max_memory=App.get_running_app().config.getint('btm', 'btm_dms_size')*1000,
            save_data=bool(App.get_running_app().config.getint('btm', 'btm_dms_save')),
            save_name='btm_dms.p',
            home_path='data',
            )
        self.handler = BtmOptimizerHandler(App.get_running_app().config.get('optimization', 'solver'))
        self.handler.dms = self.dms

    def on_enter(self):
        ab = self.manager.nav_bar
        ab.reset_nav_bar()
        ab.set_title('Behind-the-Meter Applications')

        help_button = NavigationButton(
            text='help',
            on_release=self.open_help_carousel,
        )

        ab.action_view.add_widget(help_button)

        # data_manager = App.get_running_app().data_manager
        
        # # Check if any data is available.
        # if not data_manager.data_bank:
        #     no_data_popup = WarningPopup()
        #     no_data_popup.popup_text.text = "Looks like you haven't downloaded any data yet. Try using QuESt Data Manager to get some data before returning here!"
        #     no_data_popup.dismiss_button.text = "Got it, take me back!"

        #     no_data_popup.bind(on_dismiss=partial(ab.go_to_screen, 'index'))
        #     no_data_popup.open()
    
    def open_help_carousel(self, *args):
        """
        """
        help_carousel_view = HelpCarouselModalView()
        help_carousel_view.title.text = "QuESt BTM"

        slide_01_text = "QuESt BTM is a collection of tools for behind-the-meter energy storage use cases."

        slide_02_text = "The Time-of-Use Cost Savings wizard estimates the cost savings with behind-the-meter energy storage, particularly for time-of-use and/or net metering customers. You will need the following data to use this tool:\n* Utility rate structure\n* Load profile (or import your own)\n\nYou may also add a co-located photovoltaic power profile or import your own."

        slides = [
            (os.path.join("es_gui", "resources", "help_views", "btm", "01.png"), slide_01_text),
            (os.path.join("es_gui", "resources", "help_views", "btm", "02.png"), slide_02_text),
        ]

        help_carousel_view.add_slides(slides)
        help_carousel_view.open()
