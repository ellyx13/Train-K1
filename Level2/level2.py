import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import xlsxwriter

def write_Data(worksheet, name_Course, list_View, number_Lesson, list_Author, list_Thumbnail):
    for i in range(0, len(name_Course)):
        number_Row = str(i+2)
        worksheet.write('A' + number_Row, name_Course[i])
        worksheet.write('B' + number_Row, list_View[i])
        worksheet.write('C' + number_Row, number_Lesson[i])
        worksheet.write('D' + number_Row, list_Author[i])
        worksheet.write('E' + number_Row, list_Thumbnail[i])
driver = webdriver.Chrome("chromedriver.exe")
driver.get("https://howkteam.vn/learn")

courseList = driver.find_elements(By.CSS_SELECTOR, "#course-list > div")

course_Name = []
course_Author = []
course_View = []
course_Lesson = []
course_Thumbnail = []

for course in courseList:
    lineText = course.text.splitlines()
    course_Name.append(lineText[0])
    lessonAndView = lineText[3].split(' ')
    course_Lesson.append(lessonAndView[0])
    course_View.append(lessonAndView[3])
    author = course.find_element(By.CSS_SELECTOR, "div > div.block-content.block-content-full.useravatar-edit-container > a").get_attribute('text').strip()
    course_Author.append(author)
    img_src = course.find_element(By.TAG_NAME, "img").get_attribute("src")
    course_Thumbnail.append(img_src)

workbook = xlsxwriter.Workbook('kteam_Lesson.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1', 'Lesson name')
worksheet.write('B1', 'View')
worksheet.write('C1', 'Number of lessons')
worksheet.write('D1', 'Author')
worksheet.write('E1', 'Thumbnail')

write_Data(worksheet, course_Name, course_View, course_Lesson, course_Author, course_Thumbnail)

workbook.close()
