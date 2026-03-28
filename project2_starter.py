# SI 201 HW4 (Library Checkout System)
# Your name:
# Your student id:
# Your email:
# Who or what you worked with on this homework (including generative AI like ChatGPT):
# If you worked with generative AI also add a statement for how you used it.
# e.g.:
# Asked ChatGPT for hints on debugging and for suggestions on overall code structure
#
# Did your use of GenAI on this assignment align with your goals and guidelines in your Gen AI contract? If not, why?
#
# --- ARGUMENTS & EXPECTED RETURN VALUES PROVIDED --- #
# --- SEE INSTRUCTIONS FOR FULL DETAILS ON METHOD IMPLEMENTATION --- #

from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
import requests  # kept for extra credit parity


# IMPORTANT NOTE:
"""
If you are getting "encoding errors" while trying to open, read, or write from a file, add the following argument to any of your open() functions:
    encoding="utf-8-sig"
"""


def load_listing_results(html_path) -> list[tuple]:
    """
    Load file data from html_path and parse through it to find listing titles and listing ids.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples containing (listing_title, listing_id)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    newlst = []
    with open(html_path, "r", encoding = "utf-8-sig") as file:
        this = file.read()
        soup = BeautifulSoup(this, "html.parser")
        all_divs = soup.find_all("div", class_ = "t1jojoys")
        for div in all_divs:
            id1 = div.get("id", None)
            name = div.get_text(strip=True)
            if re.match(r"^title_",id1) and name:
                id1 = id1[6:]
                newlst.append((name, id1))
        return newlst
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def get_listing_details(listing_id) -> dict:
    """
    Parse through listing_<id>.html to extract listing details.

    Args:
        listing_id (str): The listing id of the Airbnb listing

    Returns:
        dict: Nested dictionary in the format:
        {
            "<listing_id>": {
                "policy_number": str,
                "host_type": str,
                "host_name": str,
                "room_type": str,
                "location_rating": float
            }
        }
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    dic = {}
    dic[str(listing_id)] = {}
    path = "/Users/yibing_ronnieq/Documents/SI201/project2-w26-yibing/html_files"
    newpath = os.path.join(path, f"listing_{listing_id}.html")
    with open(newpath, "r", encoding="utf-8-sig") as file:
        this = file.read()
        soup = BeautifulSoup(this, "html.parser")
        #policy number
        poli = soup.find_all(class_="ll4r2nl")
        for i in poli:
            policy = re.match(r"^STR.+$", i.get_text(strip=True)) or re.match(r"^2022.+STR$", i.get_text(strip=True))
            if policy:
                    dic[str(listing_id)]["policy_number"] = policy.group()
            policy = re.match(r"^pending$", i.get_text(strip=True).lower())
            if policy:
                dic[str(listing_id)]["policy_number"] = "Pending"
            policy = re.match(r"^exempt$", i.get_text(strip=True).lower())
            if policy:
                dic[str(listing_id)]["policy_number"] = "Exempt"
            policy = None
        if dic[str(listing_id)].get("policy_number", None) == None:
            dic[str(listing_id)]["policy_number"] = "Pending"
        #superhost
        super_h = soup.find_all(class_="_1qsawv5")
        if super_h:
            for i in super_h:
                if re.match(r"^.+\sis\sa\sSuperhost$", i.get_text(strip=True)):
                    dic[str(listing_id)]["host_type"] = "Superhost"
        if dic[str(listing_id)].get("host_type", None) == None:
            dic[str(listing_id)]["host_type"] = "regular"
        #name and room
        n_r = soup.find_all(class_=["_14i3z6h", "hnwb2pb"])
        for i in n_r:
            theresult = re.match(r"^(.*)[Hh]osted\sby\s(.+)$", i.get_text(strip=True))
            if theresult:
                #name
                name = theresult.group(2)
                name = re.sub(r"(\b&\b) | (\band\b)", "And", name)
                dic[str(listing_id)]["host_name"] = name
                #room
                room = theresult.group(1)
                if re.search(r"\bprivate\b", room.lower().strip()):
                    dic[str(listing_id)]["room_type"] = "Private Room"
                elif re.search(r"\bshared\b", room.lower().strip()):
                    dic[str(listing_id)]["room_type"] = "Shared Room"
                else:
                    dic[str(listing_id)]["room_type"] = "Entire Room"
                
        #rating
        lst = soup.find(class_="_12si43g")
        if lst:
            a = lst.get_text(strip=True)
            dic[str(listing_id)]["location_rating"] = float(a[0:3])
        else:
            dic[str(listing_id)]["location_rating"] = float(0.0)
        return dic
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def create_listing_database(html_path) -> list[tuple]:
    """
    Use prior functions to gather all necessary information and create a database of listings.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples. Each tuple contains:
        (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    lst = load_listing_results(html_path)
    returnlst = []
    for i in lst:
        dic = get_listing_details(i[1])
        print(dic)
        returnlst.append((i[0], i[1], dic[i[1]]["policy_number"], dic[i[1]]["host_type"], dic[i[1]]["host_name"], dic[i[1]]["room_type"], dic[i[1]]["location_rating"]))
    return returnlst
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def output_csv(data, filename) -> None:
    """
    Write data to a CSV file with the provided filename.

    Sort by Location Rating (descending).

    Args:
        data (list[tuple]): A list of tuples containing listing information
        filename (str): The name of the CSV file to be created and saved to

    Returns:
        None
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    with open(filename, "w", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerrow(["Listing Title", "Listing ID", "Policy Number", 
               "Host Type", "Host Name", "Room Type", "Location Rating"])
        lst = sorted(data, key=lambda x:x[6], reverse=True)
        writer.writerows(lst)
    
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def avg_location_rating_by_room_type(data) -> dict:
    """
    Calculate the average location_rating for each room_type.

    Excludes rows where location_rating == 0.0 (meaning the rating
    could not be found in the HTML).

    Args:
        data (list[tuple]): The list returned by create_listing_database()

    Returns:
        dict: {room_type: average_location_rating}
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def validate_policy_numbers(data) -> list[str]:
    """
    Validate policy_number format for each listing in data.
    Ignore "Pending" and "Exempt" listings.

    Args:
        data (list[tuple]): A list of tuples returned by create_listing_database()

    Returns:
        list[str]: A list of listing_id values whose policy numbers do NOT match the valid format
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


# EXTRA CREDIT
def google_scholar_searcher(query):
    """
    EXTRA CREDIT

    Args:
        query (str): The search query to be used on Google Scholar
    Returns:
        List of titles on the first page (list)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


class TestCases(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.search_results_path = os.path.join(self.base_dir, "html_files", "search_results.html")

        self.listings = load_listing_results(self.search_results_path)
        self.detailed_data = create_listing_database(self.search_results_path)

    def test_load_listing_results(self):
        # TODO: Check that the number of listings extracted is 18.
        # TODO: Check that the FIRST (title, id) tuple is  ("Loft in Mission District", "1944564").
        pass

    def test_get_listing_details(self):
        html_list = ["467507", "1550913", "1944564", "4614763", "6092596"]

        # TODO: Call get_listing_details() on each listing id above and save results in a list.

        # TODO: Spot-check a few known values by opening the corresponding listing_<id>.html files.
        # 1) Check that listing 467507 has the correct policy number "STR-0005349".
        # 2) Check that listing 1944564 has the correct host type "Superhost" and room type "Entire Room".
        # 3) Check that listing 1944564 has the correct location rating 4.9.
        pass

    def test_create_listing_database(self):
        # TODO: Check that each tuple in detailed_data has exactly 7 elements:
        # (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)

        # TODO: Spot-check the LAST tuple is ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8).
        pass

    def test_output_csv(self):
        out_path = os.path.join(self.base_dir, "test.csv")

        # TODO: Call output_csv() to write the detailed_data to a CSV file.
        # TODO: Read the CSV back in and store rows in a list.
        # TODO: Check that the first data row matches ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"].

        os.remove(out_path)

    def test_avg_location_rating_by_room_type(self):
        # TODO: Call avg_location_rating_by_room_type() and save the output.
        # TODO: Check that the average for "Private Room" is 4.9.
        pass

    def test_validate_policy_numbers(self):
        # TODO: Call validate_policy_numbers() on detailed_data and save the result into a variable invalid_listings.
        # TODO: Check that the list contains exactly "16204265" for this dataset.
        pass


def main():
    detailed_data = create_listing_database(os.path.join("html_files", "search_results.html"))
    output_csv(detailed_data, "airbnb_dataset.csv")


if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)