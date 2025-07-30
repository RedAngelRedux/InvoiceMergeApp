import os
import fitz #PyMuPDF

from core.invoice_processor import extract_number

def split_waybill_pdfs(folder):
    for filename in os.listdir(folder):
        if filename.lower().endswith(".pdf"):
            doc = fitz.open(os.path.join(folder,filename))
            invoice_chunks = []
            current_chunk = []
            current_account = None

            for i in range(len(doc)):
                text = doc[i].get_text()
                acct = extract_number(text,[r'ACCOUNT:\s*([A-Za-z0-9]+)'])

                if acct: #Detected start of new invoice

                    if current_chunk:
                        invoice_chunks.append((current_account,current_chunk))
                    current_chunk = [i]
                    current_account = acct
                else:
                    current_chunk.append(i)

            # Add last chunk
            
            if current_chunk and current_account:
                invoice_chunks.append((current_account,current_chunk))

            # Save each invoice as a separate PDF

            for acct, pages in invoice_chunks:
                out_doc = fitz.open()
                for p in pages:
                    out_doc.insert_pdf(doc, from_page=p, to_page=p)
                out_path = os.path.join(folder,f"{acct}_Waybill.pdf")
                out_doc.save(out_path)     
                if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
                    print(f"✅ File saved and non-empty: {out_path}")
                else:
                    print(f"⚠️ File missing or empty: {out_path}")           
                out_doc.close()

            doc.close()
