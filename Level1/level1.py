import requests
from bs4 import BeautifulSoup
import xlsxwriter

url = "https://howkteam.vn/learn"

def get_Name_Course(url, soup):
    list_Name_Raw = soup.find_all('h4', {'class' : 'font-size-default font-w600 mb-10 text-overflow-dot'})
    list_Name_Course = []
    for name in list_Name_Raw:
        list_Name_Course.append(str(name.text))
    return list_Name_Course
def get_Number_Lesson(url, soup):
    list_Number_Raw = soup.find_all('div', {'class' : 'd-inline-block mr-10'})
    number = []
    for number_Lesson in list_Number_Raw:
        number_Raw = number_Lesson.text.split(' ')[0]
        number.append(int(number_Raw.replace('\n', '')))
    return number
def get_View(url, soup):
    list_View = []
    list_View_Raw = soup.find_all('div', {'class' : 'block-content block-content-full block-content-sm bg-body-light text-muted font-size-sm'})
    for div in list_View_Raw:
        view = div.find_all('strong')[1].text
        list_View.append(int(view.replace('.','')))
    return list_View
def get_Author(url, soup):
    list_Author = []
    list_Author_Raw = soup.find_all('div', {'class' : 'block-content block-content-full useravatar-edit-container'})
    for div in list_Author_Raw:
        author = str(div.find_all('span')[1].text)
        list_Author.append(author)
    return list_Author
def get_Thumbnail(url, soup):
    list_Thumbnail = []
    list_Thumbnail_Raw = soup.find_all('img', {'class' : 'img-fluid options-item w-100'})
    for img in list_Thumbnail_Raw:
        link_Img = str(img['src'])
        list_Thumbnail.append(link_Img)
    return list_Thumbnail
def write_Data(worksheet, name_Course, list_View, number_Lesson, list_Author, list_Thumbnail):
    for i in range(0, len(name_Course)):
        number_Row = str(i+2)
        worksheet.write('A' + number_Row, name_Course[i])
        worksheet.write('B' + number_Row, list_View[i])
        worksheet.write('C' + number_Row, number_Lesson[i])
        worksheet.write('D' + number_Row, list_Author[i])
        worksheet.write('E' + number_Row, list_Thumbnail[i])
get_URL = requests.get(url)
get_Text = get_URL.text
soup = BeautifulSoup(get_Text, "html.parser")
name_Course = get_Name_Course(url, soup)
number_Lesson = get_Number_Lesson(url, soup)
list_View = get_View(url, soup)
list_Author = get_Author(url, soup)
list_Thumbnail = get_Thumbnail(url, soup)

workbook = xlsxwriter.Workbook('kteam_Lesson.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1', 'Lesson name')
worksheet.write('B1', 'View')
worksheet.write('C1', 'Number of lessons')
worksheet.write('D1', 'Author')
worksheet.write('E1', 'Thumbnail')

write_Data(worksheet, name_Course, list_View, number_Lesson, list_Author, list_Thumbnail)

workbook.close()



