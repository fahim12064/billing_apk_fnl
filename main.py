from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivy.storage.jsonstore import JsonStore
from datetime import datetime

class MainScreen(MDScreen):
    pass

class AdminLoginScreen(MDScreen):
    def verify_credentials(self, username, password):
        if username == "rohan" and password == "rohan11":
            pin_store = JsonStore('pin.json')
            if not pin_store.exists('admin_pin'):
                self.manager.current = 'pin_set'
            else:
                self.manager.current = 'admin_dashboard'
        else:
            self.ids.login_error.text = "Invalid credentials!"

class PinSetScreen(MDScreen):
    def set_pin(self, pin):
        if len(pin) == 4 and pin.isdigit():
            pin_store = JsonStore('pin.json')
            pin_store.put('admin_pin', pin=pin)
            self.manager.current = 'admin_dashboard'
        else:
            self.ids.pin_error.text = "PIN must be 4 digits!"

class AdminDashboardScreen(MDScreen):
    pass

class AddUserScreen(MDScreen):
    def add_user(self, username, ip_name, ip_password, pin):
        pin_store = JsonStore('pin.json')
        if not pin_store.exists('admin_pin') or pin_store.get('admin_pin')['pin'] != pin:
            self.ids.add_user_error.text = "Invalid PIN!"
            return
        user_store = JsonStore('users.json')
        if user_store.exists(ip_name):
            self.ids.add_user_error.text = "IP Name already exists!"
            return
        user_store.put(ip_name, username=username, ip_password=ip_password, join_date=str(datetime.now()),
                       added_by="rohan", bill_updates={}, last_updated_by="")
        self.ids.add_user_error.text = "User added successfully!"
        self.manager.current = 'admin_dashboard'

class UserListScreen(MDScreen):
    def on_enter(self):
        self.load_user_list()

    def load_user_list(self, filter_text=""):
        self.ids.user_table.clear_widgets()
        user_store = JsonStore('users.json')
        headers = ['Serial', 'Username', 'IP Name', 'Last Month', 'This Month', 'View Profile']
        for header in headers:
            self.ids.user_table.add_widget(MDLabel(text=header, bold=True, size_hint_y=None, height=30))
        filtered_ips = []
        for ip_name in user_store:
            username = user_store[ip_name]['username']
            if filter_text.lower() in username.lower():
                filtered_ips.append(ip_name)
        for idx, ip_name in enumerate(filtered_ips):
            user = user_store[ip_name]
            self.ids.user_table.add_widget(MDLabel(text=str(idx + 1), size_hint_y=None, height=30))
            username_btn = MDFlatButton(text=user['username'], size_hint_y=None, height=30)
            username_btn.bind(on_release=lambda x, ip=ip_name: self.goto_bill_update(ip))
            self.ids.user_table.add_widget(username_btn)
            self.ids.user_table.add_widget(MDLabel(text=ip_name, size_hint_y=None, height=30))
            last_month = user.get('bill_updates', {}).get('2025-05', 'Not Paid')
            this_month = user.get('bill_updates', {}).get('2025-06', 'Not Paid')
            self.ids.user_table.add_widget(MDLabel(text=last_month, size_hint_y=None, height=30))
            self.ids.user_table.add_widget(MDLabel(text=this_month, size_hint_y=None, height=30))
            view_btn = MDRaisedButton(text='View', size_hint_y=None, height=30)
            view_btn.bind(on_release=lambda x, ip=ip_name: self.goto_profile(ip))
            self.ids.user_table.add_widget(view_btn)

    def filter_user_list(self, search_text):
        self.load_user_list(filter_text=search_text)

    def goto_bill_update(self, ip_name):
        bill_screen = self.manager.get_screen('bill_update')
        bill_screen.ids.ip_name.text = ip_name
        self.manager.current = 'bill_update'

    def goto_profile(self, ip_name):
        profile_screen = self.manager.get_screen('view_profile')
        profile_screen.display_profile(ip_name)
        self.manager.current = 'view_profile'

class BillUpdateScreen(MDScreen):
    def update_bill(self, ip_name, month, pin):
        if month == "Select Month":
            self.ids.bill_error.text = "Please select a valid month!"
            return
        pin_store = JsonStore('pin.json')
        if not pin_store.exists('admin_pin') or pin_store.get('admin_pin')['pin'] != pin:
            self.ids.bill_error.text = "Invalid PIN!"
            return
        user_store = JsonStore('users.json')
        if not user_store.exists(ip_name):
            self.ids.bill_error.text = "User not found!"
            return
        user = user_store[ip_name]
        user['bill_updates'][month] = f"Paid on {datetime.now().strftime('%Y-%m-%d')}"
        user['last_updated_by'] = "rohan"
        user_store.put(ip_name, **user)
        self.ids.bill_error.text = "Bill updated successfully!"
        self.manager.current = 'admin_dashboard'

class ViewProfileScreen(MDScreen):
    def display_profile(self, ip_name):
        user_store = JsonStore('users.json')
        if user_store.exists(ip_name):
            user = user_store[ip_name]
            profile_text = (f"Username: {user['username']}\n"
                            f"IP Name: {ip_name}\n"
                            f"Password: {user['ip_password']}\n"
                            f"Join Date: {user['join_date']}\n"
                            f"Added By: {user['added_by']}\n"
                            f"Last Updated By: {user['last_updated_by']}\n"
                            f"Last 6 Months Bills:\n")
            months = ['2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06']
            for month in months:
                status = user.get('bill_updates', {}).get(month, 'Not Paid')
                profile_text += f"{month}: {status}\n"
            self.ids.profile_info.text = profile_text
        else:
            self.ids.profile_info.text = "User not found!"

class PinChangeScreen(MDScreen):
    def change_pin(self, password, old_pin, new_pin):
        if password != "rohan11":
            self.ids.pin_change_error.text = "Invalid password!"
            return
        pin_store = JsonStore('pin.json')
        if not pin_store.exists('admin_pin') or pin_store.get('admin_pin')['pin'] != old_pin:
            self.ids.pin_change_error.text = "Invalid old PIN!"
            return
        if len(new_pin) != 4 or not new_pin.isdigit():
            self.ids.pin_change_error.text = "New PIN must be 4 digits!"
            return
        pin_store.put('admin_pin', pin=new_pin)
        self.ids.pin_change_error.text = "PIN changed successfully!"
        self.manager.current = 'admin_dashboard'

class UserLoginScreen(MDScreen):
    def verify_user(self, ip_name, password):
        user_store = JsonStore('users.json')
        if user_store.exists(ip_name) and user_store[ip_name]['ip_password'] == password:
            self.manager.get_screen('view_profile').display_profile(ip_name)
            self.manager.current = 'view_profile'
        else:
            self.ids.user_login_error.text = "Invalid IP Name or Password!"

class BillingApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        sm = MDScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(AdminLoginScreen(name='admin_login'))
        sm.add_widget(PinSetScreen(name='pin_set'))
        sm.add_widget(AdminDashboardScreen(name='admin_dashboard'))
        sm.add_widget(AddUserScreen(name='add_user'))
        sm.add_widget(UserListScreen(name='user_list'))
        sm.add_widget(BillUpdateScreen(name='bill_update'))
        sm.add_widget(ViewProfileScreen(name='view_profile'))
        sm.add_widget(PinChangeScreen(name='pin_change'))
        sm.add_widget(UserLoginScreen(name='user_login'))
        return sm

if __name__ == '__main__':
    BillingApp().run()