from argparse import ArgumentParser
from typing import List, Optional, Sequence
import requests
import json
import html
import xml.etree.ElementTree as ET

from unicodedata import category


class UnhandledException(Exception):
    pass


def parse_xtml_to_dict(xml: str) -> dict[str, any]:
    """
    Parses the XML string and returns a dictionary, only including keys for
    tags that are actually present in the feed.
    """

    def _get_text(element, tag):
        node = element.find(tag)
        if node is not None and node.text:
            return html.unescape(node.text.strip())
        return None

    def _get_all_texts(element, tag):
        nodes = element.findall(tag)
        return [html.unescape(node.text.strip()) for node in nodes if node.text]

    try:
        root = ET.fromstring(xml)
    except ET.ParseError as e:
        raise UnhandledException(e)

    channel = root.find('channel')
    if channel is None:
        raise UnhandledException('Channel not found')

    # Start with an empty dictionary for the final result.
    parsed_data = {}

    # Dynamically add channel-level data if it exists.
    channel_tags = ['title', 'link', 'lastBuildDate', 'pubDate', 'language', 'managingEditor', 'description']
    for tag in channel_tags:
        value = _get_text(channel, tag)
        if value is not None:
            parsed_data[tag] = value

    # Handle multi-value channel category. Use the singular key 'category'.
    channel_categories = _get_all_texts(channel, 'category')
    if channel_categories:
        parsed_data['category'] = channel_categories

    # --- This is the corrected item parsing logic ---
    items_list = []

    # Use a SINGLE loop to process all items.
    for item_element in channel.findall('item'):
        # Create an empty dictionary for each individual item.
        item_dict = {}

        # Define the tags to look for in an item.
        item_tags = ['title', 'author', 'pubDate', 'link', 'description']

        # Loop through the single-value tags and add them if they exist.
        for tag in item_tags:
            value = _get_text(item_element, tag)
            if value is not None:
                item_dict[tag] = value

        # Handle the item's categories. Use the singular key 'category'.
        item_categories = _get_all_texts(item_element, 'category')
        if item_categories:
            item_dict['category'] = item_categories

        # If we found any data for this item, add its dictionary to our list.
        if item_dict:
            items_list.append(item_dict)

    # After checking all items, add the list to our main dictionary
    # only if the list is not empty.
    if items_list:
        parsed_data['items'] = items_list

    return parsed_data


def _format_json(data: dict) -> List[str]:
    return [json.dumps(data, indent=2)]


def _format_console(data: dict) -> List[str]:
    output = []

    if data.get("title"):
        output.append(f'Feed: {data["title"]}')
    if data.get("link"):
        output.append(f'Link: {data["link"]}')
    if data.get("lastBuildDate"):
        output.append(f'Last Build Date: {data["lastBuildDate"]}')
    if data.get("pubDate"):
        output.append(f'Publish Date: {data["pubDate"]}')
    if data.get("language"):
        output.append(f'Language: {data["language"]}')
    if data.get("category"):
        output.append(f'Categories: {", ".join(data["category"])}')
    if data.get("managingEditor"):
        output.append(f'Editor: {data["managingEditor"]}')
    if data.get("description"):
        output.append(f'Description: {data["description"]}')



    if data.get("items"):
        output.append("")



    items = data.get("items", [])
    for index, item in enumerate(items):
        if item.get("title"):
            output.append(f"Title: {item['title']}")
        if item.get("author"):
            output.append(f"Author: {item['author']}")
        if item.get("pubDate"):
            output.append(f"Published: {item['pubDate']}")
        if item.get("link"):
            output.append(f"Link: {item['link']}")
        if item.get("category"):
            output.append(f"Categories: {', '.join(item['category'])}")
        if item.get("description"):
            output.append("")
            output.append(item["description"])

        if index < len(items) - 1:
            output.append("")
            output.append("")

    return output

def rss_parser(
    xml: str,
    limit: Optional[int] = None,
    json: bool = False,
) -> List[str]:

    parsed_data = parse_xtml_to_dict(xml)


    if limit is not None and 'items' in parsed_data:
        parsed_data['items'] = parsed_data['items'][:limit]

    if json:
        return _format_json(parsed_data)
    else:
        return _format_console(parsed_data)





def main(argv: Optional[Sequence] = None):
    """
    The main function of your task.
    """
    parser = ArgumentParser(
        prog="rss_reader",
        description="Pure Python command-line RSS reader.",
    )
    parser.add_argument("source", help="RSS URL", type=str, nargs="?")
    parser.add_argument(
        "--json", help="Print result as JSON in stdout", action="store_true"
    )
    parser.add_argument(
        "--limit", help="Limit news topics if this parameter provided", type=int
    )

    args = parser.parse_args(argv)


    if not args.source:
        print("Error: A source URL is required.")
        parser.print_help()
        return 1

    xml = requests.get(args.source).text
    try:
        # Step 1: Try to make the web request
        response = requests.get(args.source)
        # Step 2: Check if the request was successful (e.g., not a 404 or 500 error)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Step 3A: If the request fails, print a clear error and exit
        print(f"Error fetching the URL: {e}")
        return 1
    else:
        # Step 3B: ONLY if the request was successful, proceed
        xml = response.text
        try:
            output_lines = rss_parser(xml, args.limit, json=args.json)
            print("\n".join(output_lines))
            return 0
        except UnhandledException as e:
            print(f"Error processing the feed: {e}")
            return 1


if __name__ == "__main__":
    main()
