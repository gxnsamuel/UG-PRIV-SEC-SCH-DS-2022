import json
from collections import defaultdict

def process_schools_to_hierarchy(input_json_path, output_json_path):
    # Read data from the initial JSON file
    with open(input_json_path, 'r') as infile:
        schools_data = json.load(infile)

    # Dictionary to hold hierarchical structure
    hierarchy = {
        "title": "Private Secondary Schools in Uganda",
        "description": "List of all private secondary schools in Uganda as of 28th March 2022, organized by District, County, Subcounty, and Parish",
    }

    total_schools = len(schools_data)

    # Group data into the hierarchical structure
    district_dict = defaultdict(lambda: {
        "title": "",
        "total_schools": 0,
        "total_counties": 0,
        "total_subcounties": 0,
        "total_parishes": 0,
        "counties": defaultdict(lambda: {
            "title": "",
            "total_schools": 0,
            "total_subcounties": 0,
            "total_parishes": 0,
            "subcounties": defaultdict(lambda: {
                "title": "",
                "total_schools": 0,
                "total_parishes": 0,
                "parishes": defaultdict(lambda: {
                    "title": "",
                    "total_schools": 0,
                    "schools": []
                })
            })
        })
    })

    # Build hierarchy from flat data
    for school in schools_data:
        district = school.get("DISTRICT", "Unknown")
        county = school.get("COUNTY", "Unknown")
        subcounty = school.get("SUBCOUNTY", "Unknown")
        parish = school.get("PARISH", "Unknown")
        school_name = school.get("SCHOOL NAME", "Unknown")

        district_entry = district_dict[district]
        district_entry["title"] = district
        district_entry["total_schools"] += 1

        county_entry = district_entry["counties"][county]
        county_entry["title"] = county
        county_entry["total_schools"] += 1

        subcounty_entry = county_entry["subcounties"][subcounty]
        subcounty_entry["title"] = subcounty
        subcounty_entry["total_schools"] += 1

        parish_entry = subcounty_entry["parishes"][parish]
        parish_entry["title"] = parish
        parish_entry["total_schools"] += 1
        parish_entry["schools"].append(school_name)

    # Convert defaultdict to a normal dictionary and calculate summary stats
    total_districts = len(district_dict)

    total_counties = 0
    total_subcounties = 0
    total_parishes = 0

    for district, district_entry in district_dict.items():
        district_entry["counties"] = list(district_entry["counties"].values())
        district_entry["total_counties"] = len(district_entry["counties"])
        total_counties += district_entry["total_counties"]

        for county_entry in district_entry["counties"]:
            county_entry["subcounties"] = list(county_entry["subcounties"].values())
            county_entry["total_subcounties"] = len(county_entry["subcounties"])
            total_subcounties += county_entry["total_subcounties"]

            for subcounty_entry in county_entry["subcounties"]:
                subcounty_entry["parishes"] = list(subcounty_entry["parishes"].values())
                subcounty_entry["total_parishes"] = len(subcounty_entry["parishes"])
                total_parishes += subcounty_entry["total_parishes"]

        district_entry["total_subcounties"] = sum(county["total_subcounties"] for county in district_entry["counties"])
        district_entry["total_parishes"] = sum(county["total_parishes"] for county in district_entry["counties"])

    hierarchy["districts"] = list(district_dict.values())

    # Computing averages
    avg_schools_per_district = total_schools / total_districts if total_districts else 0
    avg_schools_per_county = total_schools / total_counties if total_counties else 0
    avg_schools_per_subcounty = total_schools / total_subcounties if total_subcounties else 0
    avg_schools_per_parish = total_schools / total_parishes if total_parishes else 0

    avg_schools_per_county_on_district = avg_schools_per_county / avg_schools_per_district if avg_schools_per_district else 0
    avg_schools_per_subcounty_on_district = avg_schools_per_subcounty / avg_schools_per_district if avg_schools_per_district else 0
    avg_schools_per_parish_on_district = avg_schools_per_parish / avg_schools_per_district if avg_schools_per_district else 0

    avg_schools_per_subcounty_on_county = avg_schools_per_subcounty / avg_schools_per_county if avg_schools_per_county else 0
    avg_schools_per_parish_on_county = avg_schools_per_parish / avg_schools_per_county if avg_schools_per_county else 0

    avg_schools_per_parish_on_subcounty = avg_schools_per_parish / avg_schools_per_subcounty if avg_schools_per_subcounty else 0

    # Add metrics to hierarchy
    hierarchy.update({
        "total_schools": total_schools,
        "total_districts": total_districts,
        "total_counties": total_counties,
        "total_subcounties": total_subcounties,
        "total_parishes": total_parishes,
        "average_schools_per_district": avg_schools_per_district,
        "average_schools_per_county": avg_schools_per_county,
        "average_schools_per_subcounty": avg_schools_per_subcounty,
        "average_schools_per_parish": avg_schools_per_parish,
        "average_schools_per_county_on_district": avg_schools_per_county_on_district,
        "average_schools_per_subcounty_on_district": avg_schools_per_subcounty_on_district,
        "average_schools_per_parish_on_district": avg_schools_per_parish_on_district,
        "average_schools_per_subcounty_on_county": avg_schools_per_subcounty_on_county,
        "average_schools_per_parish_on_county": avg_schools_per_parish_on_county,
        "average_schools_per_parish_on_subcounty": avg_schools_per_parish_on_subcounty
    })

    # Write the new structure to JSON
    with open(output_json_path, 'w') as outfile:
        json.dump(hierarchy, outfile, indent=4)

# Execute the organization process
if __name__ == "__main__":
    input_json_path = "private_schools_sorted_by_district.json"
    output_json_path = "organized_private_schools.json"

    try:
        process_schools_to_hierarchy(input_json_path, output_json_path)
        print(f"Data organized and saved to {output_json_path}")
    except Exception as e:
        print(f"An error occurred: {e}")