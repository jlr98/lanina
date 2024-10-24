import os, sys

from content_construction import construct_needed_components, gather_needed_imports, generate_action_code
from setup_cleanup import load_base_component, load_config, load_css, write_to_file, run_build, clean_up

def main(project):
  # define paths for base component data and output location
  svelte_base_component_path = os.path.join('svelte-scrolly-base','src', 'App.svelte')
  svelte_temp_path = os.path.join('projects', f'temp.svelte')

  # load base component data and indices for content injection
  base_component_lines, so_script_idx, action_idx, eo_script_idx, so_style_idx = load_base_component(svelte_base_component_path)

  # load the configuration file for the project
  config = load_config(project)

  # create imports and components to add to base
  action_code = generate_action_code(config['scroller'] if 'scroller' in config else {})
  components_to_insert, nested_components = construct_needed_components(config['components'], config['theme'] if 'theme' in config else {})
  imports_to_insert = gather_needed_imports(config['components'] + nested_components)
  css_to_insert = load_css(project)

  # inject imports and components into base
  new_component = (base_component_lines[0:so_script_idx]
                + imports_to_insert
                + base_component_lines[so_script_idx:action_idx]
                + action_code
                + base_component_lines[action_idx:eo_script_idx]
                + components_to_insert
                + base_component_lines[eo_script_idx:so_style_idx]
                + css_to_insert
                + base_component_lines[so_style_idx:])

  write_to_file(svelte_temp_path, new_component)
  run_build()
  clean_up(svelte_temp_path, project)
    
if __name__ == '__main__':
  main(sys.argv[1])