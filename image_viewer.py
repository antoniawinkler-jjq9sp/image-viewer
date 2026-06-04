import os
import sys
from pathlib import Path
import re

class ImageViewer():
    __image_dir = ""
    __images = []
    __output_path = ""

    def __init__(self, image_dir : str, output_path : str = "./image_viewer_outputs/output.html"):
        self.__image_dir = image_dir
        self.__images = self.__get_valid_images_from_dir(self.__image_dir)
        self.__output_path = output_path

    @property
    def image_dir(self):
        return self.__image_dir
    
    @image_dir.setter
    def image_dir(self, pth : str):
        self.__image_dir = pth
        self.__images = self.__get_valid_images_from_dir(self.__image_dir)

    @property
    def images(self):
        return self.__images
    
    @property
    def output_path(self):
        return self.__output_path
    
    @output_path.setter
    def output_path(self, pth : str):
        self.__output_path = pth

    def sort_images(self, descending : bool = False):
        """
        Sorts images alphabetically (A-Z) according to their filenames. If descending, sorts Z-A.
        """
        if descending:
            self.__images.sort(reverse = True)
        else:
            self.__images.sort()

    def sort_images_by_regex(self, patterns : list[str], 
                             descending : bool = False,
                             remove_unmatched_images : bool = False):
        """
        Sorts images according to a list of regex patterns. 
        Image filenames matching the first pattern are sorted first (if descending, they are sorted last).
        Image filenames matching no patterns are sorted last without modifying their original order (if descending, they are sorted first).
        If `remove_unmatched_images` is true, image filenames matching no patterns are removed.
        """

        self.__images = self.__regex_sort(self.__images, patterns, remove_unmatched_images)

        if descending:
            self.__images.reverse()

    
    def __regex_sort(self, images : list[str], 
                     patterns : list[str], 
                     remove_unmatched_images : bool):
        sorted = []
        unsorted = images
        for pattern in patterns:
            matches = [x for x in unsorted if re.search(pattern , x)]
            for m in matches:
                unsorted.remove(m)
            sorted.extend(matches)

        if not remove_unmatched_images and len(unsorted) > 0:
            sorted.extend(unsorted)

        return sorted
    
    def remove_image(self, image_name : str):
        if image_name in self.__images:
            self.__images.remove(image_name)
        else:
            print(f"{image_name} was not found.", file=sys.stderr)

    def render_html(self):
        with open('image_viewer_template.html', 'r') as f:
            filedata = f.read()
            filedata = filedata.replace(
                    "IMAGE_FILES",
                    ", ".join([f"\"{x}\"" for x in self.__images])
                    )
            img_dir = Path(self.__image_dir).resolve()
            filedata = filedata.replace("IMAGE_DIR", img_dir.as_posix())
            output = Path(self.__output_path).with_suffix(".html")
        
        output.parent.mkdir(parents=True, exist_ok=True)

        with open(output, 'w') as f:
            f.write(filedata)
        
        print(f"HTML file saved to {output}")

    def __get_valid_images_from_dir(self, dir) -> list[str]:
        try:
            images = os.listdir(dir)
            if len(images) == 0:
                raise Exception(f"Directory {dir} is empty.")
        except Exception as e:
            print(e)

        valid_images = []
        for i in images:
            if self.__validate_image(i):
                valid_images.append(i)
        return valid_images

    def __validate_image(self, image: str) -> bool:
        if (image.endswith(".png") 
            or image.endswith(".jpg") 
            or image.endswith(".jpeg") 
            ):
            return True
        else:
            print(f"File {os.path.join(self.__image_dir, image)} is not a valid image (must be PNG, JPG, or JPEG).", file=sys.stderr)
            return False

        
    
    
                
