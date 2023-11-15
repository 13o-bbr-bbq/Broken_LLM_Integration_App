# Broken Chatbot
![Version](https://img.shields.io/badge/release-v0.0.1-blue) ![Release date](https://img.shields.io/badge/release_date-november_2023-%23Clojure) ![License](https://img.shields.io/badge/License-MIT-%23326ce5)  
![Docker](https://img.shields.io/badge/Docker-%230db7ed) ![ChatGPT](https://img.shields.io/badge/ChatGPT-74aa9c) ![LangChain](https://img.shields.io/badge/LangChain-0.0.305-%23EB0443) ![Python](https://img.shields.io/badge/Python-3.11.6-ffdd54) ![FastAPI](https://img.shields.io/badge/FastAPI-0.103.2-005571) ![React](https://img.shields.io/badge/React-17.0.2-%2361DAFB) ![MySQL](https://img.shields.io/badge/MySQL-8.0.28-%2300f)

<img src="./assets/images/broken_chatbot_logo.png" width="35%">
  
created by ChatGPT  

Broken Chatbot is an application for verifying vulnerabilities in LLM applications, such as Prompt Injection, Prompt Leaking, and P2SQL Injection.

|Note|
|:---|
|This LLM application is very vulnerable and should only be used in a local environment. It should not be made public.|

---

## Overview
By using LLM integration middleware such as Flowise and LangChain, it is easy to develop "LLM applications" that integrate Web applications, LLM, and DBMS. As a result, the number of LLM applications is increasing. However, LLM applications have different attack surfaces than conventional Web applications. As noted in the [OWASP Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/), there are numerous new attack surfaces for LLM applications.  

Therefore, if an LLM application is developed without "cyber security" in mind, it may be attacked. Thus, it is important for LLM applications developers to consider "security specific to LLM applications" in addition to conventional security, and to take measures to avoid or mitigate damage in the event of an attack.  

So, we have released an LLM application called  "Broken Chatbot", to help LLM application developers understand the vulnerabilities and countermeasures specific to LLM applications. Broken Chatbot has vulnerabilities specific to LLM applications, such as Prompt Injection, Prompt Leaking, and P2SQL Injection. LLM application developers can use Broken Chatbot to experience these vulnerabilities and learn how to defend against them.  

## Features
The current version of Broken Chatbot contains the following vulnerabilities.  

- Prompt Injection  
- Prompt Leaking  
- P2SQL Injection

### Prompt Injection
Prompt Injection is a technique used to manipulate or exploit conversational AI systems, like chatbots or voice assistants, by crafting inputs that include hidden or unexpected instructions within them. This technique can be used to alter the behavior of the AI in unintended ways or to extract information that should not be accessible.  

### Prompt Leaking
Prompt Leaking refers to a situation where a conversational AI, like a chatbot or a language model, inadvertently reveals parts of its internal prompts, training data, or operational instructions within its responses. This can happen due to flaws in the AI's design or when it's tricked into divulging more information than it's supposed to.  

### P2SQL Injection
P2SQL Injection is an attack in which a malicious Prompt is inputted into an LLM application, such as a chatbot or voice assistant integrated with the LLM and DBMS, to manipulate the DBMS. If an LLM application is P2SQL Injected, it can cause extensive damage, including data theft, falsification, and deletion from the DBMS.  

## Installation

1. Install Docker Engine and Docker Compose.  
Broken Chatbot is launched using the Docker Engine and Docker Compose.  
Therefore, please refer to the following web sites to install Docker Engine and Docker Compose.  
[https://docs.docker.com/](https://docs.docker.com/)  

2. Get Broken Chatbot repository.  
Execute the following command to copy the Broken Chatbot repository to your local environment.  

```bash
~$ git clone https://github.com/13o-bbr-bbq/Broken_LLM_Integration_App.git
```

3. Create `.env` file.  
Create a configuration file for Broken Chatbot.  
Please refer to the sample shown below.  

```bash
# MySQL.
DB_USERNAME=root
DB_PASSWORD=root
DB_HOST=db
DB_NAME=broken_chatbot

# ChatGPT.
OPENAI_API_KEY=your_api_key
OPENAI_MODEL_NAME=your_model_name
OPENAI_MAX_TOKENS=256
OPENAI_TEMPERATURE=0.9
OPENAI_VERBOSE=true
```

`your_api_key` is OpenAI API Key. `your_model_name` is OpenAI GPT's model name.  
So, `your_api_key` and `your_model_name` should be your available API Key and model name.
You can obtain this information from the following web site.  

[https://platform.openai.com/](https://platform.openai.com/)

4. Placement of `.env` files.  
Place the .env file you created in the following path.  

```bash
Broken_LLM_Integration_App/chatapp/backend/
```

5. Importing Table Data.  
The current version of Broken Chatbot accesses the DBMS (MySQL) `users` table.  
The structure of the `users` table is shown below.  

```python
# User table.
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    full_name = Column(String(100))
```

If you want to import the sample data we have prepared into users table, please use the following data:  
[Sample data](./assets/sample_data/broken_chatbot_users.csv)  

6. Building Broken Chatbot.  
Execute the following command to build Broken Chatbot.  

```bash
~$ Broken_LLM_Integration_App/chatapp/docker-compose build
```

7. Launch Broken Chatbot.  
Execute the following command to start Broken Chatbot.  

```bash
~$ Broken_LLM_Integration_App/chatapp/docker-compose up
```
8. Access Broken Chatbot.  
Using a web browser, access the following URL.  

```bash
http://localhost:3000
```

## Usage
The following figure shows the Broken Chatbot UI.  

<img src="./assets/images/broken_chatbot_screenshot.png" width="40%">  

Broken Chatbot uses "React" for the frontend, "FastAPI" for the backend, "OpenAI GPT" for LLM, and "LangChain" for LLM integration middleware. In addition, the DBMS that Broken Chatbot connects to is "MySQL".

Users can start chatting by inputting a Prompt in the input form (Send a message) at the bottom of the screen and clicking the "Send" button. The Prompt inputted by the user will be displayed with a blue background on the right side of the chat history. The response from Broken Chatbot is shown on the left side of the screen with an orange background.  

Users can also toggle the behavior of the Broken Chatbot by selecting the pull-down menu to the left of the "Send" button.  
The menu of choices available in the current version of Broken Chatbot is as following:  

- Leak Lv.1  
- SQLi Lv.1  
- SQLi Lv.2  

### Leak Lv.1  
In the "Leak Lv.1" mode, you will experience `Prompt Injection` and `Prompt Leaking`.  
Try to steal the `Prompt Template` from Broken Chatbot by crafting the Prompt you input.  

### SQLi Lv.1  
In the "Leak Lv.1" mode, you will experience a simple `P2SQL Injection`.  
You can try to steal information from the `users` table that `Broken Chatbot` connects to, tamper with records, delete records, etc. by crafting a Prompt you input.

### SQLi Lv.2  
In the "Leak Lv. 2" mode, you will experience a `slightly more difficult P2SQL injection`. In this mode, Broken Chatbot is controlled to not tamper with or delete records using a `defensive Prompt Template`.  
So, you can try to bypass the `defensive Prompt Template` using `Prompt Injection` and tamper or delte records of `users` table.  

## License
[MIT License](https://github.com/13o-bbr-bbq/Broken_LLM_Integration_App/blob/main/LICENSE)  

## Contact us
13o-bbr-bbq (@bbr_bbq)  
[https://twitter.com/bbr_bbq](https://twitter.com/bbr_bbq)  
