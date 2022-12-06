import requests
import time

contry_code = ["com", "dji", "eth", "gmb", "gin", "ken", "mdg", "mli", "mus", "moz", "mar", "nam", "ner", "sen", "sle", "syc", "tgo", "tun", "uga", "znz", "arg", "blz", "bol", "chl", "col", "cri", "ecu", "slv", "gtm", "guy", "hnd", "mex", "nic", "pan", "pry", "per", "ury", "ven", "019", "033", "005", "irn", "jor", "lao", "lbn", "mal", "npl", "pak", "pse", "lka", "sy11", "etm", "vnm", "yem", "alb", "esp", "srb", "tur", "atg", "dma", "dom", "jam", "grd", "lca", "kna", "vct", "tto", "pac", "GAR15"]
country_name =["Comoros", "Djibouti", "Ethiopia", "Gambia", "Guinea", "Kenya", "Madagascar", "Mali", "Mauritius", "Mozambique", "Morocco", "Namibia", "Niger", "Senegal", "Sierra Leone", "Seychelles", "Togo", "Tunisia", "Uganda", "Zanzibar (United Rep. of Tanzania)", "Argentina", "Belize", "Bolivia", "Chile", "Colombia", "Costa Rica", "Ecuador", "El Salvador", "Guatemla", "Guyana", "Honduras", "Mexico", "Nicaragua", "Panama", "Paraguay", "Peru", "Uruguay", "Venezuela", "India Orissa", "India Tamil Nadu", "India Uttarakhand", "I. R. Iran", "Jordan", "Laos", "Lebanon", "Maldives", "Nepal", "Pakistan", "Palestine", "Sri Lanka", "Syrian Arab Republic", "Timor Leste", "Viet Nam", "Yemen", "Albania", "Spain", "Serbia", "Turkey", "Antigua and Barbuda", "Dominica", "Dominican Republic", "Jamaica", "Grenada", "Saint Lucia", "Saint Kitts and Nevis", "Saint Vincent and the Grenadines", "Trinidad and Tobago", "Secretary of Pacific Community (23 counries)", "Datasets for the G∀R 2015"]
base_url = "https://www.desinventar.net/DesInventar/download/DI_export_"

for i, (code, country) in enumerate(zip(contry_code, country_name)):
    new_url = base_url + code + ".zip"
    print(i)
    print(country)
    r = requests.get(new_url)
    with open(f"{country}.zip", 'wb') as f:
        f.write(r.content)
        f.close
    time.sleep(1)