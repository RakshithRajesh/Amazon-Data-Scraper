from requests_html import HTMLSession
import pandas as pd

url = "https://www.amazon.in/s?k=Laptop"

s = HTMLSession()
r = s.get(url)
r.html.render(sleep=5)
print(r.status_code)

for i in range(11):
    url = f"https://www.amazon.in/s?k=Laptop&page={i}"
    r = s.get(url)
    r.html.render(sleep=5)
    print(r.status_code)

    print(f"Found Page: {i}")

    asins = []
    product_urls = []

    product_asins = r.html.find("div[data-asin]")

    for product in product_asins:
        if product.attrs["data-asin"] != "":
            asins.append(product.attrs["data-asin"])

    for asin in asins:
        product_urls.append(f"https://amazon.in/dp/{asin}")

    namelist = []
    pricelist = []
    ratinglist = []

    for url in product_urls:

        print(url)
        r = s.get(url)
        r.html.render(sleep=5)
        print(r.status_code)

        try:
            name = r.html.xpath('//*[@id="productTitle"]', first=True).text
            price = r.html.xpath('//*[@id="priceblock_ourprice"]', first=True).text
            ratings = r.html.xpath('//*[@id="acrPopover"]/span[1]/a/i[1]/span')[0].text

            namelist.append(name)
            pricelist.append(price)
            ratinglist.append(ratings)
        except:
            try:
                name = r.html.xpath('//*[@id="productTitle"]', first=True).text
                price = r.html.xpath('//*[@id="priceblock_dealprice"]', first=True).text

                namelist.append(name)
                pricelist.append(price)
            except:
                name = r.html.xpath('//*[@id="productTitle"]', first=True).text
                price = "No Price"

                namelist.append(name)
                pricelist.append(price)

try:
    df = pd.DataFrame({"Title": namelist, "Price": pricelist, "Link": product_urls})
    df.to_csv("Demo.csv")
    print("Done...")
except:
    print(
        f"""
    May be the Length of the lists are not the same:
    Name List: {len(namelist)}
    Price List: {len(pricelist)}
    URL List: {len(product_urls)}
    """
    )
