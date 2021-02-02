from behave import step

from utils import assert_attribute
from utils import IfcFile
from bimtester.ifc import IfcStore


@step("The project must have an identifier of {guid}")
def step_impl(context, guid):
    assert_attribute(IfcStore.file.by_type("IfcProject")[0], "GlobalId", guid)


@step('The project name, code, or short identifier must be "{value}"')
def step_impl(context, value):
    assert_attribute(IfcStore.file.by_type("IfcProject")[0], "Name", value)


@step('The project must have a longer form name of "{value}"')
def step_impl(context, value):
    assert_attribute(IfcStore.file.by_type("IfcProject")[0], "LongName", value)


@step('The project must be described as "{value}"')
def step_impl(context, value):
    assert_attribute(IfcStore.file.by_type("IfcProject")[0], "Description", value)


@step('The project must be categorised under "{value}"')
def step_impl(context, value):
    assert_attribute(IfcStore.file.by_type("IfcProject")[0], "ObjectType", value)


@step('The project must contain information about the "{value}" phase')
def step_impl(context, value):
    assert_attribute(IfcStore.file.by_type("IfcProject")[0], "Phase", value)


@step("The project must contain 3D geometry representing the shape of objects")
def step_impl(context):
    assert get_subcontext("Body", "Model", "MODEL_VIEW")


@step("The project must contain 3D geometry representing clearance zones")
def step_impl(context):
    assert get_subcontext("Clearance", "Model", "MODEL_VIEW")


@step("The project must contain 3D geometry representing the center of gravity of objects")
def step_impl(context):
    assert get_subcontext("CoG", "Model", "MODEL_VIEW")


@step("The project must contain 3D geometry representing the object bounding boxes")
def step_impl(context):
    assert get_subcontext("Box", "Model", "MODEL_VIEW")


def get_subcontext(identifier, type, target_view):
    project = IfcFile.get().by_type("IfcProject")[0]
    for rep_context in project.RepresentationContexts:
        for subcontext in rep_context.HasSubContexts:
            if (
                subcontext.ContextIdentifier == identifier
                and subcontext.ContextType == type
                and subcontext.TargetView == target_view
            ):
                return True
    assert False, "The subcontext with identifier {}, type {}, and target view {} could not be found".format(
        identifier, type, target_view
    )


@step('the project has a {attribute_name} attribute with a value of "{attribute_value}"')
def step_impl(context, attribute_name, attribute_value):
    project = IfcFile.get().by_type("IfcProject")[0]
    assert getattr(project, attribute_name) == attribute_value
