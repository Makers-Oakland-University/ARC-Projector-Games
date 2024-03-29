#!/usr/bin/env python3

import sys

class LocationParser(): 
    def __init__(self, field_width_pixels = 1920, field_height_pixels =1080, field_width_meters = 4.2, field_height_meters = 2.5, debug_print=False, lidar_file_path_file = "lidar_input_file_location.txt"):
        """LOCATION PARSER, if you're creating new games copy this entire class and the two lines directly after it
            you need to indicate the location of the file that is generated by the ROS system. This class will map that position to the 
            pixel coordinates and give you a list of the read points

        Args:
            field_width_pixels (int, optional): the width of the field read by the lidar through ROS, this can be found by looking in PolyGen or by viewing it in RVIZ. Defaults to 1920.
            field_height_pixels (int, optional): height of the field read by the lidar through ROS. Defaults to 1080.
            field_width_meters (int, optional): resolution width of the output game . Defaults to 4.
            field_height_meters (int, optional): resolution height of the output game . Defaults to 2.
            debug_print (bool, optional): prints parsed information to the terminal for debugging when True. Defaults to False.
            lidar_file_path_file (str, optional): Location of the file which points to the 'lidar_output.txt' file that is going to be used. If using the movement_simulation.py file then place the file path of the lidar_output.txt file that is in the repo folder. . Defaults to "lidar_input_file_location.txt".
        """
        try:
            with open(lidar_file_path_file, 'r') as f: 
                self.file_location = f.read().replace("\n", "").replace("\r", "")
                print("ARC-Projector-Games LocationParser operating on lidar position information located in \"%s\"" % self.file_location)
                try:
                    with open(self.file_location, 'r') as f2: 
                        data = f2.read()
                        print("Found lidar_output.txt file")
                except FileNotFoundError: 
                    print("information contained in '%s' does not point to a usable lidar_output.txt file, double check the path entered into this file and re-run the program" % lidar_file_path_file)
                    sys.exit()

        except FileNotFoundError: 
            with open(lidar_file_path_file, 'w') as f: 
                f.write("")

            #big long help string to explain whats gone wrong 
            print("LocationParser was unable to find the location file pointing to 'lidar_output.txt' a pointer file was created in the same folder as this python script with the name '%s'" % lidar_file_path_file)
            print("Please open the '%s' text file and input the path to the lidar_output.txt data file used to communicate tracked objects to the python games" % lidar_file_path_file)
            print("if you are on linux you can find the full path to a file by right clicking on the folder and selecting 'open in terminal' then typing 'readlink -f <your file>")
            print("Example: ")
            print("If you were running the games using the movement_simulation.py file and the repo were cloned to your documents (on linux) then the full contents of the '%s' file should be:" % lidar_file_path_file)
            print("/home/matthew/Documents/ARC-Projector-Games/lidar_output.txt")
            print("")
            print("Note: LocationParser was unable to obtain input file, the program will now exit")
            print("Please read the above information to correct this problem")
            sys.exit()

        self.debug_print = debug_print

        #size of the polygon that is displayed in rviz
        self.field_width_meters = field_width_meters
        self.field_height_meters = field_height_meters

        #resolution of the game
        self.field_width_pixels = field_width_pixels
        self.field_height_pixels = field_height_pixels


    def getPositions(self): 
        """Reads the lidar_output.txt file and parses the file contents into an array of positions 

        Returns:
            List (Tuple (float)): positions contained in the lidar_output.txt file generated by the ROS lidar system.
        """

        #open the file in read mode
        with open(self.file_location, 'r') as f:

            #read file as string
            position_string = f.read()

            #list of positions that we will be returning 
            position_list = []

            #split the read in string by line, this gives us one string per line of text generated by the ROS system
            xy_position_lines= position_string.split('\n')

            #loop through each line of text
            for a in xy_position_lines: 

                #now we do the conversion from string to float
                #the conversion is read_value * output_unit/input_unit 
                #the ros system publishes locations in meters, based on the field size we can map it to a position with this. 
                try:
                    position = (float(a.split(',')[1]) * self.field_width_pixels/self.field_width_meters, float(a.split(',')[0]) * self.field_height_pixels/self.field_height_meters)        

                    #if we were able to parse the point, add it to the list
                    position_list.append(position)
                except IndexError: 
                    if(self.debug_print):
                        print("Failed to parse position from \'%s\'" % a)
                    else:
                        pass
            
            #terminal spam, can be commented out
            if(self.debug_print):
                print(position_list)
           
            # return positions
            return position_list
