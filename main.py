from pyVmomi import vim
from pyVim.connect import SmartConnectNoSSL, Disconnect
from tools import cli, service_instance, tasks, pchelper
from kivy.uix.screenmanager import ScreenManager, Screen
import select
import shutil
import socket
import threading
import time
from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.animation import Animation
from kivy.clock import Clock, mainthread
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.anchorlayout import AnchorLayout

Builder.load_string("""
<MenuScreen>:
    
<AnimWidget@Widget>:
    canvas:
        Color:
            rgba: 0.7, 0.3, 0.9, 1
        Rectangle:
            pos: self.pos
            size: self.size
    size_hint: None, None
    size: 400, 30


<RootWidget>:
    cols: 2

    canvas:
        Color:
            rgba: 0.9, 0.9, 0.9, 1
        Rectangle:
            pos: self.pos
            size: self.size

    anim_box: anim_box
    but_1: but_1
    lab_1: lab_1
    lab_2: lab_2

    Button:
        id: but_1
        font_size: 20
        text: 'Развернуть Dallas Lock'
        on_press: root.start_second_thread(lab_2.text)
    
    Button:
        id: but_2
        font_size: 20
        text: 'Включить отслеживание сборки'
        on_press: root.start_second_thread(lab_2.text)
    
    Label:
        id: lab_1
        font_size: 30
        color: 0.6, 0.6, 0.6, 1
        text_size: self.width, None
        halign: 'center'

    AnchorLayout:
        id: anim_box

    Label:
        id: lab_2
        font_size: 100
        color: 0.8, 0, 0, 1
        text: '3'
""")

class MenuScreen(Screen):
    pass

class RootWidget(GridLayout):

    def clone_vm(self):
        try:
            connect = SmartConnectNoSSL(host='192.168.13.138', user='kvn', pwd='5745Ayc')
        except Exception as e:
            print("Сервер ESXi недоступен")
        content = connect.content
        template_name = 'Windows 11 Insider Preview'
        vm_folder = 'Kaznacheev'
        datacenter_name = 'Datacenter'
        datastore_name = 'vsan_DatastoreSSD'
        cluster_name = 'CZI_Cluster 2_6.7'
        resource_pool = 'Kaznacheev'

        template = pchelper.get_obj(content, [vim.VirtualMachine], template_name)
        print('TEMPLATE : ', template)

        datacenter = pchelper.get_obj(content, [vim.Datacenter], datacenter_name)
        print('DATACENTER', datacenter)

        destfolder = pchelper.search_for_obj(content, [vim.Folder], vm_folder)
        print('DESTINATION : ', destfolder)

        datastore = pchelper.search_for_obj(content, [vim.Datastore], datastore_name)
        print('DATASTORE : ', datastore)

        cluster = pchelper.search_for_obj(content, [vim.ClusterComputeResource], cluster_name)
        print('CLUSTER : ', cluster)

        resource_pool = pchelper.search_for_obj(content, [vim.ResourcePool], resource_pool)
        print('RESOURCE_POOL :', resource_pool)

        vmconf = vim.vm.ConfigSpec()

        try:
            rec = content.storageResourceManager.RecommendDatastores(storageSpec=storagespec)
            rec_action = rec.recommendations[0].action[0]
            real_datastore_name = rec_action.destination.name
        except Exception:
            real_datastore_name = template.datastore[0].info.name

        datastore = pchelper.get_obj(content, [vim.Datastore], real_datastore_name)

        # set relospec
        relospec = vim.vm.RelocateSpec()
        relospec.datastore = datastore
        relospec.pool = resource_pool

        clonespec = vim.vm.CloneSpec()
        clonespec.location = relospec
        clonespec.powerOn = True

        print("cloning VM...")

        task = template.Clone(folder=destfolder, name="KVN_Win11", spec=clonespec)
        info_tasks1 = tasks.wait_for_tasks(connect, [task])

        print("VM cloned.")

    def start_second_thread(self, l_text):
        threading.Thread(target=self.second_thread, args=(l_text,)).start()

    def second_thread(self, label_text):
        # Remove a widget, update a widget property, create a new widget,
        # add it and animate it in the main thread by scheduling a function
        # call with Clock.
        Clock.schedule_once(self.start_test, 0)
        # Do some thread blocking operations.
        time.sleep(5)
        l_text = str(int(label_text) * 3000)
        # Update a widget property in the main thread by decorating the
        # called function with @mainthread.
        self.update_label_text(l_text)
        # Do some more blocking operations.
        time.sleep(2)
        # Remove some widgets and update some properties in the main thread
        # by decorating the called function with @mainthread.
        self.stop_test()
        # Start a new thread with an infinite loop and stop the current one.
        threading.Thread(target=self.infinite_loop).start()

    def start_test(self, *args):
        # Remove the button.
        self.remove_widget(self.but_1)
        # Update a widget property.
        self.lab_1.text = ('Запущена установка новой сборки Dallas Lock...')
        # Create and add a new widget.
        anim_bar = Factory.AnimWidget()
        self.anim_box.add_widget(anim_bar)
        # Animate the added widget.
        anim = Animation(opacity=0.3, width=100, duration=0.6)
        anim += Animation(opacity=1, width=400, duration=0.8)
        anim.repeat = True
        anim.start(anim_bar)

    @mainthread
    def update_label_text(self, new_text):
        self.lab_2.text = new_text

    @mainthread
    def stop_test(self):
        self.lab_1.text = ('Установка завершена')
        self.lab_2.text = str(int(self.lab_2.text) + 1)
        self.remove_widget(self.anim_box)
    def infinite_loop(self):
        iteration = 0
        while True:
            if self.stop.is_set():
                # Stop running this thread so the main Python process can exit.
                return
            iteration += 1
            print('Infinite loop, iteration {}.'.format(iteration))
            time.sleep(1)


class DallasLockConfiguratorApp(App):

    def on_stop(self):
        # The Kivy event loop is about to stop, set a stop signal;
        # otherwise the app window will close, but the Python process will
        # keep running until all secondary threads exit.
        self.root.stop.set()

    def build(self):
        return RootWidget()

if __name__ == '__main__':
    DallasLockConfiguratorApp().run()
