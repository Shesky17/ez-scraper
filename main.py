from tkinter import *
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


# =============================== window ===============================
window = Tk()
window.title("EZ-Scrape")
window.geometry("640x480")
upperFrame = Frame(window)
upperFrame.pack(side=TOP, fill=X, expand=TRUE)
upperLeft = Frame(upperFrame)
upperLeft.pack(side=LEFT)
upperRight = Frame(upperFrame)
upperRight.pack(side=RIGHT, fill=X, expand=TRUE)

centerFrame = Frame(window)
centerFrame.pack(fill=BOTH, expand=True)
lowerFrame = Frame(window)
lowerFrame.pack(side=BOTTOM)

# =============================== labels ===============================
lbl_url = Label(upperLeft, text="Enter url: ", font=("Arial Bold", 12))
lbl_url.pack(side=TOP, padx=50, pady=(0, 5))

lbl_tag = Label(upperLeft, text="Tag you want to scrape: ", font=("Arial Bold", 12))
lbl_tag.pack(side=TOP, padx=50, pady=5)

lbl_class = Label(upperLeft, text="class/id (optional)", font=("Arial Bold", 12))
lbl_class.pack(side=TOP, padx=50, pady=5)

lbl_limit = Label(upperLeft, text="Limit results up to: ", font=("Arial Bold", 12))
lbl_limit.pack(side=TOP, padx=50, pady=5)

# =============================== text area ===============================
txt_url = Entry(upperRight)
txt_url.pack(fill=BOTH, expand=TRUE, padx=(10, 20), pady=(6, 5))

txt_tag = Entry(upperRight)
txt_tag.pack(expand=TRUE, fill=X, padx=(10, 20), pady=10)

txt_class = Entry(upperRight)
txt_class.pack(expand=TRUE, fill=X, padx=(10, 20), pady=10)

txt_limit = Entry(upperRight)
txt_limit.pack(expand=TRUE, fill=X, padx=(10, 20), pady=10)

# =============================== result area ===============================
scrollbar = Scrollbar(centerFrame)
scrollbar.pack(side=RIGHT, fill=Y)

result_box = Listbox(centerFrame, yscrollcommand=scrollbar.set, selectmode=MULTIPLE)
result_box.pack(fill=BOTH, expand=TRUE, padx=30, pady=10)
scrollbar.config(command=result_box.yview)


def scrap(url):
    clear_result()
    has_limit = False
    search_limit = 0

    if not url:
        result_box.insert(END, "Please fill out all the information needed")
    else:
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.get(url)
        bs = BeautifulSoup(driver.page_source, "html.parser")

        # storing url/tag/class etc and strip white space
        txt_url.delete(0, END)
        txt_url.insert(0, url)
        tag_to_search = txt_tag.get().replace(" ", "")
        txt_tag.delete(0, END)
        txt_tag.insert(0, tag_to_search)
        class_to_search = txt_class.get().replace(" ", "")
        txt_class.delete(0, END)
        txt_class.insert(0, class_to_search)

        # error handling
        if txt_limit.get() and str.isdigit(txt_limit.get()):
            has_limit = True
            search_limit = int(txt_limit.get())

        if has_limit:
            finding = bs.find(tag_to_search, class_=class_to_search).find_all("p")
            if search_limit > len(finding):
                search_limit = len(finding)
            result_box.insert(0, "Found " + str(len(finding)) + " results. Displaying " + str(search_limit) + " results.")
            for i in range(0, search_limit):
                result_box.insert(i+1, finding[i].text)
        else:
            index = 1
            finding = bs.find(tag_to_search, class_=class_to_search).find_all("p")
            result_box.insert(0, "Found " + str(len(finding)) + " results. Displaying all")
            for p in finding:
                result_box.insert(index, p.text)


def clear_all():
    txt_url.delete(0, END)
    txt_tag.delete(0, END)
    txt_class.delete(0, END)
    txt_limit.delete(0, END)
    result_box.delete(0, END)


def clear_result():
    result_box.delete(0, END)


def main():
    # Add search and clear buttons
    clear_all_btn = Button(lowerFrame, text="Clear All", command=clear_all)
    clear_all_btn.configure(height=2, width=9)
    clear_all_btn.grid(column=0, row=0, padx=(30, 20), pady=(8, 20))

    clear_res_btn = Button(lowerFrame, text="Clear Results", command=clear_result)
    clear_res_btn.configure(height=2, width=9)
    clear_res_btn.grid(column=1, row=0, padx=(30, 20), pady=(8, 20))

    search_btn = Button(lowerFrame, text="Search", command=lambda: scrap(txt_url.get().replace(" ", "")))
    search_btn.configure(height=2, width=9)
    search_btn.grid(column=2, row=0, padx=(20, 30), pady=(8, 20))

    # Window non-resizable
    window.mainloop()


if __name__ == "__main__":
    main()
