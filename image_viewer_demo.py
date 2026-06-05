import image_viewer

# --- Setup
my_image_viewer = image_viewer.ImageViewer(
    image_dir = "./subtracted_continuous_features",
    output_path = "./outputs/my_output.html" # optional, defaults to "./image_viewer_outputs/output.html"
)

# --- Image directory and output path can be configured later
my_image_viewer.image_dir = "./subtracted_continuous_features"
my_image_viewer.output_path = "./outputs/my_output.html"

# --- Image options
print(my_image_viewer.images) # shows image filenames currently loaded
#my_image_viewer.remove_image("1-HPHF_continuous.png") # remove images
# Note: currently cannot add images, only images in the image_dir folder are loaded

# --- Sorting images
my_image_viewer.sort_images(descending = False) # alphabetical sort
# Note: this treats '1' and '10' as  before '2'. To avoid this, number your files '001', '002',... '010'
my_image_viewer.sort_images_by_regex(["HPHF", "HP", "HF"], descending = False, remove_unmatched_images = True) # regex pattern matching sort
#print(my_image_viewer.images)

# --- Creates HTML file in specified output_path
my_image_viewer.render_html()

# The most convenient way of viewing HTMLs is right-clicking the file in VS Code as pressing "Open in Integrated Browser"
