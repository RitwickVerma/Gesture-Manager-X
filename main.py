#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Gdk, GdkPixbuf
import os
import sys
import gestureHelper as gh
import daemonHelper as dh
import settingsHelper as sh

EXEC_FOLDER = os.path.dirname(os.path.realpath(__file__)) + "/"
builder = Gtk.Builder()
builder.add_from_file(EXEC_FOLDER + "ui.glade")
HOME = os.environ.get('HOME')

# settings = Gtk.Settings.get_default()
# settings.set_property("gtk-application-prefer-dark-theme", True)

class App(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self,
                                 application_id="org.laughingstock.gesturemanagerx",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.connect("activate", self.activateCb)

    def do_startup(self):
        # start the application
        Gtk.Application.do_startup(self)

    def activateCb(self, app):
        window = builder.get_object("window")
        # window.set_wmclass("Gesture Manager X", "Gesture Manager X")
        window.set_title("Gesture Manager X")
        app.add_window(window)
        appMenu = Gio.Menu()
        appMenu.append("About", "app.about")
        appMenu.append("Quit", "app.quit")
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.on_about_activate)
        builder.get_object("aboutdialog").connect(
            "delete-event", lambda *_: builder.get_object("aboutdialog").hide() or True)
        app.add_action(about_action)
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit_activate)
        app.add_action(quit_action)
        app.set_app_menu(appMenu)
        window.show_all()

    def on_about_activate(self, *agrs):
        builder.get_object("aboutdialog").show()

    def on_quit_activate(self, *args):
        self.quit()

listbox_gestures=builder.get_object('listBoxGestures')
entry_shortcut_command=builder.get_object('entryShortcutCommand')
# image_gesture_animation=builder.get_object('imageGestureAnimation')
popovermenu_daemon_control = builder.get_object('popoverMenuDaemonControl')
listbox_popover_daemon_control=builder.get_object('ListboxPopoverDaemonControl')
image_daemon_status=builder.get_object('imageDaemonStatus')
switch_daemon_autostart=builder.get_object('switchDaemonAutostart')

button_start_daemon=builder.get_object('buttonStartDaemon')
button_stop_daemon=builder.get_object('buttonStopDaemon')
button_restart_daemon=builder.get_object('buttonRestartDaemon')

popovermenu_settings_control = builder.get_object('popoverMenuSettingsControl')
spin_button_swipe_threshold = builder.get_object('spinButtonSwipeThreshold')
spin_button_gesture_timeout = builder.get_object('spinButtonGestureTimeout')

STATUS_I_SIZE=Gtk.IconSize.MENU
def update_daemon_status():
    status=dh.get_daemon_running()
    if status:
        image_daemon_status.set_from_icon_name('gtk-yes', STATUS_I_SIZE)
        button_start_daemon.set_sensitive(False)
        button_stop_daemon.set_sensitive(True)
        button_restart_daemon.set_sensitive(True)
    else:
        image_daemon_status.set_from_icon_name('gtk-no', STATUS_I_SIZE)
        button_start_daemon.set_sensitive(True)
        button_stop_daemon.set_sensitive(False)
        button_restart_daemon.set_sensitive(False)
    image_daemon_status.show()

def update_daemon_autostart_status():
    status=dh.get_daemon_autostart()
    switch_daemon_autostart.set_state(status)

def populate_gestures_listbox():
    for g in gh.GESTURES_POSSIBLE:
        box=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box.set_margin_top(6)
        box.set_margin_start(6)
        box.set_margin_end(6)
        box.set_margin_bottom(6)
        label=Gtk.Label()
        label.set_text(str(g).replace('_',' ',1))
        box.pack_start(label, False, True, 0)
        row=Gtk.ListBoxRow()
        row.add(box)
        row.value=g
        listbox_gestures.add(row)
        listbox_gestures.show_all()

def populate_settings():
    spin_button_gesture_timeout.set_value(float(sh.gesture_timeout))
    spin_button_swipe_threshold.set_value(float(sh.swipe_threshold))

populate_gestures_listbox()
populate_settings()
update_daemon_status()
update_daemon_autostart_status()

class Handler:

    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def on_buttonReassignShortcut_clicked(self, btn):
        gh.add_gesture(listbox_gestures.get_selected_row().value,
            entry_shortcut_command.get_text())
        dh.restart_daemon()

    def on_buttonRemoveGesture_clicked(self, btn):
        gh.remove_gesture(listbox_gestures.get_selected_row().value)
        entry_shortcut_command.set_text('')
        dh.restart_daemon()

    def on_listBoxGestures_row_selected(self, listbox, row):
        if row:
            gesture = row.value
            command = gh.get_gesture(str(gesture))
            entry_shortcut_command.set_text(command)

    def on_buttonDaemonControl_clicked(self, btn):
        popovermenu_daemon_control.show_all()

    # define start, stop, restart, autostart toggle

    def on_buttonStartDaemon_clicked(self, btn):
        dh.start_daemon()
        update_daemon_status()

    def on_buttonStopDaemon_clicked(self, btn):
        dh.stop_daemon()
        update_daemon_status()

    def on_buttonRestartDaemon_clicked(self, btn):
        dh.restart_daemon()
        update_daemon_status()

    def on_switchDaemonAutostart_state_set(self, switch, state):
        dh.set_daemon_autostart(state)
        update_daemon_autostart_status()

    def on_buttonSettingsControl_clicked(self, btn):
        popovermenu_settings_control.show_all()

    def on_spinButtonSwipeThreshold_value_changed(self, btn):
        sh.set_swipe_threshold(btn.get_value_as_int())
    
    def on_spinButtonGestureTimeout_value_changed(self, btn):
        sh.set_gesture_timeout(btn.get_value())


builder.connect_signals(Handler())


if __name__ == "__main__":
    app = App()
    app.run(sys.argv)
