from tkinter import Tk, Canvas, PhotoImage, Button, Label, Entry, StringVar
from PIL import Image, ImageTk, ExifTags
import os
import random
import subprocess
import atexit
import sys

class Game:
        def setup_canvas(self):
                if self.image_counter > 0:
                        img_count_str = " (Images Ranked = " + str(self.image_counter) + ")"
                else:
                        img_count_str = ""
                
                print("=======================================================================================================================")
                print(f"ROUND #{self.round_counter}"+img_count_str)
                print("Selecting and loading images...")
                print("")
                
                self.image_count = random.randint(3,4) # Decide on number of images for the round
                self.image_counter += self.image_count # Update total image counter
                self.round_counter += 1 # Update round counter

                image_paths = [os.path.join(self.images_directory, image) for image in self.get_random_images()]
                sizes = [(self.canvas_width/self.image_count, self.canvas_height-100)] * self.image_count  # You can adjust the sizes if needed

                for index, (image_path, size) in enumerate(zip(image_paths, sizes)):
                    self.image_path[index] = image_path
                    self.image[index] = self.load_and_resize_image(image_path, size)
                    self.canvas.create_image((self.canvas_width/(self.image_count*2)) + ((self.canvas_width/self.image_count) * index), (self.canvas_height-100)/2, anchor='c', image=self.image[index])

                self.create_image_labels()
                self.create_ranking_widgets()

                
                
                
                # Check if the images all already have the same ranking, and try again if that is the case
                ratings = []
                for image_path in image_paths:
                        ratings.append(os.path.basename(image_path)[3])
                print("Image Ratings: "+str(ratings))
                if all(element == ratings[0] for element in ratings):
                        if ratings[0] != '0':
                                print("All ratings are the same, skipping round...")
                                self.clear_canvas()

        def load_and_resize_image(self, image_path, size):
                image_pil = Image.open(image_path)
                return ImageTk.PhotoImage(self.resize_to_fit(image_pil, size))

        def create_image_labels(self):
            for i in range(self.image_count):
                label = Label(self.canvas, text=f"#{i+1}", font=("Arial", 36))
                label.place(x=(i * (self.canvas_width/self.image_count)) + (self.canvas_width/(self.image_count*2)), y=80)  # Adjust the x-coordinate based on image index
                self.objects.append(label)

        def create_ranking_widgets(self):
                widget_loc_x = self.canvas_width/2-50
                widget_loc_y = self.canvas_height-120

                exit_button = Button(self.root, text="QUIT", command=lambda: self.cleanup_temp_files_and_quit(), takefocus=False)
                exit_button.place(x=self.canvas_width/2-20, y=20)

                label = Label(self.root, text="Rank the images from best to worst:")
                label.place(x=widget_loc_x,y=widget_loc_y-15)
                self.objects.append(label)

                self.entry = Entry(self.root, textvariable=self.rank_var)
                self.entry.place(x=widget_loc_x,y=widget_loc_y+15)
                self.entry.focus_set()
                self.entry.bind('<Return>', lambda event=None: submit_button.invoke())
                self.entry.bind('<Tab>', lambda event=None: submit_button.invoke())
                self.entry.bind('<Escape>', lambda event=None: exit_button.invoke())
                self.objects.append(self.entry)

                submit_button = Button(self.root, text="Submit", command=self.submit_ranking, takefocus=False)
                submit_button.place(x=widget_loc_x+55,y=widget_loc_y+45)

                self.objects.append(submit_button)

                self.rank_var.set("")

        def submit_ranking(self):
                ranking = self.rank_var.get().split()[0]
                if len(ranking) == self.image_count and all(ranking.count(str(i+1)) == 1 for i in range(self.image_count)):
                        initial_ratings = ""

                        for img_path in self.image_path:
                                if img_path != 0:
                                        # Extract the basename of the file
                                        base_name = os.path.basename(img_path)
                                        fourth_character = base_name[3]
                                        if fourth_character in ['1', '2', '3', '4', '5']:
                                                initial_ratings = initial_ratings+fourth_character
                                        else:
                                                initial_ratings = initial_ratings+str(self.initialization_rating)
                                                self.initialization_rating += 1
                                                if self.initialization_rating > 5:
                                                        self.initialization_rating = 1
                        sorted_ratings = ''.join(sorted(initial_ratings, reverse=True))

                        rating_index = 0
                        for char in ranking:
                                match char:
                                        case '1': current_image = self.image_path[0]
                                        case '2': current_image = self.image_path[1]
                                        case '3': current_image = self.image_path[2]
                                        case '4': current_image = self.image_path[3]
                                        case '5': current_image = self.image_path[4]
                                        case '6': current_image = self.image_path[5]
                                self.write_star_rating(current_image,sorted_ratings[rating_index])
                                rating_index += 1

                        self.clear_canvas()
                else:
                        print(f"Error: Please rank images 1 to {self.image_count} with no duplicates.")
                        self.rank_var.set("")
                        self.entry.focus_set()

        def get_random_images(self):
                image_files = [os.path.join(root, f) for root, dirs, files in os.walk(self.images_directory) for f in files if f.endswith(('.jxl'))]
                if len(image_files) < self.image_count:
                    raise ValueError("There must be at least six images in the directory.")

                random_images = random.sample(image_files, self.image_count)
                for jxl in random_images:
                        self.convert_jxl_to_jpeg(jxl)
                return self.tempfiles

        def convert_jxl_to_jpeg(self, input_path):
            output_path = os.path.splitext(input_path)[0] + ".jpg"
            try:
                # Assuming djxl is in your system's PATH
                subprocess.run(['djxl', input_path, output_path, '--quiet'], check=True)
                self.tempfiles.append(os.path.splitext(input_path)[0] + ".jpg")
            except subprocess.CalledProcessError as e:
                print(f"Conversion failed: {e}")

        def clear_canvas(self):
                # Destroy Objects
                for item in self.objects:
                        item.destroy()

                # Clear Canvas
                self.canvas.delete("all")

                # Clear Tempfiles
                self.cleanup_temp_files()

                # Reset Lists
                self.objects = []
                self.tempfiles = []
                self.image = [0,0,0,0,0,0]
                self.image_path = [0,0,0,0,0,0]

                # Setup Canvas Anew
                self.setup_canvas()

        def star_to_percent(self, star_rating):
                print(f"Star Rating: {star_rating}")
                match star_rating:
                        case '1': return '1'
                        case '2': return '25'
                        case '3': return '50'
                        case '4': return '75'
                        case '5': return '99'

        def write_star_rating(self, image_path, rating_value):
                # Write rating to metadata using exiftool
                rating_percent = self.star_to_percent(rating_value)
                real_image_path = os.path.splitext(image_path)[0]+".jxl"
                subprocess.run(['exiftool', '-overwrite_original','-IgnoreMinorErrors','-Rating='+rating_value, '-RatingPercent='+rating_percent,real_image_path], check=True)
                xmp_path = real_image_path + ".xmp"
                if os.path.exists(xmp_path):
                        subprocess.run(['exiftool', '-overwrite_original','-IgnoreMinorErrors', '-Rating='+rating_value, '-RatingPercent='+rating_percent,xmp_path], check=True)

                path = os.path.dirname(image_path)
                name = os.path.basename(image_path)
                name = self.modify_char(name,3,str(rating_value))
                name = os.path.join(path,name)
                self.change_filename(image_path,name)

        def resize_to_fit(self, image, size):
                """
                Resize the image to fit within the specified size while preserving the aspect ratio.
                """
                original_width, original_height = image.size
                target_width, target_height = size

                # Calculate the aspect ratios
                width_ratio = target_width / original_width
                height_ratio = target_height / original_height

                # Choose the smallest ratio to ensure that the entire image fits within the specified size
                resize_ratio = min(width_ratio, height_ratio)

                # Calculate the new dimensions
                new_width = int(original_width * resize_ratio)
                new_height = int(original_height * resize_ratio)

                # Resize the image
                return image.resize((new_width, new_height), Image.ANTIALIAS if hasattr(Image, 'ANTIALIAS') else Image.LANCZOS)


        def loop_negative_to(self, value_checking, loop_to):
                if value_checking < 0:
                        return loop_to + value_checking + 1
                else:
                        return value_checking

        def change_filename(self, old_filename, new_filename):
                try:
                        original_name = old_filename
                        prospective_name = new_filename
                        original_name = os.path.splitext(original_name)[0]+".jxl" # Process the names as if they were using the JXL extension,
                        prospective_name = os.path.splitext(prospective_name)[0]+".jxl" # regardless of what extensions were passed as arguments.
                        
                        prospective_basename = os.path.basename(prospective_name)
                        prospective_path = os.path.dirname(prospective_name)

                        # Read and increment the Base 36 counter
                        b36_odometer = [self.b36_to_b10(prospective_basename[4]),self.b36_to_b10(prospective_basename[5]),self.b36_to_b10(prospective_basename[6]),self.b36_to_b10(prospective_basename[7]),self.b36_to_b10(prospective_basename[8]),self.b36_to_b10(prospective_basename[9])]
                        b36_odometer[5] += (self.image_count-1)
                        b36_index = 5
                        while b36_odometer[b36_index] >= 36:
                                b36_odometer[b36_index] -= 36
                                b36_odometer[self.loop_negative_to(b36_index-1,5)] += 1
                                b36_index = self.loop_negative_to(b36_index-1,5)

                        b36_odometer = [self.b10_to_b36(b36_odometer[0]),self.b10_to_b36(b36_odometer[1]),self.b10_to_b36(b36_odometer[2]),self.b10_to_b36(b36_odometer[3]),self.b10_to_b36(b36_odometer[4]),self.b10_to_b36(b36_odometer[5])]
                        prospective_basename = self.modify_char(prospective_basename,4,b36_odometer[0])
                        prospective_basename = self.modify_char(prospective_basename,5,b36_odometer[1])
                        prospective_basename = self.modify_char(prospective_basename,6,b36_odometer[2])
                        prospective_basename = self.modify_char(prospective_basename,7,b36_odometer[3])
                        prospective_basename = self.modify_char(prospective_basename,8,b36_odometer[4])
                        prospective_basename = self.modify_char(prospective_basename,9,b36_odometer[5])
                        prospective_name = os.path.join(prospective_path,prospective_basename)

                        while os.path.exists(prospective_name):
                                print(f"A different file with the desired name already exists: {prospective_name}")
                                prospective_basename = os.path.basename(prospective_name)
                                prospective_path = os.path.dirname(prospective_name)
                                prospective_basename = self.modify_char(prospective_basename,random.randint(6,9),self.random_char())
                                prospective_name = os.path.join(prospective_path,prospective_basename)
                                print(f"Let's try {prospective_name} instead...")
                        os.rename(original_name,prospective_name)
                        print(f"{original_name} >>> {prospective_name}")
                        # Check for existence of XMP sidecar and rename it
                        xmp = original_name+".xmp" 
                        if os.path.exists(xmp):
                                xmp2 = prospective_name+".xmp"
                                os.rename(xmp,xmp2)
                                print("Sidecar detected and renamed.")

                except FileNotFoundError:
                    print(f"Error: {old_filename} not found.")
                except Exception as e:
                    print(f"An error occurred: {e}")

        def modify_char(self, string, char_position, new_char):
            return string[:char_position] + new_char + string[char_position+1:]

        def random_char(self):
                return "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"[random.randint(0,35)]

        def b36_to_b10(self, char):
                char = char.upper()
                if '0' <= char <= '9':
                    return int(char)
                elif 'A' <= char <= 'Z':
                    return ord(char) - ord('A') + 10
                else:
                    return 0

        def b10_to_b36(self, num):
            if num < 0:
                raise ValueError("Input must be a non-negative integer")
            elif num == 0:
                return '0'

            digits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            result = ''
            
            while num:
                num, remainder = divmod(num, 36)
                result = digits[remainder] + result
            
            return result


        def __init__(self,root):
                self.root = root
                self.rank_var = StringVar()
                self.objects = []
                self.tempfiles = []
                self.image = [0,0,0,0,0,0]
                self.image_path = [0,0,0,0,0,0]
                self.image_count = 4
                self.initialization_rating = random.randint(1, 5)
                self.round_counter = 1
                self.image_counter = 0
                self.entry = None

                ###############################################
                #CONFIGURATION VARIABLES:
                self.images_directory = "C:/Users/yaywa/Desktop/Test/"
                self.canvas_width = 2550
                self.canvas_height = 1400
                ###############################################

                self.canvas = Canvas(root, width=self.canvas_width, height=self.canvas_height)
                self.canvas.pack()
                self.setup_canvas()

        def cleanup_temp_files(self):
                for temp_file in self.tempfiles:
                    os.remove(temp_file)
                self.tempfiles = []

        def cleanup_temp_files_and_quit(self):
                for temp_file in self.tempfiles:
                    os.remove(temp_file)
                self.tempfiles = []
                sys.exit()


if __name__ == "__main__":
    root = Tk()
    root.title("Random Image Rumble!")

    game = Game(root)

    root.mainloop()
