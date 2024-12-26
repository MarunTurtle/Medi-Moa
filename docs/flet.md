
Controls reference
Flet UI is built of controls. Controls are organized into hierarchy, or a tree, where each control has a parent (except Page) and container controls like Column, Dropdown can contain child controls, for example:

Page
 ├─ TextField
 ├─ Dropdown
 │   ├─ Option
 │   └─ Option
 └─ Row
     ├─ ElevatedButton
     └─ ElevatedButton

Control gallery live demo

Controls by categories
🗃️ Layout
22 items

🗃️ Navigation
8 items

🗃️ Information Displays
12 items

🗃️ Buttons
18 items

🗃️ Input and Selections
16 items

🗃️ Dialogs, Alerts and Panels
13 items

🗃️ Charts
5 items

🗃️ Animations
3 items

🗃️ Utility
22 items

Common control properties
Flet controls have the following properties:

adaptive
adaptive property can be specified for a control in the following cases:

A control has matching Cupertino control with similar functionality/presentation and graphics as expected on iOS/macOS. In this case, if adaptive is True, either Material or Cupertino control will be created depending on the target platform.

These controls have their Cupertino analogs and adaptive property:

AlertDialog
AppBar
Checkbox
ListTile
NavigationBar
Radio
Slider
Switch
A control has child controls. In this case adaptive property value is passed on to its children that don't have their adaptive property set.

The following container controls have adaptive property:

Card
Column
Container
Dismissible
ExpansionPanel
FletApp
GestureDetector
GridView
ListView
Page
Row
SafeArea
Stack
Tabs
View
badge
The badge property (available in almost all controls) supports both strings and Badge objects.

bottom
Effective inside Stack only. The distance that the child's bottom edge is inset from the bottom of the stack.

data
Arbitrary data that can be attached to a control.

disabled
Every control has disabled property which is False by default - control and all its children are enabled. disabled property is mostly used with data entry controls like TextField, Dropdown, Checkbox, buttons. However, disabled could be set to a parent control and its value will be propagated down to all children recursively.

For example, if you have a form with multiple entry controls you can disable them all together by disabling container:

c = ft.Column(controls=[
    ft.TextField(),
    ft.TextField()
])
c.disabled = True
page.add(c)

expand
When a child Control is placed into a Column or a Row you can "expand" it to fill the available space. expand property could be a boolean value (True - expand control to fill all available space) or an integer - an "expand factor" specifying how to divide a free space with other expanded child controls.

For more information and examples about expand property see "Expanding children" sections in Column or Row.

expand_loose
Effective only if expand is True.

If expand_loose is True, the child control of a Column or a Row will be given the flexibility to expand to fill the available space in the main axis (e.g., horizontally for a Row or vertically for a Column), but will not be required to fill the available space.

The default value is False.

Here is the example of Containers placed in Rows with expand_loose = True:

import flet as ft


class Message(ft.Container):
    def __init__(self, author, body):
        super().__init__()
        self.content = ft.Column(
            controls=[
                ft.Text(author, weight=ft.FontWeight.BOLD),
                ft.Text(body),
            ],
        )
        self.border = ft.border.all(1, ft.Colors.BLACK)
        self.border_radius = ft.border_radius.all(10)
        self.bgcolor = ft.Colors.GREEN_200
        self.padding = 10
        self.expand = True
        self.expand_loose = True


def main(page: ft.Page):
    chat = ft.ListView(
        padding=10,
        spacing=10,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    Message(
                        author="John",
                        body="Hi, how are you?",
                    ),
                ],
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.END,
                controls=[
                    Message(
                        author="Jake",
                        body="Hi I am good thanks, how about you?",
                    ),
                ],
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    Message(
                        author="John",
                        body="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.",
                    ),
                ],
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.END,
                controls=[
                    Message(
                        author="Jake",
                        body="Thank you!",
                    ),
                ],
            ),
        ],
    )

    page.window.width = 393
    page.window.height = 600
    page.window.always_on_top = False

    page.add(chat)


ft.app(main)




height
Imposed Control height in virtual pixels.

left
Effective inside Stack only. The distance that the child's left edge is inset from the left of the stack.

parent
Points to the direct ancestor(parent) of this control.

It defaults to None and will only have a value when this control is mounted (added to the page tree).

The Page control (which is the root of the tree) is an exception - it always has parent=None.

right
Effective inside Stack only. The distance that the child's right edge is inset from the right of the stack.

tooltip
The tooltip property (available in almost all controls) now supports both strings and Tooltip objects.

top
Effective inside Stack only. The distance that the child's top edge is inset from the top of the stack.

visible
Every control has visible property which is True by default - control is rendered on the page. Setting visible to False completely prevents control (and all its children if any) from rendering on a page canvas. Hidden controls cannot be focused or selected with a keyboard or mouse and they do not emit any events.

width
Imposed Control width in virtual pixels.

Transformations
offset
Applies a translation transformation before painting the control.

The translation is expressed as a transform.Offset scaled to the control's size. For example, an Offset with a x of 0.25 will result in a horizontal translation of one quarter the width of the control.

The following example displays container at 0, 0 top left corner of a stack as transform applies -1 * 100, -1 * 100 (offset * control_size) horizontal and vertical translations to the control:

import flet as ft

def main(page: ft.Page):

    page.add(
        ft.Stack(
            [
                ft.Container(
                    bgcolor="red",
                    width=100,
                    height=100,
                    left=100,
                    top=100,
                    offset=ft.transform.Offset(-1, -1),
                )
            ],
            width=1000,
            height=1000,
        )
    )

ft.app(main)

opacity
Defines the transparency of the control.

Value ranges from 0.0 (completely transparent) to 1.0 (completely opaque without any transparency) and defaults to 1.0.

rotate
Transforms control using a rotation around the center.

The value of rotate property could be one of the following types:

number - a rotation in clockwise radians. Full circle 360° is math.pi * 2 radians, 90° is pi / 2, 45° is pi / 4, etc.
transform.Rotate - allows to specify rotation angle as well as alignment - the location of rotation center.
For example:

ft.Image(
    src="https://picsum.photos/100/100",
    width=100,
    height=100,
    border_radius=5,
    rotate=Rotate(angle=0.25 * pi, alignment=ft.alignment.center_left)
)

scale
Scale control along the 2D plane. Default scale factor is 1.0 - control is not scaled. 0.5 - the control is twice smaller, 2.0 - the control is twice larger.

Different scale multipliers can be specified for x and y axis, but setting Control.scale property to an instance of transform.Scale class:

from dataclasses import field

class Scale:
    scale: float = field(default=None)
    scale_x: float = field(default=None)
    scale_y: float = field(default=None)
    alignment: Alignment = field(default=None)

Either scale or scale_x and scale_y could be specified, but not all of them, for example:

ft.Image(
    src="https://picsum.photos/100/100",
    width=100,
    height=100,
    border_radius=5,
    scale=Scale(scale_x=2, scale_y=0.5)
)

========================

Card
A material design card: a panel with slightly rounded corners and an elevation shadow.

Examples
Live example

Python
import flet as ft

def main(page):
    page.title = "Card Example"
    page.add(
        ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.ALBUM),
                            title=ft.Text("The Enchanted Nightingale"),
                            subtitle=ft.Text(
                                "Music by Julie Gable. Lyrics by Sidney Stein."
                            ),
                        ),
                        ft.Row(
                            [ft.TextButton("Buy tickets"), ft.TextButton("Listen")],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ]
                ),
                width=400,
                padding=10,
            )
        )
    )

ft.app(main)



Properties
clip_behavior
The content will be clipped (or not) according to this option.

Value is of type ClipBehavior and defaults to ClipBehavior.NONE.

color
The card's background color.

content
The Control that should be displayed inside the card.

This control can only have one child. To lay out multiple children, let this control's child be a control such as Row, Column, or Stack, which have a children property, and then provide the children to that control.

elevation
Controls the size of the shadow below the card. Default value is 1.0.

is_semantic_container
Set to True (default) if this card represents a single semantic container, or to False if it instead represents a collection of individual semantic nodes (different types of content).

margin
The empty space that surrounds the card.

Value can be one of the following types: int, float, or Margin.

shadow_color
The color to paint the shadow below the card.

shape
The shape of the card.

Value is of type OutlinedBorder and defaults to RoundedRectangleBorder(radius=4.0).

show_border_on_foreground
Whether the shape of the border should be painted in front of the content or behind.

Defaults to True.

surface_tint_color
The color used as an overlay on color to indicate elevation.

If this is None, no overlay will be applied. Otherwise this color will be composited on top of color with an opacity related to elevation and used to paint the background of the card.

Defaults to None.

variant
Defines the card variant to be used.

Value is of type CardVariant and defaults to CardVariant.ELEVATED.

========================

Column
A control that displays its children in a vertical array.

To cause a child control to expand and fill the available vertical space set its expand property.

Examples
Live example

Column spacing

Python
import flet as ft

def main(page: ft.Page):
    def items(count):
        items = []
        for i in range(1, count + 1):
            items.append(
                ft.Container(
                    content=ft.Text(value=str(i)),
                    alignment=ft.alignment.center,
                    width=50,
                    height=50,
                    bgcolor=ft.Colors.AMBER,
                    border_radius=ft.border_radius.all(5),
                )
            )
        return items

    def spacing_slider_change(e):
        col.spacing = int(e.control.value)
        col.update()

    gap_slider = ft.Slider(
        min=0,
        max=100,
        divisions=10,
        value=0,
        label="{value}",
        width=500,
        on_change=spacing_slider_change,
    )

    col = ft.Column(spacing=0, controls=items(5))

    page.add(ft.Column([ ft.Text("Spacing between items"), gap_slider]), col)

ft.app(main)

Column wrapping

Python
import flet as ft

HEIGHT = 400

def main(page: ft.Page):
    def items(count):
        items = []
        for i in range(1, count + 1):
            items.append(
                ft.Container(
                    content=ft.Text(value=str(i)),
                    alignment=ft.alignment.center,
                    width=30,
                    height=30,
                    bgcolor=ft.Colors.AMBER,
                    border_radius=ft.border_radius.all(5),
                )
            )
        return items

    def slider_change(e):
        col.height = float(e.control.value)
        col.update()

    width_slider = ft.Slider(
        min=0,
        max=HEIGHT,
        divisions=20,
        value=HEIGHT,
        label="{value}",
        width=500,
        on_change=slider_change,
    )

    col = ft.Column(
        wrap=True,
        spacing=10,
        run_spacing=10,
        controls=items(10),
        height=HEIGHT,
    )

    page.add(
        ft.Column(
            [
                ft.Text(
                    "Change the column height to see how child items wrap onto multiple columns:"
                ),
                width_slider,
            ]
        ),
        ft.Container(content=col, bgcolor=ft.Colors.AMBER_100),
    )

ft.app(main)


Column vertical alignments

Python
import flet as ft

def main(page: ft.Page):
    def items(count):
        items = []
        for i in range(1, count + 1):
            items.append(
                ft.Container(
                    content=ft.Text(value=str(i)),
                    alignment=ft.alignment.center,
                    width=50,
                    height=50,
                    bgcolor=ft.Colors.AMBER_500,
                )
            )
        return items

    def column_with_alignment(align: ft.MainAxisAlignment):
        return ft.Column(
            [
                ft.Text(str(align), size=10),
                ft.Container(
                    content=ft.Column(items(3), alignment=align),
                    bgcolor=ft.Colors.AMBER_100,
                    height=400,
                ),
            ]
        )

    page.add(
        ft.Row(
            [
                column_with_alignment(ft.MainAxisAlignment.START),
                column_with_alignment(ft.MainAxisAlignment.CENTER),
                column_with_alignment(ft.MainAxisAlignment.END),
                column_with_alignment(ft.MainAxisAlignment.SPACE_BETWEEN),
                column_with_alignment(ft.MainAxisAlignment.SPACE_AROUND),
                column_with_alignment(ft.MainAxisAlignment.SPACE_EVENLY),
            ],
            spacing=30,
            alignment=ft.MainAxisAlignment.START,
        )
    )

ft.app(main)

Column horizontal alignments

Python
import flet as ft

def main(page: ft.Page):
    def items(count):
        items = []
        for i in range(1, count + 1):
            items.append(
                ft.Container(
                    content=ft.Text(value=str(i)),
                    alignment=ft.alignment.center,
                    width=50,
                    height=50,
                    bgcolor=ft.Colors.AMBER_500,
                )
            )
        return items

    def column_with_horiz_alignment(align: ft.CrossAxisAlignment):
        return ft.Column(
            [
                ft.Text(str(align), size=16),
                ft.Container(
                    content=ft.Column(
                        items(3),
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=align,
                    ),
                    bgcolor=ft.Colors.AMBER_100,
                    width=100,
                ),
            ]
        )

    page.add(
        ft.Row(
            [
                column_with_horiz_alignment(ft.CrossAxisAlignment.START),
                column_with_horiz_alignment(ft.CrossAxisAlignment.CENTER),
                column_with_horiz_alignment(ft.CrossAxisAlignment.END),
            ],
            spacing=30,
            alignment=ft.MainAxisAlignment.START,
        )
    )

ft.app(main)

Infinite scroll list
The following example demonstrates adding of list items on-the-fly, as user scroll to the bottom, creating the illusion of infinite list:

import threading
import flet as ft

class State:
    i = 0

s = State()
sem = threading.Semaphore()

def main(page: ft.Page):
    def on_scroll(e: ft.OnScrollEvent):
        if e.pixels >= e.max_scroll_extent - 100:
            if sem.acquire(blocking=False):
                try:
                    for i in range(0, 10):
                        cl.controls.append(ft.Text(f"Text line {s.i}", key=str(s.i)))
                        s.i += 1
                    cl.update()
                finally:
                    sem.release()

    cl = ft.Column(
        spacing=10,
        height=200,
        width=200,
        scroll=ft.ScrollMode.ALWAYS,
        on_scroll_interval=0,
        on_scroll=on_scroll,
    )
    for i in range(0, 50):
        cl.controls.append(ft.Text(f"Text line {s.i}", key=str(s.i)))
        s.i += 1

    page.add(ft.Container(cl, border=ft.border.all(1)))

ft.app(main)

Scrolling column programmatically

The following example demonstrates various scroll_to() options as well as defines a custom scrollbar theme:

import flet as ft

def main(page: ft.Page):
    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            track_color={
                ft.ControlState.HOVERED: ft.Colors.AMBER,
                ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT,
            },
            track_visibility=True,
            track_border_color=ft.Colors.BLUE,
            thumb_visibility=True,
            thumb_color={
                ft.ControlState.HOVERED: ft.Colors.RED,
                ft.ControlState.DEFAULT: ft.Colors.GREY_300,
            },
            thickness=30,
            radius=15,
            main_axis_margin=5,
            cross_axis_margin=10,
            # interactive=False,
        )
    )

    cl = ft.Column(
        spacing=10,
        height=200,
        width=float("inf"),
        scroll=ft.ScrollMode.ALWAYS,
    )
    for i in range(0, 100):
        cl.controls.append(ft.Text(f"Text line {i}", key=str(i)))

    def scroll_to_offset(e):
        cl.scroll_to(offset=100, duration=1000)

    def scroll_to_start(e):
        cl.scroll_to(offset=0, duration=1000)

    def scroll_to_end(e):
        cl.scroll_to(offset=-1, duration=2000, curve=ft.AnimationCurve.EASE_IN_OUT)

    def scroll_to_key(e):
        cl.scroll_to(key="20", duration=1000)

    def scroll_to_delta(e):
        cl.scroll_to(delta=40, duration=200)

    def scroll_to_minus_delta(e):
        cl.scroll_to(delta=-40, duration=200)

    page.add(
        ft.Container(cl, border=ft.border.all(1)),
        ft.ElevatedButton("Scroll to offset 100", on_click=scroll_to_offset),
        ft.Row(
            [
                ft.ElevatedButton("Scroll to start", on_click=scroll_to_start),
                ft.ElevatedButton("Scroll to end", on_click=scroll_to_end),
            ]
        ),
        ft.ElevatedButton("Scroll to key '20'", on_click=scroll_to_key),
        ft.Row(
            [
                ft.ElevatedButton("Scroll -40", on_click=scroll_to_minus_delta),
                ft.ElevatedButton("Scroll +40", on_click=scroll_to_delta),
            ]
        ),
    )

ft.app(main)

Properties
alignment
How the child Controls should be placed vertically.

Value is of type MainAxisAlignment.

auto_scroll
True if scrollbar should automatically move its position to the end when children updated. Must be False for scroll_to() method to work.

controls
A list of Controls to display inside the Column.

horizontal_alignment
How the child Controls should be placed horizontally.

Value is of type CrossAxisAlignment and defaults to CrossAxisAlignment.START.

on_scroll_interval
Throttling in milliseconds for on_scroll event. Default is 10.

rtl
True to set text direction to right-to-left. Default is False.

run_spacing
Spacing between runs when wrap=True. Default value is 10.

scroll
Enables a vertical scrolling for the Column to prevent its content overflow.

Value is of type ScrollMode and defaults to ScrollMode.None.

spacing
Spacing between controls in a Column. Default value is 10 virtual pixels. Spacing is applied only when alignment is set to start, end or center.

tight
Specifies how much space should be occupied vertically.

Defaults to False - allocate all space to children.

wrap
When set to True the Column will put child controls into additional columns (runs) if they don't fit a single column.

Methods
scroll_to(offset, delta, key, duration, curve)
Moves scroll position to either absolute offset, relative delta or jump to the control with specified key.

offset is an absolute value between minimum and maximum extents of a scrollable control, for example:

products.scroll_to(offset=100, duration=1000)

offset could be a negative to scroll from the end of a scrollable. For example, to scroll to the very end:

products.scroll_to(offset=-1, duration=1000)

delta allows moving scroll relatively to the current position. Use positive delta to scroll forward and negative delta to scroll backward. For example, to move scroll on 50 pixels forward:

products.scroll_to(delta=50)

key allows moving scroll position to a control with specified key. Most of Flet controls have key property which is translated to Flutter as "global key". key must be unique for the entire page/view. For example:

import flet as ft

def main(page: ft.Page):
    cl = ft.Column(
        spacing=10,
        height=200,
        width=200,
        scroll=ft.ScrollMode.ALWAYS,
    )
    for i in range(0, 50):
        cl.controls.append(ft.Text(f"Text line {i}", key=str(i)))

    def scroll_to_key(e):
        cl.scroll_to(key="20", duration=1000)

    page.add(
        ft.Container(cl, border=ft.border.all(1)),
        ft.ElevatedButton("Scroll to key '20'", on_click=scroll_to_key),
    )

ft.app(main)

note
scroll_to() method won't work with ListView and GridView controls building their items dynamically.

duration is scrolling animation duration in milliseconds. Defaults to 0 - no animation.

curve configures animation curve. Property value is AnimationCurve enum. Defaults to AnimationCurve.EASE.

Events
on_scroll
Fires when scroll position is changed by a user.

Event handler argument is an instance of OnScrollEvent class.

Expanding children
When a child Control is placed into a Column you can "expand" it to fill the available space. Every Control has expand property that can have either a boolean value (True - expand control to fill all available space) or an integer - an "expand factor" specifying how to divide a free space with other expanded child controls. For example, this code creates a column with a Container taking all available space and a Text control at the bottom serving as a status bar:

r = ft.Column([
  ft.Container(expand=True, content=ft.Text("Here is search results")),
  ft.Text("Records found: 10")
])

The following example with numeric expand factors creates a Column with 3 containers in it and having heights of 20% (1/5), 60% (3/5) and 20% (1/5) respectively:

r = ft.Column([
  ft.Container(expand=1, content=ft.Text("Header")),
  ft.Container(expand=3, content=ft.Text("Body")),
  ft.Container(expand=1, content=ft.Text("Footer"))
])

In general, the resulting height of a child in percents is calculated as expand / sum(all expands) * 100%.

If you need to give the child Control of the Column the flexibility to expand to fill the available space vertically but not require it to fill the available space, set its expand_loose property to True.

Container
Container allows to decorate a control with background color and border and position it with padding, margin and alignment.

Examples
Live example

Clickable container

Python
import flet as ft

def main(page: ft.Page):
    page.title = "Containers - clickable and not"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add(
        ft.Row(
            [
                ft.Container(
                    content=ft.Text("Non clickable"),
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.Colors.AMBER,
                    width=150,
                    height=150,
                    border_radius=10,
                ),
                ft.Container(
                    content=ft.Text("Clickable without Ink"),
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.Colors.GREEN_200,
                    width=150,
                    height=150,
                    border_radius=10,
                    on_click=lambda e: print("Clickable without Ink clicked!"),
                ),
                ft.Container(
                    content=ft.Text("Clickable with Ink"),
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.Colors.CYAN_200,
                    width=150,
                    height=150,
                    border_radius=10,
                    ink=True,
                    on_click=lambda e: print("Clickable with Ink clicked!"),
                ),
                ft.Container(
                    content=ft.Text("Clickable transparent with Ink"),
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    width=150,
                    height=150,
                    border_radius=10,
                    ink=True,
                    on_click=lambda e: print("Clickable transparent with Ink clicked!"),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

ft.app(main)

Properties

alignment
Align the child control within the container.

Value is of type Alignment.

animate
Enables container "implicit" animation that gradually changes its values over a period of time.

Value is of type AnimationValue.

bgcolor
Defines the background color of the container.

blend_mode
The blend mode applied to the color or gradient background of the container.

Value is of type BlendMode and defaults to BlendMode.MODULATE.

blur
Applies Gaussian blur effect under the container.

The value of this property could be one of the following:

a number - specifies the same value for horizontal and vertical sigmas, e.g. 10.
a tuple - specifies separate values for horizontal and vertical sigmas, e.g. (10, 1).
an instance of Blur
For example:

ft.Stack(
    [
        ft.Container(
            content=ft.Text("Hello"),
            image_src="https://picsum.photos/100/100",
            width=100,
            height=100,
        ),
        ft.Container(
            width=50,
            height=50,
            blur=10,
            bgcolor="#44CCCC00",
        ),
        ft.Container(
            width=50,
            height=50,
            left=10,
            top=60,
            blur=(0, 10),
        ),
        ft.Container(
            top=10,
            left=60,
            blur=ft.Blur(10, 0, ft.BlurTileMode.MIRROR),
            width=50,
            height=50,
            bgcolor="#44CCCCCC",
            border=ft.border.all(2, ft.Colors.BLACK),
        ),
    ]
)


border
A border to draw above the background color.

Value is of type Border.

border_radius
If specified, the corners of the container are rounded by this radius.

Value is of type BorderRadius.

clip_behavior
The content will be clipped (or not) according to this option.

Value is of type ClipBehavior and defaults to ClipBehavior.ANTI_ALIAS if border_radius is not None; otherwise ClipBehavior.NONE.

color_filter
Applies a color filter to the container.

Value is of type ColorFilter.

content
A child Control contained by the container.

foreground_decoration
The foreground decoration.

Value is of type BoxDecoration.

gradient
Defines the gradient background of the container.

Value is of type Gradient.

ignore_interactions
Whether to ignore all interactions with this container and its descendants.

Defaults to False.

image
An image to paint above the bgcolor or gradient. If shape=BoxShape.CIRCLE then this image is clipped to the circle's boundary; if border_radius is not Nonethen the image is clipped to the given radii.

Value is of type DecorationImage.

image_fit
How to inscribe the image into the space allocated during layout.

Value is of type ImageFit and defaults to ImageFit.NONE.

Deprecated in v0.24.0 and will be removed in v0.27.0. Use image.fit instead.

image_opacity
Sets image opacity when blending with a background.

Value ranges between 0.0(fully transparent) and 1.0(fully opaque).

Deprecated in v0.24.0 and will be removed in v0.27.0. Use image.opacity instead.

image_repeat
How to paint any portions of the layout bounds not covered by the image.

Value is of type ImageRepeat and defaults to ImageRepeat.NO_REPEAT.

Deprecated in v0.24.0 and will be removed in v0.27.0. Use image.repeat instead.

image_src
Sets an image as a container background. See Image.src for more details.

Deprecated in v0.24.0 and will be removed in v0.27.0. Use image.src instead.

image_src_base64
Sets an image encoded as Base-64 string as a container background. See Image.src_base64 for more details.

Deprecated in v0.24.0 and will be removed in v0.27.0. Use image.src_base64 instead.

ink
True to produce ink ripples effect when user clicks the container.

Defaults to False.

ink_color
The splash color of the ink response.

margin
Empty space to surround the decoration and child control.

Value is of type Margin class or a number.

padding
Empty space to inscribe inside a container decoration (background, border). The child control is placed inside this padding.

Value is of type Padding or a number.

rtl
True to set text direction to right-to-left.

Defaults to False.

shadow
Shadows cast by the container.

Value is of type BoxShadow or a List[BoxShadow].

shape
Sets the shape of the container.

Value is of type BoxShape and defaults to BoxShape.RECTANGLE.

theme_mode
Setting theme_mode "resets" parent theme and creates a new, unique scheme for all controls inside the container. Otherwise the styles defined in container's theme property override corresponding styles from the parent, inherited theme.

Value is of type ThemeMode and defaults to ThemeMode.SYSTEM.

theme
Allows setting a nested theme for all controls inside the container and down the tree.

Value is of type Theme class.

Usage example

import flet as ft

def main(page: ft.Page):
    # Yellow page theme with SYSTEM (default) mode
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.YELLOW,
    )

    page.add(
        # Page theme
        ft.Container(
            content=ft.ElevatedButton("Page theme button"),
            bgcolor=ft.Colors.SURFACE_VARIANT,
            padding=20,
            width=300,
        ),

        # Inherited theme with primary color overridden
        ft.Container(
            theme=ft.Theme(color_scheme=ft.ColorScheme(primary=ft.Colors.PINK)),
            content=ft.ElevatedButton("Inherited theme button"),
            bgcolor=ft.Colors.SURFACE_VARIANT,
            padding=20,
            width=300,
        ),
        
        # Unique always DARK theme
        ft.Container(
            theme=ft.Theme(color_scheme_seed=ft.Colors.INDIGO),
            theme_mode=ft.ThemeMode.DARK,
            content=ft.ElevatedButton("Unique theme button"),
            bgcolor=ft.Colors.SURFACE_VARIANT,
            padding=20,
            width=300,
        ),
    )

ft.app(main)


url
The URL to open when the container is clicked. If provided, on_click event is fired after that.

url_target
Where to open URL in the web mode.

Value is of type UrlTarget and defaults to UrlTarget.BLANK.

Events
on_click
Fires when a user clicks the container. Will not be fired on long press.

on_hover
Fires when a mouse pointer enters or exists the container area. data property of event object contains true (string) when cursor enters and false when it exits.

A simple example of a container changing its background color on mouse hover:

import flet as ft

def main(page: ft.Page):
    def on_hover(e):
        e.control.bgcolor = "blue" if e.data == "true" else "red"
        e.control.update()

    page.add(
        ft.Container(width=100, height=100, bgcolor="red", ink=False, on_hover=on_hover)
    )

ft.app(main)


on_long_press
Fires when the container is long-pressed.

on_tap_down
Fires when a user clicks the container with or without a long press.

Event handler argument is of type ContainerTapEvent.

info
If ink is True, e will be plain ControlEvent with empty data instead of ContainerTapEvent.

A simple usage example:

import flet as ft

def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def on_long_press(e):
        print("on long press")
        page.add(ft.Text("on_long_press triggered"))

    def on_click(e):
        print("on click")
        page.add(ft.Text("on_click triggered"))

    def on_tap_down(e: ft.ContainerTapEvent):
        print("on tap down", e.local_x, e.local_y)
        page.add(ft.Text("on_tap_down triggered"))

    c = ft.Container(
        bgcolor=ft.Colors.RED,
        content=ft.Text("Test Long Press"),
        height=100,
        width=100,
        on_click=on_click,
        on_long_press=on_long_press,
        on_tap_down=on_tap_down,
    )
    
    page.add(c)

ft.app(main)

======================================

DataTable
A Material Design data table.

Examples
Live example

A simple DataTable

import flet as ft

def main(page: ft.Page):
    page.add(
        ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("First name")),
                ft.DataColumn(ft.Text("Last name")),
                ft.DataColumn(ft.Text("Age"), numeric=True),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("John")),
                        ft.DataCell(ft.Text("Smith")),
                        ft.DataCell(ft.Text("43")),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Jack")),
                        ft.DataCell(ft.Text("Brown")),
                        ft.DataCell(ft.Text("19")),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Alice")),
                        ft.DataCell(ft.Text("Wong")),
                        ft.DataCell(ft.Text("25")),
                    ],
                ),
            ],
        ),
    )

ft.app(main)

A styled DataTable

import flet as ft

def main(page: ft.Page):
    page.add(
        ft.DataTable(
            width=700,
            bgcolor="yellow",
            border=ft.border.all(2, "red"),
            border_radius=10,
            vertical_lines=ft.BorderSide(3, "blue"),
            horizontal_lines=ft.BorderSide(1, "green"),
            sort_column_index=0,
            sort_ascending=True,
            heading_row_color=ft.Colors.BLACK12,
            heading_row_height=100,
            data_row_color={ft.ControlState.HOVERED: "0x30FF0000"},
            show_checkbox_column=True,
            divider_thickness=0,
            column_spacing=200,
            columns=[
                ft.DataColumn(
                    ft.Text("Column 1"),
                    on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                ft.DataColumn(
                    ft.Text("Column 2"),
                    tooltip="This is a second column",
                    numeric=True,
                    on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
            ],
            rows=[
                ft.DataRow(
                    [ft.DataCell(ft.Text("A")), ft.DataCell(ft.Text("1"))],
                    selected=True,
                    on_select_changed=lambda e: print(f"row select changed: {e.data}"),
                ),
                ft.DataRow([ft.DataCell(ft.Text("B")), ft.DataCell(ft.Text("2"))]),
            ],
        ),
    )

ft.app(main)

DataTable properties
bgcolor
The background color for the table.

border
The border around the table.

The value is an instance of Border class.

border_radius
Border corners.

Border radius is an instance of BorderRadius class.

checkbox_horizontal_margin
Horizontal margin around the checkbox, if it is displayed.

clip_behavior
The content will be clipped (or not) according to this option.

Value is of type ClipBehavior and defaults to ClipBehavior.ANTI_ALIAS if border_radius!=None; otherwise ClipBehavior.HARD_EDGE.

column_spacing
The horizontal margin between the contents of each data column.

columns
A list of DataColumn controls describing table columns.

data_row_color
The background color for the data rows.

The effective background color can be made to depend on the ControlState state, i.e. if the row is selected, pressed, hovered, focused, disabled or enabled. The color is painted as an overlay to the row. To make sure that the row's InkWell is visible (when pressed, hovered and focused), it is recommended to use a translucent background color.

data_row_min_height
The minimum height of each row (excluding the row that contains column headings).

Defaults to 48.0 and must be less than or equal to data_row_max_height.

data_row_max_height
The maximum height of each row (excluding the row that contains column headings). Set to float("inf") for the height of each row to adjust automatically with its content.

Defaults to 48.0 and must be greater than or equal to data_row_min_height.

data_text_style
The text style for data rows. An instance of TextStyle class.

divider_thickness
The width of the divider that appears between TableRows. Must be greater than or equal to zero.

Defaults to 1.0.

gradient
The background gradient for the table.

Value is of type Gradient.

heading_row_alignment
The alignment of the heading row.

Value is of type MainAxisAlignment.

heading_row_color
The background color for the heading row.

The effective background color can be made to depend on the ControlState state, i.e. if the row is pressed, hovered, focused when sorted. The color is painted as an overlay to the row. To make sure that the row's InkWell is visible (when pressed, hovered and focused), it is recommended to use a translucent color.

heading_row_height
The height of the heading row.

heading_text_style
The text style for the heading row. An instance of TextStyle class.

horizontal_lines
Set the color and width of horizontal lines between rows. An instance of BorderSide class.

horizontal_margin
The horizontal margin between the edges of the table and the content in the first and last cells of each row.

When a checkbox is displayed, it is also the margin between the checkbox the content in the first data column.

rows
A list of DataRow controls defining table rows.

show_bottom_border
Whether a border at the bottom of the table is displayed.

By default, a border is not shown at the bottom to allow for a border around the table defined by decoration.

show_checkbox_column
Whether the control should display checkboxes for selectable rows.

If True, a Checkbox will be placed at the beginning of each row that is selectable. However, if DataRow.on_select_changed is not set for any row, checkboxes will not be placed, even if this value is True.

If False, all rows will not display a Checkbox.

sort_ascending
Whether the column mentioned in sort_column_index, if any, is sorted in ascending order.

If True, the order is ascending (meaning the rows with the smallest values for the current sort column are first in the table).

If False, the order is descending (meaning the rows with the smallest values for the current sort column are last in the table).

sort_column_index
The current primary sort key's column.

If specified, indicates that the indicated column is the column by which the data is sorted. The number must correspond to the index of the relevant column in columns.

Setting this will cause the relevant column to have a sort indicator displayed.

When this is None, it implies that the table's sort order does not correspond to any of the columns.

vertical_lines
Set the color and width of vertical lines between columns.

Value is of type BorderSide.

DataTable events
on_select_all
Invoked when the user selects or unselects every row, using the checkbox in the heading row.

If this is None, then the DataRow.on_select_changed callback of every row in the table is invoked appropriately instead.

To control whether a particular row is selectable or not, see DataRow.on_select_changed. This callback is only relevant if any row is selectable.

DataColumn
Column configuration for a DataTable.

One column configuration must be provided for each column to display in the table.

label
The column heading.

Typically, this will be a Text control. It could also be an Icon (typically using size 18), or a Row with an icon and some text.

numeric
Whether this column represents numeric data or not.

The contents of cells of columns containing numeric data are right-aligned.

tooltip
The column heading's tooltip.

This is a longer description of the column heading, for cases where the heading might have been abbreviated to keep the column width to a reasonable size.

DataColumn events
on_sort
Called when the user asks to sort the table using this column.

If not set, the column will not be considered sortable.

DataRow
Row configuration and cell data for a DataTable.

One row configuration must be provided for each row to display in the table.

The data for this row of the table is provided in the cells property of the DataRow object.

cells
The data for this row - a list of DataCell controls.

There must be exactly as many cells as there are columns in the table.

color
The color for the row.

By default, the color is transparent unless selected. Selected rows has a grey translucent color.

The effective color can depend on the ControlState state, if the row is selected, pressed, hovered, focused, disabled or enabled. The color is painted as an overlay to the row. To make sure that the row's InkWell is visible (when pressed, hovered and focused), it is recommended to use a translucent color.

selected
Whether the row is selected.

If on_select_changed is non-null for any row in the table, then a checkbox is shown at the start of each row. If the row is selected (True), the checkbox will be checked and the row will be highlighted.

Otherwise, the checkbox, if present, will not be checked.

DataRow events
on_long_press
Called if the row is long-pressed.

If a DataCell in the row has its DataCell.on_tap, DataCell.on_double_tap, DataCell.on_long_press, DataCell.on_tap_cancel or DataCell.on_tap_down callback defined, that callback behavior overrides the gesture behavior of the row for that particular cell.

on_select_changed
Called when the user selects or unselects a selectable row.

If this is not null, then the row is selectable. The current selection state of the row is given by selected.

If any row is selectable, then the table's heading row will have a checkbox that can be checked to select all selectable rows (and which is checked if all the rows are selected), and each subsequent row will have a checkbox to toggle just that row.

A row whose on_select_changed callback is null is ignored for the purposes of determining the state of the "all" checkbox, and its checkbox is disabled.

If a DataCell in the row has its DataCell.on_tap callback defined, that callback behavior overrides the gesture behavior of the row for that particular cell.

DataCell
The data for a cell of a DataTable.

One list of DataCell objects must be provided for each DataRow in the DataTable.

content
The data for the row.

Typically a Text control or a Dropdown control.

If the cell has no data, then a Text widget with placeholder text should be provided instead, and placeholder should be set to True.

This control can only have one child. To lay out multiple children, let this control's child be a widget such as Row, Column, or Stack, which have controls property, and then provide the children to that widget.

placeholder
Whether the child is actually a placeholder.

If this is True, the default text style for the cell is changed to be appropriate for placeholder text.

show_edit_icon
Whether to show an edit icon at the end of the cell.

This does not make the cell actually editable; the caller must implement editing behavior if desired (initiated from the on_tap callback).

If this is set, on_tap should also be set, otherwise tapping the icon will have no effect.

DataCell events
on_double_tap
Called when the cell is double tapped.

If specified, tapping the cell will call this callback, else (tapping the cell will attempt to select the row ( if DataRow.on_select_changed is provided).

on_long_press
Called if the cell is long-pressed.

If specified, tapping the cell will invoke this callback, else tapping the cell will attempt to select the row ( if DataRow.on_select_changed is provided).

on_tap
Called if the cell is tapped.

If specified, tapping the cell will call this callback, else tapping the cell will attempt to select the row ( if DataRow.on_select_changed is provided).

on_tap_cancel
Called if the user cancels a tap was started on cell.

If specified, cancelling the tap gesture will invoke this callback, else tapping the cell will attempt to select the row (if DataRow.on_select_changed is provided).

on_tap_down
Called if the cell is tapped down.

If specified, tapping the cell will call this callback, else tapping the cell will attempt to select the row ( if DataRow.on_select_changed is provided).

Divider
A thin horizontal line, with padding on either side.

In the material design language, this represents a divider.

Examples
Live example

Python
import flet as ft

def main(page: ft.Page):

    page.add(
        ft.Column(
            [
                ft.Container(
                    bgcolor=ft.Colors.AMBER,
                    alignment=ft.alignment.center,
                    expand=True,
                ),
                ft.Divider(),
                ft.Container(bgcolor=ft.Colors.PINK, alignment=ft.alignment.center, expand=True),
                ft.Divider(height=1, color="white"),
                ft.Container(
                    bgcolor=ft.Colors.BLUE_300,
                    alignment=ft.alignment.center,
                    expand=True,
                ),
                ft.Divider(height=9, thickness=3),
                ft.Container(
                    bgcolor=ft.Colors.DEEP_PURPLE_200,
                    alignment=ft.alignment.center,
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        ),
    )

ft.app(main)



Properties
color
The color to use when painting the line.

height
The divider's height extent. The divider itself is always drawn as a horizontal line that is centered within the height specified by this value.

Defaults to 16.0.

leading_indent
The amount of empty space to the leading edge of the divider.

Defaults to 0.0.

thickness
The thickness of the line drawn within the divider. A divider with a thickness of 0.0 is always drawn as a line with a height of exactly one device pixel.

Defaults to 0.0.

trailing_indent
The amount of empty space to the trailing edge of the divider.

Defaults to 0.0.

==========================================


ListTile
A single fixed-height row that typically contains some text as well as a leading or trailing icon.

Examples
Live example


Python
import flet as ft

def main(page):
    page.title = "ListTile Examples"
    page.add(
        ft.Card(
            content=ft.Container(
                width=500,
                content=ft.Column(
                    [
                        ft.ListTile(
                            title=ft.Text("One-line list tile"),
                        ),
                        ft.ListTile(title=ft.Text("One-line dense list tile"), dense=True),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.SETTINGS),
                            title=ft.Text("One-line selected list tile"),
                            selected=True,
                        ),
                        ft.ListTile(
                            leading=ft.Image(src="/icons/icon-192.png", fit="contain"),
                            title=ft.Text("One-line with leading control"),
                        ),
                        ft.ListTile(
                            title=ft.Text("One-line with trailing control"),
                            trailing=ft.PopupMenuButton(
                                icon=ft.Icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(text="Item 1"),
                                    ft.PopupMenuItem(text="Item 2"),
                                ],
                            ),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.ALBUM),
                            title=ft.Text("One-line with leading and trailing controls"),
                            trailing=ft.PopupMenuButton(
                                icon=ft.Icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(text="Item 1"),
                                    ft.PopupMenuItem(text="Item 2"),
                                ],
                            ),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.SNOOZE),
                            title=ft.Text("Two-line with leading and trailing controls"),
                            subtitle=ft.Text("Here is a second title."),
                            trailing=ft.PopupMenuButton(
                                icon=ft.Icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(text="Item 1"),
                                    ft.PopupMenuItem(text="Item 2"),
                                ],
                            ),
                        ),
                    ],
                    spacing=0,
                ),
                padding=ft.padding.symmetric(vertical=10),
            )
        )
    )

ft.app(main)


Properties
adaptive
If the value is True, an adaptive ListTile is created based on whether the target platform is iOS/macOS.

On iOS and macOS, a CupertinoListTile is created, which has matching functionality and presentation as ListTile, and the graphics as expected on iOS. On other platforms, a Material ListTile is created.

If a CupertinoListTile is created, the following parameters are ignored: autofocus, dense, is_three_line, selected and on_long_press event.

Defaults to False.

autofocus
True if the control will be selected as the initial focus. If there is more than one control on a page with autofocus set, then the first one added to the page will get focus.

bgcolor
The list tile's background color.

bgcolor_activated
The list tile's splash color after the tile was tapped.

content_padding
The tile's internal padding. Insets a ListTile's contents: its leading, title, subtitle, and trailing controls.

Value is of type Padding and defaults to padding.symmetric(horizontal=16).

dense
Whether this list tile is part of a vertically dense list. Dense list tiles default to a smaller height.

enable_feedback
Whether detected gestures should provide acoustic and/or haptic feedback. On Android, for example, setting this to True produce a click sound and a long-press will produce a short vibration.

Defaults to True.

horizontal_spacing
The horizontal gap between the title and the leading/trailing controls.

Defaults to 16.

hover_color
The tile's color when hovered.

icon_color
Defines the default color for the Icons present in leading and trailing.

is_three_line
Whether this list tile is intended to display three lines of text.

If True, then subtitle must be non-null (since it is expected to give the second and third lines of text).

If False, the list tile is treated as having one line if the subtitle is null and treated as having two lines if the subtitle is non-null.

When using a Text control for title and subtitle, you can enforce line limits using Text.max_lines.

leading
A Control to display before the title.

leading_and_trailing_text_style
The TextStyle for the leading and trailing controls.

min_height
The minimum height allocated for this control.

If None or not set, default tile heights are 56.0, 72.0, and 88.0 for one, two, and three lines of text respectively. If dense is True, these defaults are changed to 48.0, 64.0, and 76.0.

Note that, a visual density value or a large title will also adjust the default tile heights.

min_leading_width
The minimum width allocated for the leading control.

Defaults to 40.

min_vertical_padding
The minimum padding on the top and bottom of the title and subtitle controls.

Defaults to 4.

mouse_cursor
The cursor to be displayed when a mouse pointer enters or is hovering over this control. The value is MouseCursor enum.

selected
If this tile is also enabled then icons and text are rendered with the same color. By default the selected color is the theme's primary color.

selected_color
Defines the color used for icons and text when selected=True.

selected_tile_color
Defines the background color of ListTile when selected=True.

shape
The tile's shape. The value is an instance of OutlinedBorder class.

subtitle
Additional content displayed below the title. Typically a Text widget.

If is_three_line is False, this should not wrap. If is_three_line is True, this should be configured to take a maximum of two lines. For example, you can use Text.max_lines to enforce the number of lines.

subtitle_text_style
The TextStyle for the subtitle control.

style
Defines the font used for the title.

Value is of type ListTileStyle and defaults to ListTileStyle.LIST.

text_color
The color used for text. Defines the color of Text controls found in title, subtitle, leading, and trailing.

title
A Control to display as primary content of the list tile.

Typically a Text control. This should not wrap. To enforce the single line limit, use Text.max_lines.

title_alignment
Defines how leading and trailing are vertically aligned relative to the titles (title and subtitle).

Value is of type ListTileAlignment and defaults to ListTileAlignment.THREE_LINE in Material 3 or ListTileAlignment.TITLE_HEIGHT in Material 2.

title_text_style
The TextStyle for the title control.

toggle_inputs
Whether clicking on a list tile should toggle the state of Radio, Checkbox or Switch inside the tile.

Defaults to False.

trailing
A Control to display after the title. Typically an Icon control.

url
The URL to open when the list tile is clicked. If registered, on_click event is fired after that.

url_target
Where to open URL in the web mode.

Value is of type UrlTarget and defaults to UrlTarget.BLANK.

visual_density
Defines how compact the control's layout will be.

Value is of type ThemeVisualDensity.

Events
on_click
Fires when a user clicks or taps the list tile.

on_long_press
Fires when the user long-presses on this list tile.


==================================


ListView
A scrollable list of controls arranged linearly.

ListView is the most commonly used scrolling control. It displays its children one after another in the scroll direction. In the cross axis, the children are required to fill the ListView.

info
ListView is very effective for large lists (thousands of items). Prefer it over Column or Row for smooth scrolling.

Examples
Live example

Auto-scrolling ListView
Python
from time import sleep
import flet as ft

def main(page: ft.Page):
    page.title = "Auto-scrolling ListView"

    lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

    count = 1

    for i in range(0, 60):
        lv.controls.append(ft.Text(f"Line {count}"))
        count += 1

    page.add(lv)

    for i in range(0, 60):
        sleep(1)
        lv.controls.append(ft.Text(f"Line {count}"))
        count += 1
        page.update()

ft.app(main)


Properties
auto_scroll
True if scrollbar should automatically move its position to the end when children updated. Must be False for scroll_to() method to work.

cache_extent
Items that fall in the cache area (area before or after the visible area that are about to become visible when the user scrolls) are laid out even though they are not (yet) visible on screen. The cacheExtent describes how many pixels the cache area extends before the leading edge and after the trailing edge of the viewport.

The total extent, which the viewport will try to cover with controls, is cache_extent before the leading edge + extent of the main axis + cache_extent after the trailing edge.

clip_behavior
The content will be clipped (or not) according to this option.

Value is of type ClipBehavior and defaults to HARD_EDGE.

controls
A list of Controls to display inside ListView.

divider_thickness
If greater than 0 then Divider is used as a spacing between list view items.

first_item_prototype
True if the dimensions of the first item should be used as a "prototype" for all other items, i.e. their height or width will be the same as the first item.

Defaults to False.

horizontal
True to layout ListView items horizontally.

item_extent
A fixed height or width (for horizontal ListView) of an item to optimize rendering.

on_scroll_interval
Throttling in milliseconds for on_scroll event.

Defaults to 10.

padding
The amount of space by which to inset the children.

Value is of typePadding.

reverse
Defines whether the scroll view scrolls in the reading direction.

Defaults to False.

semantic_child_count
The number of children that will contribute semantic information.

spacing
The height of Divider between ListView items. No spacing between items if not specified.

Methods
scroll_to(offset, delta, key, duration, curve)
Moves scroll position to either absolute offset, relative delta or jump to the control with specified key.

See Column.scroll_to() for method details and examples.

Events
on_scroll
Fires when scroll position is changed by a user.

Event handler argument is an instance of OnScrollEvent class.

===================+

Page
Page is a container for View controls.

A page instance and the root view are automatically created when a new user session started.

Properties
auto_scroll
True if scrollbar should automatically move its position to the end when children updated. Must be False for scroll_to() method to work.

appbar
An AppBar control to display at the top of the Page.

banner
A Banner control to display at the top of the Page.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use page.overlay.append(banner) instead.

bgcolor
Background color of the Page.

A color value could be a hex value in #ARGB format (e.g. #FFCC0000), #RGB format (e.g. #CC0000) or a named color from flet.colors module.

bottom_appbar
BottomAppBar control to display at the bottom of the Page. If both bottom_appbar and navigation_bar properties are provided, NavigationBar will be displayed.

bottom_sheet
BottomSheet control to display.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use page.overlay.append(bottom_sheet) instead.

browser_context_menu
Used to enable or disable the context menu that appears when the user right-clicks on the web page.

Value is of type BrowserContextMenu.

🌎 Web only.

client_ip
IP address of the connected user.

🌎 Web only.

client_user_agent
Browser details of the connected user.

🌎 Web only.

controls
A list of Controls to display on the Page.

For example, to add a new control to a page:

Python
page.controls.append(ft.Text("Hello!"))
page.update()

or to get the same result as above using page.add() method

To remove the top most control on the page:

Python
page.controls.pop()
page.update()

dark_theme
Customizes the theme of the application when in dark theme mode.

Value is an instance of the Theme() class - more information in the theming guide.

debug
True if Flutter client of Flet app is running in debug mode.

decoration
The background decoration.

Value is of type BoxDecoration.

design
Reserved for future use.

dialog
An AlertDialog control to display.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use page.overlay.append(dialog) instead.

drawer
A NavigationDrawer control to display as a panel sliding from the start edge of the page.

end_drawer
A NavigationDrawer control to display as a panel sliding from the end edge of the page.

floating_action_button
A FloatingActionButton control to display on top of Page content.

floating_action_button_location
Defines a position for the FloatingActionButton.

Value is of type FloatingActionButtonLocation enum. Default is FloatingActionButtonLocation.END_FLOAT.

fonts
Defines the custom fonts to be used in the application.

Value is a dictionary, in which the keys represent the font family name used for reference and the values

Key: The font family name used for reference.
Value: The font source, either an absolute URL or a relative path to a local asset. The following font file formats are supported .ttc, .ttf and .otf.
Usage example here.

height
A height of a web page or content area of a native OS window containing Flet app. This property is read-only. It's usually being used inside page.on_resize handler.

horizontal_alignment
How the child Controls should be placed horizontally.

Property value is CrossAxisAlignment enum. Default is START.

locale_configuration
A locale configuration for the app.

Value is of type LocaleConfiguration.

media
Provides details about app media (screen, window). See MediaQueryData in Flutter docs for more info.

Value is of type PageMediaData.

note
In most cases you should be fine by wrapping your content into SafeArea control.

name
Page name as specified in ft.app() call. Page name is set when Flet app is running as web app. This is a portion of the URL after host name.

navigation_bar
NavigationBar control to display at the bottom of the page. If both bottom_appbar and navigation_bar properties are provided, NavigationBar will be displayed.

on_scroll_interval
Throttling in milliseconds for on_scroll event.

Defaults to 10.

overlay
A list of Controls displayed as a stack on top of main page contents.

padding
A space between page contents and its edges. Default value is 10 pixels from each side. To set zero padding:

Python
page.padding = 0
page.update()

Value is of type Padding.

platform
Operating system the application is running on.

Value is of type PagePlatform.

This property can be used to create adaptive UI with different controls depending on the operating system:

def main(page: ft.Page):
    if page.platform == ft.PagePlatform.MACOS:
        page.add(ft.CupertinoDialogAction("Cupertino Button"))
    else:
        page.add(ft.TextButton("Material Button"))

You can also set this property for testing purposes:

import flet as ft


def main(page):
    def set_android(e):
        page.platform = ft.PagePlatform.ANDROID
        page.update()
        print("New platform:", page.platform)

    def set_ios(e):
        page.platform = "ios"
        page.update()
        print("New platform:", page.platform)

    page.add(
        ft.Switch(label="Switch A", adaptive=True),
        ft.ElevatedButton("Set Android", on_click=set_android),
        ft.ElevatedButton("Set iOS", on_click=set_ios),
    )

    print("Default platform:", page.platform)


ft.app(main)

platform_brightness
The current brightness mode of the host platform.

Value is read-only and of type Brightness.

pubsub
A simple PubSub implementation for passing messages between app sessions.

subscribe(handler)
Subscribe current app session for broadcast (no topic) messages. handler is a function or method with a single message argument, for example:

def main(page: ft.Page):

    def on_broadcast_message(message):
        print(message)

    page.pubsub.subscribe(on_broadcast_message)

subscribe_topic(topic, handler)
Subscribe current app session to a specific topic. handler is a function or method with two arguments: topic and message, for example:

def main(page: ft.Page):

    def on_message(topic, message):
        print(topic, message)

    page.pubsub.subscribe_topic("general", on_message)

send_all(message)
Broadcast message to all subscribers. message could be anything: a simple literal or a class instance, for example:

@dataclass
class Message:
    user: str
    text: str

def main(page: ft.Page):

    def on_broadcast_message(message):
        page.add(ft.Text(f"{message.user}: {message.text}"))

    page.pubsub.subscribe(on_broadcast_message)

    def on_send_click(e):
        page.pubsub.send_all(Message("John", "Hello, all!"))

    page.add(ft.ElevatedButton(text="Send message", on_click=on_send_click))

send_all_on_topic(topic, message)
Send message to all subscribers on specific topic.

send_others(message)
Broadcast message to all subscribers except sender.

send_others_on_topic(topic, message)
Send message to all subscribers on specific topic except sender.

unsubscribe()
Unsubscribe current app session from broadcast messages, for example:

@dataclass
class Message:
    user: str
    text: str

def main(page: ft.Page):

    def on_leave_click(e):
        page.pubsub.unsubscribe()

    page.add(ft.ElevatedButton(text="Leave chat", on_click=on_leave_click))

unsubscribe_topic(topic)
Unsubscribe current app session from specific topic.

unsubscribe_all()
Unsubscribe current app session from broadcast messages and all topics, for example:

def main(page: ft.Page):
    def client_exited(e):
        page.pubsub.unsubscribe_all()

    page.on_close = client_exited

pwa
True if the application is running as Progressive Web App (PWA).

Value is read-only.

query
A part of app URL after ?. The value is an instance of QueryString with helper methods for fetching query parameters.

route
Get or sets page's navigation route. See Navigation and routing section for more information and examples.

rtl
True to set text direction to right-to-left.

Defaults to False.

scroll
Enables a vertical scrolling for the Page to prevent its content overflow.

Value is of type ScrollMode.

session
A simple key-value storage for session data.

session_id
A unique ID of user's session. This property is read-only.

snack_bar
A SnackBar control to display.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use page.overlay.append(snack_bar) instead.

spacing
Vertical spacing between controls on the Page. Default value is 10 virtual pixels. Spacing is applied only when alignment is set to start, end or center.

splash
A Control that will be displayed on top of Page contents. ProgressBar or ProgressRing could be used as an indicator for some lengthy operation, for example:

Python
from time import sleep
import flet as ft


def main(page: ft.Page):
    progress_bar = ft.ProgressBar(visible=False)
    page.overlay.append(progress_bar)

    def button_click(e):
        progress_bar.visible = True
        e.control.disabled = True
        page.update()
        sleep(3)
        progress_bar.visible = False
        e.control.disabled = False
        page.update()

    page.add(ft.ElevatedButton("Do some lengthy task!", on_click=button_click))


ft.app(main)

Deprecated in v0.23.0 and will be removed in v0.26.0. Use page.overlay.append(splash) instead.

show_semantics_debugger
True turns on an overlay that shows the accessibility information reported by the framework.

theme
Customizes the theme of the application when in light theme mode. Currently, a theme can only be automatically generated from a "seed" color. For example, to generate light theme from a green color.

Value is an instance of the Theme() class - more information in the theming guide.

theme_mode
The page's theme mode.

Value is of type ThemeMode and defaults to ThemeMode.SYSTEM.

title
A title of browser or native OS window, for example:

Python
page.title = "My awesome app"
page.update()

url
The complete web app's URL.

vertical_alignment
How the child Controls should be placed vertically.

Value is of type MainAxisAlignment and defaults to MainAxisAlignment.START.

views
A list of View controls to build navigation history.

The last view in the list is the one displayed on a page.

The first view is a "root" view which cannot be popped.

web
True if the application is running in the web browser.

width
A width of a web page or content area of a native OS window containing Flet app. This property is read-only. It's usually being used inside page.on_resize handler.

window
A class with properties/methods/events to control app's native OS window.

Value is of type Window.

window_always_on_top
🖥️ Desktop only. Sets whether the window should show always on top of other windows.

Defaults to False.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use Page.window.always_on_top instead.

window_bgcolor
🖥️ Desktop only. Sets background color of an application window.

Use together with page.bgcolor to make a window transparent:

import flet as ft

def main(page: ft.Page):
    page.window.bgcolor = ft.Colors.TRANSPARENT
    page.bgcolor = ft.Colors.TRANSPARENT
    page.window.title_bar_hidden = True
    page.window.frameless = True
    page.window.left = 400
    page.window.top = 200
    page.add(ft.ElevatedButton("I'm a floating button!"))

ft.app(main)

Deprecated in v0.23.0 and will be removed in v0.26.0. Use Page.window.bgcolor instead.

window_focused
🖥️ Desktop only. Set to True to focus a native OS window with a Flet app.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use Page.window.focused instead.

window_frameless
🖥️ Desktop only. Set to True to make app window frameless.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use Page.window.frameless instead.

window_full_screen
🖥️ Desktop only. Set to True to switch app's native OS window to a fullscreen mode.

Defaults to False.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use Page.window.full_screen instead.

window_height
🖥️ Desktop only. Get or set the height of a native OS window containing Flet app.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use Page.window.height instead.

window_left
🖥️ Desktop only. Get or set a horizontal position of a native OS window - a distance in virtual pixels from the left edge of the screen.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use Page.window.left instead.

window_maximizable
🖥️ Desktop only. Set to False to hide/disable native OS window's "Maximize" button.

Defaults to True.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use Page.window.maximizable instead.

window_maximized
🖥️ Desktop only. True if a native OS window containing Flet app is maximized; otherwise False. Set this property to True to programmatically maximize the window and set it to False to unmaximize it.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use Page.window.maximized instead.

window_max_height
🖥️ Desktop only. Get or set the maximum height of a native OS window containing Flet app.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use Page.window.max_height instead.

window_max_width
🖥️ Desktop only. Get or set the maximum width of a native OS window containing Flet app.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use Page.window.max_width instead.

window_minimizable
🖥️ Desktop only. Set to False to hide/disable native OS window's "Minimize" button.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use Page.window.minimizable instead.

Defaults to True.

window_minimized
🖥️ Desktop only. True if a native OS window containing Flet app is minimized; otherwise False. Set this property to True to programmatically minimize the window and set it to False to restore it.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use Page.window.minimized instead.

window_min_height
🖥️ Desktop only. Get or set the minimum height of a native OS window containing Flet app.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use Page.window.min_height instead.

window_min_width
🖥️ Desktop only. Get or set the minimum width of a native OS window containing Flet app.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use Page.window.min_width instead.

window_movable
🖥️ Desktop only. macOS only. Set to False to prevent user from changing a position of a native OS window containing Flet app.

Defaults to True.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use Page.window.movable instead.

window_opacity
🖥️ Desktop only. Sets the opacity of a native OS window. The value must be between 0.0 (fully transparent) and 1.0 (fully opaque).

Deprecated in v0.23.0 and will be removed in v0.26.0. Use Page.window.opacity instead.

window_resizable
🖥️ Desktop only. Set to False to prevent user from resizing a native OS window containing Flet app.

Defaults to True.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use Page.window.resizable instead.

window_title_bar_hidden
🖥️ Desktop only. Set to True to hide window title bar. See WindowDragArea control that allows moving an app window with hidden title bar.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use Page.window.title_bar_hidden instead.

window_title_bar_buttons_hidden
🖥️ Desktop only. Set to True to hide window action buttons when a title bar is hidden.

Has effect on macOS only.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use Page.window.title_bar_buttons_hidden instead.

window_top
🖥️ Desktop only. Get or set a vertical position of a native OS window - a distance in virtual pixels from the top edge of the screen.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use Page.window.top instead.

window_prevent_close
🖥️ Desktop only. Set to True to intercept the native close signal. Could be used together with page.on_window_event (close) event handler and page.window_destroy() to implement app exit confirmation logic - see page.window_destroy() for code example.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use Page.window.prevent_close instead.

window_progress_bar
🖥️ Desktop only. The value from 0.0 to 1.0 to display a progress bar on Task Bar (Windows) or Dock (macOS) application button.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use Page.window.progress_bar instead.

window_skip_task_bar
🖥️ Desktop only. Set to True to hide application from the Task Bar (Windows) or Dock (macOS).

Deprecated in v0.23.0 and will be removed in v0.26.0. Use Page.window.skip_task_bar instead.

window_visible
🖥️ Desktop only. Set to True to make application window visible. Used when the app is starting with a hidden window.

The following program starts with a hidden window and makes it visible in 3 seconds:

from time import sleep

import flet as ft

def main(page: ft.Page):
    page.add(ft.Text("Hello!"))

    sleep(3)
    page.window.visible = True
    page.update()  

ft.app(main, view=ft.AppView.FLET_APP_HIDDEN)

Note view=ft.AppView.FLET_APP_HIDDEN which hides app window on start.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use Page.window.visible instead.

window_width
🖥️ Desktop only. Get or set the width of a native OS window containing Flet app.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use Page.window.width instead.

Methods
add(*controls)
Adds controls to page

page.add(ft.Text("Hello!"), ft.FilledButton("Button"))

can_launch_url(url)
Checks whether the specified URL can be handled by some app installed on the device.

Returns True if it is possible to verify that there is a handler available. A False return value can indicate either that there is no handler available, or that the application does not have permission to check. For example:

On recent versions of Android and iOS, this will always return False unless the application has been configuration to allow querying the system for launch support.
On web, this will always return False except for a few specific schemes that are always assumed to be supported (such as http(s)), as web pages are never allowed to query installed applications.
close(control)
Closes the provided control.

It sets the control.open=False and calls update().

close_banner()
Closes active banner.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use page.close(banner) instead.

close_bottom_sheet()
Closes active bottom sheet.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use page.close(bottom_sheet) instead.

close_dialog()
Closes active dialog.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use page.close(dialog) instead.

close_drawer()
Closes active drawer.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use page.close(drawer) instead.

close_end_drawer()
Closes active end drawer.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use page.close(end_drawer) instead.

close_snack_bar()
Closes active end drawer.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use page.close(snack_bar) instead.

close_in_app_web_view()
Closes in-app web view opened with launch_url().

📱 Mobile only.

error(message)
fetch_page_details()
get_clipboard()
Get the last text value saved to a clipboard on a client side.

get_control(id)
Get a control by its id.

Example:

import flet as ft

def main(page: ft.Page):
    x = ft.IconButton(ft.Icons.ADD)
    page.add(x)
    print(type(page.get_control(x.uid)))

ft.app(main)

get_upload_url(file_name, expires)
Generates presigned upload URL for built-in upload storage:

file_name - a relative to upload storage path.
expires - a URL time-to-live in seconds.
For example:

upload_url = page.get_upload_url("dir/filename.ext", 60)

To enable built-in upload storage provide upload_dir argument to flet.app() call:

ft.app(main, upload_dir="uploads")

go(route)
A helper method that updates page.route, calls page.on_route_change event handler to update views and finally calls page.update().

insert(at, *controls)
Inserts controls at specific index of page.controls list.

launch_url(url)
Opens url in a new browser window.

Optional method arguments:

web_window_name - window tab/name to open URL in: UrlTarget.SELF - the same browser tab, UrlTarget.BLANK - a new browser tab (or in external application on mobile device) or <your name> - a named tab.
web_popup_window - set to True to display a URL in a browser popup window. Defaults to False.
window_width - optional, popup window width.
window_height - optional, popup window height.
login(provider, fetch_user, fetch_groups, scope, saved_token, on_open_authorization_url, complete_page_html, redirect_to_page, authorization)
Starts OAuth flow. See Authentication guide for more information and examples.

logout()
Clears current authentication context. See Authentication guide for more information and examples.

open(control)
Opens the provided control.

Adds this control to the page.overlay, sets the control.open=True, then calls update().

remove(*controls)
Removes specific controls from page.controls list.

remove_at(index)
Remove controls from page.controls list at specific index.

run_task(handler, *args, **kwargs)
Run handler coroutine as a new Task in the event loop associated with the current page.

run_thread(handler, *args)
Run handler function as a new Thread in the executor associated with the current page.

scroll_to(offset, delta, key, duration, curve)
Moves scroll position to either absolute offset, relative delta or jump to the control with specified key.

See Column.scroll_to() for method details and examples.

set_clipboard(data)
Set clipboard data on a client side (user's web browser or a desktop), for example:

Python
page.set_clipboard("This value comes from Flet app")

show_banner(banner: Banner)
Displays the banner at the top of the page.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use page.open(banner) instead.

show_bottom_sheet(bottom_sheet: BottomSheet)
Displays bottom sheet at the bottom of the page.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use page.open(bottom_sheet) instead.

show_dialog(dialog: AlertDialog)
Displays dialog.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use page.open(dialog) instead.

show_drawer(drawer: NavigationDialog)
Displays drawer.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use page.open(drawer) instead.

show_end_drawer(drawer: NavigationDialog)
Displays end_drawer.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use page.open(end_drawer) instead.

show_snack_bar(snack_bar: SnackBar)
Displays SnackBar at the bottom of the page.

*Deprecated in v0.23.0 and will be removed in v0.26.0. Use page.open(snack_bar) instead.

window_center()
🖥️ Desktop only. Move app's native OS window to a center of the screen.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use Page.window.center() instead.

window_close()
🖥️ Desktop only. Closes application window.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use Page.window.close() instead.

window_destroy()
🖥️ Desktop only. Forces closing app's native OS window. This method could be used with page.window_prevent_close = True to implement app exit confirmation:

import flet as ft

def main(page: ft.Page):
    page.title = "MyApp"

    def handle_window_event(e):
        if e.data == "close":
            page.open(confirm_dialog)

    page.window.prevent_close = True
    page.window.on_event = handle_window_event

    def handle_yes(e):
        page.window.destroy()

    def handle_no(e):
        page.close(confirm_dialog)

    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Please confirm"),
        content=ft.Text("Do you really want to exit this app?"),
        actions=[
            ft.ElevatedButton("Yes", on_click=handle_yes),
            ft.OutlinedButton("No", on_click=handle_no),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.add(ft.Text('Try exiting this app by clicking window\'s "Close" button!'))

ft.app(main)

window_to_front()
🖥️ Desktop only. Brings application window to a foreground.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use Page.window.to_front() instead.

Events
on_app_lifecycle_state_change
Triggers when app lifecycle state changes.

You can use this event to know when the app becomes active (brought to the front) to update UI with the latest information. This event works on iOS, Android, all desktop platforms and web.

Event handler argument is of type AppLifecycleStateChangeEvent.

on_close
Fires when a session has expired after configured amount of time (60 minutes by default).

on_connect
Fires when a web user (re-)connects to a page session. It is not triggered when an app page is first opened, but is triggered when the page is refreshed, or Flet web client has re-connected after computer was unlocked. This event could be used to detect when a web user becomes "online".

on_disconnect
Fires when a web user disconnects from a page session, i.e. closes browser tab/window.

on_error
Fires when unhandled exception occurs.

on_keyboard_event
Fires when a keyboard key is pressed.

Event handler argument is of type KeyboardEvent.

on_login
Fires upon successful or failed OAuth authorization flow.

See Authentication guide for more information and examples.

on_logout
Fires after page.logout() call.

on_media_change
Fires when page.media has changed.

Event handler argument is of type PageMediaData.

on_platform_brigthness_change
Fires when brightness of app host platform has changed.

on_resize
Fires when a browser or native OS window containing Flet app is resized by a user, for example:

Python
def page_resize(e):
    print("New page size:", page.window.width, page.window_height)

page.on_resize = page_resize

Event handler argument is of type WindowResizeEvent.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use Page.on_resized instead.

on_resized
Fires when a browser or native OS window containing Flet app is resized by a user, for example:

Python
def page_resized(e):
    print("New page size:", page.window.width, page.window_height)

page.on_resized = page_resized

Event handler argument is of type WindowResizeEvent.

on_route_change
Fires when page route changes either programmatically, by editing application URL or using browser Back/Forward buttons.

Event handler argument is of type RouteChangeEvent.

on_scroll
Fires when page's scroll position is changed by a user.

Event handler argument is of type OnScrollEvent.

on_view_pop
Fires when the user clicks automatic "Back" button in AppBar control.

Event handler argument is of type ViewPopEvent.

on_window_event
Fires when an application's native OS window changes its state: position, size, maximized, minimized, etc.

Event handler argument is of type WindowEvent.

Deprecated in v0.23.0 and will be removed in v0.26.0. Use Page.window.on_event instead.

Magic methods
__contains__(control)
Checks if a control is present on the page, for example:

import flet as ft


def main(page: ft.Page):
    hello = ft.Text("Hello, World!")
    page.add(hello)
    print(hello in page)  # True
    
    
ft.app(main)

ResponsiveRow
ResponsiveRow borrows the idea of grid layout from Bootstrap web framework.

ResponsiveRow allows aligning child controls to virtual columns. By default, a virtual grid has 12 columns, but that can be customized with ResponsiveRow.columns property.

Similar to expand property, every control now has col property which allows specifying how many columns a control should span. For example, to make a layout consisting of two columns spanning 6 virtual columns each:

import flet as ft

ft.ResponsiveRow([
    ft.Column(col=6, controls=[ft.Text("Column 1")]),
    ft.Column(col=6, controls=[ft.Text("Column 2")])
])

ResponsiveRow is "responsive" because it can adapt the size of its children to a changing screen (page, window) size. col property in the example above is a constant number which means the child will span 6 columns for any screen size.

If ResponsiveRow's child doesn't have col property specified it spans the maximum number of columns.

col can be configured to have a different value for specific "breakpoints". Breakpoints are named dimension ranges:

Breakpoint	Dimension
xs	<576px
sm	≥576px
md	≥768px
lg	≥992px
xl	≥1200px
xxl	≥1400px
For example, the following example collapses content into a single column on a mobile device and takes two columns on larger screens:

import flet as ft

ft.ResponsiveRow([
    ft.Column(col={"sm": 6}, controls=[ft.Text("Column 1")]),
    ft.Column(col={"sm": 6}, controls=[ft.Text("Column 2")])
])

Examples
Live example

ResponsiveRow

Python
import flet as ft

def main(page: ft.Page):
    def page_resize(e):
        pw.value = f"{page.width} px"
        pw.update()

    page.on_resize = page_resize

    pw = ft.Text(bottom=50, right=50, style="displaySmall")
    page.overlay.append(pw)
    page.add(
        ft.ResponsiveRow(
            [
                ft.Container(
                    ft.Text("Column 1"),
                    padding=5,
                    bgcolor=ft.Colors.YELLOW,
                    col={"sm": 6, "md": 4, "xl": 2},
                ),
                ft.Container(
                    ft.Text("Column 2"),
                    padding=5,
                    bgcolor=ft.Colors.GREEN,
                    col={"sm": 6, "md": 4, "xl": 2},
                ),
                ft.Container(
                    ft.Text("Column 3"),
                    padding=5,
                    bgcolor=ft.Colors.BLUE,
                    col={"sm": 6, "md": 4, "xl": 2},
                ),
                ft.Container(
                    ft.Text("Column 4"),
                    padding=5,
                    bgcolor=ft.Colors.PINK_300,
                    col={"sm": 6, "md": 4, "xl": 2},
                ),
            ],
        ),
        ft.ResponsiveRow(
            [
                ft.TextField(label="TextField 1", col={"md": 4}),
                ft.TextField(label="TextField 2", col={"md": 4}),
                ft.TextField(label="TextField 3", col={"md": 4}),
            ],
            run_spacing={"xs": 10},
        ),
    )
    page_resize(None)

ft.app(main)

Properties
alignment
How the child Controls should be placed horizontally.

Value is of type MainAxisAlignment and defaults to MainAxisAlignment.START.

columns
The number of virtual columns to layout children.

Defaults to 12.

controls
A list of Controls to display inside the ResponsiveRow.

rtl
True to set text direction to right-to-left.

Defaults to False.

run_spacing
Spacing between runs when row content is wrapped on multiple lines.

Defaults to 10.

spacing
Spacing between controls in a row in virtual pixels. It is applied only when alignment is set to MainAxisAlignment.START, MainAxisAlignment.END or MainAxisAlignment.CENTER.

Defaults to 10.

vertical_alignment
How the child Controls should be placed vertically.

Value is of type CrossAxisAlignment and defaults to CrossAxisAlignment.START.

===============+
Row
A control that displays its children in a horizontal array.

To cause a child control to expand and fill the available horizontal space set its expand property.

Examples
Live example

Row spacing

Python
import flet as ft

def main(page: ft.Page):
    def items(count):
        items = []
        for i in range(1, count + 1):
            items.append(
                ft.Container(
                    content=ft.Text(value=str(i)),
                    alignment=ft.alignment.center,
                    width=50,
                    height=50,
                    bgcolor=ft.Colors.AMBER,
                    border_radius=ft.border_radius.all(5),
                )
            )
        return items

    def gap_slider_change(e):
        row.spacing = int(e.control.value)
        row.update()

    gap_slider = ft.Slider(
        min=0,
        max=50,
        divisions=50,
        value=0,
        label="{value}",
        on_change=gap_slider_change,
    )

    row = ft.Row(spacing=0, controls=items(10))

    page.add(ft.Column([ ft.Text("Spacing between items"), gap_slider]), row)

ft.app(main)

Row wrapping

Python
import flet as ft

def main(page: ft.Page):
    def items(count):
        items = []
        for i in range(1, count + 1):
            items.append(
                ft.Container(
                    content=ft.Text(value=str(i)),
                    alignment=ft.alignment.center,
                    width=50,
                    height=50,
                    bgcolor=ft.Colors.AMBER,
                    border_radius=ft.border_radius.all(5),
                )
            )
        return items

    def slider_change(e):
        row.width = float(e.control.value)
        row.update()

    width_slider = ft.Slider(
        min=0,
        max=page.window.width,
        divisions=20,
        value=page.window.width,
        label="{value}",
        on_change=slider_change,
    )

    row = ft.Row(
        wrap=True,
        spacing=10,
        run_spacing=10,
        controls=items(30),
        width=page.window.width,
    )

    page.add(
        ft.Column(
            [
                ft.Text(
                    "Change the row width to see how child items wrap onto multiple rows:"
                ),
                width_slider,
            ]
        ),
        row,
    )

ft.app(main)

Row horizontal alignments

Python
import flet as ft

def main(page: ft.Page):
    def items(count):
        items = []
        for i in range(1, count + 1):
            items.append(
                ft.Container(
                    content=ft.Text(value=str(i)),
                    alignment=ft.alignment.center,
                    width=50,
                    height=50,
                    bgcolor=ft.Colors.AMBER_500,
                )
            )
        return items

    def row_with_alignment(align: ft.MainAxisAlignment):
        return ft.Column(
            [
                ft.Text(str(align), size=16),
                ft.Container(
                    content=ft.Row(items(3), alignment=align),
                    bgcolor=ft.Colors.AMBER_100,
                ),
            ]
        )

    page.add(
        row_with_alignment(ft.MainAxisAlignment.START),
        row_with_alignment(ft.MainAxisAlignment.CENTER),
        row_with_alignment(ft.MainAxisAlignment.END),
        row_with_alignment(ft.MainAxisAlignment.SPACE_BETWEEN),
        row_with_alignment(ft.MainAxisAlignment.SPACE_AROUND),
        row_with_alignment(ft.MainAxisAlignment.SPACE_EVENLY),
    )


ft.app(main)

Row vertical

Python
import flet as ft

def main(page: ft.Page):
    def items(count):
        items = []
        for i in range(1, count + 1):
            items.append(
                ft.Container(
                    content=ft.Text(value=str(i)),
                    alignment=ft.alignment.center,
                    width=50,
                    height=50,
                    bgcolor=ft.Colors.AMBER_500,
                )
            )
        return items

    def row_with_vertical_alignment(align: ft.CrossAxisAlignment):
        return ft.Column(
            [
                ft.Text(str(align), size=16),
                ft.Container(
                    content=ft.Row(items(3), vertical_alignment=align),
                    bgcolor=ft.Colors.AMBER_100,
                    height=150,
                ),
            ]
        )

    page.add(
        row_with_vertical_alignment(ft.CrossAxisAlignment.START),
        row_with_vertical_alignment(ft.CrossAxisAlignment.CENTER),
        row_with_vertical_alignment(ft.CrossAxisAlignment.END),
    )

ft.app(main)

Properties
alignment
How the child Controls should be placed horizontally.

Value is of type MainAxisAlignment and defaults to MainAxisAlignment.START.

auto_scroll
True if scrollbar should automatically move its position to the end when children updated. Must be False for scroll_to() method to work.

controls
A list of Controls to display inside the Row.

rtl
True to set text direction to right-to-left.

Defaults to False.

run_spacing
Spacing between runs when wrap=True.

Defaults to 10.

scroll
Enables horizontal scrolling for the Row to prevent its content overflow.

Value is of type ScrollMode.

spacing
Spacing between controls in a row. Default value is 10 virtual pixels. Spacing is applied only when alignment is set to MainAxisAlignment.START, MainAxisAlignment.END or MainAxisAlignment.CENTER.

on_scroll_interval
Throttling in milliseconds for on_scroll event.

Defaults to 10.

tight
Specifies how much space should be occupied horizontally.

Defaults to False, meaning all space is allocated to children.

vertical_alignment
How the child Controls should be placed vertically.

Value is of type CrossAxisAlignment and defaults to CrossAxisAlignment.START.

wrap
When set to True the Row will put child controls into additional rows (runs) if they don't fit a single row.

Methods
scroll_to(offset, delta, key, duration, curve)
Moves scroll position to either absolute offset, relative delta or jump to the control with specified key.

See Column.scroll_to() for method details and examples.

Events
on_scroll
Fires when scroll position is changed by a user.

Event handler argument is an instance of OnScrollEvent class.

Expanding children
When a child Control is placed into a Row you can "expand" it to fill the available space. Every Control has expand property that can have either a boolean value (True - expand control to fill all available space) or an integer - an "expand factor" specifying how to divide a free space with other expanded child controls. For example, this code creates a row with a TextField taking all available space and an ElevatedButton next to it:

r = ft.Row([
  ft.TextField(hint_text="Enter your name", expand=True),
  ft.ElevatedButton(text="Join chat")
])

The following example with numeric expand factors creates a Row with 3 containers in it and having widths of 20% (1/5), 60% (3/5) and 20% (1/5) respectively:

r = ft.Row([
  ft.Container(expand=1, content=ft.Text("A")),
  ft.Container(expand=3, content=ft.Text("B")),
  ft.Container(expand=1, content=ft.Text("C"))
])

In general, the resulting width of a child in percents is calculated as expand / sum(all expands) * 100%.

If you need to give the child Control of the Row the flexibility to expand to fill the available space horizontally but not require it to fill the available space, set its expand_loose property to True.

==================+

SafeArea
A control that insets its content by sufficient padding to avoid intrusions by the operating system.

For example, this will indent the content by enough to avoid the status bar at the top of the screen.

It will also indent the content by the amount necessary to avoid The Notch on the iPhone X, or other similar creative physical features of the display.

When a minimum_padding is specified, the greater of the minimum padding or the safe area padding will be applied.

Example
Live example

import flet as ft

class State:
    counter = 0

def main(page: ft.Page):
    state = State()

    def add_click(e):
        state.counter += 1
        counter.value = str(state.counter)
        counter.update()

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD, on_click=add_click
    )
    page.add(
        ft.SafeArea(
            ft.Container(
                counter := ft.Text("0", size=50),
                alignment=ft.alignment.center,
            ),
            expand=True,
        )
    )

ft.app(main)

Properties
bottom
Whether to avoid system intrusions on the bottom side of the screen.

Defaults to True.

content
A Control to display inside safe area.

left
Whether to avoid system intrusions on the left.

Defaults to True.

maintain_bottom_view_padding
Specifies whether the SafeArea should maintain the bottom MediaQueryData.viewPadding instead of the bottom MediaQueryData.padding, defaults to False.

For example, if there is an onscreen keyboard displayed above the SafeArea, the padding can be maintained below the obstruction rather than being consumed. This can be helpful in cases where your layout contains flexible controls, which could visibly move when opening a software keyboard due to the change in the padding value. Setting this to true will avoid the UI shift.

minimum
This minimum padding to apply.

The greater of the minimum insets and the media padding will be applied.

Deprecated (renamed) in v0.23.0 and will be removed in v0.26.0. Use minimum_padding instead.

minimum_padding
This minimum padding to apply.

The greater of the minimum insets and the media padding will be applied.

right
Whether to avoid system intrusions on the right.

Defaults to True.

top
Whether to avoid system intrusions at the top of the screen, typically the system status bar.

Defaults to True.

=================

Stack
A control that positions its children on top of each other.

This control is useful if you want to overlap several children in a simple way, for example having some text and an image, overlaid with a gradient and a button attached to the bottom.

Stack is also useful if you want to implement implicit animations that require knowing absolute position of a target value.

Examples
Live example

Transparent title over an image

Python
import flet as ft

def main(page: ft.Page):
    st = ft.Stack(
        [
            ft.Image(
                src=f"https://picsum.photos/300/300",
                width=300,
                height=300,
                fit=ft.ImageFit.CONTAIN,
            ),
            ft.Row(
                [
                    ft.Text(
                        "Image title",
                        color="white",
                        size=40,
                        weight="bold",
                        opacity=0.5,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        width=300,
        height=300,
    )

    page.add(st)

ft.app(main)

Avatar with online status

Python
import flet as ft

def main(page):
    page.add(
        ft.Stack(
            [
                ft.CircleAvatar(
                    foreground_image_url="https://avatars.githubusercontent.com/u/5041459?s=88&v=4"
                ),
                ft.Container(
                    content=ft.CircleAvatar(bgcolor=ft.Colors.GREEN, radius=5),
                    alignment=ft.alignment.bottom_left,
                ),
            ],
            width=40,
            height=40,
        )
    )

ft.app(main, view=ft.AppView.WEB_BROWSER)


Absolute positioning inside Stack

Python
import flet as ft

def main(page: ft.Page):

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.add(
        ft.Container(
            ft.Stack(
                [
                    ft.Container(width=20, height=20, bgcolor=ft.Colors.RED, border_radius=5),
                    ft.Container(
                        width=20,
                        height=20,
                        bgcolor=ft.Colors.YELLOW,
                        border_radius=5,
                        right=0,
                    ),
                    ft.Container(
                        width=20,
                        height=20,
                        bgcolor=ft.Colors.BLUE,
                        border_radius=5,
                        right=0,
                        bottom=0,
                    ),
                    ft.Container(
                        width=20,
                        height=20,
                        bgcolor=ft.Colors.GREEN,
                        border_radius=5,
                        left=0,
                        bottom=0,
                    ),
                    ft.Column(
                        [
                            ft.Container(
                                width=20,
                                height=20,
                                bgcolor=ft.Colors.PURPLE,
                                border_radius=5,
                            )
                        ],
                        left=35,
                        top=35,
                    ),
                ]
            ),
            border_radius=8,
            padding=5,
            width=100,
            height=100,
            bgcolor=ft.Colors.BLACK,
        )
    )

ft.app(main)


Properties
alignment
The alignment of the non-positioned (those that do not specify an alignment - ex neither top nor bottom - in a particular axis and partially-positioned controls.

clip_behavior
The content will be clipped (or not) according to this option.

Value is of type ClipBehavior and defaults to ClipBehavior.HARD_EDGE.

controls
A list of Controls to display inside the Stack. The last control in the list is displayed on top.

fit
How to size the non-positioned controls.

Value is of type StackFit and defaults to StackFit.LOOSE.

Edit this page


===============+


Tabs
The Tabs control is used for navigating frequently accessed, distinct content categories. Tabs allow for navigation between two or more content views and relies on text headers to articulate the different sections of content.

Examples
Live example

Tabs

Python
import flet as ft

def main(page: ft.Page):

    t = ft.Tabs(
        selected_index=1,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Tab 1",
                content=ft.Container(
                    content=ft.Text("This is Tab 1"), alignment=ft.alignment.center
                ),
            ),
            ft.Tab(
                tab_content=ft.Icon(ft.Icons.SEARCH),
                content=ft.Text("This is Tab 2"),
            ),
            ft.Tab(
                text="Tab 3",
                icon=ft.Icons.SETTINGS,
                content=ft.Text("This is Tab 3"),
            ),
        ],
        expand=1,
    )

    page.add(t)

ft.app(main)

Tabs properties
animation_duration
Duration of animation in milliseconds of switching between tabs.

Defaults to 50.

clip_behavior
The content will be clipped (or not) according to this option.

Value is of type ClipBehavior.

divider_color
The color of the divider.

divider_height
The height of the divider.

Defaults to 1.0.

enable_feedback
Whether detected gestures should provide acoustic and/or haptic feedback. On Android, for example, setting this to True produce a click sound and a long-press will produce a short vibration.

Defaults to True.

indicator_border_radius
The radius of the indicator's corners.

indicator_border_side
The color and weight of the horizontal line drawn below the selected tab.

indicator_color
The color of the indicator(line that appears below the selected tab).

indicator_padding
Locates the selected tab's underline relative to the tab's boundary. The indicator_tab_size property can be used to define the tab indicator's bounds in terms of its (centered) tab widget with False, or the entire tab with True.

indicator_tab_size
True for indicator to take entire tab.

indicator_thickness
The thickness of the indicator. Value must be greater than zero.

Defaults to 3.0 when secondary=False, else 3.0.

is_secondary
Whether to create a secondary/nested tab bar. Secondary tabs are used within a content area to further separate related content and establish hierarchy.

Defaults to False.

label_color
The color of selected tab labels.

label_padding
The padding around the tab label.

Value is of type Padding.

label_text_style
The text style of the tab labels.

Value is of type TextStyle.

mouse_cursor
The cursor to be displayed when a mouse pointer enters or is hovering over this control. The value is MouseCursor enum.

overlay_color
Defines the ink response focus, hover, and splash colors in various ControlState states. The following ControlState values are supported: PRESSED, HOVERED and FOCUSED.

padding
The padding around the Tabs control.

Value is of type Padding.

selected_index
The index of currently selected tab.

scrollable
Whether this tab bar can be scrolled horizontally.

If scrollable is True, then each tab is as wide as needed for its label and the entire Tabs controls is scrollable. Otherwise each tab gets an equal share of the available space.

splash_border_radius
Defines the clipping radius of splashes that extend outside the bounds of the tab.

Value is of type BorderRadius.

tab_alignment
Specifies the horizontal alignment of the tabs within the Tabs control.

Value is of type TabAlignment and defaults to TabAlignment.START, if scrollable=True, and to TabAlignment.FILL, if scrollable=False.

tabs
A list of Tab controls.

unselected_label_color
The color of unselected tab labels.

unselected_label_text_style
The text style of the unselected tab labels.

Value is of type TextStyle.

Tabs events
on_change
Fires when selected_index changes.

on_click
Fires when a tab is clicked.

Tab properties
content
A Control to display below the Tab when it is selected.

icon
An icon to display on the left of Tab text.

tab_content
A Control representing custom tab content replacing text and icon.

text
Tab's display name.



================+


VerticalDivider
A thin vertical line, with padding on either side.

In the material design language, this represents a divider.

Examples
Live example

Python
import flet as ft

def main(page: ft.Page):

    page.add(
        ft.Row(
            [
                ft.Container(
                    bgcolor=ft.Colors.ORANGE_300,
                    alignment=ft.alignment.center,
                    expand=True,
                ),
                 ft.VerticalDivider(),
                ft.Container(
                    bgcolor=ft.Colors.BROWN_400,
                    alignment=ft.alignment.center,
                    expand=True,
                ),
                 ft.VerticalDivider(width=1, color="white"),
                ft.Container(
                    bgcolor=ft.Colors.BLUE_300,
                    alignment=ft.alignment.center,
                    expand=True,
                ),
                 ft.VerticalDivider(width=9, thickness=3),
                ft.Container(
                    bgcolor=ft.Colors.GREEN_300,
                    alignment=ft.alignment.center,
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        )
    )

ft.app(main)


Properties
color
The color to use when painting the line.

leading_indent
The amount of empty space to the leading edge of the divider.

Defaults to 0.0.

thickness
The thickness of the line drawn within the divider. A divider with a thickness of 0.0 is always drawn as a line with a width of exactly one device pixel.

Defaults to 0.0.

trailing_indent
The amount of empty space to the trailing edge of the divider.

Defaults to 0.0.

width
The divider's width. The divider itself is always drawn as a vertical line that is centered within the width specified by this value. I

Defaults to 16.0.



===================


View
View is the top most container for all other controls.

A root view is automatically created when a new user session started. From layout perspective the View represents a Column control, so it has a similar behavior and shares same properties.

Properties
appbar
A AppBar control to display at the top of the Page.

auto_scroll
True if scrollbar should automatically move its position to the end when children updated. Must be False for scroll_to() to work.

bgcolor
Background color of the view.

controls
A list of Controls to display on the Page.

For example, to add a new control to a page:

Python
page.controls.append(ft.Text("Hello!"))
page.update()

or to get the same result as above using page.add() shortcut method:

Python
page.add(ft.Text("Hello!"))

To remove the top most control on the page:

Python
page.controls.pop()
page.update()

Value is of a list of Controls.

decoration
The background decoration.

Value is of type BoxDecoration.

drawer
A NavigationDrawer control to display as a panel sliding from the start edge of the view.

end_drawer
A NavigationDrawer control to display as a panel sliding from the end edge of the view.

floating_action_button
A FloatingActionButton control to display on top of Page content.

floating_action_button_location
Describes position of floating_action_button

Value is of type FloatingActionButtonLocation

foreground_decoration
The foreground decoration.

Value is of type BoxDecoration.

fullscreen_dialog
Whether this view is a full-screen dialog.

In Material and Cupertino, being fullscreen has the effects of making the app bars have a close button instead of a back button. On iOS, dialogs transitions animate differently and are also not closeable with the back swipe gesture.

Value is of type bool and defaults to False.

horizontal_alignment
How the child Controls should be placed horizontally.

Value is of type CrossAxisAlignment and defaults to CrossAxisAlignment.START.

on_scroll_interval
Throttling in milliseconds for on_scroll event.

Value is of type int and defaults to 10.

padding
A space between page contents and its edges.

Value is of type PaddingValue and defaults to padding.all(10).

route
View's route - not currently used by Flet framework, but can be used in a user program to update page.route when a view popped.

Value is of type str

scroll
Enables a vertical scrolling for the Page to prevent its content overflow.

Value is of type ScrollMode.

spacing
Vertical spacing between controls on the Page. Default value is 10 virtual pixels. Spacing is applied only when vertical_alignment is set to MainAxisAlignment.START, MainAxisAlignment.END or MainAxisAlignment.CENTER.

Value is of type [OptionalNumber] and defaults to 10

vertical_alignment
How the child Controls should be placed vertically.

Value is of type MainAxisAlignment and defaults to MainAxisAlignment.START.

Methods
scroll_to(offset, delta, key, duration, curve)
Moves scroll position to either absolute offset, relative delta or jump to the control with specified key.

See Column.scroll_to() for method details and examples.

Events
on_scroll
Fires when scroll position is changed by a user.

Event handler argument is of type OnScrollEvent.


=================


MenuBar
A menu bar that manages cascading child menus.

It could be placed anywhere but typically resides above the main body of the application and defines a menu system for invoking callbacks in response to user selection of a menu item.

Examples
Live example

Python
import flet as ft


def main(page: ft.Page):
    appbar_text_ref = ft.Ref[ft.Text]()

    def handle_menu_item_click(e):
        print(f"{e.control.content.value}.on_click")
        page.open(ft.SnackBar(content=ft.Text(f"{e.control.content.value} was clicked!")))
        appbar_text_ref.current.value = e.control.content.value
        page.update()

    def handle_submenu_open(e):
        print(f"{e.control.content.value}.on_open")

    def handle_submenu_close(e):
        print(f"{e.control.content.value}.on_close")

    def handle_submenu_hover(e):
        print(f"{e.control.content.value}.on_hover")

    page.appbar = ft.AppBar(
        title=ft.Text("Menus", ref=appbar_text_ref),
        center_title=True,
        bgcolor=ft.Colors.BLUE,
    )

    menubar = ft.MenuBar(
        expand=True,
        style=ft.MenuStyle(
            alignment=ft.alignment.top_left,
            bgcolor=ft.Colors.RED_300,
            mouse_cursor={
                ft.ControlState.HOVERED: ft.MouseCursor.WAIT,
                ft.ControlState.DEFAULT: ft.MouseCursor.ZOOM_OUT,
            },
        ),
        controls=[
            ft.SubmenuButton(
                content=ft.Text("File"),
                on_open=handle_submenu_open,
                on_close=handle_submenu_close,
                on_hover=handle_submenu_hover,
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("About"),
                        leading=ft.Icon(ft.Icons.INFO),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.GREEN_100}
                        ),
                        on_click=handle_menu_item_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Save"),
                        leading=ft.Icon(ft.Icons.SAVE),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.GREEN_100}
                        ),
                        on_click=handle_menu_item_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Quit"),
                        leading=ft.Icon(ft.Icons.CLOSE),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.GREEN_100}
                        ),
                        on_click=handle_menu_item_click,
                    ),
                ],
            ),
            ft.SubmenuButton(
                content=ft.Text("View"),
                on_open=handle_submenu_open,
                on_close=handle_submenu_close,
                on_hover=handle_submenu_hover,
                controls=[
                    ft.SubmenuButton(
                        content=ft.Text("Zoom"),
                        controls=[
                            ft.MenuItemButton(
                                content=ft.Text("Magnify"),
                                leading=ft.Icon(ft.Icons.ZOOM_IN),
                                close_on_click=False,
                                style=ft.ButtonStyle(
                                    bgcolor={
                                        ft.ControlState.HOVERED: ft.Colors.PURPLE_200
                                    }
                                ),
                                on_click=handle_menu_item_click,
                            ),
                            ft.MenuItemButton(
                                content=ft.Text("Minify"),
                                leading=ft.Icon(ft.Icons.ZOOM_OUT),
                                close_on_click=False,
                                style=ft.ButtonStyle(
                                    bgcolor={
                                        ft.ControlState.HOVERED: ft.Colors.PURPLE_200
                                    }
                                ),
                                on_click=handle_menu_item_click,
                            ),
                        ],
                    )
                ],
            ),
        ],
    )

    page.add(ft.Row([menubar]))


ft.app(main)


Properties
clip_behavior
Whether to clip the content of this control or not.

Value is of type ClipBehavior and defaults to ClipBehavior.NONE.

controls
The list of menu items that are the top level children of the MenuBar.

style
Value is of type MenuStyle.


======

Text
Text is a control for displaying text.

Examples
Live example

Custom text styles

import flet as ft

def main(page: ft.Page):
    page.title = "Text custom styles"
    page.scroll = "adaptive"

    page.add(
        ft.Text("Size 10", size=10),
        ft.Text("Size 30, Italic", size=30, color="pink600", italic=True),
        ft.Text(
            "Size 40, w100",
            size=40,
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_600,
            weight=ft.FontWeight.W_100,
        ),
        ft.Text(
            "Size 50, Normal",
            size=50,
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.ORANGE_800,
            weight=ft.FontWeight.NORMAL,
        ),
        ft.Text(
            "Size 60, Bold, Italic",
            size=50,
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.GREEN_700,
            weight=ft.FontWeight.BOLD,
            italic=True,
        ),
        ft.Text("Size 70, w900, selectable", size=70, weight=ft.FontWeight.W_900, selectable=True),
        ft.Text("Limit long text to 1 line with ellipsis", theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
        ft.Text(
            "Proin rutrum, purus sit amet elementum volutpat, nunc lacus vulputate orci, cursus ultrices neque dui quis purus. Ut ultricies purus nec nibh bibendum, eget vestibulum metus various. Duis convallis maximus justo, eu rutrum libero maximus id. Donec ullamcorper arcu in sapien molestie, non pellentesque tellus pellentesque. Nulla nec tristique ex. Maecenas euismod nisl enim, a convallis arcu laoreet at. Ut at tortor finibus, rutrum massa sit amet, pulvinar velit. Phasellus diam lorem, viverra vitae leo vitae, consequat suscipit lorem.",
            max_lines=1,
            overflow=ft.TextOverflow.ELLIPSIS,
        ),
        ft.Text("Limit long text to 2 lines and fading", theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
        ft.Text(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur quis nibh vitae purus consectetur facilisis sed vitae ipsum. Quisque faucibus sed nulla placerat sagittis. Phasellus condimentum risus vitae nulla vestibulum auctor. Curabitur scelerisque, nibh eget imperdiet consequat, odio ante tempus diam, sed volutpat nisl erat eget turpis. Sed viverra, diam sit amet blandit vulputate, mi tellus dapibus lorem, vitae vehicula diam mauris placerat diam. Morbi sit amet pretium turpis, et consequat ligula. Nulla velit sem, suscipit sit amet dictum non, tincidunt sed nulla. Aenean pellentesque odio porttitor sagittis aliquam. Name various at metus vitae vulputate. Praesent faucibus nibh lorem, eu pretium dolor dictum nec. Phasellus eget dui laoreet, viverra magna vitae, pellentesque diam.",
            max_lines=2,
        ),
        ft.Text("Limit the width and height of long text", theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
        ft.Text(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur quis nibh vitae purus consectetur facilisis sed vitae ipsum. Quisque faucibus sed nulla placerat sagittis. Phasellus condimentum risus vitae nulla vestibulum auctor. Curabitur scelerisque, nibh eget imperdiet consequat, odio ante tempus diam, sed volutpat nisl erat eget turpis. Sed viverra, diam sit amet blandit vulputate, mi tellus dapibus lorem, vitae vehicula diam mauris placerat diam. Morbi sit amet pretium turpis, et consequat ligula. Nulla velit sem, suscipit sit amet dictum non, tincidunt sed nulla. Aenean pellentesque odio porttitor sagittis aliquam. Name various at metus vitae vulputate. Praesent faucibus nibh lorem, eu pretium dolor dictum nec. Phasellus eget dui laoreet, viverra magna vitae, pellentesque diam.",
            width=700,
            height=100,
        ),
    )

ft.app(main)


Pre-defined theme text styles

import flet as ft

def main(page: ft.Page):
    page.title = "Text theme styles"
    page.scroll = "adaptive"

    page.add(
        ft.Text("Display Large", theme_style=ft.TextThemeStyle.DISPLAY_LARGE),
        ft.Text("Display Medium", theme_style=ft.TextThemeStyle.DISPLAY_MEDIUM),
        ft.Text("Display Small", theme_style=ft.TextThemeStyle.DISPLAY_SMALL),
        ft.Text("Headline Large", theme_style=ft.TextThemeStyle.HEADLINE_LARGE),
        ft.Text("Headline Medium", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM),
        ft.Text("Headline Small", theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
        ft.Text("Title Large", theme_style=ft.TextThemeStyle.TITLE_LARGE),
        ft.Text("Title Medium", theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
        ft.Text("Title Small", theme_style=ft.TextThemeStyle.TITLE_SMALL),
        ft.Text("Label Large", theme_style=ft.TextThemeStyle.LABEL_LARGE),
        ft.Text("Label Medium", theme_style=ft.TextThemeStyle.LABEL_MEDIUM),
        ft.Text("Label Small", theme_style=ft.TextThemeStyle.LABEL_SMALL),
        ft.Text("Body Large", theme_style=ft.TextThemeStyle.BODY_LARGE),
        ft.Text("Body Medium", theme_style=ft.TextThemeStyle.BODY_MEDIUM),
        ft.Text("Body Small", theme_style=ft.TextThemeStyle.BODY_SMALL),
    )

ft.app(main)

Font with variable weight

import flet as ft

def main(page: ft.Page):
    page.fonts = {
        "RobotoSlab": "https://github.com/google/fonts/raw/main/apache/robotoslab/RobotoSlab%5Bwght%5D.ttf"
    }

    t = ft.Text(
        "This is rendered with Roboto Slab",
        size=30,
        font_family="RobotoSlab",
        weight=ft.FontWeight.W_100,
    )

    def width_changed(e):
        t.weight = f"w{int(e.control.value)}"
        t.update()

    page.add(
        t,
        ft.Slider(
            min=100,
            max=900,
            divisions=8,
            label="{value}",
            width=500,
            on_change=width_changed,
        ),
    )

ft.app(main)


Rich text basics

import flet as ft

def main(page: ft.Page):
    page.add(
        ft.Text("Plain text with default style"),
        ft.Text(
            "Some text",
            size=30,
            spans=[
                ft.TextSpan(
                    "here goes italic",
                    ft.TextStyle(italic=True, size=20, color=ft.Colors.GREEN),
                    spans=[
                        ft.TextSpan(
                            "bold and italic",
                            ft.TextStyle(weight=ft.FontWeight.BOLD),
                        ),
                        ft.TextSpan(
                            "just italic",
                            spans=[
                                ft.TextSpan("smaller italic", ft.TextStyle(size=15))
                            ],
                        ),
                    ],
                )
            ],
        ),
        ft.Text(
            disabled=False,
            spans=[
                ft.TextSpan(
                    "underlined and clickable",
                    ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE),
                    on_click=lambda e: print(f"Clicked span: {e.control.uid}"),
                    on_enter=lambda e: print(f"Entered span: {e.control.uid}"),
                    on_exit=lambda e: print(f"Exited span: {e.control.uid}"),
                ),
                ft.TextSpan(" "),
                ft.TextSpan(
                    "underlined red wavy",
                    ft.TextStyle(
                        decoration=ft.TextDecoration.UNDERLINE,
                        decoration_color=ft.Colors.RED,
                        decoration_style=ft.TextDecorationStyle.WAVY,
                    ),
                    on_enter=lambda e: print(f"Entered span: {e.control.uid}"),
                    on_exit=lambda e: print(f"Exited span: {e.control.uid}"),
                ),
                ft.TextSpan(" "),
                ft.TextSpan(
                    "overlined blue",
                    ft.TextStyle(
                        decoration=ft.TextDecoration.OVERLINE, decoration_color="blue"
                    ),
                ),
                ft.TextSpan(" "),
                ft.TextSpan(
                    "overlined and underlined",
                    ft.TextStyle(
                        decoration=ft.TextDecoration.OVERLINE
                        | ft.TextDecoration.UNDERLINE
                    ),
                ),
                ft.TextSpan(" "),
                ft.TextSpan(
                    "line through thick",
                    ft.TextStyle(
                        decoration=ft.TextDecoration.LINE_THROUGH,
                        decoration_thickness=3,
                    ),
                ),
            ],
        ),
    )

    def highlight_link(e):
        e.control.style.color = ft.Colors.BLUE
        e.control.update()

    def unhighlight_link(e):
        e.control.style.color = None
        e.control.update()

    page.add(
        ft.Text(
            disabled=False,
            spans=[
                ft.TextSpan("AwesomeApp 1.0 "),
                ft.TextSpan(
                    "Visit our website",
                    ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE),
                    url="https://google.com",
                    on_enter=highlight_link,
                    on_exit=unhighlight_link,
                ),
                ft.TextSpan(" All rights reserved. "),
                ft.TextSpan(
                    "Documentation",
                    ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE),
                    url="https://google.com",
                    on_enter=highlight_link,
                    on_exit=unhighlight_link,
                ),
            ],
        ),
    )

ft.app(main)

Rich text with borders and stroke

import flet as ft

def main(page: ft.Page):
    page.add(
        ft.Stack(
            [
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            "Greetings, planet!",
                            ft.TextStyle(
                                size=40,
                                weight=ft.FontWeight.BOLD,
                                foreground=ft.Paint(
                                    color=ft.Colors.BLUE_700,
                                    stroke_width=6,
                                    stroke_join=ft.StrokeJoin.ROUND,
                                    style=ft.PaintingStyle.STROKE,
                                ),
                            ),
                        ),
                    ],
                ),
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            "Greetings, planet!",
                            ft.TextStyle(
                                size=40,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREY_300,
                            ),
                        ),
                    ],
                ),
            ]
        )
    )

ft.app(main)

Rich text with gradient

import flet as ft

def main(page: ft.Page):
    page.add(
        ft.Text(
            spans=[
                ft.TextSpan(
                    "Greetings, planet!",
                    ft.TextStyle(
                        size=40,
                        weight=ft.FontWeight.BOLD,
                        foreground=ft.Paint(
                            gradient=ft.PaintLinearGradient(
                                (0, 20), (150, 20), [ft.Colors.RED, ft.Colors.YELLOW]
                            )
                        ),
                    ),
                ),
            ],
        )
    )

ft.app(main)

Properties
bgcolor
Text background color.

color
Text foreground color.

font_family
System or custom font family to render text with. See Fonts cookbook guide for instructions on how to import and use custom fonts in your application.

italic
True to use italic typeface.

Value is of type bool and defaults to False.

max_lines
An optional maximum number of lines for the text to span, wrapping if necessary. If the text exceeds the given number of lines, it will be truncated according to overflow.

If this is 1, text will not wrap. Otherwise, text will be wrapped at the edge of the box.

no_wrap
If False (default) the text should break at soft line breaks.

If True, the glyphs in the text will be positioned as if there was unlimited horizontal space.

Value is of type bool and defaults to False.

overflow
Controls how text overflows.

Value is of type TextOverflow and defaults to TextOverflow.FADE.

rtl
True to set text direction to right-to-left.

Defaults to False.

selectable
Whether the text should be selectable.

Defaults to False.

semantics_label
An alternative semantics label for this text.

If present, the semantics of this control will contain this value instead of the actual text. This will overwrite any of the TextSpan.semantics_labels.

This is useful for replacing abbreviations or shorthands with the full text value:

Value is of type str.

ft.Text("$$", semantics_label="Double dollars")

size
Text size in virtual pixels.

Value is of type OptionalNumber and defaults to 14.

spans
The list of TextSpan objects to build a rich text paragraph.

style
The text's style.

Value is of type TextStyle.

text_align
Text horizontal align.

Value is of type TextAlign and defaults to TextAlign.LEFT.

theme_style
Pre-defined text style.

Value is of type TextThemeStyle.

value
The text displayed.

Value is of type str.

weight
Font weight.

Value is of type FontWeight and defaults to FontWeight.NORMAL.

Edit this page


===============



ProgressBar
A material design linear progress indicator, also known as a progress bar.

A control that shows progress along a line.

There are two kinds of linear progress indicators:

Determinate. Determinate progress indicators have a specific value at each point in time, and the value should increase monotonically from 0.0 to 1.0, at which time the indicator is complete. To create a determinate progress indicator, use a non-null value between 0.0 and 1.0.
Indeterminate. Indeterminate progress indicators do not have a specific value at each point in time and instead indicate that progress is being made without indicating how much progress remains. To create an indeterminate progress indicator, use a null value.
Examples
Live example

Python
from time import sleep

import flet as ft

def main(page: ft.Page):
    pb = ft.ProgressBar(width=400)

    page.add(
        ft.Text("Linear progress indicator", style="headlineSmall"),
        ft.Column([ ft.Text("Doing something..."), pb]),
        ft.Text("Indeterminate progress bar", style="headlineSmall"),
        ft.ProgressBar(width=400, color="amber", bgcolor="#eeeeee"),
    )

    for i in range(0, 101):
        pb.value = i * 0.01
        sleep(0.1)
        page.update()

ft.app(main)


Properties
value
The value of this progress indicator. A value of 0.0 means no progress and 1.0 means that progress is complete. The value will be clamped to be in the range 0.0 - 1.0.

Defaults to None, meaning that this progress indicator is indeterminate - displays a predetermined animation that does not indicate how much actual progress is being made.

bar_height
The minimum height of the line used to draw the linear indicator.

Defaults to 4.

border_radius
The border radius of both the indicator and the track. Border radius is an instance of BorderRadius class.

Defaults to border_radius.all(0) - rectangular shape.

bgcolor
Color of the track being filled by the linear indicator.

color
The progress indicator's color.

semantics_label
The Semantics.label for this progress indicator.

semantics_value
The Semantics.value for this progress indicator.

tooltip
The text displayed when hovering the mouse over the control.

Edit this page



============

ProgressRing
A material design circular progress indicator, which spins to indicate that the application is busy.

A control that shows progress along a circle.

There are two kinds of circular progress indicators:

Determinate. Determinate progress indicators have a specific value at each point in time, and the value should increase monotonically from 0.0 to 1.0, at which time the indicator is complete. To create a determinate progress indicator, use a non-null value between 0.0 and 1.0.
Indeterminate. Indeterminate progress indicators do not have a specific value at each point in time and instead indicate that progress is being made without indicating how much progress remains. To create an indeterminate progress indicator, use a null value.
Examples
Live example

Python
from time import sleep
import flet as ft

def main(page: ft.Page):
    pr = ft.ProgressRing(width=16, height=16, stroke_width = 2)

    page.add(
        ft.Text("Circular progress indicator", style="headlineSmall"),
        ft.Row([pr, ft.Text("Wait for the completion...")]),
        ft.Text("Indeterminate cicrular progress", style="headlineSmall"),
        ft.Column(
            [ft.ProgressRing(), ft.Text("I'm going to run for ages...")],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    for i in range(0, 101):
        pr.value = i * 0.01
        sleep(0.1)
        page.update()

ft.app(main)


Properties
bgcolor
Color of the circular track being filled by the circular indicator.

color
The progress indicator's color.

semantics_label
The Semantics.label for this progress indicator.

semantics_value
The Semantics.value for this progress indicator.

stroke_align
The relative position of the stroke. Value typically ranges be -1.0 (inside stroke) and 1.0 (outside stroke).

Defaults to 0 - centered.

stroke_cap
The progress indicator's line ending.

Value is of type StrokeCap.

stroke_width
The width of the line used to draw the circle.

tooltip
The text displayed when hovering the mouse over the control.

value
The value of this progress indicator. A value of 0.0 means no progress and 1.0 means that progress is complete. The value will be clamped to be in the range 0.0 - 1.0. If None, this progress indicator is indeterminate, which means the indicator displays a predetermined animation that does not indicate how much actual progress is being made.

==============