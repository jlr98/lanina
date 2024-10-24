import json, uuid, re
import urllib.parse

void_elements = [
  'area',
  'base',
  'br',
  'col',
  'command',
  'embed',
  'hr',
  'img',
  'input',
  'keygen',
  'link',
  'meta',
  'param',
  'source',
  'track',
  'wbr'
]

void_tags = [
  'Arrow',
  'Divider',
  'Imgchanger',
  'MarkdownSection',
  'Imggrid'
]

tag_prop_types = {
  'Divider': {
    'hr': bool
  },
  'Filler': {
    'center': bool,
    'wide': bool,
    'short': bool,
  },
  'Footer': {
    'bgimage': str,
    'bgcolor': str,
    'bgfixed': bool,
    'center': bool,
    'short': bool
  },
  'Header': {
    'bgimage': str,
    'bgcolor': str,
    'bgfixed': bool,
    'center': bool,
    'short': bool
  },
  'Imgchanger': {
    'src': str,
    'alt': str,
    'changeTime': int,
    'caption': str,
    'title': str
  },
  'Media': {
    'col': str,
    'grid': str,
    'caption': str,
    'height': int,
    'gap': int,
    'title': str
  },
  'Scroller': {
    'top': int,
    'bottom': int,
    'threshold': float,
    'query': str,
    'parallax': bool,
    'splitscreen': bool,
    'id': str
  },
  'Section': {
    'col': str
  },
  'Markdownsection': {
    'col': str,
    'markdownFilePath': str,
    'dataId': str,
    'sectionId': str,
    'sectionClass': str,
    'sectionStyle': dict
  },
  'Arrow': {
    'color': str,
    'animation': bool,
    'center': bool
  },
  'Tableofcontents': {
    'indentAmount': int,
    'headingSelector': str,
    'btnBgColor': str,
    'btnTextColor': str,
    'tableBgColor': str,
    'tableTextColor': str,
    'scrollPaddingTop': str
  },
  'Graph': {
    'station': str,
    'acisParams': dict,
    'acisDataProcessor': str
  },
  'Selector': {
    'value': str,
    'options': list,
    'label': str,
    'borderColor': str,
    'labelColor': str,
    'labelBGColor': str,
    'labelOffset': str,
    'fontSize': str,
    'bgColor': str,
    'textColor': str
  },
  'Imggrid': {
    'width': int,
    'height': int,
    'rows': int,
    'cols': int,
    'imgs': list,
    'gap': int
  },
  'Scrollerbackground': {
    'bgStates': list,
    'bgShowing': str,
    'attributes': dict,
    'offsetTop': str
  },
  'Noaaheader': {
    'date': str,
    'sectionTitle': str
  }
}

default_theme = {
  "text": "#222",
  "muted": "#777",
  "background": "#fff"
}

class ComponentConstructor:
  def __init__(self, tag=None):
    if tag == None:
      raise Exception('Missing tag argument')
    if (not type(tag) is str):
      raise Exception('Tag argument must be a string')
    self.tag = tag[0].capitalize() + tag[1:].lower()
    if self.tag not in tag_prop_types:
      print(self.tag, tag_prop_types.keys())
      raise Exception(f'Tag type "{self.tag}" is not valid')
    self.prop_types = tag_prop_types[self.tag]
    self.is_void_element = self.tag in void_tags
    self.close_tag = f'</{self.tag}>\n'

  def stringify_theme(self, theme_dict, theme_key):
    theme = theme_dict[theme_key] if theme_key in theme_dict else default_theme
    return f' theme={{{json.dumps(theme)}}}'

  def construct_open_tag(self, props, theme):
    open_tag = f'<{self.tag}'

    # adds theme to component using user defined default if themes are defined but theme for
    # # this component isnt defined or this files' default if neither is defined
    open_tag += self.stringify_theme(theme, (props['theme'] if 'theme' in props else 'default'))

    for prop, value in props.items():
      # skip 'theme' prop as it is handled already
      if prop == 'theme':
        continue

      if prop != 'slot':
        if prop not in self.prop_types or (type(value) != self.prop_types[prop] and type(value) not in self.prop_types[prop]):
          raise Exception(f'Invalid prop type {prop}: {str(value)}')

      if prop == 'id' and self.tag == 'Scroller':
        open_tag += f' bind:id={{id["{value}"]}}'
        continue
      elif prop == 'value' and self.tag == 'Selector':
        open_tag += (' bind:value=' + value)
        continue
      elif value == True or str(value).lower() == 'true':
        str_value = '{true}'
      elif value == False or str(value).lower() == 'false':
        str_value = '{false}'
      elif type(value) == dict or type(value) == list:
        str_value = '{' + json.dumps(value) + '}'
      elif type(value) == str and '${' in value and '}' in value:
        str_value = '{`' + json.dumps(value)[1:-1] + '`}'
      else:
        str_value = json.dumps(value)

      # Fix up text so that variable usage works
      str_value = re.sub(r'^("{)(\S*)(}")$',r'{\2}', str_value)
      str_value = re.sub(r'[:\s]("{)(\S*)(}")',r'\2', str_value)

      open_tag += f' {prop}={str_value}'
    open_tag += ('/>\n' if self.is_void_element else '>')
    return open_tag
  
  def assemble_html_from_dict(self, html_tag_dict, theme):
    if not type(html_tag_dict) is dict:
      raise Exception('Error parsing html_content. Make sure html_content is a list of dicts')

    tag = html_tag_dict["tag"].lower()

    id_defined = False
    html_open = f'<{tag}'
    if 'attributes' in html_tag_dict:
      for attribute, value in html_tag_dict['attributes'].items():
        if attribute == 'id': id_defined = True
        if attribute == 'style':
          html_open += f' {attribute}="{"".join([f"{cssAttr}: {cssVal};" for cssAttr, cssVal in value.items()])}"'
        else:
          html_open += f' {attribute}="{value}"'
    
    if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'] and not id_defined:
      if 'text' in html_tag_dict:
        t = '_'.join(html_tag_dict['text'].split(' '))
      else:
        t = 'No_title'
      html_open += f' id="{urllib.parse.quote(t)}"'

    if html_tag_dict["tag"] in void_elements:
      html_open += '/>'
      html_close = ''
    else:
      html_open += '>'
      html_close = f'</{tag}>'
    
    nested_components = []
    if 'text' in html_tag_dict:
      html_text = html_tag_dict['text']
    elif 'html_content' in html_tag_dict:
      html_text, nested_components = self.construct_html_content(html_tag_dict['html_content'], theme)
    else:
      html_text = ''

    return html_open + html_text + html_close, nested_components
  
  def assemble_component_from_dict(self, html_tag_dict, theme):
    try:
      html_content = html_tag_dict['html_content']
    except:
      html_content = []

    try:
      props = html_tag_dict['props']
    except:
      props = {}

    return ComponentConstructor(html_tag_dict['type']).create_content(html_content, props, theme)

  def construct_html_content(self, html_content, theme):
    html_strs = []
    nested_components = []
    for html_tag_dict in html_content:
      if "tag" in html_tag_dict:
        html_str, ncs = self.assemble_html_from_dict(html_tag_dict, theme)
        html_strs.append(html_str)
        nested_components += ncs
      elif "type" in html_tag_dict:
        html_str, ncs = self.assemble_component_from_dict(html_tag_dict, theme)
        nested_components = nested_components + ncs + [{ "type": html_tag_dict["type"] }]
        html_strs.append(html_str)
    return ''.join(html_strs), nested_components

  def create_content(self, html_content=[], props={}, theme={}):
    open_tag = self.construct_open_tag(props, theme)
    if self.is_void_element:
      return open_tag, []
    
    html_str, nested_components = self.construct_html_content(html_content, theme)
    return open_tag + html_str + self.close_tag, nested_components