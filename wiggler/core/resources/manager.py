import copy
import os
import pkg_resources
import pygame
import shutil
import tempfile
import yaml
import zipfile

from wiggler.core.cast import Cast
from wiggler.core.self_sufficiency import SelfSufficiency
from wiggler.engine.background import Background
from wiggler.engine.events import EventQueue


project_load
  load_characters
  load_backgrounds

Factory(Asset):

class ProjectManager(object):
        self._render_dir = tempfile.mkdtemp(prefix="wiggler-modules-")
        os.mkdir(self.render_dir)
        self.controller_module = os.path.join(self._render_dir,
                                              "controller.py")

        # self.main_event_queue = EventQueue()
        self.reset_modules_dir()

    #def reset_modules_dir(self):
    def reset_render_dir(self):
        shutil.rmtree(self.render_dir)
        os.mkdir(self.render_dir)

    def unzip_project(self, filename=None):
        temp_dir = tempfile.mkdtemp(prefix="wiggler-project-")
        if filename is not None:
            self.filename = filename
            with zipfile.ZipFile(self.filename, 'r') as project_file:
                project_file.extractall(self.temp_dir)
        with open(self.def_filename) as project_file:
            project_def = yaml.load(project_file.read())
        return temp_dir
        return project_def

    def zip_project(self, filename=None):
        if filename is None:
            filename = self.filename
        with zipfile.ZipFile(filename, 'w') as project_file:
            for root, dirs, files in os.walk(self.temp_dir):
                rel_path = os.path.relpath(root, start=self.temp_dir)
                project_file.write(root, rel_path)
                for name in files:
                    project_file.write(
                        os.path.join(root, name),
                        os.path.join(rel_path, name))

    def cleanup_project(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

        self.projectres = None
        self.project_def = None


class EngineManager():
        # pygame resources
        self.clock = None
        self.resolution = None
        self.cast = Cast(self)
        self.engine_events = None
        self.background = Background(self)


class ResourcesManager()
        self.selfsuff = SelfSufficiency(self)


class Engine():

    def set_pygame_resources(self):
        self.resolution = self.conf['stage_resolution']
        sound_channels = self.conf['sound_channels']
        reserved_channels = self.conf['reserved_channels']
        self.sound_channels = SoundChannels(sound_channels, reserved_channels)
        self.clock = pygame.time.Clock()
        self.engine_events = EventQueue()

