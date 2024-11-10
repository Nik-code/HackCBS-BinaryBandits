# main.py
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import fitz  # PyMuPDF
from database import SessionLocal, PDFDocument, Question
import uuid
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body
import os

os.environ["GROQ_API_KEY"] = "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"

from langchain_groq import ChatGroq

llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

# messages = [
#     (
#         "system",
#         "You are a helpful assistant that translates English to French. Translate the user sentence.",
#     ),
#     ("human", "I love programming."),
# ]
# ai_msg = llm.invoke(messages)

# print(ai_msg.content)

app = FastAPI()

allowed_origins = [
    "http://localhost:5173"
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # List of allowed origins
    allow_credentials=True,  # Allow cookies to be sent with requests
    allow_methods=["*"],  # Allow all HTTP methods (e.g., GET, POST)
    allow_headers=["*"],  # Allow all headers
)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Function to extract text from PDF using PyMuPDF
def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with fitz.open(file_path) as pdf:
        for page_num in range(pdf.page_count):
            page = pdf.load_page(page_num)
            text += page.get_text("text")
    return text


# Endpoint to upload PDF
@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...), db=Depends(get_db)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDFs are allowed.")

    # Save PDF locally
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Extract text from PDF
    extracted_text = extract_text_from_pdf(file_path)

    # Store metadata and content in the database
    pdf_doc = PDFDocument(filename=file.filename, content=extracted_text)
    db.add(pdf_doc)
    db.commit()
    db.refresh(pdf_doc)

    return {"filename": file.filename, "content": extracted_text, "id": pdf_doc.id}


# Function to retrieve the stored PDF text from the database
def get_pdf_content(db: Session, doc_id: int) -> str:
    pdf_doc = db.query(PDFDocument).filter(PDFDocument.id == doc_id).first()
    if not pdf_doc:
        raise HTTPException(status_code=404, detail="Document not found.")
    return pdf_doc.content


# Endpoint to process question and return an answer
# @app.post("/ask-question/")
# async def ask_question(doc_id: int, question: str, db: Session = Depends(get_db)):
#     # Retrieve the content of the PDF document
#     pdf_content = get_pdf_content(db, doc_id)

#     # Set up the language model
#     messages = [
#     (
#         "system",
#         f"I will give you the docuemnt content then I will also provide if any previous converstion is there, answer my question based on pdf's content and previous answers if any. Document content: {pdf_content}\nQuestion: {question}\nAnswer: Just give the answer in precise manner  onthing else",
#     )
#     ]
#     ai_msg = llm.invoke(messages)

#     # Use LangChain to process the question and retrieve answer based on PDF content
#     # response = llm(f"Document content: {pdf_content}\nQuestion: {question}\nAnswer:")

#     return {"question": question, "answer": ai_msg.content}

def get_previous_context(db: Session, doc_id: int, session_id: str) -> str:
    """Retrieve previous Q&A pairs as context for linked questions."""
    questions = db.query(Question).filter(
        Question.doc_id == doc_id, Question.session_id == session_id
    ).all()
    context = ""
    for q in questions:
        context += f"Q: {q.question_text}\nA: {q.answer_text}\n"
    return context


@app.post("/ask-question/")
async def ask_question(doc_id: int = Body(...), question: str = Body(...), session_id: str = Body(None),
                       db: Session = Depends(get_db)):
    # Retrieve the content of the PDF document
    pdf_content = get_pdf_content(db, doc_id)

    # If session_id is not provided, create a new one
    if not session_id:
        session_id = str(uuid.uuid4())

    # Get context if it's a linked question
    previous_context = get_previous_context(db, doc_id, session_id)

    # Set up language model and include previous Q&A context
    messages = [
        (
            "system",
            f"""
        You are an AI that answers questions based on a document's content. 
        The document content is as follows:
        {pdf_content}

        Previous conversation context (if any) is provided below in a Q&A format:
        {previous_context}

        User's current question:
        {question}

        Please provide a precise and direct answer based on the document content and the previous conversation, if relevant. Do not add any additional information.
        """,
        )
    ]
    ai_msg = llm.invoke(messages)
    # prompt = f"{previous_context}\nDocument content: {pdf_content}\nQ: {question}\nA:"

    # # Generate the response
    # answer = llm(prompt)

    # Store question and answer in the database
    question_record = Question(
        doc_id=doc_id, session_id=session_id, question_text=question, answer_text=ai_msg.content
    )
    db.add(question_record)
    db.commit()

    return {"session_id": session_id, "question": question, "answer": ai_msg.content}