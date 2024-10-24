# scrolly-generator

A Python script that reads in an JSON file and outputs a Javascript file that can be dropped into a website.

## Table of Contents
- [scrolly-generator](#scrolly-generator)
  - [Table of Contents](#table-of-contents)
  - [Setup](#setup)
  - [Usage](#usage)
    - [Input directory project structure](#input-directory-project-structure)
      - [styles.css](#stylescss)
        - [Available Global Classes](#available-global-classes)
          - [col-full](#col-full)
          - [col-extra-wide](#col-extra-wide)
          - [col-wide](#col-wide)
          - [col-medium](#col-medium)
          - [col-narrow](#col-narrow)
          - [height-full](#height-full)
          - [height-full-minus-title](#height-full-minus-title)
          - [center](#center)
          - [middle](#middle)
          - [caption](#caption)
      - [config.json](#configjson)
    - [Component Objects](#component-objects)
      - [Available Components](#available-components)
        - [Arrow](#arrow)
        - [Divider](#divider)
        - [Filler](#filler)
        - [Footer](#footer)
        - [Graph](#graph)
        - [Header](#header)
        - [Imgchanger](#imgchanger)
        - [Imggrid](#imggrid)
        - [Markdownsection](#markdownsection)
        - [Media](#media)
        - [Noaaheader](#noaaheader)
        - [Scroller](#scroller)
        - [Scrollerbackground](#scrollerbackground)
        - [Section](#section)
        - [Selector](#selector)
        - [Tableofcontents](#tableofcontents)
    - [Scroller Object](#scroller-object)
    - [Theme Object](#theme-object)
    - [Quirks and Helpful Tips](#quirks-and-helpful-tips)
  - [Development](#development)

## Setup

Build the Docker image using `docker build -t scrolly_generator:1 -f Dockerfile .`
*NOTE* The build process may take a few minutes to complete.

[^ Back to Top ^](#table-of-contents)


## Usage

Run the build command: `docker compose run --rm scrolly_generator python scrolly_generator_scripts/scrolly_generator.py projects/[PROJECT_NAME]` from the root directory of this package to create a Javascript file for `[PROJECT_NAME]`. Replace `[PROJECT_NAME]` with the name of the directory you want to build from that is within `projects/`. This command will create `/projects/[PROJECT_NAME]/build` which will contain all of the necessary files for you to run your website.

In order to add the file into a website you must add `<div id="scrolly"></div>` into `index.html` and inject the Javascript file into the page. If you are using this generator to create your entire website then this is done for you. If you want to use a framework (such as React) in conjunction with this generator you can see an example of how to inject this output in `/sample/react`. The important pieces are that `sample.dist.js` resides in `/public` and the `/src/App.js` utilizes the "useScript" hook to run `sample.dist.js`.

[^ Back to Top ^](#table-of-contents)


### Input directory project structure
Each project should be structured as below:

```
└── projects
    └── [project name]
        ├── config.json
        ├── style.css (optional)
        └── markdown (optional)
            └── Any necessary markdown (.md) files
        └── assets (optional)
            └── Any necessary assets like images
```

[^ Back to Top ^](#table-of-contents)


#### styles.css

This optional file can include any css that you wish to include in the project. This can be helpful to import custom fonts, fine tune layouts, and customize components.

If you are targeting a specific HTML tag. the selector must be written as below and it may be necessary to include "!important" if it is overwritting a style defined in `/svelte-scrolly-base/src/App.svelte`.
```
:global(footer) {
  margin-top: 10px !important;
}
```

[^ Back to Top ^](#table-of-contents)


##### Available Global Classes

The following classes are defined with a global scope so that they are usable with any HTML element defined in your [config.json](#configjson) by adding them to the "class" key in "attributes" (see the example in [component objects](#component-objects) for implementation details).

######   col-full
  |Property Name|Property Value|
  |----|----|
  |width|100%|

[^ Back to Top ^](#table-of-contents)

######  col-extra-wide
  |Property Name|Property Value|
  |----|----|
  |width|100%|
  |max-width|1280px|
  |margin|0px 24px|

[^ Back to Top ^](#table-of-contents)

######  col-wide
  |Property Name|Property Value|
  |----|----|
  |width|100%|
  |max-width|980px|
  |margin|0px 24px|

[^ Back to Top ^](#table-of-contents)

######  col-medium
  |Property Name|Property Value|
  |----|----|
  |width|100%|
  |max-width|680px|
  |margin|0px 24px|

[^ Back to Top ^](#table-of-contents)

######  col-narrow
  |Property Name|Property Value|
  |----|----|
  |width|100%|
  |max-width|540px|
  |margin|0px 24px|

[^ Back to Top ^](#table-of-contents)

######  height-full
  |Property Name|Property Value|
  |----|----|
  |min-height|100vh|

[^ Back to Top ^](#table-of-contents)

######  height-full-minus-title
  If adding a "backgroundTitle" slot to a [**Scroller**](#scroller) component, add this class to the "background" slot element. This will adjust the [**Scroller**](#scroller) to account for the "backgroundTitle".

  |Property Name|Property Value|
  |----|----|
  |min-height|100vh - 60px|

[^ Back to Top ^](#table-of-contents)

######  center
  |Property Name|Property Value|
  |----|----|
  |text-align|center|

[^ Back to Top ^](#table-of-contents)

######  middle
  Vertically centers content, useful to center "background" slot content in [**Scroller**](#scroller) components.

  |Property Name|Property Value|
  |----|----|
  |height|100%|
  |display|flex|
  |flex-direction|column|
  |justify-content|center|

[^ Back to Top ^](#table-of-contents)

######  caption
  Used internally for [**Media**](#media) and [**Imgchanger**](#imgchanger) components to style the "caption" elements.

  |Property Name|Property Value|
  |----|----|
  |margin-top|8px|
  |text-align|left|
  |font-size|14px|
  |color|#777|

[^ Back to Top ^](#table-of-contents)

#### config.json

This file must contain a "components" key and the value should be an array of [component objects](#component-objects).

If a [**Scroller**](#scroller) component is being used, you must provide a "scroller" key containing a [scroller object](#scroller-object).

You may also provide an optional "theme" key with a [theme object](#theme-object).

[^ Back to Top ^](#table-of-contents)

### Component Objects

Each component object must contain a "type" that corresponds to one of the components in these docs. The object can also contain "props" (as noted in the relevant components' documentation) and some can accept "attributes" (like [**Section**](#section)). Any component not noted as a "void element" can accept "html_content" which should be an array of more components or HTML objects. All components can accept a "props" key "theme" which should be a string matching a key in the [theme object](#theme-object).

HTML objects must contain a "tag" with a value of a valid HTML element. If applicable, the object can accept a "text" key with a string value that will be the text in the output element. HTML objects can also accept an "attributes" object which can contain any attributes that the tag normally would in HTML (like a "class" string or "style" object).

Below is a simple example:
```
{
  "components": {
    "type": "Header",
    "html_content": [{
      "tag": "h1",
      "text": "This is the title"
    },{
      "tag": "p",
      "text": "This is a short text description of the page contents",
      "attributes": {
        "class": "text-big",
        "style": {
          "margin-top": "5px"
        }
      }
    }]
  }
}
```

[^ Back to Top ^](#table-of-contents)


#### Available Components
##### Arrow

A downward facing arrow that can be used to indicate content below and includes an optional animation.

*Void element: does not accept html_content*

|Prop Name|Type|Default|Description|
|----|----|----|----|
|color|string|black|Changes the color of the arrow|
|animation|bool|true|Causes the arrow to move up and down in a bouncing motion|

[^ Back to Top ^](#table-of-contents)

---


##### Divider

A horizontal divider that can be used between sections.

*Void element: does not accept html_content*

|Prop Name|Type|Default|Description|
|----|----|----|----|
|hr|bool|true|Uses an 'hr' element. If false it will be a blank spacer|

[^ Back to Top ^](#table-of-contents)

---


##### Filler

This is for full screen captions etc, typically used to introduce an article or to provide a break/transition between sections.

|Prop Name|Type|Default|Description|
|----|----|----|----|
|center|bool|true|Centers content in the component|
|short|bool|false|Shortens the component to 70vh (default is 100vh)|
|wide|bool|false|Makes the component full width|

[^ Back to Top ^](#table-of-contents)

---


##### Footer

A footer component for the bottom of the article, with an optional background image which can be static or scroll with the text.

|Prop Name|Type|Default|Description|
|----|----|----|----|
|bgimage|string|null|a URL for an image that will be used as the background of the footer. This has priority over "bgcolor"|
|bgcolor|string|null|a color to use as the background for the footer|
|bgfixed|boolean|false|Allows the background image to move as the user scrolls |
|center|boolean|true|Centers the header content within the footer|
|short|boolean|false|Shortens the footer to 15vh (default is 30vh)|

[^ Back to Top ^](#table-of-contents)

---


##### Graph

A scatter plot component to display data directly from ACIS.

|Prop Name|Type|Default|Description|
|----|----|----|----|
|station|object|null|Required. Object requires 'value' key. The value of 'value' must be a valid SID for the ACIS API.|
|acisParams|object|null|Required. Object must be a valid parameters object for the ACIS API.|
|acisDataProcessor|string|default|Determines how to process the data after it is fetched but before displaying. You may need to have a developer create a processor for your use case. Available options are: 'default', 'basic'|

Data Processor Options:
__default__: No processing occurs. Whatever the API returns is what is displayed
__basic__: Converts the first param to 'x' and the second to 'y'. Adds the season and if it was an El Nino year to the point data.

[^ Back to Top ^](#table-of-contents)

---


##### Header

A full height component for the top of the article, with an optional background image which can be static or scroll with the text.

|Prop Name|Type|Default|Description|
|----|----|----|----|
|bgimage|string|null|a URL for an image that will be used as the background of the header. This has priority over "bgcolor"|
|bgcolor|string|null|a color to use as the background for the header|
|bgfixed|boolean|false|Allows the background image to move as the user scrolls |
|center|boolean|true|Centers the header content within the header|
|short|boolean|false|Shortens the header to 85vh (default is 100vh)|

[^ Back to Top ^](#table-of-contents)

---


##### Imgchanger

A component similar to the [**Media**](#media) component. If the "src", "caption", or "title" prop value changes then the component will fade out (using half of the "changeTime"), change the content while hidden, then fade back in (using the other half of the "changeTime").

*Void element: does not accept html_content*

|Prop Name|Type|Default|Description|
|----|----|----|----|
|alt|string|''|A string to display if the image does not load and for screen reader usage|
|caption|string|''|Adds the string to a caption element below the image. If including HTML use single quotes, not double|
|changeTime|string|500|Number of milliseconds it should take to change from one image to the next|
|src|string|null|A URL or relative path to an image to be used in the display|
|title|string|''|Adds the string to an h3 element above the image|

[^ Back to Top ^](#table-of-contents)

---


##### Imggrid

A component to display several imgs in a grid pattern. On img hover a popup displays the images 'hoverText'. On img click, opens the fullsize img in a modal. Allows for many grid sizes, accepts videos as MP4s, and can place a title and/or caption on each img. It is not recommended to use this for multiple videos, and adding titles and captions to grids larger than 1x1 can look messy, especially if not all imgs have them.

*Void element: does not accept html_content*

|Prop Name|Type|Default|Description|
|----|----|----|----|
|width|string|100%|Sets width of entire grid|
|height|string|calc(100vh - 110px)|Sets height of entire grid. Default is specific to use with [**Noaaheader**](#noaaheader), it is recommended that you define this property yourself|
|rows|integer|1|Number of rows to create|
|cols|integer|1|Number of columns to create|
|gap|integer|0|Space to leave between each img|
|imgs|list|[]|List of img objects. See below for object structure|

Image Object Structure:
```
{
  src: string,
  title: string,
  alt: string,
  caption: string,
  gridColSpan: integer,
  gridRowSpan: integer,
  hoverText: string
}
```
alt, caption, source, and title are described in [**Imgchanger**](#imgchanger).
gridcolspan - number of columns the img should take up
gridrowspan - number of rows the img should take up
hoverText - text to display in popup when imgis hovered over

[^ Back to Top ^](#table-of-contents)

---


##### Markdownsection

A component to display markdown content as an easier alternative to writing HTML in `config.json`. Any markdown files that are used in these components should be contained in `/markdown/`, a top level directory available to the final website. Either a __markdownFilePath__ or a __dataId__ must be defined and there must be a markdown files with the same name in the previously mentioned directory.

*Void element: does not accept html_content*


|Prop Name|Type|Default|Description|
|----|----|----|----|
|markdownFilePath|string|null|Name of markdown file in `/markdown/`|
|dataId|string|''|Name of markdown file in `/markdown/`. Also used for state changes as described in [**Scroller**](#scroller)|
|col|string|medium|Size of the column to use for the markdown content. Other options are shown in [**Section**](#section)|
|sectionId|string|''|Used to define the id of the section HTML element that is created as the container for the markdown content|
|sectionClass|string|''|Used to define the class of the section HTML element that is created as the container for the markdown content|
|sectionStyle|object|{}|Used to overwrite style definitions for the section HTML element that is created as the container for the markdown content|

[^ Back to Top ^](#table-of-contents)

---


##### Media

Used to create DIVS for content within a responsive grid (for maps, charts, images etc). It also allows for full width media, a title, and a caption.

|Prop Name|Type|Default|Description|
|----|----|----|----|
|caption|string|null|Adds the string to a caption element below the content grid. If including HTML use single quotes, not double|
|col|string|medium|Options are 'narrow', 'medium', 'wide', 'extra-wide', and 'full'|
|gap|integer|12|Sets the grid gap|
|grid|string|null|Defines the width of the grid. Options are 'narrow', 'medium', and 'wide'|
|height|integer|200|Sets the height of each row in the grid|
|title|string|null|Adds the string to an h3 element above the content grid|

[^ Back to Top ^](#table-of-contents)

---


##### Noaaheader

Premade header component for use in El Niño products.

*Void element: does not accept html_content*

|Prop Name|Type|Default|Description|
|----|----|----|----|
|sectionTitle|string|''|Section title to display in left side subheading. This should be a state variable passed in via `config.json` like `"{state.stickyTitle}"`|
|date|string|''|Date to display in right side subheading|

[^ Back to Top ^](#table-of-contents)

---


##### Scroller

This is a really important component that allows for dynamic scroll-triggered content with interactions coded in Javascript. It is coded by Rich Harris (the creator of Svelte), and is documented [here](https://github.com/sveltejs/svelte-scroller), but has been re-styled with CSS in this repo.

This component will take a bit of time to get your head around. Within each Scroller component you'll need to include a [**Scrollerbackground**](#scrollerbackground) component (as described [here](#scrollbackground)) and a div element with a "slot" attribute of "foreground".

The "foreground" slot should contain a series of [**Section**](#section) and [**Markdownsection**](#markdownsection) elements, which contain the text captions. Each section should have a "data-id" attribute that corresponds to an action (see the [scroller object](#scroller-object) section). If there is no desired state change for a particular section, then the "data-id" should match the previous sections' "data-id".

|Prop Name|Type|Default|Description|
|----|----|----|----|
|top|integer|0|The vertical position that the top of the foreground must scroll past before the background becomes fixed, as a proportion of window height|
|bottom|integer|1|The inverse of top — once the bottom of the foreground passes this point, the background becomes unfixed|
|threshold|float|0.5|Once a section crosses this point, it becomes 'active'|
|query|string|'section'|A CSS selector that describes the individual sections of your foreground|
|parallax|boolean|false|If true, the background will scroll such that the bottom edge reaches the bottom at the same time as the foreground. This effect can be unpleasant for people with high motion sensitivity, so use it advisedly|
|splitscreen|boolean|false|Allows the foreground and background to viewed in separate, non-overlapping columns as the user scrolls|
|id|string|null|Should match a key in the actions portion of the scroller object in the [config.json](#configjson) file|

[^ Back to Top ^](#table-of-contents)

---


##### Scrollerbackground

This component should only be used within a [**Scroller**](#scroller). It allows you to change the content shown as the user scrolls through your page.

**NOTE:** to use this you must supply a prop with the key "slot" and value "background"! This is how the [**Scroller**](#scroller) knows how to render it.

|Prop Name|Type|Default|Description|
|----|----|----|----|
|bgStates|list|[]|List of background state objects. See below for example|
|bgShowing|string|''|Name of the background that should be showing. This should be a "state" variable passed in like `{state.bgThatShouldBeShowing}`|
|offsetTop|string|'0px'|Shift the component down in the page. Used to leave space for headers|

Background State Object Structure:
```
{
  showWhen: string,
  type: string,
  props: object
}
```
showWhen - when "bgShowing" matches this value, this background will be shown
type - component to show, like an [**Imggrid**](#imggrid)
props - the props object that corresponds to the component type selected above

[^ Back to Top ^](#table-of-contents)

---


##### Section

Basic component. Mostly for text content, but can take any HTML or other component needed.

The section component can also accept an "attributes" object with a "data-id" key for use in a [**Scroller**](#scroller) "foreground" slot.

|Prop Name|Type|Default|Description|
|----|----|----|----|
|col|string|medium|Options are 'narrow', 'medium', 'wide', 'extra-wide', and 'full'|

[^ Back to Top ^](#table-of-contents)

---


##### Selector

A dropdown selector component to allow users to change state variables.

*Void element: does not accept html_content*

|Prop Name|Type|Default|Description|
|----|----|----|----|
|bgColor|string|white|Background color of the container surrounding the selector|
|borderColor|string|rgb(150,150,150)|Border color of the container surrounding the selector|
|fontSize|string|16px|Size of the font for the component|
|label|string|''|Label text for the selector|
|labelBGColor|string|default|Overrides background color of the label container. If default, uses 'bgColor' instead|
|labelColor|string|default|Overrides text color of the label. If default, uses the 'textColor' instead|
|labelOffset|string|-0.8em|Where to position the label vertically|
|options|list|undefined|Required. A list of the options to use in the selector. Each option should be an object containing "name" and "value" keys|
|textColor|string|black|Color of the text for the component|
|value|string or integer|undefined|Required. Currently selected value. Should be a "state" variable passed in like `{state.stationId}`|

[^ Back to Top ^](#table-of-contents)

---


##### Tableofcontents

A self constructing table of contents component that allows users to easily move through your content. It searches the page for elements matching the "headingSelector" and creates an entry for each element, using the inner text of the element as the text for the entry. Elements that are assigned the class "toc-exclude" are excluded from the table (as long as "headingSelector" includes ':not(.toc-exclude)'). If the element does not already contain an ID property (necessary for scrollTo funcitonality) one is assigned to it.

*Void element: does not accept html_content*

|Prop Name|Type|Default|Description|
|----|----|----|----|
|headingSelector|string|':is(h2, h3, h4):not(.toc-exclude)'|CSS selector string to find elements that should be included in the table of contents|
|scrollPaddingTop|string|70px|Offsets the scroll when a link is clicked. Used to account for things like headers that cover a portion of the top of the screen|
|indentAmount|integer|30|Number of pixels to indent each level in the heirarchy by|

[^ Back to Top ^](#table-of-contents)

---



### Scroller Object

```
"scroller": {
  "state": {
    "imgAlt": "Sample alt text 1",
    "imgCaption": "Sample caption 1",
    "imgSrc": "sample1.png",
    "imgTitle": "Sample Title 1",
    "title": "Section title 1"
  },
  "actions": {
    "sample": {
      "sample01": [
        ["imgAlt", "Sample alt text 1"],
        ["imgCaption", "Sample caption 1"],
        ["imgSrc", "sample1.png"],
        ["imgTitle", "Sample Title 1"],
        ["title", "Section title 1"]
      ],
      "sample02": [
        ["imgAlt", "Sample alt text 2"],
        ["imgCaption", "Sample caption 2"],
        ["imgSrc", "sample2.png"],
        ["imgTitle", "Sample Title 2"],
        ["title", "Section title 1"]
      ]
    }
  }
}
```

In this sample, as the user scrolls from the "sample01" section to the "sample02" section the img, its title, its caption, and its alt text will all change, but the section title at the top of the screen will not.

The "state" section of the sample defines the initial values that the scroller variables will contain. Any variable that is going to be used must be defined with a valid value here.

The "actions" section of the sample defines what should happen as the user scrolls. The key "sample" should match the "id" of a [**Scroller**](#scroller) component. The value of this key should be an object that contains one key per [**Section**](#section) defined in the "foreground" slot of the [**Scroller**](#scroller). The value of each of these keys should be an array of `[stateVariableName, newValue]`. Each of these arrays will be evaluated and executed as the user scrolls into the relevant section.

[^ Back to Top ^](#table-of-contents)



### Theme Object

A theme can be define in [config.json](#configjson) as below. *Note: "muted" is only used in the [**Divider**](#divider) component.

```
"theme": {
  "light": {
    "text": "#222",
    "muted": "#777",
    "background": "#fff"
  },
  "dark": {
    "text": "#fff",
    "muted": "#bbb",
    "background": "#222"
  }
}
```

[^ Back to Top ^](#table-of-contents)



### Quirks and Helpful Tips
- In captions, make sure to use hexadecimal reference between '&#x' and ';' to inject unicode characters.
- When including html inside the 'text' of an html tag you can use either single or double quotes, but double quotes must be escaped with '\'.
- If using 'img' tags, the 'src' attribute should point to where the image being linked will be in production. For example, in a React app, if the image is named 'test.png' and it is in '/public/assets/' the 'src' attributes should be './assets/test.png'. This applies to [**Imgchanger**](#imgchanger) components as well.
- If you want the scroller sections to be closer together, allowing the background content to change with less scrolling, you can change the top and bottom padding as shown in the sample in the [**Scroller**](#scroller) component (note the style definition in the second sample of the foreground).
- A live example of what can be done with this package can be found [here](https://elnino.nrcc.cornell.edu/).
- There is an example project located in `/sample/project/` to help get you started. You can explore the code there, or copy it into the `/projects` directory and run the build command in [**Usage**](#usage) to see the output from the Scrolly generator.

[^ Back to Top ^](#table-of-contents)



## Development

Svelte components can easily be added for use by:
1. Placing the `*.svelte` file into `/svelte-scrolly-base/src/components/` directory. Be sure that the file name begins with an upper case character and the rest of the name is lower case (i.e. "Imgchanger.svelte")
2. In `/scrolly_generator_scripts/ComponentConstructor.py` add the prop type definitions to the "tag_prop_types" dictionary. "theme" does not need to be included, but any props that the component can be supplied with should be. If the component is a void element (like an "img" or "br") its name should also be included in the "void_tags" list.
3. Add any revelevant tests to `/scrolly_generator_scripts/test_component_constructor.py` to ensure that everything works properly and to keep maintenance easy. All tests in this file can be run by executing `python -m unittest discover scrolly_generator_scripts/` from the root directory of this package. *These tests are not exhaustive and mainly exist to ensure that the ComponentConstructor class operates. It does not ensure that `/run_scrolly_generator.py` will create operational Javascript.*
4. Rerun the `docker build` command in the Setup section to make the new component available for use.