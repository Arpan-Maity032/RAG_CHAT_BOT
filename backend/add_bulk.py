import os
from ragservice import rag_model

Doc_Dir = "documents_to_add"

def add_all():
    if not os.path.exists(Doc_Dir):
        os.makedirs(Doc_Dir)
        print(f"Created '{Doc_Dir}'.Bulk files are added here")
        return
    files = [f for f in os.listdir(Doc_Dir) if f != ".gitkeep"]
    print(f"found {len(files)} files..")


    for filename in files:
        file_path = os.path.join(Doc_Dir, filename )
        try:
            print(f"added {filename}...")
            rag_model.addFile(file_path,filename)
            print("Done")

        except Exception as e:
            print(f"Error {e}")

if __name__ == "__main__":
    add_all()