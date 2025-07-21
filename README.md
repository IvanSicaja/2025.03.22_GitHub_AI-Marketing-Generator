🧾 🎯 Project title: AI Marketing Generator  
<br/>🎥 YouTube Demo: To be added

📦GitHub Source Code: <https://github.com/IvanSicaja/23_AI_Marketing_Generator>


🏷️ My Personal Profiles:

🎥 Video Portfolio: To be added

📦 GitHub Profile: <https://github.com/IvanSicaja>

🔗 LinkedIn: <https://www.linkedin.com/in/ivan-si%C4%8Daja-832682222>

\----------------------------------------------------------------------------------------------------------------

### 📚🔍 Project description: ⬇︎⬇︎⬇︎

### 💡 App Purpose

Create multi-platform ad content in multiple languages with a single click.

This application, called **AI Marketing Generator**, creates all types of ads you need, tailored to various use cases:

- **For website promotion**, it generates long-form SEO-optimized content.
- **For social media platforms** (Facebook, Instagram, LinkedIn, X), it creates short, engaging posts with hashtags, emojis, and brand voice tone.
- **For digital platforms** (e.g., YouTube ads), it delivers concise, persuasive, high-conversion ad texts.

The idea is that app support **personalized advertising**, allowing you to tailor content using customer data such as name, search history, click behavior, and product browsing time. This is easily toggled via a personalization setting.

The idea is that app also supports **image and video ad generation** based on product descriptions or templates. Although not fully implemented in this prototype, the feature is actively under research. Currently, image generation results can be promising using technologies such as Stable Diffusion, ComfyUI workflows, masking techniques, and prompt engineering. However, the output is often far from perfect and usually requires additional editing—something that goes against the core purpose of the app, which is to automate and simplify the ad creation process. It is only a matter of time before image and video generation quality improves significantly. Integrating a better image/video generation model into the pipeline would require practically just two lines of code. Additionally, **video ads are known to attract up to 7 x more attention** than static image ads.

Additionally, the app is designed to **leverage real-time marketing trends**, integrating tools like **Google Trends**, **Keyword Planner**, **Search Console**, and **Analytics APIs**. While some third-party Google APIs couldn’t be configured during the free-tier testing, the foundation is there and future implementation is planned.

You can also enrich your ad campaigns by adding extra creative text outside your product database using the additional_description variable—perfect for a final personal or emotional touch.

### 🧠 How It Works

A database is created in .csv format containing the following columns: Product_ID, Name, Type, Category, Price_Euros, Description, Tags/Keywords, Reviews, and Rating. CSV is used for simplicity, but other formats such as **PostgreSQL** or **SQL** can be easily integrated.

**Prompt engineering** is implemented using **LangChain** to define the specific type of ad to be generated (SEO, social media, etc.). Since every model can respond differently—even to the same prompt—prompt design plays a crucial role in generating consistent and high-quality results.

Text generation is powered by **Large Language Models (LLMs)** via **Hugging Face’s Dedicated Inference Endpoint**. The model used here is **meta-llama/Llama-3.1-8B-Instruct**, which receives structured product information and returns tailored ad content.

At this stage, **Retrieval-Augmented Generation (RAG)** is not utilized, as it was not essential for this prototype.

Currently, output is displayed in the console for development purposes. A frontend interface using **HTML**, **CSS**, **JavaScript**, and **Bootstrap** can be added for production deployment.

The application is exposed via a lightweight **Flask API**, enabling integration with other services and tools.

Local testing is fully supported. Scripts are included to:

- Evaluate model token limits
- Send requests to the Flask API locally (Postman-like functionality)

Once local testing is successful, the app is **Dockerized**, and the test procedures are repeated on the containerized version to ensure production readiness.

There’s no need to write Kubernetes configuration files. The app is deployed using **Google Cloud Run**, which offers:

- **Auto-scaling**
- **Built-in logging**
- **Monitoring**
- And is available under a free-tier plan for 3 months

After successful local testing, the app is ready for deployment. The entire **CI/CD workflow** is automated using **GitHub Actions**. Deployment is triggered on each commit to the main branch. Secrets are stored in **GitHub Secrets**. They can be stored in a more secure way, but for this prototype, this method was sufficient and practical for demonstration purposes.

For deployment, platforms like **Microsoft Azure**, **AWS**, or **Google Cloud** can be used. Since I’m a **research-oriented person** and had not previously worked with Google Cloud, I chose it to explore something new. I was positively surprised by its **clean interface** and **developer-friendly experience**, especially in comparison to other platforms.

The following services are enabled within Google Cloud for this project:

- **Cloud Run API**
- **IAM roles**
- **Artifact Registry API**
- **Cloud Storage API**

Appropriate **IAM roles** are assigned to ensure correct permissions for all services.

The .csv database is uploaded to **Google Cloud Storage**. With **Cloud Run Gen2** and **GCS FUSE**, the CSV file is mounted directly into the container as a shared service volume, ensuring all containers access the same dataset without duplication.

The CI/CD process begins with authentication between **GitHub Actions** and **Google Cloud**.

Once authenticated, the pipeline installs the **Google Cloud CLI (Command Line Interface)** to interact with the cloud project.

Since the app is containerized using **Docker**, authentication is also performed with **Google Artifact Registry** to allow Docker images to be pushed.

Docker images are built using **timestamp-based naming** to avoid overwriting during deployments and ensure traceability of versions.

After building the image, it is uploaded to the **Google Artifact Registry**.

Finally, the containerized application is deployed to **Google Cloud Run** with the desired configuration, making the app globally accessible.

### ⚠️ Note

This application is a **prototype** developed for **research and development** purposes. While some features are not fully implemented in this version—such as image/video generation, personalization, or real-time keyword integration - **each of them has been deeply researched** to understand:

- What is technically possible
- What is valuable to implement
- What is not worth pursuing at this stage
- And how exactly they could be implemented when needed

This is the power of research: it helps define the scope and direction of development, not just by building features blindly, but by making **informed decisions** about what belongs in the product and when. Even though certain features are labeled as _not implemented_, they are **not overlooked**. Instead, they have been carefully analyzed, prototyped in isolation, or intentionally excluded to keep the application focused, lightweight, and extendable.

In summary, the prototype is **not about building everything at once**, but about knowing **what to build, why, and how**—and that’s where true engineering value lies.

### **🔧 Tech Stack**

Python, Flask, GitHub Actions, GitHub Secrets, Docker, Google Cloud Run, Google Artifact Registry, Google Cloud CLI, IAM Roles, Cloud Storage, Cloud Run, Artifact Registry, LLMs, Hugging Face, Transformers, Meta Llama, LangChain, Prompt Engineering, Stable Diffusion, ComfyUI Workflows, Google Trends API, Google Keyword Planner, Google Analytics API, Google Search Console API, Database creation, GCS FUSE, Postman, custom testing scripts, Auto-scaling, Workflow automation

### **📣 Hashtags Section**

\# AI #MarketingTech #GenAI #PromptEngineering #StableDiffusion #LangChain #LLM #FlaskAPI #GoogleCloud #CloudRun #Docker #GitHubActions #HuggingFace #MetaLlama #AIMarketing #AdTech #MLDeployment #ComfyUI #CloudComputing #AIContentCreation #MultilingualMarketing #PersonalizedAds #Automation #VideoMarketing #ImageGeneration #StartupTech #OpenSourceProject #PythonDeveloper #DataDrivenMarketing #InnovativeTech
