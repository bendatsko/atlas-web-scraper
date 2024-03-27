from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

# Define EE and CS courses for categorization
ee_courses = [215, 216, 230, 270, 320, 311, 312, 320, 330, 334, 351, 370, 373, 411, 413, 414, 418, 419, 420, 421, 423, 425, 427, 429, 430, 434, 452, 455, 460, 461, 463, 470, 473, 530]
cs_courses = [201, 203, 280, 285, 281, 270, 312, 367, 370, 376, 373, 388, 390, 427, 440, 441, 442, 445, 448, 449, 467, 470, 471, 473, 475, 476, 477, 478, 481, 482, 483, 484, 485, 486, 487, 489, 490, 491, 492, 493, 494, 495, 497]

driver = webdriver.Chrome()

# Navigate to course page for manual 2FA login
driver.get("https://atlas.ai.umich.edu/course/EECS%20110/")
input("Log in manually in the browser window. Press 'Enter' here to continue...")

def LoadCourseDetails(course_code):
    driver.get(f"https://atlas.ai.umich.edu/course/EECS%20{course_code}/")

    try:
        course_name_element = driver.find_element(By.CSS_SELECTOR, "h2.text-large")
        course_name = course_name_element.text.strip()
        
        workload_element = driver.find_element(By.CSS_SELECTOR, "h5.workload-highlight")
        workload_percentage = workload_element.text.strip()
        
        increased_element = driver.find_element(By.CSS_SELECTOR, "h5.increased-interest-highlight")
        increased_percentage = increased_element.text.strip()
        
        desire_element = driver.find_element(By.CSS_SELECTOR, "h5.desire-highlight")
        desire_percentage = desire_element.text.strip()
        
        median_grade_element = driver.find_element(By.CSS_SELECTOR, "p.grade-median span.bold.blue-highlight-text")
        median_grade = median_grade_element.text.strip()

        # course category
        category = "CS" if course_code in cs_courses else "EE"
        if course_code in ee_courses and course_code in cs_courses:
            category = "EE, CS"

        return course_code, course_name, workload_percentage, increased_percentage, desire_percentage, median_grade, category
    except Exception as e:
        print(f"EECS {course_code} not found. Skipping.")
        return None

with open('umich_courses.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Course Code", "Course Name", "Workload Percentage", "Increased Interest Percentage", "Desire to Take Percentage", "Median Grade", "Category"])
    
    for course_code in range(100, 501):
        course_details = LoadCourseDetails(course_code)
        if course_details:
            writer.writerow(course_details)
            print(f"EECS {course_code} data written to CSV.")

driver.quit()
print("Scraping complete.")
