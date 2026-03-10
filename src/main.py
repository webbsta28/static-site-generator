from textnode import *



def main():
    dummy = TextNode("This is some anchor text", TextType("[anchor text](url)"), "https://www.boot.dev")
    print(dummy)

main()