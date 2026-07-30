# 🧑‍💼 AI Recruitment Assistant - Setup Guide (Roman Urdu)

Yeh guide aapko step-by-step batayegi ke is project ko apne computer par kaise
chalana hai. Koi bhi coding knowledge zaroori nahi — bas yeh steps follow karein.

---

## Cheez jo aapko chahiye

1. **Python 3.10 ya usse naya version** — computer mein install hona chahiye.
2. **Internet connection** — packages install karne aur Gemini AI ko call karne ke liye.
3. **Google Gemini API Key (FREE)** — neeche step 3 mein bataya gaya hai kaise banayen.

---

## Step 1: Zip file ko extract karein

1. Jo `AI-Recruitment-Assistant.zip` file aapko di gayi hai, usay kisi bhi folder
   mein (jaise Desktop par) **extract / unzip** kar lein.
2. Extract karne ke baad aapko `AI-Recruitment-Assistant` naam ka ek folder milega.

---

## Step 2: Python installed hai ya nahi check karein

Apne computer par **Command Prompt** (Windows) ya **Terminal** (Mac/Linux) kholein
aur yeh likhein:

```
python --version
```

Agar version number show ho (jaise `Python 3.11.5`), toh Python already installed hai.

Agar error aaye ya Python installed nahi hai, toh yahan se download karein:
👉 https://www.python.org/downloads/

**Zaroori (Windows walon ke liye):** Install karte waqt neeche wala box
**"Add Python to PATH"** zaroor tick karein.

---

## Step 3: Gemini API Key banayein (FREE hai)

1. Yeh link kholein: https://aistudio.google.com/app/apikey
2. Apne Google account se login karein.
3. **"Create API Key"** button par click karein.
4. Jo key banegi (lambi si string, jaise `AIzaSy...`) usay copy kar lein.
   Yeh key baad mein use karni hai — safe jagah save kar lein.

---

## Step 4: Terminal mein project folder tak jayein

Command Prompt / Terminal mein likhein (path apne hisaab se badal dein):

```
cd Desktop/AI-Recruitment-Assistant
```

Agar aapne file kisi aur jagah rakhi hai toh us folder ka sahi path likhein.

---

## Step 5: Zaroori packages install karein

Isi terminal mein yeh command likhein aur Enter dabayein:

```
pip install -r requirements.txt
```

Yeh command internet se saari zaroori libraries (Streamlit, LangChain, Gemini
connector, waghera) download aur install kar degi. Isme 2-5 minute lag saktay hain.

**Agar `pip` command na chale:** iski jagah `pip3` try karein:

```
pip3 install -r requirements.txt
```

---

## Step 6: Apni API Key project mein daalein

1. Project folder mein ek file hai jiska naam **`.env.example`** hai.
2. Us file ko **copy** karein aur naye copy ka naam **`.env`** rakh dein
   (dot ke saath, sirf `.env`, koi extension nahi).
3. `.env` file ko kisi bhi text editor (Notepad, VS Code, waghera) mein kholein.
4. Yeh line dhoondein:
   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```
5. `your_gemini_api_key_here` ki jagah apni Step 3 wali asal API key paste kar dein.
   Final line kuch aisi honi chahiye (yeh sirf example hai, apni asal key use karein):
   ```
   GOOGLE_API_KEY=AIzaSyD4xxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
6. File **save** kar dein.

⚠️ **Note:** `.env` file ko kabhi kisi ke saath share na karein ya GitHub par
upload na karein — yeh aapki private key hai.

---

## Step 7: App ko run karein

Terminal mein (jo abhi bhi project folder mein khula hai) yeh likhein:

```
streamlit run app.py
```

Kuch second mein aapka browser khud khul jayega aur app dikhayi degi
(agar na khule toh terminal mein diya gaya link, jaise `http://localhost:8501`,
manually browser mein paste kar dein).

---

## Step 8: App ko use karein

1. **Left sidebar** mein **"Upload Job Description (PDF)"** par click karke
   ek Job Description PDF upload karein.
   (Aap `data/` folder mein di gayi sample JD files bhi use kar saktay hain.)
2. **"Upload Resume(s)"** par click karke ek ya multiple resume PDFs upload karein.
   (`data/` folder mein 5 sample resumes bhi maujood hain testing ke liye.)
3. **"Analyze Resume(s)"** button par click karein.
4. Thodi der intezaar karein — AI har resume ko parhega, JD se compare karega,
   score dega, aur recommendation banayega.
5. Har candidate ka tab khol kar unki summary, matching/missing skills,
   interview questions, aur HR recommendation dekhein.
6. Sab se neeche **"Candidate Ranking"** table mein saare candidates ek
   comparison table mein rank kiye gaye honge.
7. **"Export Ranking as CSV"** button se result CSV file mein download kar saktay hain.

---

## App band karna

Terminal mein `Ctrl + C` dabayein, ya terminal window band kar dein.

Dobara chalane ke liye bas Step 7 wala command dobara likhein:
```
streamlit run app.py
```
(Step 5 aur 6 dobara karne ki zaroorat nahi — woh sirf ek baar karni hoti hai.)

---

## Aam Masail (Common Problems) aur Hal

| Masla | Hal |
|---|---|
| `GOOGLE_API_KEY is missing` wala error | Check karein ke `.env` file bani hai (sirf `.env.example` nahi), aur usme asal key paste ki hui hai. |
| `model not found` wala error | Google purane Gemini models waqtan waqtan band karta rehta hai. `.env` file mein `GEMINI_MODEL` line ko `gemini-flash-latest` rakhein (yeh khud-ba-khud current model use karta hai), ya https://ai.google.dev/gemini-api/docs/models par jaake koi bhi current valid model name daal dein. |
| `ModuleNotFoundError` wala error | Step 5 wala command (`pip install -r requirements.txt`) dobara chalayein. |
| "Analyze Resume(s)" button disabled/grey hai | Pehle Job Description AUR kam se kam ek Resume dono upload karna zaroori hai. |
| App bohot slow chal rahi hai | Har resume ke liye AI 5 alag calls karta hai — is liye thoda time lagta hai. 5 resumes ke liye 1-2 minute normal hai. |
| Browser khud nahi khula | Terminal mein diya gaya link (jaise `http://localhost:8501`) copy karke browser mein manually paste kar dein. |

---

## Khulasa (Summary) - Sirf 3 Commands

Agar sab kuch pehle se set ho chuka hai (`.env` file ban chuki hai), toh
agli baar app chalane ke liye sirf yeh karna hai:

```
cd AI-Recruitment-Assistant
streamlit run app.py
```

Bas! App khul jayegi. 🎉
