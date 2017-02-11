import pickle
class Game_Object:

    def __init__(self, objects_coordinates,object_size):

        self.objects_coordinates = objects_coordinates
        self.object_size = object_size
        
    def add_an_object(self, object_coordinates):

        self.objects_coordinates.append(object_coordinates)

    def __getitem__(self,i):

        return self.objects_coordinates[i]

    def __setitem__(self,i,coordinates):

        self.objects_coordinates[i] = coordinates

    def __delitem__(self,i):

        self.objects_cordinates[i] = None

    def append(self,new_object):

        self.objects_coordinates.append(new_object)

    def save_game_object(self,file_name):

        with open(file_name,'wb') as save:

            pickle.dump(self,save)
            
    def load_game_object(file_name):

        self = 0
        with open(file_name,'rb') as save:

            self = pickle.load(save)
        return self
