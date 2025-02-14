import docx
# 讀取文件並切割內文
def process_document(file_path):
    doc = docx.Document(file_path)
    full_text = []
    
    for paragraph in doc.paragraphs:
        full_text.append(paragraph.text)
    
    return "\n".join(full_text)

# 切割內文為可管理的區塊
def split_text(text, chunk_size=1024, overlap=256):  # 設定預設 chunk_size 和 overlap
    chunks = []
    lines = text.split('\n')
    current_chunk = []
    current_length = 0
    for i in range(len(lines)):
        current_chunk.append(lines[i])
        current_length += len(lines[i])
        if current_length >= chunk_size:
            chunks.append('\n'.join(current_chunk))   
            # 計算要保留的重疊行數
            overlap_lines = []
            overlap_length = 0 
            # 從當前 chunk 的尾部開始，保留足夠的行數來達到 overlap 大小
            for line in reversed(current_chunk):
                if overlap_length + len(line) <= overlap:
                    overlap_lines.insert(0, line)
                    overlap_length += len(line)
                else:
                    break          
            current_chunk = overlap_lines
            current_length = overlap_length
    # 處理最後剩餘的文本
    if current_chunk:
        chunks.append('\n'.join(current_chunk))
    return chunks
