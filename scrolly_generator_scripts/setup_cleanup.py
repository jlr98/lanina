import os, subprocess, json, shutil, sys

def load_config(project):
  # load default config options
  with open(os.path.join(sys.path[0], 'default_config.json'), 'r') as f:
    default_config = json.load(f)
  
  # load use config options
  path = os.path.join(project, 'config.json')
  if os.path.exists(path):
    with open(path, 'r') as f:
      user_config = json.load(f)
  else:
    user_config = {}

  # return config dict with default overwritten by user definitions
  return {**default_config, **user_config}

def load_css(project):
  path = os.path.join(project, 'styles.css')
  if os.path.exists(path):
    with open(path, 'r') as f:
      css = f.readlines()
  else:
    css = ['']
  css[-1] += '\n'
  return css

def load_base_component(path):
  # load base component
  with open(path, 'r') as f:
    base_component_lines = f.readlines()

  # find the start of the script for import injections
  so_script_idx = base_component_lines.index('<script>\n') + 1
  # find the injection point for actions code
  action_idx = base_component_lines.index('//Actions\n') + 1
  # find the end of the script for component injections
  eo_script_idx = base_component_lines.index('</script>\n') + 1
  # find the start of the style for css injection
  so_style_idx = base_component_lines.index('<style global>\n') + 1

  return base_component_lines, so_script_idx, action_idx, eo_script_idx, so_style_idx

def write_to_file(path, data):
  # write new app to temporary file
  with open(path, 'w') as f:
    f.writelines(data)

def run_build():
  # build the temp app into a temp dist.js
  subprocess.call(['npm', 'run', 'build', '--prefix', os.path.join('svelte-scrolly-base')])


def construct_index_html(f_name):
  return f'''
      <!DOCTYPE html>
      <html lang="en">
        <head>
          <meta charset="utf-8" />
          <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
          <meta name="viewport" content="width=device-width, initial-scale=1" />
          <meta name="theme-color" content="#000000" />
          <meta
            name="description"
            content="Scrolly Website"
          />
          <link rel="manifest" href="%PUBLIC_URL%/manifest.json" />
          <title>Scrolly Website</title>
        </head>
        <body>
          <noscript>You need to enable JavaScript to run this app.</noscript>
          <div id="scrolly"></div>  
          <script src="{f_name}"></script>
        </body>
      </html>
    '''

def clean_up(svelte_temp_path, project):
  try:
    # remove temp files and rename final dist.js file
    os.remove(svelte_temp_path)
    build_path = os.path.join(project, 'build')
    if os.path.exists(build_path):
      shutil.rmtree(build_path)
    build_path = shutil.copytree(project, build_path)
    os.remove(os.path.join(build_path, 'config.json'))
    os.remove(os.path.join(build_path, 'styles.css'))
    f_name = f'{project.split("/")[1]}.dist.js'
    shutil.move(os.path.join('projects', 'temp.dist.js'), os.path.join(build_path, f_name))
    with open(os.path.join(build_path, 'index.html'), 'w') as f:
      f.write(construct_index_html(f_name))
  except FileNotFoundError:
    print('Could not clean up properly, some files were missing. There is most likely a useful error message above this.')