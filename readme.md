# InstaProject

This is a Python script that was designed to automate the process of fetching product data from an e-commerce website, and then posting that data to Instagram using the `instabot` library. The script fetches product data such as product name, ID, URL, price, discount, and image URL. It then posts this data to Instagram with a caption that includes the product's title, discount, price, and affiliate link.

The script also includes functionality to keep track of which products have been seen and posted, to avoid posting the same product multiple times.

Please note that this script was written a long time ago and is not currently maintained. As such, it may not work as expected due to changes in the `instabot` library, the e-commerce website's API, or Instagram's rules and regulations regarding automated posting.

## Dependencies

This script requires the following Python libraries:

- `requests`
- `instabot`
- `bs4`
- `logging`
- `time`
- `random`
- `csv`
- `datetime`
- `pandas`
- `json`
- `shutil`
- `PIL`
- `os`
- `glob`

## Usage

To use this script, you will need to replace the placeholders for the Instagram username and password, and the affiliate code. You will also need to have a CSV file named `seen.csv` in the same directory as the script, which is used to keep track of which products have been seen.

The main class in the script is `pbot`, which takes a niche and a file as arguments. The `populate` method fetches product data from the e-commerce website, and the `task` method posts this data to Instagram.

```python
b = pbot("bags", "bags.csv")
b.task()
```


Again, please note that this script is not currently maintained and may not work as expected.