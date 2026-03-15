from textnode import *
from htmlnode import *
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    split_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            split_list.append(node)
            continue
        temp = node.text.split(delimiter)
        
        if len(temp) % 2 == 0:
            raise Exception("no closing delimiter")
        for i in range(len(temp)):
            if len(temp[i]) != 0:
                if i % 2 != 0:
                    split_list.append(TextNode(temp[i], text_type))
                else:
                    split_list.append(TextNode(temp[i], TextType.TEXT))
    return split_list


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_node = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_node.append(node)
            continue
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_node.append(TextNode(node.text, TextType.TEXT))
            continue
        remaining_text = node.text
        for image in images:
            sections = remaining_text.split(f"![{image[0]}]({image[1]})", 1)
            if sections[0] != "":
                new_node.append(TextNode(sections[0], TextType.TEXT))
            new_node.append(TextNode(image[0], TextType.IMAGE, image[1]))
            remaining_text = sections[1]
        if remaining_text != "":
            new_node.append(TextNode(remaining_text, TextType.TEXT))
    return new_node


def split_nodes_link(old_nodes):
    new_node = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_node.append(node)
            continue
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_node.append(TextNode(node.text, TextType.TEXT))
            continue
        remaining_text = node.text
        for link in links:
            sections = remaining_text.split(f"[{link[0]}]({link[1]})", 1)
            if sections[0] != "":
                new_node.append(TextNode(sections[0], TextType.TEXT))
            new_node.append(TextNode(link[0], TextType.LINK, link[1]))
            remaining_text = sections[1]
        if remaining_text != "":
            new_node.append(TextNode(remaining_text, TextType.TEXT))
    return new_node

def text_to_textnodes(text):
    node = [TextNode(text, TextType.TEXT)]
    split_image = split_nodes_image(node)
    split_link = split_nodes_link(split_image)
    delimiters = {TextType.BOLD: "**", TextType.ITALIC: "_", TextType.CODE: "`"}
    for type in delimiters:
        new_nodes = split_nodes_delimiter(split_link, delimiters[type], type)
        split_link = new_nodes
    return new_nodes

