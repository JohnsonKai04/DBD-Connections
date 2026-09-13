import pytesseract
import pyautogui
from PIL import ImageOps
from collections import Counter
pytesseract.pytesseract.tesseract_cmd = r"E:\Tesser\tesseract.exe"

SURVIVORS = [
    "dwight fairfield", "meg thomas", "claudette morel", "jake park",
    "nea karlsson", "laurie strode", "ace visconti", "bill overbeck",
    "feng min", "david king", "quentin smith", "david tapp", "kate denson",
    "adam francis", "jeff johansen", "jane romero", "ash williams",
    "nancy wheeler", "steve harrington", "yui kimura", "zarina kassir",
    "cheryl mason", "felix richter", "élodie rakoto", "lee yun-jin",
    "jill valentine", "leon scott kennedy", "mikaela reid", "jonah vasquez",
    "yoichi asakawa", "haddie kaur", "ada wong", "rebecca chambers",
    "vittorio toscano", "thalita lyra", "renato lyra", "gabriel soma",
    "nicolas cage", "ellen ripley", "alan wake", "sable ward",
    "aestri yazar & baermar uraz", "lara croft", "trevor belmont",
    "taurie cain", "orela rose", "rick grimes", "michonne grimes",
    "vee boonyasak", "dustin henderson", "eleven", "kwon tae-young",
    "shane wiigwaas", "aurora stardotter",
]

Y = 180
X1 = 740
X2 = 960
X3 = 1210
WIDTH = 120
HEIGHT = 100
DEBUG = False

def scanScreen(playerX, img):
    results = []
    color = 100
    region = (playerX, Y, WIDTH, HEIGHT)
    img = pyautogui.screenshot(region=region)

    gray = ImageOps.grayscale(img)
    gray = gray.resize((gray.width * 6, gray.height * 6))
    if(DEBUG): gray.save(f"{playerX}_{color}_normal.png")
    if(DEBUG): img.save(f"{playerX}_color.png")


    while(color < 250):
        bw = gray.point(lambda x: 0 if x < color else 255, '1')
        color += 5
        text = pytesseract.image_to_string(bw, config="--psm 6").lower()
        if(text == ""): continue

        for name in SURVIVORS:
            if name in text:
                text = text.split("\n", 1)[1].replace("\n", "")
                results.append(text)

    if not name:
        print(f"No name found for {playerX}")
        return False
    name = Counter(results)
    name = name.most_common(1)[0][0]


    print(f"Most Common name: {name}")

def main():
    img = pyautogui.screenshot()
    scanScreen(X1, img)
    scanScreen(X2, img)
    scanScreen(X3, img)



if __name__ == "__main__":
    main()