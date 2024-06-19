## Project Overview
Does your company handle paper or scanned documents like invoices, purchase orders, or underwriting documents? Recent advancements in generative AI are revolutionizing cost reduction through automation.

## Key Developments:
Improved OCR Accuracy: Machine-learning-based optical character recognition (OCR) models have significantly improved over the past three years, addressing issues like blurry text and unusual fonts. Now, cloud services like Microsoft Azure Form Recognition, Amazon Textract, and Google's Tesseract library offer high accuracy without needing custom models.

## System Architecture-
Advanced AI Language Models: These models can now take the text output from OCR systems, analyze it, convert it into structured data (e.g., JSON), and automate actions within a company's systems based on document content.
![iamage_1](https://github.com/shivam221997/optical-character-recognition-using-Gen-AI/assets/156662255/ccb5cc8d-67c9-4ad0-86c0-ec1037fdbd75)


## Impact:
This combination of technologies enables:

High-accuracy text conversion from scanned documents.

Automated data processing and action-taking, reducing the need for manual labor.
## Prediction
Large amounts of routine back-office work, often offshored to developing countries, will soon be almost entirely automated using machine learning OCR systems and advanced AI language models.

# Showing Code Flow Using Images-

Step-1
Run the code in pycharm 
'''use the command- uvicorn main:app --reload
'''
 ![image_4](https://github.com/shivam221997/optical-character-recognition-using-Gen-AI/assets/156662255/f3623cbb-8052-4ea3-bf95-6741108747f1)


Step-2
After opening the FAST API server. The interface will look like this-
 
![image_1](https://github.com/shivam221997/optical-character-recognition-using-Gen-AI/assets/156662255/1d4efd56-17f9-4ce1-b3ac-ce38180472a6)

STEP-3
Next step to provide the document from which data need to be extracted.
![image_2](https://github.com/shivam221997/optical-character-recognition-using-Gen-AI/assets/156662255/320984bb-b98b-451c-a69f-47913c4d16aa)

Step-4
As we upload the document at the end point of FAST API server . it accept the pdf and do internal processing to extract images and then call google gen ai model . finally it returns a Json response.

![image_3](https://github.com/shivam221997/optical-character-recognition-using-Gen-AI/assets/156662255/c405b803-d283-441c-b914-3967e1b423bd)
