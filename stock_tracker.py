import os
import sys
import time
import argparse
import pandas as pd
from yahoo_fin.stock_info import get_live_price
from google_speech import Speech
from pynput import keyboard

get_notifications = lambda title, message : os.system(f'notify-send "{title}" "{message}"')

should_break = False


class GetLiveUpdates:


    abbrevations_dict = {
        'Microsoft': 'msft', 
        'Netflix': 'nflx',
        'Facebook': 'fb',
        'Apple': 'aapl',
        'Google': 'googl',
    }

    COMBINATION = {
        keyboard.Key.esc,
        keyboard.Key.ctrl
    }

    current = set()

    def __init__(self, company=None, abbreviation=None, time_interval=None, companies_list=None):
        self.company = company
        self.abbreviation = abbreviation
        self.time_interval = time_interval
        self.companies_list = companies_list

    def speak(self, message, language):
        speech = Speech(message, language)
        speech.play()

    def on_press(self, key):
        global should_break
        if key in self.COMBINATION:
            self.current.add(key)
            if all(k in self.current for k in self.COMBINATION):
                should_break = True
                msg = 'stopping program in a bit...'
                print(msg)
                self.speak(msg, 'en')
                sys.exit('stopping program')

    def on_release(self, key):
        try:
            self.current.remove(key)
        except KeyError:
            pass

    def get_data(self):
        global should_break
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            while should_break is False:
                old_price = get_live_price(self.abbreviation)
                time.sleep(self.time_interval)
                new_price = get_live_price(self.abbreviation)
                if not old_price == new_price:
                    print(new_price)
                    get_notifications(f'Stock Price Changed for {self.company}', f'New Price: {new_price}')
                    msg = f'Stock Price Changed for {self.company}. New Price: {new_price}'
                    self.speak(msg, 'en')
                else:
                    print('unchanged')
            listener.join()

    def get_multi_company_data(self):
        global should_break
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            while should_break is False:
                for index, company in enumerate(self.companies_list):
                    if company in self.abbrevations_dict:
                        old_price = get_live_price(self.abbrevations_dict[company])
                        time.sleep(self.time_interval)
                        new_price = get_live_price(self.abbrevations_dict[company])
                        if not old_price == new_price:
                            print(new_price)
                            get_notifications(f'Stock Price Changed for {company}', f'New Price: {new_price}')
                            msg = f'Stock Price Changed for {company}. New Price: {new_price}'
                            self.speak(msg, 'en')
                        else:
                            print('unchanged')
                    else:
                        msg = f'Support for {company}\'s stock live tracking has not been added by the developer.'
                        print(msg)
                        self.speak(msg, 'en')
                        self.companies_list.pop(index)
            listener.join()


# updates = GetLiveUpdates(
#     company='Netflix',
#     abbreviation='nflx',
#     time_interval=5.0
# )


# updates.get_data()


# updates = GetLiveUpdates(
#     companies_list=['Netflix', 'Facebook', 'Microsoft'],
#     time_interval=5.0
# )


# updates.get_multi_company_data()



parser = argparse.ArgumentParser(description='Get live stock prices')
parser.add_argument('--company', dest='company', type=str, help='Company Name')
parser.add_argument('--abbreviation', dest='abbreviation', type=str, help='Company Abbreviation')
parser.add_argument('--delay', dest='delay', type=float, help='Time Interval in seconds', required=True)
parser.add_argument('--companies', dest='companies', nargs='+', help='List of companies to track')
parser.add_argument('-single', '--single', action='store_true')
parser.add_argument('-multi', '--multi', action='store_true')

args = parser.parse_args()

use_single_company_tracker = args.single
use_multi_company_tracker = args.multi
company = args.company
abbreviation = args.abbreviation
time_interval = args.delay
companies = args.companies

if use_single_company_tracker:
    updates = GetLiveUpdates(
        company=company,
        abbreviation=abbreviation,
        time_interval=time_interval
    )
    updates.get_data()
elif use_multi_company_tracker:
    updates = GetLiveUpdates(
        companies_list=companies,
        time_interval=time_interval
    )
    updates.get_multi_company_data()
