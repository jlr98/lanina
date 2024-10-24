import json
from ComponentConstructor import ComponentConstructor, tag_prop_types

def initialize_constructors():
  constructors = {}
  for tag in tag_prop_types:
    constructors[tag.lower()] = ComponentConstructor(tag)
  return constructors

def construct_needed_components(components, theme):
  CONSTRUCTORS = initialize_constructors()
  
  # create component contents
  components_to_insert = []
  nested_components = []
  for component in components:
      comp_name = component['type'].lower()

      try:
        html_content = component['html_content']
      except:
        html_content = []

      try:
        props = component['props']
      except:
        props = {}

      # create component and add it to the list
      c, nested_cs = CONSTRUCTORS[comp_name].create_content(html_content, props, theme)
      components_to_insert.append(c)
      nested_components += nested_cs
  return components_to_insert, nested_components

def gather_needed_imports(components):
  # create import statements for all needed component types
  types_handled = []
  imports_to_insert = []
  for component in components:
    # Get component name, skip loop if already handled
    comp_name = component['type']
    if comp_name in types_handled: continue

    # Ensure first letter capitalization for proper import
    import_name = comp_name[0].capitalize() + comp_name[1:].lower()

    # Create the import statement
    new_import = f'\timport {import_name} from "/svelte-scrolly-base/src/components/{import_name}.svelte";\n'

    # Add items to lists
    imports_to_insert.append(new_import)
    types_handled.append(comp_name)
  return imports_to_insert

def generate_action_code(scroller_dict):
  lines = []
  if scroller_dict and type(scroller_dict) == dict and 'state' in scroller_dict and 'actions' in scroller_dict:
    lines.append(f'const state = {json.dumps(scroller_dict["state"])};\n')
    lines.append(f'const actions = {json.dumps(scroller_dict["actions"])};\n')
  else:
    lines.append(f'const state = {{}};\n')
    lines.append(f'const actions = {{}};\n')
  return lines