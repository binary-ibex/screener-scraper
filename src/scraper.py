import argparse
from utils import generate_excel, link_extractor



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file", help="flag to specify the links are put in data.txt file", action="store_true")
    args = parser.parse_args()
    if args.file:
        with open('data.txt', 'r') as fd:
            data = fd.read()
    else:
        data = input("Enter the link => ")
    links = link_extractor(data)
    if links:
        generate_excel(links)
    else:
        print("No links found")





    

