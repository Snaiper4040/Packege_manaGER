import xml.etree.ElementTree as ET
from typing import List, Optional

class Manifest:
    def __init__(self,
                 name: str,
                 version: str,
                 creation_date: str,
                 sha256: str,
                 dependencies: List[str],
                 supported_os: List[str],
                 supported_arch: List[str],
                 builder: Optional[str] = None):
        self.name = name
        self.version = version
        self.creation_date = creation_date
        self.sha256 = sha256
        self.dependencies = dependencies
        self.supported_os = supported_os
        self.supported_arch = supported_arch
        self.builder = builder

    @classmethod
    def from_file(cls, filepath: str) -> "Manifest":
        """
        Загружает манифест из XML-файла и возвращает объект Manifest.
        """
        tree = ET.parse(filepath)
        root = tree.getroot()

        name = root.findtext("name")
        version = root.findtext("version")
        creation_date = root.findtext("creationDate")
        sha256 = root.findtext("sha256")

        dependencies = [dep.text for dep in root.findall("dependencies/dependency")]
        supported_os = [os.text for os in root.findall("supportedOS/os")]
        supported_arch = [arch.text for arch in root.findall("supportedArch/arch")]

        builder = root.findtext("builder")

        return cls(
            name=name,
            version=version,
            creation_date=creation_date,
            sha256=sha256,
            dependencies=dependencies,
            supported_os=supported_os,
            supported_arch=supported_arch,
            builder=builder
        )
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            version=data['version'],
            creation_date=data['creation_date'],
            sha256=data['sha256'],
            dependencies=data['dependencies'],
            supported_os=data['supported_os'],
            supported_arch=data['supported_arch'],
            builder=data.get('builder')
        )

    def __repr__(self):
        return (f"Manifest(name={self.name!r}, version={self.version!r}, creation_date={self.creation_date!r}, "
                f"sha256={self.sha256!r}, dependencies={self.dependencies!r}, "
                f"supported_os={self.supported_os!r}, supported_arch={self.supported_arch!r}, "
                f"builder={self.builder!r})")

#ПРИМЕР ИСПОЛЬЗОВАНИЯ:

"""
from manifest import Manifest

manifest = Manifest.from_file("path/to/manifest.xml")
print(manifest)
print("Builder:", manifest.builder)
"""