import weatherrouting
import math
import json

def intersects(s0,s1):
    dx0 = s0[1][0]-s0[0][0]
    dx1 = s1[1][0]-s1[0][0]
    dy0 = s0[1][1]-s0[0][1]
    dy1 = s1[1][1]-s1[0][1]
    p0 = dy1*(s1[1][0]-s0[0][0]) - dx1*(s1[1][1]-s0[0][1])
    p1 = dy1*(s1[1][0]-s0[1][0]) - dx1*(s1[1][1]-s0[1][1])
    p2 = dy0*(s0[1][0]-s1[0][0]) - dx0*(s0[1][1]-s1[0][1])
    p3 = dy0*(s0[1][0]-s1[1][0]) - dx0*(s0[1][1]-s1[1][1])
    return (p0*p1<=0) & (p2*p3<=0)

class mock_point_validity:
    def __init__(self, track, factor=4, mode = 'island'):
        self.mode = mode
        self.track = track
        self.mean_point = ((track[0][0]+track[1][0])/2,(track[0][1]+track[1][1])/2)
        self.distance = math.dist(track[0], track[1])
        self.mean_island = weatherrouting.utils.pointDistance(*(track[0]+track[1]))/factor
        #self.north_land = [[self.mean_point[0]+self.distance/20,self.mean_point[1]],[self.track[1][0]+self.distance,self.track[1][1]]]
        #self.south_land = [[self.mean_point[0]-self.distance/20,self.mean_point[1]],[self.track[0][0]-self.distance,self.track[0][1]]]
        self.north_land = [[self.mean_point[0],self.mean_point[1]+self.distance/20],[self.track[1][0],self.track[1][1]+self.distance]]
        self.south_land = [[self.mean_point[0],self.mean_point[1]-self.distance/20],[self.track[0][0],self.track[0][1]-self.distance]]
        self.geojson_default = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "id": 1,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            self.mean_point[1],
                            self.mean_point[0]
                        ]
                    },
                    "properties": {"strait":"mean"}
                },
                {
                    "type": "Feature",
                    "id": 1,
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [
                            [self.north_land[0][1],self.north_land[0][0]],
                            [self.north_land[1][1],self.north_land[1][0]]
                        ]
                    },
                    "properties": {"strait":"north"}
                },

                {
                    "type": "Feature",
                    "id": 1,
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [
                            [self.south_land[0][1],self.south_land[0][0]],
                            [self.south_land[1][1],self.south_land[1][0]]
                        ]
                    },
                    "properties": {"strait":"south"}
                }
            ]
        }
        if mode == "strait":
            return
            print (json.dumps(self.geojson_default))
            

    def point_validity(self, y, x):
        if self.mode == "island":
            if weatherrouting.utils.pointDistance(x,y,*(self.mean_point)) < self.mean_island:
                return False
            else:
                return True

    def line_validity(self, y1, x1, y2, x2):
        if self.mode == "island":
            if weatherrouting.utils.pointDistance(x1,y2,*(self.mean_point)) < self.mean_island:
                return False
            else:
                return True
        elif self.mode == "strait":
            track = [[y1,x1],[y2,x2]]
            if intersects(track,self.north_land) or intersects(track,self.south_land):
                return False
            else:
                return True