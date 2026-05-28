# Image Viewer

## About

Display PNG/JPG/JPEG images in an interactive HTML file.

## Usage

Put these files at the **same** directory level as the Python file you are importing `image_viewer` into.

```
my_folder/
    ⤷ image_dir/
    ⤷ image_viewer.py
    ⤷ image_viewer_template.html
    ⤷ ...
```

### Example usage:

```python
import image_viewer

my_image_viewer = image_viewer.ImageViewer()

my_image_viewer.add_images_from_directory("./my_images/")

my_image_viewer.render_html("./output_dir/)
```

_The most convenient way of viewing HTMLs is right-clicking the file in VS Code and pressing "Open in Integrated Browser."_

_HTMLs can be saved as PDFs using the 'Print' feature of web browsers._

### Add images:

```python
my_image_viewer.add_images_from_directory("./my_images/")

my_image_viewer.add_image("./my_images/image1.png")
```

### Remove images:

```python
my_image_viewer.remove_image("./my_images/image1.png")

my_image_viewer.remove_all_images()
```

### Render HTML:

```python
my_image_viewer.render_html("./output_dir/")
```

### View image filenames:

```python
print(my_image_viewer.images)
```

### Sort alphabetically:

_Note: this treats '1' and '10' as before '2'. To avoid this, number your files '001', '002',... '010'_

```python
my_image_viewer.sort_images(descending = False)
```

### Sort according to RegEx patterns:

```python
my_image_viewer.sort_images_by_regex(["pattern1", "pattern2",...],
                                     descending = False,
                                     remove_unmatched_images = False
                                    )
```
