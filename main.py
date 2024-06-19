import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from io import BytesIO
from PIL import Image
import fitz
import google.generativeai as genai
import json
from fastapi import HTTPException, status

# --- Configuration ---
SAVE_DIR = "extracted_images"
GOOGLE_API_KEY = "put your API key"
MODEL_CONFIG = {
    "temperature": 0.2,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

# Ensure the save directory exists
os.makedirs(SAVE_DIR, exist_ok=True)

# Configure the Generative AI model
genai.configure(api_key=GOOGLE_API_KEY)

# Load the Gemini model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
)

# --- FastAPI Setup ---
app = FastAPI()

# --- Helper Functions ---
def extract_first_page(pdf_data):
    try:
        # Open the PDF with PyMuPDF
        pdf_document = fitz.open(stream=pdf_data, filetype="pdf")

        # Get the first page
        first_page = pdf_document.load_page(0)

        # Render the page to a pixmap (image)
        pix = first_page.get_pixmap()

        # Convert the pixmap to a PIL image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Save the image to a BytesIO object for response
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        return img_byte_arr

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error extracting first page from PDF: {str(e)}")

def is_pdf(file: UploadFile):
    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"File '{file.filename}' must be a PDF format.")

# --- API Endpoint ---
@app.post("/DOC_Aanlysis_By_OCR/")
async def analyze_receipts(files: list[UploadFile] = File(...)):
    try:
        # Initialize an empty list to store results
        results = []

        for file in files:
            try:
                # Check if the file is a PDF
                is_pdf(file)

                # Read the uploaded PDF file
                pdf_data = await file.read()

                # Extract the first page of the PDF as an image
                img_byte_arr = extract_first_page(pdf_data)

                # Format the image data for Gemini
                image_parts = [
                    {
                        "mime_type": "image/png",
                        "data": img_byte_arr.getvalue()
                    }
                ]

                # Define the system prompt for JSON conversion
                system_prompt = """
                       You are a specialist in comprehending receipts.
                       Input images in the form of receipts will be provided to you.
                       Your task is to convert the invoice data from the image into a well-formatted JSON object,
                       including appropriate JSON tags for all the data elements in the image.
                       """

                # Define the user prompt for JSON conversion
                user_prompt = """
                       Extract the following information from the invoice:
                       1. Bill Date
                       2. Bill Amount
                       3. Bill Period
                       4. Sanctioned Load
                       5. Bill Due Date
                       6. Unit Consumed
                       7. Present Reading
                       8. Previous Reading
                       9. Previous Outstanding
                       """

                # Construct the input prompt for Gemini
                input_prompt = [system_prompt, image_parts[0], user_prompt]

                # Generate content using the Gemini model
                response = model.generate_content(input_prompt)
                answer = response.text
                answer = answer.split('json', 1)[1]
                answer = answer[:-3].strip()
                answer = json.loads(answer)

                # Append the result to the list
                results.append({"filename": file.filename, "page_1": answer})

            except HTTPException as http_err:
                raise http_err
            except Exception as err:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error processing file '{file.filename}': {str(err)}")

        # Return all JSON outputs as a FastAPI response
        return JSONResponse({"results": results})

    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {str(err)}")

# --- Run the FastAPI app ---
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
