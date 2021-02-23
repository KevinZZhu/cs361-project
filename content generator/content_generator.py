# Kevin Zhu
# CS 361
# Content Generator Project

import sys
import re
import tkinter as tk
import wikipedia


def process_btn():
    """Event handler for when the generate button is clicked, gets the keywords from 2 entries"""
    # reset error message text
    lbl_message.config(text="")
    m_screen.update()

    # get keywords from entry boxes
    keyword1 = ent_key1.get()
    keyword2 = ent_key2.get()

    # find wikipedia page for keyword1, and find first paragraph that contains both keywords
    wiki_page = find_wiki_page(keyword1)
    if wiki_page == "":
        print("CG ERROR: No page found")
        lbl_message["text"] = "ERROR: No page matching keyword 1 found."
        return
    paragraph = find_paragraph(wiki_page, keyword1.lower(), keyword2.lower())
    if paragraph == "":
        print("CG ERROR: No paragraph found")
        lbl_message["text"] = "ERROR: No paragraph containing both keywords found."
        return

    # output keywords and paragraph to csv, and output paragraph to textbox
    create_output_csv(keyword1, keyword2, paragraph)
    lbl_message["text"] = "The generated paragraph has also been saved to cg_output.csv"
    txt_output.delete("1.0", tk.END)
    txt_output.insert("1.0", paragraph)
    return


def find_wiki_page(keyword: str) -> str:
    """Finds and returns the first wikipedia page matching the keyword, returns empty string if page not found"""
    # find and return first page matching keyword that is not a disambiguation page
    search_results = wikipedia.search(keyword)
    if len(search_results) == 0:
        return ""
    for result in search_results:
        try:
            wikipedia.page(search_results[0])
        except wikipedia.exceptions.DisambiguationError:
            continue
        return result
    # if a page is not found, return empty string
    return ""


def find_paragraph(page: str, keyword1: str, keyword2: str) -> str:
    """Finds and returns the first paragraph on the wikipedia page that contains both keywords, returns empty string if
    paragraph not found"""
    # split content of wiki page into paragraphs by new line, store each paragraph as a separate element in list
    # turn auto_suggest off to get the correct page
    page_content = wikipedia.page(page, auto_suggest=False).content.split('\n')

    # look for keywords in the paragraph
    for paragraph in page_content:
        # variables to track if keywords were found
        k1_found = False
        k2_found = False
        parsed_par = re.split(r'\W+', paragraph)
        # iterate through list of words, looking for both keywords
        for word in parsed_par:
            if word.lower() == keyword1:
                k1_found = True
            if word.lower() == keyword2:
                k2_found = True
            if k1_found and k2_found:
                return paragraph
    # return empty string if no matching paragraph is found
    return ""


def create_output_csv(keyword1: str, keyword2: str, paragraph: str):
    """Creates an output csv file with the keywords and a paragraph that contains the keywords"""
    # create or truncate cg_output.csv file
    with open("cg_output.csv", "w", encoding="utf-8") as out_file:
        out_file.write("input_keywords,output_content\n")
        out_file.write(f"{keyword1};{keyword2},\"{paragraph}\"")
    return


if __name__ == '__main__':
    if len(sys.argv) > 2:
        raise SystemExit(f"Usage: {sys.argv[0]} [filename] \n"
                         f"filename: (optional) name of input file")

    # if no input file specified, open gui
    if len(sys.argv) == 1:
        # set up tkinter screen
        m_screen = tk.Tk()
        m_screen.title("Content Generator")

        # allow grid cells to change size with window size
        m_screen.rowconfigure(0, weight=1, minsize=300)
        m_screen.columnconfigure(0, weight=1, minsize=225)
        m_screen.columnconfigure(1, weight=1, minsize=75)
        m_screen.columnconfigure(2, weight=1, minsize=450)

        # set up frames
        frm_keyword = tk.Frame(m_screen)
        frm_btn = tk.Frame(m_screen)
        frm_output = tk.Frame(m_screen)
        frm_keyword.grid(row=0, column=0)
        frm_btn.grid(row=0, column=1)
        frm_output.grid(row=0, column=2)

        # create labels and keyword entry boxes
        tk.Label(frm_keyword, text="Enter your keywords:").grid(row=0, columnspan=2, sticky="w", pady="2")
        tk.Label(frm_keyword, text="Keyword 1: ").grid(row=1)
        tk.Label(frm_keyword, text="Keyword 2: ").grid(row=2)
        ent_key1 = tk.Entry(frm_keyword)
        ent_key2 = tk.Entry(frm_keyword)
        lbl_message = tk.Label(frm_keyword, text="", height=3, justify="left", wraplength=200)
        ent_key1.grid(row=1, column=1)
        ent_key2.grid(row=2, column=1)
        lbl_message.grid(row=3, columnspan=2, sticky="w")

        # create generate button
        btn_generate = tk.Button(frm_btn, width=10, text="Generate", command=process_btn)
        btn_generate.pack()

        # create output label field
        lbl_output_description = tk.Label(frm_output, text="Output Content:").grid(row=0, column=0, sticky="n")
        txt_output = tk.Text(frm_output, width=50, height=15)
        txt_output.insert("1.0", "Your generated content will appear here")
        txt_output.grid(row=1, column=0)
        m_screen.mainloop()

    # if input specified, don't open gui and instead directly output to csv file
    else:
        with open(sys.argv[1], "r") as in_file:
            # skip first header line of csv
            in_file.readline()
            # keep line with keywords
            key_line = in_file.readline()
            # parse keywords from second line
            key1 = key_line.split(';')[0].rstrip()
            key2 = key_line.split(';')[1].rstrip()

            # call functions to find wiki page and function
            page_name = find_wiki_page(key1)
            if page_name == "":
                print("CG ERROR: No page found")
                sys.exit(1)
            wiki_par = find_paragraph(page_name, key1.lower(), key2.lower())
            if wiki_par == "":
                print("CG ERROR: No paragraph found")
                sys.exit(1)
            create_output_csv(key1, key2, wiki_par)
            print("Generated content saved to file cg_output.csv")
