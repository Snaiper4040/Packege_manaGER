import os
import xml.etree.ElementTree as ET

class PgesManager:
    def __init__(self, cache_dir: str):
        self.cache_dir = cache_dir
        self.file_path = os.path.join(cache_dir, 'pges.xml')
        if os.path.exists(self.file_path):
            self.tree = ET.parse(self.file_path)
            self.root = self.tree.getroot()
        else:
            self.root = ET.Element('pges')
            self.tree = ET.ElementTree(self.root)
            self.save()

    def save(self):
        self.tree.write(self.file_path, encoding='utf-8', xml_declaration=True)

    def add_package(self, pge_name: str, need_build: bool = False):
        # Проверяем наличие пакета
        if self.get_package(pge_name) is not None:
            print(f"Пакет '{pge_name}' уже записан в pges.xml")
            return

        pge_elem = ET.SubElement(self.root, 'pge')
        pge_elem.text = pge_name

        # Добавляем состояния
        def add_state(tag, value):
            elem = ET.SubElement(pge_elem, tag)
            elem.text = 'True' if value else 'False'

        add_state('in_cache', False)
        add_state('installed', False)
        if need_build:
            add_state('built', False)

        self.save()

    def get_package(self, pge_name: str):
        for pge_elem in self.root.findall('pge'):
            # Текст у <pge> — это имя пакета
            if (pge_elem.text or '').strip() == pge_name:
                info = {
                    'in_cache': False,
                    'installed': False,
                    'built': None
                }
                for state in info.keys():
                    elem = pge_elem.find(state)
                    if elem is not None:
                        info[state] = (elem.text == 'True')
                return info
        print(f"Пакет '{pge_name}' отсутствует в pges.xml")
        return None

    def update_package(self, pge_name: str, in_cache: bool = None,
                       installed: bool = None, built: bool = None):
        for pge_elem in self.root.findall('pge'):
            if (pge_elem.text or '').strip() == pge_name:
                # Обновяем только указанные состояния
                def update_state(tag, value):
                    if value is None:
                        return
                    elem = pge_elem.find(tag)
                    elem.text = 'True' if value else 'False'

                update_state('in_cache', in_cache)
                update_state('installed', installed)
                update_state('built', built)

                self.save()
                return True
        print(f"Пакет '{pge_name}' отсутствует в pges.xml")
        return False
    
    def remove_package(self, pge_name: str):
        for pge_elem in self.root.findall('pge'):
            if (pge_elem.text or '').strip() == pge_name:
                self.root.remove(pge_elem)
                self._save_pges()
                return
        
        print(f"Пакет '{pge_name}' отсутствует в pges.xml")
        return False
    
    def add_built_field(self, pge_name: str):
        for pge_elem in self.root.findall('pge'):
            if (pge_elem.text or '').strip() == pge_name:
                built_elem = pge_elem.find('built')
                if built_elem is None:
                    built_elem = ET.SubElement(pge_elem, 'built')
                    built_elem.text = 'false'
                    self._save_xml()
                    return
            return
        print(f"Пакет '{pge_name}' отсутствует в pges.xml")
        return
    
# ПРИМЕР ИСПОЛЬЗОАНИЯ:

"""
pm = PgesManager('/path/to/cache')

pm.add_package('pge1', need_build=True)
print(pm.get_package('pge1'))
# {'in_cache': False, 'installed': False, 'builded': False}

pm.update_package('pge1', in_cache=True, installed=True, builded=True)
print(pm.get_package('pge1'))
# {'in_cache': True, 'installed': True, 'builded': True}

pm.add_built_field('my-package')
"""
