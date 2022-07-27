
##############################################################
# Clone and Pull awesome-home-kubernetes repositories
# Clone or pull all repositories mentioned in the readme for [awesome-home-kubernetes](https://github.com/k8s-at-home/awesome-home-kubernetes).
## Pre requisties
# ```
# pip3 install bs4
# ```
##############################################################
import os
import argparse
from urllib.request import urlopen
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
currentDir = os.getcwd()

parser.add_argument("-d", "--directory", dest="directory", default=currentDir ,help="Path to directory to clone all repositories in")
args = parser.parse_args()
print("Cloning in directory {}".format(args.directory))

url = "https://github.com/k8s-at-home/awesome-home-kubernetes"
output = urlopen(url).read()

parsed_html = BeautifulSoup(output, features="html.parser")
rows = parsed_html.find("article", {"class": "markdown-body"}).find_all("tr")

links = []
for row in rows:
    for each_a in row.find_all("a"):
        href = each_a["href"]
        if href.startswith("https://github") and href.count("/") == 4:
            links.append(href)
            print(href)


for link in links:
    repoSlash = link.rindex("/")
    repoName = link[repoSlash + 1 : len(link)]
    profileSlash = link.rindex("/", 0, repoSlash)
    profile = link[profileSlash + 1 : repoSlash]

    folderName = profile + "_" + repoName
    path = os.path.join(args.directory, folderName)
    cloneOrPull = os.system("git clone "
        + link
        + " "
        + path
        + " 2> /dev/null || (cd "
        + path
        + " ; git pull)"
    )
    print("Command ran with exit code %d" % cloneOrPull)
