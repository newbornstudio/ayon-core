from ayon_core.pipeline import (
    load,
    get_representation_path,
)
from ayon_core.lib import EnumDef
from ayon_core.pipeline.load import LoadError
from ayon_core.hosts.substancepainter.api.pipeline import (
    imprint_container,
    set_container_metadata,
    remove_container_metadata
)
from ayon_core.hosts.substancepainter.api.lib import (
    parse_substance_attributes_setting,
    parse_subst_attrs_reloading_mesh
)


import substance_painter.project


class SubstanceLoadProjectMesh(load.LoaderPlugin):
    """Load mesh for project"""

    product_types = {"*"}
    representations = {"abc", "fbx", "obj", "gltf", "usd", "usda", "usdc"}

    label = "Load mesh"
    order = -10
    icon = "code-fork"
    color = "orange"
    project_templates = []

    @classmethod
    def get_options(cls, contexts):
        template_enum = [template["name"] for template in cls.project_templates]
        return [
            EnumDef("project_template",
                    items=template_enum,
                    default="default",
                    label="Project Template")
        ]

    def load(self, context, name, namespace, options=None):

        # Get user inputs
        template_name = options.get("project_template", "default")
        template_settings = parse_substance_attributes_setting(
            template_name, self.project_templates)
        sp_settings = substance_painter.project.Settings(**template_settings)
        if not substance_painter.project.is_open():
            # Allow to 'initialize' a new project
            path = self.filepath_from_context(context)

            settings = substance_painter.project.create(
                mesh_file_path=path, settings=sp_settings
            )
        else:
            # Reload the mesh
            mesh_settings = parse_subst_attrs_reloading_mesh(
                template_name, self.project_templates)
            # TODO: fix the hardcoded when the preset setting in SP addon.
            settings = substance_painter.project.MeshReloadingSettings(**mesh_settings)

            def on_mesh_reload(status: substance_painter.project.ReloadMeshStatus):  # noqa
                if status == substance_painter.project.ReloadMeshStatus.SUCCESS:  # noqa
                    self.log.info("Reload succeeded")
                else:
                    raise LoadError("Reload of mesh failed")

            path = self.filepath_from_context(context)
            substance_painter.project.reload_mesh(path,
                                                  settings,
                                                  on_mesh_reload)

        # Store container
        container = {}
        project_mesh_object_name = "_ProjectMesh_"
        imprint_container(container,
                          name=project_mesh_object_name,
                          namespace=project_mesh_object_name,
                          context=context,
                          loader=self)

        # We want store some options for updating to keep consistent behavior
        # from the user's original choice. We don't store 'preserve_strokes'
        # as we always preserve strokes on updates.
        # TODO: update the code
        container["options"] = {
            "import_cameras": template_settings["import_cameras"],
        }

        set_container_metadata(project_mesh_object_name, container)

    def switch(self, container, context):
        self.update(container, context)

    def update(self, container, context):
        repre_entity = context["representation"]

        path = get_representation_path(repre_entity)

        # Reload the mesh
        container_options = container.get("options", {})
        settings = substance_painter.project.MeshReloadingSettings(
            import_cameras=container_options.get("import_cameras", True),
            preserve_strokes=True
        )

        def on_mesh_reload(status: substance_painter.project.ReloadMeshStatus):
            if status == substance_painter.project.ReloadMeshStatus.SUCCESS:
                self.log.info("Reload succeeded")
            else:
                raise LoadError("Reload of mesh failed")

        substance_painter.project.reload_mesh(path, settings, on_mesh_reload)

        # Update container representation
        object_name = container["objectName"]
        update_data = {"representation": repre_entity["id"]}
        set_container_metadata(object_name, update_data, update=True)

    def remove(self, container):

        # Remove OpenPype related settings about what model was loaded
        # or close the project?
        # TODO: This is likely best 'hidden' away to the user because
        #       this will leave the project's mesh unmanaged.
        remove_container_metadata(container["objectName"])
