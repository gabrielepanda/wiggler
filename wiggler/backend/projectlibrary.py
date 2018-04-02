import os
import tempfile
import shutil
import uuid
import yaml
import zipfile


project_tree_file_content = {
    "assets_type": "project",
    "assets_priority": "project",
    "assets_dir": "project",
    "assets": {},
}

class ProjectLibrary(object):

    def __init__(self, project_file):
        if project_file is not None:
            self._render_dir = tempfile.mkdtemp(prefix="wiggler-project-")
            self.unzip_project()
        elif project_dir is not None:
            self._render_dir = project_dir
        else:
            self.create_new_project()

    def wipe_render_dir(self):
        shutil.rmtree(self._render_dir)
        os.mkdir(self._render_dir)

    def create_new_project(self):
        self.assets_dir = os.path.join(self._render_dir, "assets")
        os.mkdir(self.assets_dir)
        self.src_dir = os.path.join(self._render_dir, "src")
        os.mkdir(self.src_dir)
        # add setup.py
        self.controller_module = os.path.join(self._render_dir,
                                              "controller.py")
        project_tree_dir = os.path.join(self.assets_dir, "project")
        os.mkdir(project_tree_dir)
        project_tree_filename = os.path.join(self.assets_dir, "project.yaml")
        project_tree_file_content["id"] = str(uuid.uuid4())
        with open(project_tree_filename, "w") as project_tree_file:
            yaml.safe_dump(project_tree_file_content, stream=project_tree_file, default_flow_style=False)

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

