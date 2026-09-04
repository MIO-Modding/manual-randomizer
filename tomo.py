# This program is called Tomo because it's the randomizer
# intended for use by people given the 'Manual' nature.
# If it was the real rando it would be called Samsk,
# and if it was a poptracker it would be called Shii.

import json
import sys
import os

def sanitize(name):
    return name.replace(":", ">").replace("|", ",")

def get_items(items):
    return list(map(item_world_to_manual, items))

def item_world_to_manual(item):
    classification = item["classification"]
    if item["saveEntry"]:
        prefix, postfix = item["saveEntry"].split(":", 1)
        name = f"{item["saveEntry"]} ({item["name"]})"
    else:
        prefix = "MISC"
        postfix = "N/A"
        name = f"{item["name"]}"

    # Specific categories to group items for logic
    # and yaml settings
    category = [
        sanitize(prefix)
    ]
    world_item_name = item["name"]
    if world_item_name.startswith("Candle"):
        category.append("candles")
    if world_item_name.startswith("Fragmented Serial Number"):
        category.append("serial_numbers")
    if world_item_name.startswith("Old Core"):
        category.append("old_cores")
    if world_item_name == "Slash":
        category.append("slash")
    
    return {
        "name": sanitize(name),
        "id": item["id"],
        "vanilla_item": item["name"],
        "category": category,
        "filler": classification == 0,
        "progression": classification & 1 > 0,
        "usefull": classification & 2 > 0,
        "trap": classification & 4 > 0,
        "progression_skip_balancing": classification & 9 == 9,
    }

def get_locations(locations, catalog):
    location_lambda = lambda location: location_world_to_manual(location, catalog)
    victory = [
        {
            "name": "Ati Ending",
            "region": "HUB_hub_central",
            "category": "Victory",
            "requires": "|Ati Defeated|",
            "victory": True
        },
        {
            "name": "Shii Ending",
            "region": "GA_roof_core",
            "category": "Victory",
            "requires": "|Shii Defeated|",
            "victory": True
        },
    ]
    return list(map(location_lambda, locations)) + victory

def location_world_to_manual(location, catalog):
    split = location["roomName"].split("_")
    if len(split)<3:
        prefix = location["roomName"]
    else:
        prefix = "_".join(split[:2])
    item_name = location["vanillaItem"]["itemName"]
    # Special cases for locations which would otherwise
    # be duplicates
    if location["roomName"] == "GA_bou_up_F1" and \
                item_name == "Crystallized Nacre":
        if location["name"].endswith("Above a Door"):
            item_name += "_upper"
        else:
            item_name += "_lower"
    if location["roomName"] == "LQ_under_mast_C1" and \
                item_name == "Crystallized Nacre":
        if location["name"].endswith("Right"):
            item_name += "_right"
        else:
            item_name += "_left"

    return {
        "name":sanitize(f"{location["roomName"]}--({item_name})"),
        "region":sanitize(location["roomName"]),
        "category": [sanitize(prefix)],
        "requires": parse_requirements(location["requirements"], catalog),
        "hint_entrance": location["name"],
        # Category includes room name. Name is vanilla item
        # Maybe put the descriptive text as hint_entrance,
        # rather than in the long name
    }

def get_events(events, catalog):
    event_lambda = lambda event: event_world_to_manual(event, catalog)
    canReachRegions = [
        {
            "name": sanitize(region),
            "region": sanitize(region),
        } for region in [
            "HUB_hub_asc",
            "LQ_city_mast_F0",
            "ST_tube_factory_P9",
            "ST_tube_vanilla_C4"
        ]
    ]
    extraEvents = [ # There should be a way to do this without the events...
        {
            "name": "true",
        },
        {
            "name": "false",
            "requires": "|false|"
        }
    ]
    return list(map(event_lambda, events)) + canReachRegions + extraEvents

def event_world_to_manual(event, catalog):
    category = []
    item_name = event["itemName"]
    if item_name in ["Find " + lad for lad in ["Tan", "Cos", "Sin", "Rad"]]:
        category.append("scraplings")
    return {
        "name":sanitize(event["itemName"]),
        "region":sanitize(event["roomName"]),
        # "visible":True,
        "category": category,
        "requires": parse_requirements(event["requirements"], catalog),
        # There should probably be the actual save flag somewhere
        # in the name of the event?
    }


def get_regions(rooms, transitions, catalog):
    out = dict(map(room_to_region, rooms))
    for t in transitions:
        fr = t["fromName"]
        to = t["toName"]
        reqs = parse_requirements(t["requirements"], catalog)
        out[fr]["exit_requires"][to] = reqs
    # TODO Let Starting Room be dynamically chosen in the yaml
    out["ST_security_fall_P1"]["starting"] = True
    return out

def room_to_region(room):
    return (sanitize(room["name"]), {
        "connects_to": [
            sanitize(t["linkedRoomName"]) for t in room["transitions"]
        ],
        "exit_requires": dict()
    })

def parse_requirements(reqs, catalog, OptAll=True):
    if not reqs: return ""
    if OptAll: return f"OptAll({parse_requirements(reqs,catalog,False)})"
    match reqs["rule"]:
        case "Has":
            item_name = reqs["args"]["item_name"]
            if item_name in catalog:
                if item_name == "Slash":
                    return f"(|{catalog["Slash"]}| OR {{YamlDisabled(Randomize Slash)}})"
                return f"|{catalog[item_name]}|"
            else:
                return f"|{sanitize(item_name)}|"
        case "Or":
            return f"({" OR ".join(
                map(lambda req: parse_requirements(req, catalog, False),
                    reqs["children"])
            )})"
        case "And":
            return f"({" AND ".join(
                map(lambda req: parse_requirements(req, catalog, False),
                    reqs["children"])
            )})"
        case "HasFromListUnique":
            # first_item = reqs["args"]["item_names"][0]
            # return f"|{catalog[first_item] if first_item in catalog else sanitize(first_item)}|"
            match reqs["args"]["item_names"][0]:
                case "Find Tan": group = "scraplings"
                case "Find Rad": group = "scraplings"
                case "Candle (#1)": group = "candles"
                case "Fragmented Serial Number (#1)": group = "serial_numbers"
                case "Old Core (#1)": group = "old_cores"
                case _: print(f"Unknown ListUnique requirement: {reqs}")
            return f"|@{group}:{reqs["args"]["count"]}|"
        case "False_":
            return "|false|"
        case "True_":
            return "|true|"
        case "CanReachRegion":
            return f"|{sanitize(reqs["args"]["region_name"])}|"
        case _:
            print(f"Unknown rule {reqs["rule"]}")
            return ""
    return ""

def make_catalog(items):
    return dict([(item["vanilla_item"],item["name"]) for item in items])

def write_once(prefix, name, object):
    with open(os.path.join(prefix, name), 'w') as f:
        json.dump(object, indent=4, fp=f)

def write_all(world, prefix):
    with open(world) as f:
        data = json.load(f)
    rooms = data["rooms"]
    locations = data["locations"]
    transitions = data["transitions"]
    items = data["items"]
    events = data["events"]

    manual_items = get_items(items)
    catalog = make_catalog(manual_items)
    manual_locations = get_locations(locations, catalog)

    manual_regions = get_regions(rooms, transitions, catalog)
    manual_events = get_events(events, catalog)
    for object, file in [
            (manual_items, "items.json"),
            (manual_locations, "locations.json"),
            (manual_regions, "regions.json"),
            (manual_events, "events.json"),
        ]:
        write_once(prefix, file, object)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "-h":
        print("usage: tomo.py [world.json] [manual_mio_samwell/data/]")
    dir = os.path.dirname(sys.argv[0])
    if len(sys.argv) < 2:
        world = os.path.join(dir, "world.json")
    else:
        world = os.path.join(dir, sys.argv[1])
    if len(sys.argv) < 3:
        path = os.path.join(dir, "manual_mio_samwell/data")
    else:
        path = os.path.join(dir, sys.argv[2])
    write_all(world,path)


if __name__ == "__main__": main()

with open("world.json") as f:
    data = json.load(f)
rooms = data["rooms"]
locations = data["locations"]
transitions = data["transitions"]
items = data["items"]
events = data["events"]

manual_items = get_items(items)
catalog = make_catalog(manual_items)
manual_locations = get_locations(locations, catalog)
manual_regions = get_regions(rooms, transitions, catalog)
# TODO Set starting room
# And goals for that matter....
manual_events = get_events(events, catalog)
