from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Rectangle, Color
from kivy.uix.checkbox import CheckBox
from kivy.clock import Clock, mainthread
import threading
import time
from tools import cli, service_instance, tasks, pchelper
from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim

Builder.load_string("""
<StartScreen>:
    name: 'start'
    canvas:
        Color:
            rgba: 1, 1, 1, 1   
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation:'horizontal'
        Button:
            size_hint: 0.3, 0.3
            pos_hint: {"x":0.25, "top":0.6}
            text: 'Развернуть Dallas Lock сейчас'
            on_press: root.manager.current = 'deploy'
        Button:
            size_hint: 0.3, 0.3
            pos_hint: {"x":0.25, "top":0.6}
            text: 'Настроить ожидание сборки'
            on_press: root.manager.current = 'waitsettings'

<DeployScreen>:
    name: 'deploy'
    canvas:
        Color:
            rgba: 1, 1, 1, 1   
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation:'horizontal'
        Button:
            text: 'Выбрать список ОС для установки'
            size_hint: 0.3, 0.3
            pos_hint: {"x":0.25, "top":0.6}
            on_press: root.manager.current = 'setos'
        Button:
            text: 'Вернуться начальному экрану'
            size_hint: 0.3, 0.3
            pos_hint: {"x":0.25, "top":0.6}
            on_press: root.manager.current = 'start'
            
<WaitSettingsScreen>:
    name: 'waitsettings'
    canvas:
        Color:
            rgba: 1, 1, 1, 1   
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        Button:
            size_hint: 0.3, 0.3
            pos_hint: {"x":0.25, "top":0.6}
            on_press: root.manager.current = 'setwait'
            text: 'Настроить параметры ожидания'
        Button:
            size_hint: 0.3, 0.3
            pos_hint: {"x":0.25, "top":0.6}
            text: 'Назад в главное меню'
            on_press: root.manager.current = 'start'
<SetOsScreen>
    name: 'setos'
    canvas:
        Color: 
            rgba: 0, 1, 1, 1 
    StackLayout:
        orientation: 'lr-tb'
        Button:
            id: btn_1
            text: 'Windows 7'
            size_hint: [.5, .1]
            on_release: self.background_color = (0.0, 1.0, 0.0, 1.0)    
            on_press: root.start_second_thread(self)

        Button:
            id: but_2
            text: 'Windows 8'
            size_hint: [.5, .1]
            on_release: self.background_color = (0.0, 1.0, 0.0, 1.0)    
            on_press: root.start_second_thread(instance)
        Button:
            text: 'Windows 2008 R2'
            size_hint: [.5, .1]
            on_release: self.background_color = (0.0, 1.0, 0.0, 1.0)    
            on_press:root.start_second_thread(self)
        Button:
            text: 'Windows 2012'
            size_hint: [.5, .1]
            on_release: self.background_color = (0.0, 1.0, 0.0, 1.0)    
            on_press:root.start_second_thread(self)
        Button:
            text: 'Windows 2016'
            size_hint: [.5, .1]
            on_release: self.background_color = (0.0, 1.0, 0.0, 1.0)    
            on_press:root.start_second_thread(self)
        Button:
            text: 'Windows 2019'
            size_hint: [.5, .1]
            on_release: self.background_color = (0.0, 1.0, 0.0, 1.0)    
            on_press:root.start_second_thread(self)
        Button:
            text: 'Windows 10'
            size_hint: [.5, .1]
            on_release: self.background_color = (0.0, 1.0, 0.0, 1.0)    
            on_press:root.start_second_thread(self)
        Button:
            text: 'Windows 11'
            size_hint: [.5, .1]
            on_release: self.background_color = (0.0, 1.0, 0.0, 1.0)    
            on_press:root.start_second_thread(self)
    StackLayout:
        orientation: 'rl-bt'    
        Button:
            text: 'Запустить установку Dallas Lock'
            size_hint: [.3, .1]
            on_release: root.manager.current = 'start'
        Button:
            size_hint: [.3, .1]
            text: 'В главное меню'
            on_press: root.manager.current = 'start'
       
            
<SetWaitScreen>
    name: 'sewait'
    canvas:
        Color:
            rgba: 1, 1, 1, 1   
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        Button:
            size_hint: 0.3, 0.3
            pos_hint: {"x":0.25, "top":0.6}
            on_press: root.manager.current = 'start'
            text: 'Запустить ожидание Dallas Lock'
        Button:
            size_hint: 0.3, 0.3
            pos_hint: {"x":0.25, "top":0.6}
            text: 'В главное меню'
            on_press: root.manager.current = 'start'
""")

class Display(BoxLayout):
    pass

class StartScreen(Screen):
    pass

class DeployScreen(Screen):
    pass

class WaitSettingsScreen(Screen):
    pass

class SetOsScreen(Screen, App):

    def clone_vm(self, name):
        print('Подключение к серверу виртуализации')
        try:
            connect = SmartConnectNoSSL(host='192.168.13.138', user='kvn', pwd='5745Ayc')
        except Exception as e:
            print("Сервер ESXi недоступен")
        content = connect.content

        def binder(self):
            pass

        """osv = [vm for vm in templates.view if vm.config.template == True and name in vm.name]
        print(osv)

        template_name = 'Windows 11 Insider Preview'
        vm_folder = 'Deployed_fromTemplate'
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

        task = template.Clone(folder=destfolder, name=name, spec=clonespec)
        info_tasks1 = tasks.wait_for_tasks(connect, [task])

        print("VM cloned.")"""

    def start_second_thread(self, instance):
        name = instance.text
        my_thread = threading.Thread(target=self.clone_vm, args=(name,))
        my_thread.start()
    def second_thread(self, name):
        pass


class SetWaitScreen(Screen):
    pass

class DallasLockConfiguratorApp(App):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(DeployScreen(name='deploy'))
        sm.add_widget(WaitSettingsScreen(name='waitsettings'))
        sm.add_widget(SetOsScreen(name='setos'))
        sm.add_widget(SetWaitScreen(name='setwait'))
        return sm


if __name__ == '__main__':
    DallasLockConfiguratorApp().run()