import image_viewer

# --- Setup
my_image_viewer = image_viewer.ImageViewer()

my_image_viewer.add_images_from_directory("./subtracted_continuous_features/")

my_image_viewer.sort_images(descending = False)
my_image_viewer.sort_images_by_regex(["HPHF"], descending = False, remove_unmatched_images = True)
print(my_image_viewer.images)
my_image_viewer.render_html("./outputs/my_output.html")

my_image_viewer.remove_all_images()
my_image_viewer.add_image("./subtracted_continuous_features/001-HPHF_continuous.png")
my_image_viewer.add_image("./subtracted_continuous_features/002-HF_continuous.png")
my_image_viewer.remove_image("./subtracted_continuous_features/002-HF_continuous.png")
my_image_viewer.render_html("./outputs/my_output2.html")