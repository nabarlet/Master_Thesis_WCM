from movement_path_playlist import MovementPathPlaylist
from zone_path_playlist import ZonePathPalylist
from path_playlist import PathPlaylist





class PlaylistGenerator:
    def __init__ (self, type, num=10):
        self.type=type
        self.count=num
        self.stats=[]
        
      
    def generate(self):
        for n in range(self.count):
            try:
                pl = self.type.create_random_args()
                self.stats.append(pl.calc_stats())
            except as e:
                print("Playlist generation failed: %s" % (str(e), file = sys.stderr)
            
