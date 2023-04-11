from data.models.additional import Countries, Fits, Seasons, Sizes, Types
from data.models.fabrics import Fabrics
from data.models.main_tables import Boots, Hats, LowerBody, UpperBody
from data.models.simple_tables import Brims, Clasps, Collars, Heels, Lapels, Patterns, Sleeves, TrouserLengths
from data.models.wardrobe import Wardrobe
from data.models.user import User

FIELDS = {"Boots": ["id", "name", "season", "origin", "appearance_year",
                    "popularity_start", "popularity_end",
                    "heel", "clasp", "features", "picture", "deleted"],
          "Brims": ["id", "name", "picture", "deleted"],
          "Clasps": ["id", "name", "picture", "deleted"],
          "Collars": ["id", "name", "picture", "deleted"],
          "Countries": ["id", "name", "deleted"],
          "Fabrics": ["id", "name", "warmth", "washing", "picture", "deleted"],
          "Fits": ["id", "name", "deleted"],
          "Hats": ["id", "name", "season", "origin", "appearance_year",
                   "popularity_start", "popularity_end", "brim", "features", "picture", "deleted"],
          "Heels": ["id", "name", "picture", "deleted"],
          "Lapels": ["id", "name", "picture", "deleted"],
          "Lower_body": ["id", "name", "season", "origin", "appearance_year",
                         "popularity_start", "popularity_end", "fit",
                         "clasp", "length", "features", "picture", "deleted"],
          "Patterns": ["id", "name", "picture", "deleted"],
          "Seasons": ["id", "name", "deleted"],
          "Sizes": ["id", "name", "deleted"],
          "Sleeves": ["id", "name", "picture", "deleted"],
          "Trouser_lengths": ["id", "name", "picture", "deleted"],
          "Types": ["id", "name", "deleted"],
          "Upper_body": ["id", "name", "season", "origin", "appearance_year",
                         "popularity_start", "popularity_end", "sleeves", "clasp", "collar",
                         "hood", "lapels", "pockets", "fitted", "features", "picture", "deleted"],
          "Wardrobe": ["id", "type", "name", "color", "size",
                       "fabric", "pattern", "picture", "deleted", "owner"],
          "users": ["id", "email", "hashed_password", "name", "access", "deleted"]}

SIMPLE_TABLES = ["Boots", "Brims", "Clasps", "Collars",
                 "Countries", "Fabrics", "Fits", "Hats",
                 "Heels", "Lapels", "Lower_body", "Patterns",
                 "Seasons", "Sizes", "Sleeves", "Trouser_lengths",
                 "Types", "Upper_body"]

NO_PICTURE = ["Countries", "Fits", "Seasons", "Sizes", "Types"]

SIMPLE = ["Brims", "Clasps", "Collars", "Heels", "Lapels", "Patterns", "Sleeves", "Trouser_lengths"]

TABLES = ["Boots", "Brims", "Clasps", "Collars",
          "Countries", "Fabrics", "Fits", "Hats",
          "Heels", "Lapels", "Lower_body", "Patterns",
          "Seasons", "Sizes", "Sleeves", "Trouser_lengths",
          "Types", "Upper_body", "Wardrobe", "users"]

RELATIONS = {"brim": "Brims", "clasp": "Clasps", "collar": "Collars",
             "origin": "Countries", "fabric": "Fabrics", "fit": "Fits",
             "heel": "Heels", "lapels": "Lapels", "pattern": "Patterns",
             "season": "Seasons", "size": "Sizes", "sleeves": "Sleeves",
             "length": "Trouser_lengths", "type": "Types", "owner": "User"}

TABLES_CLASSES = {"Boots": Boots, "Brims": Brims, "Clasps": Clasps, "Collars": Collars,
                  "Countries": Countries, "Fabrics": Fabrics, "Fits": Fits, "Hats": Hats,
                  "Heels": Heels, "Lapels": Lapels, "Lower_body": LowerBody, "Patterns": Patterns,
                  "Seasons": Seasons, "Sizes": Sizes, "Sleeves": Sleeves, "Trouser_lengths": TrouserLengths,
                  "Types": Types, "Upper_body": UpperBody, "Wardrobe": Wardrobe, "users": User}
