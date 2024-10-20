from services.chatgpt.utils import check_vector_store_status, upload_file, upload_file_to_vector_store

def martin_dao(s3_url,vs_id):

    uploaded_file = upload_file(s3_url)

    vector_store_file = upload_file_to_vector_store(uploaded_file,vs_id)
    
    completed_vc_file = check_vector_store_status(vs_id, vector_store_file.id)
    
    return {"uploaded_file": uploaded_file, "vector_store_file": completed_vc_file}
    
    


