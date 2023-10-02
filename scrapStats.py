from selenium import webdriver
import time

# Captures and returns formated data from table
def getTableData(driver):
    tableData = []
    # Find the table by its role or class (update this based on your specific HTML)
    table = driver.find_element('xpath', '//*[@id="content-wrap"]/div[1]/div/div[2]/div/div[4]/figure/table')

    # Get all rows in the table
    rows = table.find_elements('tag name', "tr")

    # Loop through each row to extract data
    for row in rows:
        cells = row.find_elements('tag name', "td")
        if cells:  # Check to make sure the row is not empty or a header
            # Initialize an empty dictionary to store each row's data
            row_data = {}
 
            # Extract and format each cell's data
            images = [img.get_attribute('src') for img in cells[0].find_elements('tag name', "img")]
            row_data['Images'] = images
            row_data['Tier'] = cells[1].text
            row_data['Avg Place'] = float(cells[2].text)
            row_data['Place Change'] = float(cells[3].text.replace(" ", ""))
            row_data['Winrate'] = float(cells[4].text.replace("%", ""))
            row_data['Frequency'] = cells[5].text
            
            # Append the formatted data to the table_data list
            tableData.append(row_data)
    return tableData

def main():
    # Initialize Chrome WebDriver
    print('Begin')
    driver = webdriver.Safari()
    championList = ['Aatrox', 'Sion']
    for champ in championList:
        driver.get("https://www.metatft.com/units/"+champ)
        # Wait for the page to load
        time.sleep(2)

        ### Augments
        # Find the "Augments" button and click it
        augments_button = driver.find_element('xpath', '//*[@id="content-wrap"]/div[1]/div/div[2]/div/div[4]/div/div[1]/div[2]/div/div[3]')
        augments_button.click()
        time.sleep(1)
        resData = getTableData(driver)
        print("Build Augments:")
        for i in resData:
            print(i)

        ### Builds
        # Find the "Builds" button and click it
        builds_button = driver.find_element('xpath', "//*[contains(text(), 'Builds')]")
        builds_button.click()
        time.sleep(1)

        resData = getTableData(driver)
        print("Build Data:")
        for i in resData:
            print(i)

        ### Items
        # Find the "Items" button and click it
        items_button = driver.find_element('xpath', '//*[@id="content-wrap"]/div[1]/div/div[2]/div/div[4]/div/div[1]/div[2]/div/div[2]')
        items_button.click()
        time.sleep(1)
        resData = getTableData(driver)
        print("Build Items:")
        for i in resData:
            print(i)



    # Close the driver
    driver.close()

main()